import os
from shutil import copyfile
from typing import List, Optional
from inspect import getfullargspec

from .formats import get_format, get_format_set_suitable_function, get_format_set_suitable_combination
from .vmd_spells import vmd_to_pdb
from .gmx_spells import get_tpr_structure
from .gmx_spells import merge_and_convert_trajectories as gmx_merge_and_convert_trajectories
from .mdt_spells import merge_and_convert_trajectories as mdt_merge_and_convert_trajectories
from .vmd_spells import merge_and_convert_trajectories as vmd_merge_and_convert_trajectories

# Set functions to performe structure conversions
# These functions must have 'input_structure_filename' and 'output_structure_filename' keywords
# These functions must have the 'format_sets' property
# These functions may have the 'input_trajectory_filename' keyword
structure_converting_functions = [ get_tpr_structure, vmd_to_pdb ]

# Set functions to performe trajectory conversions
# These functions must have 'input_trajectory_filename' and 'output_trajectory_filename' keywords
# These functions must have the 'format_sets' property
trajectory_converting_functions = [
    mdt_merge_and_convert_trajectories,
    gmx_merge_and_convert_trajectories,
    vmd_merge_and_convert_trajectories
]

# Handle conversions of different structure and trajectory formats
# Merge multiple input trajectories into one single output trajectory
# Inputs are the original strucutre and/or trajectory files and the list of possible output filenames
# Only one of each group of output filenames will be generated (if possible)
# Return the names of the generated output files
def convert (
    input_structure_filename :  Optional[str] = '',
    output_structure_filename : Optional[str] = '',
    input_trajectory_filenames :  Optional[List[str]] = '',
    output_trajectory_filename : Optional[str] = ''
):

    # If we have output but not input we must complain
    if output_structure_filename and not input_structure_filename:
        raise SystemExit('Missing input structure')
    if output_trajectory_filename and not input_trajectory_filenames:
        raise SystemExit('Missing input trajectory')

    # Get the first trajectory as a sample for those processes which do not require the whole trajectory
    trajectory_sample = input_trajectory_filenames[0]

    # Get file formats
    input_structure_format = get_format(input_structure_filename) if input_structure_filename else None
    output_structure_format = get_format(output_structure_filename) if output_structure_filename else None
    input_trajectory_format = get_format(trajectory_sample) if input_trajectory_filenames else None
    output_trajectory_format = get_format(output_trajectory_filename) if output_trajectory_filename else None

    # In case multiple trajectories are passed check all of them to match in the format
    trajectory_files_count = len(input_trajectory_filenames)
    if trajectory_files_count > 1:
        for filename in input_trajectory_filenames:
            if get_format(filename) != input_trajectory_format:
                raise SystemExit('All input trajectories must have the same format')

    # Convert the structure
    # Do it inside a function just to return as soon as we are done
    def convert_structure():
        # If there is no output filename it means we have nothing to do here
        if not output_structure_filename:
            return
        # If input and output formats are the same then just copy the file with the new name
        if input_structure_format == output_structure_format:
            copyfile(input_structure_filename, output_structure_filename)
            return
        # Otherwise, we must convert
        # Choose the right conversion function according to input and output formats
        request_format_set = {
            'inputs': {
                'input_structure_filename': { input_structure_format },
                'input_trajectory_filename': { input_trajectory_format }
            },
            'outputs': {
                'output_structure_filename': { output_structure_format }
            }
        }
        suitable = next(get_format_set_suitable_function(
            available_functions=structure_converting_functions,
            available_request_format_sets=[request_format_set],
        ), None)
        # If there is no function to handle this specific conversion we stop here
        if not suitable:
            raise SystemExit('Conversion from ' + input_structure_format +
                ' to ' + output_structure_format + ' is not supported')
        converting_function, formats = suitable
        # Find the function keywords
        # This is important since some functions may need a trajectory input in addition
        converting_function_keywords = getfullargspec(converting_function)[0]
        required_trajectory = 'input_trajectory_filename' in converting_function_keywords
        if required_trajectory:
            if not input_trajectory_filenames:
                raise SystemExit('The structure input format ' + input_structure_format +
                ' is missing coordinates and the output format ' + output_structure_format +
                ' needs them. An input trajectory file is required.')
            converting_function(
                input_structure_filename=input_structure_filename,
                input_trajectory_filename=trajectory_sample,
                output_structure_filename=output_structure_filename
            )
        else:
            converting_function(
                input_structure_filename=input_structure_filename,
                output_structure_filename=output_structure_filename
            )
    convert_structure()

    def convert_trajectory ():
        # If there is no output filename it means we have nothing to do here
        if not output_trajectory_filename:
            return
        # If there is only 1 input trajectory and it has the same format that the output then just copy the file with the new name
        if trajectory_files_count == 1 and input_trajectory_format == output_trajectory_format:
            copyfile(trajectory_sample, output_trajectory_filename)
            return
        # Otherwise, we must convert
        # Choose the right conversion function according to input and output formats
        request_format_set = {
            'inputs': {
                'input_structure_filename': { input_structure_format },
                'input_trajectory_filenames': { input_trajectory_format }
            },
            'outputs': {
                'output_trajectory_filename': { output_trajectory_format }
            }
        }
        suitable = next(get_format_set_suitable_function(
            available_functions=trajectory_converting_functions,
            available_request_format_sets=[request_format_set],
        ), None)
        # If there is no function to handle this specific conversion we try to combine several functions in order to do it
        if not suitable:
            print('WARNING: There is no function to do the conversion directly. Trying to combine multiple functions...')
            suitable = next(get_format_set_suitable_combination(
                available_functions=trajectory_converting_functions,
                available_request_format_sets=[request_format_set],
            ), None)
        # If there is no function to handle this specific conversion we stop here
        if not suitable:
            raise SystemExit('Conversion from ' + input_trajectory_format +
                ' to ' + output_trajectory_format + ' is not supported')
        converting_function, formats = suitable
        # Get the input structure expected format
        expected_input_structure_formats = formats['inputs'].get('input_structure_filename', False)
        # If the function expects any fromat then pass the structure
        if expected_input_structure_formats:
            converting_function(
                input_structure_filename=input_structure_filename,
                input_trajectory_filenames=input_trajectory_filenames,
                output_trajectory_filename=output_trajectory_filename
            )
        # If the function expects None then pass None
        elif expected_input_structure_formats == None:
            converting_function(
                input_structure_filename=None,
                input_trajectory_filenames=input_trajectory_filenames,
                output_trajectory_filename=output_trajectory_filename
            )
        # If the function has not the input structure argument then do not pass it
        else:
            converting_function(
                input_trajectory_filenames=input_trajectory_filenames,
                output_trajectory_filename=output_trajectory_filename
            )
    convert_trajectory()