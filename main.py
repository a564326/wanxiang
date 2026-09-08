# -*- coding: utf-8 -*-
"""万象词条录 - 主界面（Kivy）"""
import os

# ========== 中文字体注册（必须在所有 kivy import 之前） ==========
from kivy.core.text import LabelBase
from kivy.config import Config

# 字体候选列表：项目字体优先，系统字体兜底
FONT_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts", "simhei.ttf"),
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\msyh.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/system/fonts/NotoSansCJK-Regular.ttc",
]

_registered = False
for _fp in FONT_CANDIDATES:
    if os.path.exists(_fp):
        try:
            LabelBase.register(name="CJK", fn_regular=_fp)
            Config.set("kivy", "default_font", ["CJK", _fp])
            print(f"[字体] 已注册中文字体: {_fp}")
            _registered = True
            break
        except Exception as e:
            print(f"[字体] 注册失败 {_fp}: {e}")

if not _registered:
    print("[字体] 警告：未找到中文字体，中文可能显示为方块")
# ========== 字体注册结束 ==========

import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

import game_data as gd
from gacha_anim import GachaAnimation
from module_bg import ModuleBackground

__version__ = "0.2"

Window.clearcolor = (0.04, 0.04, 0.10, 1)

# ---------- 通用样式 ----------
def rarity_color(rarity):
    return gd.RARITY_META.get(rarity, {}).get("color", "#FFFFFF")

class CardLabel(Label):
    def __init__(self, **kw):
        kw.setdefault("color", (0.95, 0.95, 0.95, 1))
        kw.setdefault("font_size", "15sp")
        super().__init__(**kw)

class EntryCard(BoxLayout):
    """词条卡牌：左侧道统色条 + 稀有度金框"""
    def __init__(self, entry, **kw):
        super().__init__(orientation="horizontal", size_hint_y=None, height="64dp",
                         spacing="6dp", padding="6dp")
        self.entry = entry
        with self.canvas.before:
            Color(1, 1, 1, 0.04)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

        # 稀有度框
        self.border = BoxLayout(size_hint=(1, 1))
        self.add_widget(self.border)

        left = BoxLayout(orientation="vertical", size_hint_x=0.85, spacing=2)
        name_color = rarity_color(entry["rarity"])
        left.add_widget(CardLabel(text=f"[{gd.RARITY_META[entry['rarity']]['emoji']}] {entry['name']}",
                                  color=tuple(int(name_color[i:i+2], 16)/255 for i in (1,3,5)) + (1,),
                                  font_size="15sp", halign="left", text_size=(None, None)))
        left.add_widget(CardLabel(text=f"{entry.get('school','')}·{entry.get('slot','')}  {entry['effect']}",
                                  font_size="11sp", color=(0.75, 0.75, 0.75, 1), halign="left"))
        self.add_widget(left)

    def _update(self, *a):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ---------- 抽卡 ----------
class GachaScreen(FloatLayout):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.add_widget(ModuleBackground("gacha_bg"))

        box = BoxLayout(orientation="vertical", padding="20dp", spacing="16dp",
                        size_hint=(0.9, 0.85), pos_hint={"center_x": 0.5, "center_y": 0.5})

        box.add_widget(CardLabel(text="观想玉简", font_size="28sp", color=(0.95, 0.76, 0.2, 1)))
        box.add_widget(CardLabel(text="十连5%概率瞥见天外之象，效果不可窥测", font_size="12sp", color=(0.7,0.7,0.7,1)))

        self.anim_area = FloatLayout(size_hint_y=0.5)
        box.add_widget(self.anim_area)

        btns = BoxLayout(size_hint_y=None, height="56dp", spacing="12dp")
        btn_single = Button(text="观想·单抽", background_color=(0.2, 0.15, 0.05, 1),
                             color=(0.95, 0.76, 0.2, 1))
        btn_single.bind(on_release=lambda x: self.pull(1))
        btn_ten = Button(text="观想·十连", background_color=(0.2, 0.15, 0.05, 1),
                         color=(0.95, 0.76, 0.2, 1))
        btn_ten.bind(on_release=lambda x: self.pull(10))
        btns.add_widget(btn_single)
        btns.add_widget(btn_ten)
        box.add_widget(btns)

        self.result_area = BoxLayout(orientation="vertical", size_hint_y=0.4, spacing=2)
        box.add_widget(self.result_area)

        box.add_widget(Button(text="← 返回", size_hint_y=None, height="40dp",
                              on_release=lambda x: app.show_main()))
        self.add_widget(box)

    def pull(self, count):
        self.result_area.clear_widgets()
        # 天外候选判定
        celestial = None
        if count == 10 and random.random() < 0.05:
            celestial = random.choice(gd.get_celestial_pool())
        elif count == 1 and random.random() < 0.005:
            celestial = random.choice(gd.get_celestial_pool())

        self.anim_area.clear_widgets()
        anim = GachaAnimation(size_hint=(1, 1))
        self.anim_area.add_widget(anim)

        results = []
        if celestial:
            anim.play_celestial(celestial, callback=lambda: self._on_finish(results, celestial))
        else:
            for _ in range(count):
                rar = gd.roll_rarity()
                pool = gd.get_normal_pool()
                pool = [e for e in pool if e["rarity"] == rar and
                        e["rarity"] in gd.available_rarities(self.app.realm)]
                if not pool:
                    pool = gd.get_normal_pool()
                results.append(random.choice(pool))
            anim.play_normal(callback=lambda: self._on_finish(results, None))

    def _on_finish(self, results, celestial):
        self.result_area.clear_widgets()
        if celestial:
            self.result_area.add_widget(CardLabel(
                text=f"天外之象掠过：{celestial['name']}（效果不可窥测）— 道心+1",
                color=(1, 0.43, 0.78, 1), font_size="13sp"))
            self.app.daoxin += 1
        for e in results:
            self.result_area.add_widget(EntryCard(e))
        self.app.collected.update({e["id"]: e for e in results})
        self.app.check_celestial_unlock()

