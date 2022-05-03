from PokemonSaveStructure import *
from PokemonSaveEditorGUI import *

# Change this to the location of the default save file
# If work was continued on this aspect of the project, this would have been changed to allow for no default save file
inFileName = "pokemondata/romhack.sav"
# This address varies for each save file. Did not figure out how
startLocation = 0x2000

save = saveFile(inFileName, startLocation)

def main(): 
    GUISave(save).mainloop()

if __name__ == '__main__':
    main()