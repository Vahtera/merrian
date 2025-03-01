''' Program to search for glyphs and definitions withing a language known as "Merrian".'''

#
# Copyright (c) Anna Vahtera 2025
# With the help of Reddit user https://www.reddit.com/user/g13n4/
# Thank you for the initial code for the Language and Glyph classes!
#
# Version History:
# Version 0.1 alpha - Initial Release
# Version 0.2 alpha - Added glyphsearch()
# Version 0.3 alpha - Added ANSI color to output
# Version 0.4 alpha - Added ability to search for multiple words within one glyph definition
# Version 0.5 alpha - Added ability list all glyphs with --list
# Version 0.6 alpha - Added --glyph command line functionality.
# Version 0.7 alpha - Added ability to search a new word without quitting
# Version 0.8 alpha - Added ability to use --glyph from within program
#

import sys
import re
from libAnna.functions import clear_screen
from libAnna.colors import *

VERSION = "0.8 alpha"
ARGUMENTS = len(sys.argv)
ANS = "Y"

BGREY = "\x1b[100m"

class Language:
    glyphs = []
    @staticmethod
    def wordsearch(word: str): # method to search with a word definition
        for glyph in Language.glyphs:
            for part_of_speech in ['abstract', 'noun', 'verb', 'doer', 'place']:
                if word in getattr(glyph, part_of_speech).split("/"):
                    if part_of_speech == "abstract":
                        return f"\n {BOLD}{word.capitalize()}{ENDC} = {BLUE}{BOLD}{glyph.abstract.upper()}{ENDC} ({BOLD}{BLACK}{part_of_speech.capitalize()}{ENDC})"
                    else:
                        WORDS = [temp_string.capitalize() for temp_string in getattr(glyph, part_of_speech).split("/")]
                        return f"\n {BOLD}{", ".join(WORDS)}{ENDC} = {BOLD}{BLUE}{glyph.abstract.upper()}{ENDC}:{GREEN}{BOLD}{part_of_speech.capitalize()}{ENDC}"
                else:
                    return f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}word{ENDC}]\n"
    @staticmethod
    def glyphsearch(A: str, P: str): # method to search with "glyph, part"
        for glyph in Language.glyphs:
            if A in getattr(glyph, 'abstract').split("/"):
                ANSWER = getattr(glyph, P)
                return f"[{BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC}] {BOLD}{WHITE}{ANSWER.capitalize()}{ENDC}"
            else:
                return f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{A}, {P}{ENDC}]\n"

MERRIAN = Language() # Define Merrian as the language

class Glyph:
    def __init__(self, abstract: str, noun: str, verb: str, doer: str, place: str):
        self.abstract = abstract
        self.noun = noun
        self.verb = verb
        self.doer = doer
        self.place = place
        MERRIAN.glyphs.append(self)
    def __repr__(self):
        return (f"  {BOLD}{BLUE}{self.abstract.upper()}{ENDC}: {BOLD}{BLACK}(Abstract){ENDC} \n"
        f"    :{GREEN}{self.noun.capitalize()} {BOLD}{BLACK}(Noun){ENDC} \n"
        f"    :{GREEN}{self.verb.capitalize()} {BOLD}{BLACK}(Verb){ENDC} \n"
        f"    :{GREEN}{self.doer.capitalize()} {BOLD}{BLACK}(Doer){ENDC} \n"
        f"    :{GREEN}{self.place.capitalize()} {BOLD}{BLACK}(Place){ENDC}\n\n")

DICT = [] # Main dictionary to read the glyphs into

# Dictionary file needs to include five comma-separated strings per line.
def open_dictionary(F_NAME):
    '''Read the Glyph definitions from a list'''
    T_LIST = []
    T_DICT = []
    with open(F_NAME, "r", encoding="utf-8") as F:  # Open the File and Read the Lines into an Array
        for LINE in F:
            T_LIST = LINE.strip().split(", ")
            T_DICT.append(Glyph(*T_LIST))
    return T_DICT

