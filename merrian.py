''' Program to search for glyphs and definitions withing a language known as "Merrian".'''

#
# Copyright (c) Anna Vahtera 2025
# With the help of Reddit user https://www.reddit.com/user/g13n4/
# Thank you for the initial code for the Language and Glyph classes!
#

import sys
from libAnna.functions import clear_screen
from libAnna.colors import *

ARGUMENTS = len(sys.argv)

class Language:
    glyphs = []
    @staticmethod
    def wordsearch(word: str):
        for glyph in Language.glyphs:
            for part_of_speech in ['abstract', 'noun', 'verb', 'doer', 'place']:
                if getattr(glyph, part_of_speech) == word:
                    if part_of_speech == "abstract":
                        return f"{GREEN}{glyph.abstract.capitalize()}{ENDC} ({BOLD}{BLACK}{part_of_speech.capitalize()}{ENDC})"
                    else:
                        return f"{BOLD}{BLUE}{glyph.abstract.capitalize()}{ENDC}:{GREEN}{BOLD}{part_of_speech.capitalize()}{ENDC}"
    @staticmethod
    def glyphsearch(A: str, P: str):
        for glyph in Language.glyphs:
            if A in getattr(glyph, 'abstract'):
                ANSWER = getattr(glyph, P)
                return f"[{BOLD}{BLUE}{getattr(glyph, 'abstract').capitalize()}{ENDC}:{BOLD}{GREEN}{P.capitalize()}{ENDC}] {BOLD}{WHITE}{ANSWER.capitalize()}{ENDC}"

#print("\n [" + BOLD + BLUE + ARGS[0].capitalize() + ENDC + ":" + GREEN + BOLD + ARGS[1].capitalize() + ENDC + "] " + BOLD + WHITE + WORD + "\n" + ENDC)

MERRIAN = Language()

class Glyph:
    def __init__(self, abstract: str, noun: str, verb: str, doer: str, place: str):
        self.abstract = abstract
        self.noun = noun
        self.verb = verb
        self.doer = doer
        self.place = place
        MERRIAN.glyphs.append(self)
    def __repr__(self):
        return (f" [Glyph] Abstract: {self.abstract.capitalize()}, Noun: {self.noun.capitalize()}, Verb: {self.verb.capitalize()}, Doer: {self.doer.capitalize()}, Place: {self.place.capitalize()}")

DICT = []

# Dictionary file needs to include five comma-separated strings per line.
def open_dictionary(F_NAME):
    '''Read the Glyph definitions from a list'''
    T_LIST = []
    T_DICT = []
    with open(F_NAME, "r", encoding="utf-8") as F:  # Open the File and Read the Lines into an Array
        for LINE in F:
            T_LIST = LINE.split(", ")
            T_DICT.append(Glyph(*T_LIST))
    return T_DICT

DICT = open_dictionary("merrian.txt")

clear_screen()

if ARGUMENTS > 1:
    SEARCH = sys.argv[1].lower()
else:
    SEARCH = input(f"Enter word [{BOLD}word{ENDC}] or a combination [{BOLD}abstact, part{ENDC}] to look up: ").lower()

ARGS = SEARCH.split(", ")

if not len(ARGS) > 1:
    WORD = MERRIAN.wordsearch(SEARCH)
    try:
        print("\n [" + BOLD + SEARCH.capitalize() + "] " + ENDC + WORD + "\n" + ENDC)
    except:
        print(f"{BOLD}{RED}Error{ENDC}: Word not found in database. Make sure you spelled it correctly. You wrote: [{BOLD}{YELLOW}{SEARCH}{ENDC}]\nIn case of multiple entries, make sure you separate them with a comma and a whitespace.\n")
        sys.exit()
    
else:
    try:
        WORD = MERRIAN.glyphsearch(ARGS[0], ARGS[1])
        #print("\n [" + BOLD + BLUE + ARGS[0].capitalize() + ENDC + ":" + GREEN + BOLD + ARGS[1].capitalize() + ENDC + "] " + BOLD + WHITE + WORD + "\n" + ENDC)
        print(f"\n{WORD}\n")
    except:
        print(f"{BOLD}{RED}Error{ENDC}: Word not found in database. Make sure of spelling. You wrote [{BOLD}{YELLOW}{SEARCH}{ENDC}]\n")
        sys.exit()