# ---------- 背包 ----------
class InventoryScreen(FloatLayout):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.add_widget(ModuleBackground("bg"))
        box = BoxLayout(orientation="vertical", padding="16dp", spacing="10dp",
                        size_hint=(0.95, 0.9), pos_hint={"center_x": 0.5, "center_y": 0.5})

        box.add_widget(CardLabel(text="道统分类·词条背包", font_size="24sp", color=(0.95,0.76,0.2,1)))

        filters = GridLayout(cols=len(gd.SCHOOLS)+1, size_hint_y=None, height="40dp", spacing=2)
        filters.add_widget(Button(text="全部", on_release=lambda x: self.refresh(None)))
        for s in gd.SCHOOLS:
            filters.add_widget(Button(text=s, on_release=lambda x, sch=s: self.refresh(sch)))
        box.add_widget(filters)

        self.list_area = BoxLayout(orientation="vertical", size_hint_y=0.7)
        box.add_widget(self.list_area)

        box.add_widget(Button(text="← 返回", size_hint_y=None, height="40dp",
                              on_release=lambda x: app.show_main()))
        self.add_widget(box)
        self.refresh(None)

    def refresh(self, school):
        self.list_area.clear_widgets()
        entries = list(self.app.collected.values())
        if school:
            entries = [e for e in entries if e.get("school") == school]
        for e in entries:
            self.list_area.add_widget(EntryCard(e))

# ---------- 境界 ----------
class RealmScreen(FloatLayout):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.add_widget(ModuleBackground("realm_bg"))
        box = BoxLayout(orientation="vertical", padding="16dp", spacing="10dp",
                        size_hint=(0.95, 0.9), pos_hint={"center_x": 0.5, "center_y": 0.5})
        box.add_widget(CardLabel(text="境界突破", font_size="24sp", color=(0.95,0.76,0.2,1)))
        self.info = BoxLayout(orientation="vertical", size_hint_y=0.6, spacing=4)
        box.add_widget(self.info)
        btn = Button(text="突破（消耗道心）", size_hint_y=None, height="50dp",
                     background_color=(0.2,0.15,0.05,1), color=(0.95,0.76,0.2,1))
        btn.bind(on_release=lambda x: self.breakthrough())
        box.add_widget(btn)
        box.add_widget(Button(text="← 返回", size_hint_y=None, height="40dp",
                              on_release=lambda x: app.show_main()))
        self.add_widget(box)
        self.refresh()

    def refresh(self):
        self.info.clear_widgets()
        idx = gd.realm_index(self.app.realm)
        cur = gd.REALMS[idx]
        cost = (idx + 1) * 3
        self.info.add_widget(CardLabel(text=f"当前：{cur['name']}  装备槽 {cur['slots']}  词条池上限 {cur['pool_max']}",
                                       font_size="14sp"))
        self.info.add_widget(CardLabel(text=f"道心：{self.app.daoxin}    突破需 {cost}",
                                       font_size="14sp", color=(0.95,0.76,0.2,1)))
        if idx + 1 < len(gd.REALMS):
            nxt = gd.REALMS[idx + 1]
            self.info.add_widget(CardLabel(text=f"下一境界：{nxt['name']}（解锁 {nxt['pool_max']} 词条）",
                                           font_size="13sp", color=(0.6,0.9,0.6,1)))

    def breakthrough(self):
        idx = gd.realm_index(self.app.realm)
        cost = (idx + 1) * 3
        if self.app.daoxin < cost:
            self._popup("道心不足", f"还需 {cost - self.app.daoxin} 点道心")
            return
        if idx + 1 >= len(gd.REALMS):
            self._popup("已达巅峰", "已是最高境界")
            return
        self.app.daoxin -= cost
        self.app.realm = gd.REALMS[idx + 1]["name"]
        self.app.slots = gd.REALMS[idx + 1]["slots"]
        self._popup("突破成功", f"晋升【{self.app.realm}】！")
        self.refresh()

    def _popup(self, title, msg):
        p = Popup(title=title, content=CardLabel(text=msg, size_hint=(0.8, 0.4)),
                  size_hint=(0.7, 0.35))
        p.open()