DICT = open_dictionary("merrian.txt") # read the main language file into the Dictionary.

def list_glyphs():
    PADDING = 20
    print("\n")
    print(" ".rjust(4," ") + BOLD + YELLOW + "ABSTRACT".ljust(PADDING, " ") + " " + "Noun".ljust(PADDING, " ") + " " + "Verb".ljust(PADDING, " ") + " " + "Doer".ljust(PADDING, " ") + " " + "Place" + ENDC)
    #print("=".ljust(PADDING, "=")[:PADDING] + " =".ljust(PADDING, "=")[:PADDING] + "  =".ljust(PADDING, "=")[:PADDING] + "   =".ljust(PADDING, "=")[:PADDING] + "    =".ljust(PADDING, "=")[:PADDING])
    print(" ".rjust(4," ") + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "="))
    x = 1
    for glyph in MERRIAN.glyphs:
        if (x % 2):
            print(f"{str(x).rjust(2,"0")}: {BOLD}{BLACK}{glyph.abstract.upper().ljust(PADDING, " ")[:PADDING]}{ENDC} {glyph.noun.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.verb.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.doer.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.place.capitalize()[:PADDING]}{ENDC}")
        else:
            print(f"{str(x).rjust(2,"0")}: {BGREY}{BLACK}{glyph.abstract.upper().ljust(PADDING, " ")[:PADDING]}{ENDC}{BGREY} {glyph.noun.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.verb.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.doer.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.place.capitalize().ljust(PADDING, " ")[:PADDING]}{ENDC}")
        x += 1
    print(f"\nDatabase has a total of {CYAN}{str((x-1)*5)}{ENDC} glyps.\n")

def dictionary_search():
    clear_screen()
    print(f" {CYAN}Merrian Dictionary.{ENDC} {BOLD}{BLACK}Version{ENDC} {BOLD}{CYAN}{VERSION}{ENDC}")

    if ARGUMENTS > 1: # Check if arguments were give
        SEARCH = sys.argv[1].lower() # if yes, then try to use the first argument as the search term.
    else:
        # if not, ask the user for input.
        SEARCH = input(f"\n Enter word [{BOLD}word{ENDC}] or a combination [{BOLD}abstact, part{ENDC}] to look up: ").lower()

    #ARGS = SEARCH.split(", ") # split search into two parts, if two words were given.
    ARGS = re.split(';\s|,\s|\s',SEARCH)

    if SEARCH == "--list":
        list_glyphs()
        sys.exit()

    if len(sys.argv) > 1 and sys.argv[1] == "--glyph":
        ARGS = sys.argv
        del ARGS[0]

    if ARGS[0] == "--glyph" and len(ARGS) > 1:
        print(f"\n  \"{BOLD}{CYAN}{ARGS[1].lower()}{ENDC}\" found in the following glyphs:\n")
        for glyph in MERRIAN.glyphs:
            if ARGS[1].lower() in repr(glyph).lower():
                print(glyph)
        return True

    if not len(ARGS) > 1:
        WORD = MERRIAN.wordsearch(SEARCH) # Search for a specific word within Merrian
        try:
            print(WORD + "\n" + ENDC)
        except:
            print(f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure you spelled it correctly. You wrote: [{BOLD}{YELLOW}{ARGS[0]}{ENDC}]\n In case of multiple entries, make sure you separate them with a comma and a whitespace.\n")
            #sys.exit()
        
    else:
        try:
            WORD = MERRIAN.glyphsearch(ARGS[0], ARGS[1]) # Search for abstract+part combination within Merrian
            print(f"\n {WORD}\n")
        except:
            print(f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{", ".join(ARGS)}{ENDC}]\n")
            #sys.exit()

while ANS.lower() in ("y", "yes"):
    dictionary_search()
    
    if ARGUMENTS > 1:
        sys.exit()

    ANS = input(" Search for another word, Y/N? [Y]: ") or "Y"

    print("\n")
