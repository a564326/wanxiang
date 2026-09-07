# -*- coding: utf-8 -*-
"""抽卡动画：玉简旋转 -> 定格 / 天外之象碎裂"""
import random
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.animation import Animation
from game_data import RARITY_META, CELESTIAL

# 兼容常量
GOLD = RARITY_META["gold"]["color"]


class GachaAnimation(FloatLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._event = None

    # ---------- 普通词条 ----------
    def play_normal(self, callback=None, duration=1.6):
        self._draw_scroll(spinning=True)
        self._spawn_particles()
        self._event = Clock.schedule_interval(lambda dt: None, 0)
        anim = Animation(opacity=1, duration=duration)
        if callback:
            anim.on_complete = lambda *a: (self._settle(), callback() if callback else None)
        anim.start(self)

    # ---------- 天外之象：碎裂 ----------
    def play_celestial(self, entry, callback=None):
        self._draw_scroll(spinning=True, celestial=True)
        Clock.schedule_once(lambda dt: self._shatter(entry, callback), 0.9)

    # ---------- 绘制玉简 ----------
    def _draw_scroll(self, spinning=False, celestial=False):
        self.clear_widgets()
        with self.canvas:
            self.canvas.clear()
            cx, cy = self.center
            # 光环
            Color(0.95, 0.76, 0.2, 0.15 if not celestial else 0.5)
            Ellipse(pos=(cx-90, cy-90), size=(180, 180))
            # 玉简主体
            Color(0.9, 0.72, 0.2, 1)
            Rectangle(pos=(cx-30, cy-70), size=(60, 140))
            Color(0.3, 0.22, 0.05, 1)
            Rectangle(pos=(cx-34, cy-74), size=(68, 6))
            Rectangle(pos=(cx-34, cy+68), size=(68, 6))
            # 篆文
            Color(0.2, 0.15, 0.05, 1)
            for i in range(5):
                Line(points=[cx-18, cy-40+i*20, cx+18, cy-40+i*20], width=1.2)
            if celestial:
                Color(1, 0.43, 0.78, 0.9)
                Ellipse(pos=(cx-40, cy-40), size=(80, 80))

    def _spawn_particles(self):
        """六色流光粒子"""
        colors = ["#B0B0B0","#4CAF50","#2196F3","#9C27B0","#F1C40F","#FF6EC7"]
        with self.canvas:
            for _ in range(12):
                c = random.choice(colors)
                rgb = tuple(int(c[i:i+2],16)/255 for i in (1,3,5)) + (0.8,)
                Color(*rgb)
                a = random.uniform(0, 6.28)
                r = random.uniform(40, 90)
                Ellipse(pos=(self.center_x + r*__import__("math").cos(a) - 4,
                              self.center_y + r*__import__("math").sin(a) - 4),
                        size=(8, 8))

    def _settle(self):
        self._draw_scroll(spinning=False)

    # ---------- 碎裂 ----------
    def _shatter(self, entry, callback=None):
        self.clear_widgets()
        with self.canvas:
            self.canvas.clear()
            cx, cy = self.center
            Color(1, 0.43, 0.78, 1)
            Ellipse(pos=(cx-50, cy-50), size=(100, 100))
        # 碎片
        self._shards = []
        with self.canvas:
            for i in range(18):
                a = i * (6.28 / 18)
                self._shards.append({
                    "angle": a,
                    "dist": 10,
                    "x": cx, "y": cy,
                })
        self._t = 0
        self._event = Clock.schedule_interval(lambda dt: self._anim_shards(dt, callback), 1/60)

    def _anim_shards(self, dt, callback):
        self._t += dt
        if self._t >= 1.2:
            if self._event:
                self._event.cancel()
                self._event = None
            self.canvas.clear()
            if callback:
                callback()
            return
        self.canvas.clear()
        with self.canvas:
            cx, cy = self.center
            prog = self._t / 1.2
            Color(1, 0.43, 0.78, 1 - prog)
            for s in self._shards:
                s["dist"] = 10 + prog * 120
                x = cx + s["dist"] * __import__("math").cos(s["angle"])
                y = cy + s["dist"] * __import__("math").sin(s["angle"])
                Rectangle(pos=(x-4, y-4), size=(8, 8))
            # 整体淡出
            Color(1, 1, 1, 0.3 * (1 - prog))
            Ellipse(pos=(cx-60*(1+prog), cy-60*(1+prog)), size=(120*(1+prog), 120*(1+prog)))
