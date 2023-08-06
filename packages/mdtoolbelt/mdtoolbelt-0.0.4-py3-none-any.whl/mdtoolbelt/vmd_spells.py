# Functions powered by VMD
# Humphrey, W., Dalke, A. and Schulten, K., "VMD - Visual Molecular Dynamics", J. Molec. Graphics, 1996, vol. 14, pp. 33-38. 
# http://www.ks.uiuc.edu/Research/vmd/

import os

from subprocess import run, PIPE, STDOUT, Popen
from typing import Optional, List

from .single_frame_getter import get_last_frame
from .formats import get_format

# Set the script filename with all commands to be passed to vmd
commands_filename = '.commands.vmd'

# List all the vmd supported trajectory formats
vmd_supported_structure_formats = {'pdb', 'prmtop', 'psf', 'gro'} # DANI: Esto lo he hecho rápido, hay muchas más
vmd_supported_trajectory_formats = {'mdcrd', 'crd', 'dcd', 'xtc', 'trr', 'nc'}

# Given a vmd supported topology with no coordinates and a single frame file, generate a pdb file
def vmd_to_pdb (
    input_structure_filename : str,
    input_trajectory_filename : str,
    output_structure_filename : str):

    # DANI: Esto alomejor se podria substituit por un 'animate read' en los commands
    # https://www.ks.uiuc.edu/Research/vmd/current/ug/node121.html
    single_frame_filename = get_last_frame(input_structure_filename, input_trajectory_filename, vmd_supported_trajectory_formats)

    # Prepare a script for VMD to run. This is Tcl language
    with open(commands_filename, "w") as file:
        # Select all atoms
        file.write('set all [atomselect top "all"]\n')
        # Write the current topology in 'pdb' format
        file.write('$all frame first\n')
        file.write('$all writepdb ' + output_structure_filename + '\n')
        file.write('exit\n')

    # Run VMD
    logs = run([
        "vmd",
        input_structure_filename,
        single_frame_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()

    os.remove(commands_filename)
# Set function supported formats
vmd_to_pdb.format_sets = [
    {
        'inputs': {
            'input_structure_filename': {'psf', 'parm', 'prmtop'},
            'input_trajectory_filename': vmd_supported_trajectory_formats
        },
        'outputs': {
            'output_structure_filename': {'pdb'}
        }
    }
]

# This tool allows you to set the chain of all atoms in a selection
# This is powered by VMD and thus the selection lenguage must be the VMD's
# Arguments are as follows:
# 1 - Input pdb filename
# 2 - Atom selection (All atoms by defualt)
# 3 - Chain letter (May be the flag 'fragment', which is the default indeed)
# 4 - Output pdb filename (Input filename by default)
# WARNING: When no selection is passed, if only a part of a "fragment" is missing the chain then the whole fragment will be affected
# WARNING: VMD only handles fragments if there are less fragments than letters in the alphabet
def chainer (
    input_pdb_filename : str,
    atom_selection : Optional[str] = None,
    chain_letter : Optional[str] = None,
    output_pdb_filename : Optional[str] = None
):

    # If no atom selection is provided then all atoms are selected
    if not atom_selection:
        atom_selection = 'all'

    # If no chain letter is provided then the flag 'fragment' is used
    if not chain_letter:
        chain_letter = 'fragment'

    # If no output filename is provided then use input filename as output filename
    if not output_pdb_filename:
        output_pdb_filename = input_pdb_filename

    # Check the file exists
    if not os.path.exists(input_pdb_filename):
        raise SystemExit('ERROR: The file does not exist')
       
    with open(commands_filename, "w") as file:
        # Select the specified atoms and set the specified chain
        file.write('set atoms [atomselect top "' + atom_selection + '"]\n')
        # In case chain letter is not a letter but the 'fragment' flag, asign chains by fragment
        # Fragments are atom groups which are not connected by any bond
        if chain_letter == 'fragment':
            # Get all different chain names
            file.write('set chains_sample [lsort -unique [${atoms} get chain]]\n')
            # Set letters in alphabetic order
            file.write('set letters "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"\n')
            # Get the number of fragments
            file.write('set fragment_number [llength [lsort -unique -integer [${atoms} get fragment]]]\n')
            # For each fragment, set the chain of all atoms which belong to this fragment alphabetically
            # e.g. fragment 0 -> chain A, fragment 1 -> chain B, ...
            file.write('for {set i 0} {$i <= $fragment_number} {incr i} {\n')
            file.write('	set fragment_atoms [atomselect top "fragment $i"]\n')
            file.write('	$fragment_atoms set chain [lindex $letters $i]\n')
            file.write('}\n')
            # Otherwise, set the specified chain
        else:
            file.write('$atoms set chain ' + chain_letter + '\n')
        # Write the current topology in 'pdb' format
        file.write('set all [atomselect top "all"]\n')
        file.write('$all frame first\n')
        file.write('$all writepdb ' + output_pdb_filename + '\n')
        file.write('exit\n')

    # Run VMD
    logs = run([
        "vmd",
        input_pdb_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()

    # Remove the vmd commands file
    os.remove(commands_filename)

# Get vmd supported trajectories merged and converted to a different format
# WARNING: Note that this process is not memory efficient so beware the size of trajectories to be converted
# WARNING: The input structure filename may be None
def merge_and_convert_trajectories (
    input_structure_filename : Optional[str],
    input_trajectory_filenames : List[str],
    output_trajectory_filename : str
    ):

    # Get the format to export coordinates
    output_trajectory_format = get_format(output_trajectory_filename)

    # Although 'crd' and 'mdcrd' may be the same, VMD only recognizes 'crd' as exporting coordinates file type
    if output_trajectory_format == 'mdcrd':
        output_trajectory_format = 'crd'

    # Prepare a script for the VMD to automate the data parsing. This is Tcl lenguage
    # In addition, if chains are missing, this script asigns chains by fragment
    # Fragments are atom groups which are not connected by any bond
    with open(commands_filename, "w") as file:
        # Select all atoms
        file.write('set all [atomselect top "all"]\n')
        # Write the current trajectory in the specified format format
        file.write('animate write ' + output_trajectory_format + ' ' + output_trajectory_filename + ' waitfor all sel $all\n')
        file.write('exit\n')

    inputs = [ input_structure_filename, *input_trajectory_filenames ] if input_structure_filename else input_trajectory_filenames

    # Run VMD
    logs = run([
        "vmd",
        *inputs,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE, stderr=STDOUT).stdout.decode() # Redirect errors to the output in order to dont show them in console

    if not os.path.exists(output_trajectory_filename):
        print(logs)
        raise SystemExit('Something went wrong with VMD')

    # Remove the vmd commands file
    os.remove(commands_filename)

# Set function supported formats
merge_and_convert_trajectories.format_sets = [
    {
        'inputs': {
            'input_structure_filename': None,
            'input_trajectory_filenames': {'dcd', 'xtc', 'trr', 'nc'}
        },
        'outputs': {
            # NEVER FORGET: VMD cannot write to all formats it supports to read
            'output_trajectory_filename': {'mdcrd', 'crd', 'dcd', 'trr'}
        }
    },
    {
        'inputs': {
            'input_structure_filename': vmd_supported_structure_formats,
            'input_trajectory_filenames': {'mdcrd', 'crd'}
        },
        'outputs': {
            # NEVER FORGET: VMD cannot write to all formats it supports to read
            'output_trajectory_filename': {'mdcrd', 'crd', 'dcd', 'trr'}
        }
    }
]

# Given an atom selection in vmd syntax, return the list of atom indices it corresponds to
def get_vmd_selection_atom_indices (input_structure_filename : str, selection : str) -> List[int]:
    
    # Prepare a script for VMD to run. This is Tcl language
    # The output of the script will be written to a txt file
    atom_indices_filename = '.vmd_output.txt'
    with open(commands_filename, "w") as file:
        # Select the specified atoms
        file.write('set selection [atomselect top "' + selection + '"]\n')
        # Save atom indices from the selection
        file.write('set indices [$selection list]\n')
        # Write atom indices to a file
        file.write('set indices_file [open ' + atom_indices_filename + ' w]\n')
        file.write('puts $indices_file $indices\n')
        file.write('exit\n')

    # Run VMD
    logs = run([
        "vmd",
        input_structure_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()

    # Read the VMD output
    with open(atom_indices_filename, 'r') as file:
        raw_atom_indices = file.read()

    # Parse the atom indices string to an array of integers
    atom_indices = [ int(i) for i in raw_atom_indices.split() ]
    
    # Remove trahs files
    trash_files = [ commands_filename, atom_indices_filename ]
    for trash_file in trash_files:
        os.remove(trash_file)

    return atom_indices

# Set a function to retrieve strong bonds between 2 atom selections
# Atom selections must be in VMD selection syntax
# DANI: Lo tengo aquí pero no lo uso para nada todavia
def get_strong_bonds (structure_filename : str, atom_selection_1 : str, atom_selection_2 : str) -> list:

    # Prepare a script for the VMD to automate the commands. This is Tcl lenguage
    output_index_1_file = 'index1.text'
    output_index_2_file = 'index2.text'
    output_bonds_file = 'bonds.text'
    with open(commands_filename, "w") as file:
        # Select the specified atoms in selection 1
        file.write('set sel1 [atomselect top "' + atom_selection_1 + '"]\n')
        # Save all atom index in the selection
        file.write('set index1 [$sel1 list]\n')
        # Write those index to a file
        file.write('set indexfile1 [open ' + output_index_1_file + ' w]\n')
        file.write('puts $indexfile1 $index1\n')
        # Save all strong atoms in the selection
        file.write('set bonds [$sel1 getbonds]\n')
        # Write those bonds to a file
        file.write('set bondsfile [open ' + output_bonds_file + ' w]\n')
        file.write('puts $bondsfile $bonds\n')
        # Select the specified atoms in selection 2
        file.write('set sel2 [atomselect top "' + atom_selection_2 + '"]\n')
        # Save all atom index in the selection
        file.write('set index2 [$sel2 list]\n')
        # Write those index to a file
        file.write('set indexfile2 [open ' + output_index_2_file + ' w]\n')
        file.write('puts $indexfile2 $index2\n')
        file.write('exit\n')
        
    # Run VMD
    logs = run([
        "vmd",
        structure_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()
    
    # Read the VMD output
    with open(output_index_1_file, 'r') as file:
        raw_index_1 = file.read()
    with open(output_bonds_file, 'r') as file:
        raw_bonds = file.read()
    with open(output_index_2_file, 'r') as file:
        raw_index_2 = file.read()

    # Remove vmd files since they are no longer usefull
    for f in [ commands_filename, output_index_1_file, output_index_2_file, output_bonds_file ]:
        os.remove(f)

    # Sometimes there is a breakline at the end of the raw bonds string and it must be removed
    # Add a space at the end of the string to make the parser get the last character
    raw_bonds = raw_bonds.replace('\n', '') + ' '
    
    # Raw indexes is a string with all indexes separated by spaces
    index_1 = [ int(i) for i in raw_index_1.split() ]
    index_2 = [ int(i) for i in raw_index_2.split() ]
    
    # Parse the raw bonds string to a list of atom bonds (i.e. a list of lists of integers)
    # Raw bonds format is (for each atom in the selection):
    # '{index1, index2, index3 ...}' with the index of each connected atom
    # 'index' if there is only one connected atom
    # '{}' if there are no connected atoms
    bonds_per_atom = []
    last_atom_index = ''
    last_atom_bonds = []
    in_brackets = False
    for character in raw_bonds:
        if character == ' ':
            if len(last_atom_index) > 0:
                if in_brackets:
                    last_atom_bonds.append(int(last_atom_index))
                else:
                    bonds_per_atom.append([int(last_atom_index)])
                last_atom_index = ''
            continue
        if character == '{':
            in_brackets = True
            continue
        if character == '}':
            if last_atom_index == '':
                bonds_per_atom.append([])
                in_brackets = False
                continue
            last_atom_bonds.append(int(last_atom_index))
            last_atom_index = ''
            bonds_per_atom.append(last_atom_bonds)
            last_atom_bonds = []
            in_brackets = False
            continue
        last_atom_index += character
        
    # At this point indexes and bonds from the first selection should match in number
    if len(index_1) != len(bonds_per_atom):
        raise ValueError('Indexes (' + str(len(index_1)) + ') and atom bonds (' +  str(len(bonds_per_atom)) + ') do not match in number')
        
    # Now get all strong bonds which include an index from the atom selection 2
    crossed_bonds = []
    for i, index in enumerate(index_1):
        bonds = bonds_per_atom[i]
        for bond in bonds:
            if bond in index_2:
                crossed_bond = (index, bond)
                crossed_bonds.append(crossed_bond)
                
    return crossed_bonds