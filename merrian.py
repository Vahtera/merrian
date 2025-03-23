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
# Version 0.8 - Bugfixes and error handling.
# Version 0.9 - Added ability to store and search for complex words (consisting of multiple glyphs)
# Version 1.0a - Moved complex words to an external file and changed into importing it. 
# Version 1.0b - Fixed most of the bugs.
# Version 1.0.x - Latest word definition updates.
# Version 1.1.0 - Added ability to update definitions, if using merrian_language module.
# Version 1.1.x - Latest word definition updates.
# Version 1.2 - Changing over to x.y + rolling git commmit count as version numbering.
#

import sys
import re
import ast
import importlib.util
import subprocess
from os import system

module_name = "merrian_language"
spec = importlib.util.find_spec(module_name)
if spec is not None:
    try:
        if sys.argv[1] == "--update":
            print("Updating merrian_language...\n")
            system('git submodule update --remote --recursive')
            del sys.argv[1]
    except IndexError as err:
        print("Running program...")
    from merrian_language import words
    DICTIONARY_FILE = "merrian_language/merrian.txt"
else:
    try:
        import words
        DICTIONARY_FILE = "merrian.txt"
    except ModuleNotFoundError as err:
        print("Module merrian_language not loaded, and file words.py not found, aborting.")
        sys.exit()

from libAnna.functions import clear_screen
from libAnna.colors import *
cmd = ["git", "rev-list", "--count", "master"]
output = subprocess.check_output(cmd).strip()

VERSION = "1.2 Release: " + str(output)[2:-1]

ANS = "Y"
SILENT = False

for p in range(0, len(sys.argv)):
        if sys.argv[p] == "--silent":
            del sys.argv[p]
            SILENT = True

ARGUMENTS = len(sys.argv)
BGREY = "\x1b[100m"

class Language:
    '''Class to store the language'''
    glyphs = []
    @staticmethod
    def wordsearch(word: str): # method to search with a word definition
        '''Function to search individual words for a ABSTRACT+part combination'''
        for glyph in Language.glyphs:
            for part_of_speech in ['abstract', 'noun', 'verb', 'doer', 'place']:
                if word in getattr(glyph, part_of_speech).split("/"):
                    if part_of_speech == "abstract":
                        return f"\n {BOLD}{word.capitalize()}{ENDC} = {BLUE}{BOLD}{glyph.abstract.upper()}{ENDC} ({BOLD}{BLACK}{part_of_speech.capitalize()}{ENDC})"
                    elif part_of_speech == "verb":
                        WORDS = [temp_string for temp_string in getattr(glyph, part_of_speech).split("/")]
                        return f"\n {BOLD}to {", to ".join(WORDS)}{ENDC} = {BOLD}{BLUE}{glyph.abstract.upper()}{ENDC}:{GREEN}{BOLD}{part_of_speech.capitalize()}{ENDC}"
                    else:
                        WORDS = [temp_string for temp_string in getattr(glyph, part_of_speech).split("/")]
                        return f"\n {BOLD}{", ".join(WORDS)}{ENDC} = {BOLD}{BLUE}{glyph.abstract.upper()}{ENDC}:{GREEN}{BOLD}{part_of_speech.capitalize()}{ENDC}"
        return "NotFound"

    @staticmethod
    def glyphsearch(A: str, P: str): # method to search with "glyph, part"
        '''Function to search for ABSTRACT+part for individual words'''
        for glyph in Language.glyphs:
            if A in getattr(glyph, 'abstract').split("/"):
                ANSWER = getattr(glyph, P)
                temp_string = ANSWER.split("/")
                if P == "verb":
                    return f"[{BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC}] = {BOLD}{WHITE}to {", to ".join(temp_string)}{ENDC}"
                return f"[{BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC}] = {BOLD}{WHITE}{", ".join(temp_string)}{ENDC}"
        return f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{A}, {P}{ENDC}]\n"

    @staticmethod
    def simpleglyphsearch(A: str, P: str): # method to search with "glyph, part"
        '''Function to search for ABSTRACT+part for individual words and return a simple string'''
        for glyph in Language.glyphs:
            if A in getattr(glyph, 'abstract').split("/"):
                ANSWER = getattr(glyph, P)
                temp_string = ANSWER.split("/")
                temp_word = getattr(glyph, P).split("/")
                if P == "verb":
                    return f"{CYAN}to {", to ".join(temp_word)}{ENDC} ({BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC})"
                return f"{CYAN}{", ".join(temp_word)}{ENDC} ({BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC})"
        return f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{A}, {P}{ENDC}]\n"

    @staticmethod
    def get_glyph(abstract):
        '''Function to get a simple result for an abstract of a glyph'''
        for glyph in Language.glyphs:
            if abstract in getattr(glyph, 'abstract').split("/"):
                return f"{BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}"
        return "NotFound"


