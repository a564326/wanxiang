"""
出包前最终检查 —— 确认 APK 构建所需的一切就绪。
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
errors = []
warnings = []

def check(cond, msg):
    if cond:
        print(f"  ✓ {msg}")
    else:
        print(f"  ✗ {msg}")
        errors.append(msg)

def warn(cond, msg):
    if not cond:
        warnings.append(msg)
        print(f"  ? {msg}")

print("\n[1] 关键文件")
for f in ["main.py", "game_data.py", "gacha_anim.py",
          "module_bg.py", "buildozer.spec", "package.bat"]:
    check(os.path.exists(os.path.join(ROOT, f)), f"存在 {f}")

print("\n[2] 美术资源")
assets = os.path.join(ROOT, "assets")
for img in ["icon.png", "bg.png", "gacha_bg.png", "smelt_bg.png",
            "realm_bg.png", "celestial_bg.png"]:
    check(os.path.exists(os.path.join(assets, img)), f"assets/{img}")

print("\n[3] Python 语法")
try:
    import py_compile
    for m in ["main.py", "game_data.py", "gacha_anim.py", "module_bg.py"]:
        py_compile.compile(os.path.join(ROOT, m), doraise=True)
    print("  ✓ 全部模块语法正确")
except Exception as e:
    errors.append(f"语法错误: {e}")
    print(f"  ✗ {e}")

print("\n[4] buildozer.spec 版本对齐（应匹配 SDK 34 / NDK 26b）")
spec = open(os.path.join(ROOT, "buildozer.spec"), encoding="utf-8").read()
check("android.build_tools = 34.0.0" in spec, "build-tools = 34.0.0")
check("android.api = 34" in spec, "api = 34")
check("android.ndk = 26b" in spec, "ndk = 26b")
check("accept_sdk_license = True" in spec, "自动接受许可证")

print("\n[5] 词条库")
sys.path.insert(0, ROOT)
import importlib.util
spec_gd = importlib.util.spec_from_file_location("gd", os.path.join(ROOT, "game_data.py"))
gd = importlib.util.module_from_spec(spec_gd)
spec_gd.loader.exec_module(gd)
total = sum(len(gd.ENTRIES.get(r, [])) for r in gd.RARITY_ORDER)
check(total >= 80, f"词条总数 = {total}")

# 蓝 / 紫 / 金（不含彩）必须全部纯正向，无任何负面标记
blue_purple_gold = [e for e in gd.all_entries()
                    if e["rarity"] in ("blue", "purple", "gold")]
bp_with_neg = [e["name"] for e in blue_purple_gold if e.get("negative")]
check(len(bp_with_neg) == 0, f"蓝/紫/金无负面词条（实际 {bp_with_neg}）")

# 白色可含负面（杂质），绿色可含双刃剑——仅统计确认
white_neg = [e["name"] for e in gd.all_entries() if e["rarity"] == "white" and e.get("negative")]
green_neg = [e["name"] for e in gd.all_entries() if e["rarity"] == "green" and e.get("negative")]
print(f"    [合规] 白色负面(杂质) {len(white_neg)} 条 / 绿色双刃剑 {len(green_neg)} 条")

celestial = gd.get_celestial_pool()
check(len(celestial) >= 5, f"彩词条 = {len(celestial)}")

# 彩词条代价写在 effect 文本里（主动承担，非 random debuff）——检查是否含明确的代价/限制表述
cost_keywords = ["代价", "后果", "索取", "敌视", "枯竭", "抹杀", "损坏", "过载",
                 "降一阶", "降阶", "背叛", "全力", "对立方", "初始态度",
                 "雷罚", "逐次", "百年", "寿元", "复活后", "怒火", "仇恨"]
missing_cost = []
for e in celestial:
    hit = any(k in e["effect"] for k in cost_keywords)
    if not hit:
        missing_cost.append((e["name"], e["effect"][:40]))
check(len(missing_cost) == 0, f"彩词条均含代价/限制表述（缺失: {missing_cost}）")

print("\n" + "="*40)
if errors:
    print(f"✗ {len(errors)} 个问题，请修复后再构建：")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("✓ 全部检查通过，可以开始构建 APK")
    if warnings:
        print(f"  （{len(warnings)} 条提示，不影响构建）")
        for w in warnings:
            print(f"  - {w}")
    sys.exit(0)
