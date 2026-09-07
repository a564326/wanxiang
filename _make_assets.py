# -*- coding: utf-8 -*-
"""生成美术占位资源（沙盒无绘图库时用的纯色底图）。
本地若有 AI 原图，直接覆盖 assets/ 下同名文件即可，无需改代码。
"""
import os
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except Exception:
    HAS_PIL = False

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS, exist_ok=True)

# 背景配置：(文件名, 尺寸, 主色, 点缀色, 文字)
BG = [
    ("bg.png",          (1080, 1920), (10, 10, 26),  (241, 196, 15), "万象词条录"),
    ("gacha_bg.png",    (1080, 1920), (14, 10, 30),  (241, 196, 15), "观想玉简"),
    ("smelt_bg.png",    (1080, 1920), (20, 12, 8),   (255, 138, 101), "化道炉"),
    ("realm_bg.png",    (1080, 1920), (8, 16, 24),   (129, 199, 132), "境界突破"),
    ("celestial_bg.png",(1080, 1920), (20, 8, 24),   (255, 110, 199), "天外之象"),
]

def make_icon():
    path = os.path.join(ASSETS, "icon.png")
    if HAS_PIL:
        img = Image.new("RGBA", (1024, 1024), (10, 10, 26, 255))
        d = ImageDraw.Draw(img)
        # 玉简
        d.rectangle([300, 200, 724, 824], fill=(241, 196, 15, 255))
        d.rectangle([290, 190, 734, 210], fill=(60, 45, 10, 255))
        d.rectangle([290, 814, 734, 834], fill=(60, 45, 10, 255))
        for i in range(5):
            d.line([340, 320 + i*80, 684, 320 + i*80], fill=(60, 45, 10, 255), width=6)
        img.save(path)
    else:
        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")  # 最小占位（会被 buildozer 忽略，需本地替换）
    print(f"  icon.png")

def make_bg(name, size, bg, accent, text):
    path = os.path.join(ASSETS, name)
    if HAS_PIL:
        img = Image.new("RGB", size, bg)
        d = ImageDraw.Draw(img)
        # 光晕圆
        cx, cy = size[0]//2, size[1]//2 - 100
        for r in range(300, 0, -4):
            alpha = int(40 * (1 - r/300))
            col = tuple(min(255, c + alpha) for c in accent)
            d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
        # 篆文纹路（竖线）
        for x in range(200, size[0]-200, 60):
            d.line([x, 200, x, size[1]-200], fill=(accent[0]//3, accent[1]//3, accent[2]//3), width=2)
        try:
            font = ImageFont.truetype("msyh.ttc", 72)
        except Exception:
            font = ImageFont.load_default()
        d.text((cx-180, cy-40), text, fill=accent, font=font)
        img.save(path)
    else:
        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
    print(f"  {name}")

if __name__ == "__main__":
    print("[资源] 生成美术占位图（有 AI 原图请直接覆盖同名文件）")
    for cfg in BG:
        make_bg(*cfg)
    make_icon()
    print("[资源] 完成")