# ---------- 主界面 ----------
class MainScreen(FloatLayout):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.add_widget(ModuleBackground("bg"))

        center = BoxLayout(orientation="vertical", spacing="14dp",
                           size_hint=(0.85, 0.75), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # 中央徽章
        badge = BoxLayout(orientation="vertical", size_hint_y=None, height="110dp",
                          padding="10dp")
        with badge.canvas.before:
            Color(0.95, 0.76, 0.2, 0.12)
            Rectangle(pos=badge.pos, size=badge.size)
        badge.bind(pos=lambda *a: badge.canvas.ask_update())
        badge.add_widget(CardLabel(text="❖ 万象词条录 ❖", font_size="30sp",
                                   color=(0.95, 0.76, 0.2, 1)))
        badge.add_widget(CardLabel(text="外挂·天道不容之物", font_size="12sp", color=(0.7,0.7,0.7,1)))
        center.add_widget(badge)

        # 道心 + 境界
        center.add_widget(CardLabel(
            text=f"境界：{app.realm}    道心：{app.daoxin}    装备槽：{app.slots}",
            font_size="13sp", color=(0.85,0.85,0.85,1)))

        # 六模块网格
        grid = GridLayout(cols=2, spacing="10dp", size_hint_y=0.75)
        modules = [
            ("观想抽取", lambda: app.show_gacha(), gd.GOLD_COLOR),
            ("词条背包", lambda: app.show_inventory(), "#4FC3F7"),
            ("化道炉·熔炼", lambda: app.show_toast("化道炉·开发中"), "#FF8A65"),
            ("问道·任务", lambda: app.show_toast("问道·开发中"), "#CE93D8"),
            ("境界突破", lambda: app.show_realm(), "#81C784"),
            ("天外之象", lambda: app.show_celestial(), "#FF6EC7"),
        ]
        for name, action, color in modules:
            btn = Button(text=name, size_hint_y=None, height="58dp",
                         background_color=(0.08, 0.08, 0.16, 1),
                         color=tuple(int(color[i:i+2],16)/255 for i in (1,3,5)) + (1,))
            btn.bind(on_release=lambda x, a=action: a())
            grid.add_widget(btn)
        center.add_widget(grid)

        self.add_widget(center)

# ---------- App ----------
class WanxiangApp(App):
    def build(self):
        self.realm = "练气"
        self.daoxin = 0
        self.slots = 2
        self.collected = {}
        self.celestial_seen = []
        self.screen = MainScreen(self)
        return self.screen

    def show_main(self):
        self.screen = MainScreen(self)
        Window.clear()

    def show_gacha(self):
        self.screen = GachaScreen(self)
        Window.clear()

    def show_inventory(self):
        self.screen = InventoryScreen(self)
        Window.clear()

    def show_realm(self):
        self.screen = RealmScreen(self)
        Window.clear()

    def show_celestial(self):
        self.show_toast("天外之象：尚无彩词条凝聚")

    def show_toast(self, msg):
        p = Popup(title="万象词条录", content=CardLabel(text=msg, size_hint=(0.8, 0.4)),
                  size_hint=(0.75, 0.3))
        p.open()

    def check_celestial_unlock(self):
        idx = gd.realm_index(self.realm)
        if idx >= gd.realm_index("渡劫") and len(self.celestial_seen) == 0:
            self.celestial_seen.append(True)

if __name__ == "__main__":
    WanxiangApp().run()