MERRIAN = Language() # Define Merrian as the language

class Glyph:
    '''Class to store individual Glyphs'''
    def __init__(self, abstract: str, noun: str, verb: str, doer: str, place: str):
        self.abstract = abstract
        self.noun = noun
        self.verb = verb
        self.doer = doer
        self.place = place
        MERRIAN.glyphs.append(self)
    def __repr__(self):
        return (f"  {BOLD}{BLUE}{self.abstract.upper()}{ENDC} {BOLD}{BLACK}(Abstract){ENDC} \n"
        f"     {BOLD}{BLACK}(Noun){ENDC}: {GREEN}{", ".join(self.noun.split("/"))}{ENDC}\n"
        f"     {BOLD}{BLACK}(Verb){ENDC}: {GREEN}to {", to ".join(self.verb.split("/"))}{ENDC}\n"
        f"     {BOLD}{BLACK}(Doer){ENDC}: {GREEN}{", ".join(self.doer.split("/"))}{ENDC}\n"
        f"    {BOLD}{BLACK}(Place){ENDC}: {GREEN}{", ".join(self.place.split("/"))}{ENDC}\n")

DICT = [] # Main dictionary to read the glyphs into

def display_help():
    word_pad = 25
    '''function to display help'''
    print("\nUsage: py merrian.py [arguments] [search terms]\n")
    print("Supported arguments:\n")
    print("-h, --help".ljust(word_pad, " ") + ": Display this help page.")
    print("--update".ljust(word_pad, " ") + ": Update module merrian_language. (Word definitions.)")
    print("--list".ljust(word_pad, " ") + ": List all glyphs and complex words in the dictionary.")
    print("--glyph ['search']".ljust(word_pad, " ") + ": Looks for glyphs containing 'search' and displays all of them.\n")
    print("Search terms:\n")
    print("'word'".ljust(word_pad, " ") + ": Searches for 'word' and displays the first definition.")
    print("'word1, word2'".ljust(word_pad, " ") + ": Searches for abstract 'word1' and returns the word definition from part 'word2'.\n")
    print("Examples:\n")
    print("py merrian.py day".ljust(word_pad, " ") + ": Returns 'DAY (Abstract)'.")
    print("py merrian.py moon".ljust(word_pad, " ") + ": Returns 'moon = NIGHT/DARK/DARKNESS:Noun'.")
    print("py merrian.py day, noun".ljust(word_pad, " ") + ": Returns '[DAY/LIGHT:Noun] sun'.")
    print("py merrian.py river".ljust(word_pad, " ") + ": Returns 'river = [long (LARGE/GIGANTIC + DISTANCE)]-[water (WET:Noun)]'.")
    print("\n")
    sys.exit()

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

DICT = open_dictionary(DICTIONARY_FILE) # read the main language file into the Dictionary.

def list_glyphs():
    '''Function to print out the whole dictionary'''
    PADDING = 20
    print("\n")
    print(" ".rjust(4," ") + BOLD + YELLOW + "ABSTRACT".ljust(PADDING, " ") + " " + "Noun".ljust(PADDING, " ") + " " + "Verb".ljust(PADDING, " ") + " " + "Doer".ljust(PADDING, " ") + " " + "Place" + ENDC)
    print(" ".rjust(4," ") + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "=") + " " + "=".ljust(PADDING, "="))
    x = 0
    k = 0
    row = 1
    z = 1
    
    for glyph in MERRIAN.glyphs:
        if row % 2:
            print(f"{str(row).rjust(2,"0")}: {BOLD}{BLACK}{glyph.abstract.upper().ljust(PADDING, " ")[:PADDING]}{ENDC} {glyph.noun.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.verb.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.doer.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.place.capitalize()[:PADDING]}{ENDC}")
        else:
            print(f"{str(row).rjust(2,"0")}: {BGREY}{BLACK}{glyph.abstract.upper().ljust(PADDING, " ")[:PADDING]}{ENDC}{BGREY} {glyph.noun.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.verb.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.doer.capitalize().ljust(PADDING, " ")[:PADDING]} {glyph.place.capitalize().ljust(PADDING, " ")[:PADDING]}{ENDC}")
        row += 1

    for temp_word in MERRIAN.glyphs:
        for part in ['abstract', 'noun', 'verb', 'doer', 'place']:
            if not getattr(temp_word, part).lower() == "na":
                x += 1
            else:
                k += 1
    
    print("\nComplex words:\n")
    
    for y in words.word_list:
        print(y.ljust(12, " ") + ": " + words.word_list[y])
        z += 1
    
    print(f"\nDatabase has a total of {CYAN}{str(x)}{ENDC} glyps and {CYAN}{str(z)}{ENDC} word definitions. ({GREEN}{str(k)}{ENDC} glyph definitions missing.)\n")

