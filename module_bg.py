# -*- coding: utf-8 -*-
"""模块背景：专属插画 + 暗色遮罩"""
import os
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class ModuleBackground(Widget):
    """根据模块名加载对应插画，叠加暗色遮罩保证文字清晰。"""
    _map = {
        "gacha_bg": "gacha_bg.png",
        "smelt_bg": "smelt_bg.png",
        "realm_bg": "realm_bg.png",
        "celestial_bg": "celestial_bg.png",
        "bg": "bg.png",
    }
    _dim = {
        "gacha_bg": 0.66, "smelt_bg": 0.70, "realm_bg": 0.72,
        "celestial_bg": 0.60, "bg": 0.78,
    }

    def __init__(self, key="bg", **kw):
        super().__init__(**kw)
        self.key = key
        self._img = None
        self._mask = None
        self.bind(size=self._layout, pos=self._layout)
        Clock = None
        try:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._layout(), 0)
        except Exception:
            pass

    def _layout(self, *a):
        self.canvas.clear()
        assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        fname = self._map.get(self.key, "bg.png")
        path = os.path.join(assets, fname)
        dim = self._dim.get(self.key, 0.75)

        with self.canvas:
            # 底色
            Color(0.04, 0.04, 0.10, 1)
            Rectangle(pos=self.pos, size=self.size)
            # 插画
            if os.path.exists(path):
                from kivy.uix.image import Image
                self._img = Image(source=path, size=self.size, pos=self.pos,
                                  allow_stretch=True, keep_ratio=False)
                self.add_widget(self._img)
            # 遮罩
            Color(0.04, 0.04, 0.10, dim)
            Rectangle(pos=self.pos, size=self.size)
