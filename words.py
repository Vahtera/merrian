from libAnna.colors import *
def init(dict):
    global list
    list = {
        "river": f"[{CYAN}long{ENDC} ({dict.get_glyph("large")} + {dict.get_glyph("distance")})]-[{dict.simpleglyphsearch('wet', 'noun')}]",
        "doctor": f"[{dict.simpleglyphsearch('labor', 'doer')}]-[{dict.get_glyph("life")}]",
        "mountain": f"[{dict.get_glyph("large")} + {dict.simpleglyphsearch('earth', 'noun')}]",
        "cook": f"[{dict.simpleglyphsearch('heat', 'verb')}]-[{dict.simpleglyphsearch('flora', 'noun')}]",
    }