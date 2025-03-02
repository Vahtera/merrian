def init(dict):
    global list
    list = {
        "river": f"[{dict.get_glyph("large")} + {dict.get_glyph("distance")}]-{dict.simpleglyphsearch('wet', 'noun')}",
        "doctor": f"{dict.simpleglyphsearch('labor', 'doer')}-[{dict.get_glyph("life")}]"
    }