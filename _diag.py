import importlib.util
spec = importlib.util.spec_from_file_location("gd", "game_data.py")
gd = importlib.util.module_from_spec(spec); spec.loader.exec_module(gd)
for r in ["green", "blue", "purple", "gold", "celestial"]:
    for e in gd.ENTRIES[r]:
        neg = e[6] if len(e) > 6 else False
        if neg:
            print(f"{r:10s} idx={gd.RARITY_ORDER.index(r)}  {e[1]}  negative={neg}")
print("---")
print("green index =", gd.RARITY_ORDER.index("green"))
print("blue index  =", gd.RARITY_ORDER.index("blue"))
