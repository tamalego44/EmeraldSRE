This is the source code for my SRE of Pokemon Emerald Project.

All of these files are incomplete but represent the current state of my progress.

The "Save Editor" directory holds all the files for my makeshift Pokemon Emerald Save Editor which I stopped development on

The "hex_editor.py" file is the commandline hex editor I wrote that uses the pokemon emerald codec instead of ascii to better understand the Pokemon ROM and save file structure

The "modify_rom.py" was a simple tool to change strings in the rom file which eventually got deprecated in favor of the hex editor

The "pkmn_codec.py" contains all the information about the pokemon emerald codec

The "romhacks.py" is the tool demo'd in class that is meant to easily modify a ROM's first encounter and starter pokemon at will