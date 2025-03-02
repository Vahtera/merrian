```
'''Program to search for glyphs and definitions within a language known as "Merrian".'''

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
```
> [!IMPORTANT]
> Edit *merrian.txt.example* to include word definitions and rename to *merrian.txt*.
> 
> Edit *words.py.example* to include word definitions and rename to *words.py*.
```
Usage: py merrian.py [arguments] [search terms]

Supported arguments:

-h, --help               : Display this help page.
--update                 : Update module merrian_language. (Word definitions.)
--list                   : List all glyphs and complex words in the dictionary.
--glyph ['search']       : Looks for glyphs containing 'search' and displays all of them.

Search terms:

'word'                   : Searches for 'word' and displays the first definition.
'word1, word2'           : Searches for abstract 'word1' and returns the word definition from part 'word2'.

Examples:

py merrian.py day        : Returns 'DAY (Abstract)'.
py merrian.py moon       : Returns 'moon = NIGHT/DARK/DARKNESS:Noun'.
py merrian.py day, noun  : Returns '[DAY/LIGHT:Noun] sun'.
py merrian.py river      : Returns 'river = [long (LARGE/GIGANTIC + DISTANCE)]-[water (WET:Noun)]'.
```
> [!IMPORTANT]
> Edit **DICTIONARY_FILE** on *line 46* in merrian.py to point to merrian.txt (default working directory).

Screenshot:
![Merrian Screenshot](https://imgur.com/sx2tHIO.png)