def get_glyph(abstract):
    for glyph in MERRIAN.glyphs:
        if abstract in getattr(glyph, 'abstract').split("/"):
            #return ", ".join(getattr(glyph, 'abstract').split("/")).upper()
            return f"{BOLD}{BLUE}{getattr(glyph, 'abstract').upper()}{ENDC}"
    return "NotFound"

words.init(MERRIAN)

def dictionary_search():
    '''Main function to actually search through the dictionary'''
    global ARGUMENTS
    global SILENT
    SEARCH = ""

    if ARGUMENTS > 1: # Check if arguments were give
        temp_list = sys.argv
        del temp_list[0]
        SEARCH = ", ".join(temp_list).lower().strip() # if yes, then try to use the first argument as the search term.
    else:
        # if not, ask the user for input.
        SEARCH = input(f"\n Enter word [{BOLD}word{ENDC}] or a combination [{BOLD}abstact, part{ENDC}] to look up, or [{BOLD}--quit{ENDC}] to quit: ").lower().strip()

    if SEARCH == "--quit":
        print("\n")
        sys.exit()

    if SEARCH in ["--help", "-h"]:
        display_help()

    if " " in SEARCH:
        ARGS = re.split('; |, | ', SEARCH)
    else:
        ARGS = SEARCH

    if SEARCH == "--list":
        list_glyphs()
        sys.exit()

    if ARGUMENTS > 2 and sys.argv[1] == "--glyph":
        ARGS = sys.argv
        del ARGS[0]

    if ARGS[0] == "--glyph" and len(ARGS) > 1:
        print(f"\n  \"{BOLD}{CYAN}{ARGS[1].lower()}{ENDC}\" found in the following glyphs:\n")
        for glyph in MERRIAN.glyphs:
            if ARGS[1].lower() in repr(glyph).lower():
                print(glyph)
        return True

    if isinstance(ARGS, str):
        WORD = MERRIAN.wordsearch(SEARCH) # Search for a specific word within Merrian
        
        if not WORD == "NotFound":
            print(WORD + "\n" + ENDC)
        else:
            WORD = words.word_list.get(SEARCH, "NotFound")
            if not WORD == "NotFound":
                print("\n " + BOLD + WHITE + SEARCH + " = " + ENDC + WORD + "\n" + ENDC)
            else:
                print(f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure you spelled it correctly. You wrote: [{BOLD}{YELLOW}{SEARCH}{ENDC}]\n In case of multiple entries, make sure you separate them with a comma and a whitespace.\n")
            #sys.exit()
    else:
        try:
            WORD = MERRIAN.glyphsearch(ARGS[0], ARGS[1]) # Search for abstract+part combination within Merrian
            print(f"\n {WORD}\n")
        except:
            print(f"\n {BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{", ".join(ARGS)}{ENDC}]\n")
            #sys.exit()

if not SILENT:
    if not ARGUMENTS > 1:
        clear_screen()
    else:
        print("\n")

    print(f" {CYAN}Merrian Dictionary.{ENDC} {BOLD}{BLACK}Version{ENDC} {BOLD}{CYAN}{VERSION}{ENDC}{BOLD}{BLACK}, Database version: {ENDC}{BOLD}{CYAN}{words.VERSION}{ENDC}")

    while ANS.lower() in ("y", "yes"):
        dictionary_search()

        if ARGUMENTS > 1:
            sys.exit()
else:
    dictionary_search()
    sys.exit()