# -*- coding: utf-8 -*-
"""
抽卡动画动态适配验证 —— 用「可驱动时钟」mock 掉 kivy，真实跑一遍时序。
验证：普通定格回调、天外之象碎裂(碎片位移+自动停止)、回调仅触发一次。
"""
import os, sys, math
import importlib.util

spec = importlib.util.spec_from_file_location("gd", os.path.join(os.path.dirname(__file__), "game_data.py"))
gd = importlib.util.module_from_spec(spec); spec.loader.exec_module(gd)
sys.modules["game_data"] = gd

# ---------- mock kivy.clock.Clock ----------
class FakeClock:
    """手动推进的时间钟，取代 kivy 真实时钟"""
    def __init__(self):
        self.t = 0.0
        self._intervals = []   # (period, callback, accumulated)
        self._once = []        # [(delay, callback)]

    def schedule_interval(self, cb, period):
        self._intervals.append([period, cb, 0.0])
        return cb  # 返回 token

    def schedule_once(self, cb, delay=0):
        self._once.append([delay, cb])

    def cancel(self, token):
        # 模拟取消 interval
        self._intervals = [it for it in self._intervals if it is not token and it[1] is not token]

    def advance(self, dt):
        """推进时间，触发到期的 schedule_once 与 schedule_interval 回调"""
        # 1) 处理本次 tick 内到期的 once（按剩余时间升序，循环直到无到期项）
        self.t += dt
        progressed = True
        while progressed:
            progressed = False
            for item in list(self._once):
                delay, cb = item
                if delay <= 1e-9:
                    self._once.remove(item)
                    try:
                        cb(dt)
                    except Exception:
                        pass
                    progressed = True
                    break
                else:
                    item[0] = max(0, delay - dt)
        # 2) intervals：累积满一个 period 就触发
        for it in list(self._intervals):
            period, cb, acc = it
            it[2] = acc + dt
            if it[2] >= period:
                it[2] = 0.0
                try:
                    cb(dt)
                except Exception:
                    pass

# 在 import gacha_anim 之前，把整套 kivy 假模块注册好。
# 关键：gacha_anim 还会 `from kivy.graphics import ...`，子模块必须预先存在。

def _mkmod(name):
    """创建一个空的假模块并注册到 sys.modules，返回该模块对象。"""
    if name in sys.modules:
        return sys.modules[name]
    mod = type(sys)("kivy_stub")
    mod.__name__ = name
    mod.__package__ = name.rsplit(".", 1)[0] if "." in name else name
    sys.modules[name] = mod
    return mod

# 1) 顶层 kivy 包
kivy_pkg = _mkmod("kivy")
kivy_pkg.__path__ = ["kivy_stub_path"]  # 标记为包

# 2) 子包/子模块（预先注册，避免 import 时查找失败）
_mkmod("kivy.graphics")
_mkmod("kivy.clock")
_mkmod("kivy.animation")
_mkmod("kivy.uix")
for _sub in ("widget", "floatlayout", "image", "label", "button", "boxlayout",
             "gridlayout", "scrollview", "popup"):
    _mkmod(f"kivy.uix.{_sub}")

# ---- 最小类桩：只提供动画验证所需接口 ----
class _StubWidget:
    """模拟 kivy Widget：持有 canvas 与基础几何属性"""
    def __init__(self, **kw):
        self.canvas = _StubCanvas()
        self.pos = (0, 0)
        self.size = (100, 100)
        self.center = (50, 50)
        self.center_x = 50
        self.center_y = 50
        self.children = []
        self._callbacks = {}
    def bind(self, **kw):
        self._callbacks.update(kw)
    def add_widget(self, w):
        self.children.append(w)
    def clear_widgets(self):
        self.children = []
    def remove_widget(self, w):
        if w in self.children:
            self.children.remove(w)

class _StubCanvas:
    def __init__(self):
        self.before = self
    def clear(self):
        pass
    def add(self, inst):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False

class _StubAnimation:
    """替代 kivy.animation.Animation —— start 时立即触发 on_complete"""
    def __init__(self, **kw):
        self.on_complete = None
    def start(self, target):
        if self.on_complete:
            try:
                self.on_complete(target)
            except Exception:
                pass

# 3) 把类放到对应模块（供 `from kivy.uix.X import Y`）
sys.modules["kivy.uix.widget"].Widget = _StubWidget
sys.modules["kivy.uix.floatlayout"].FloatLayout = type("FloatLayout", (_StubWidget,), {})
sys.modules["kivy.uix.image"].Image = type("Image", (_StubWidget,), {})
sys.modules["kivy.uix.label"].Label = type("Label", (_StubWidget,), {})
sys.modules["kivy.uix.button"].Button = type("Button", (_StubWidget,), {})
sys.modules["kivy.uix.boxlayout"].BoxLayout = type("BoxLayout", (_StubWidget,), {})
sys.modules["kivy.uix.gridlayout"].GridLayout = type("GridLayout", (_StubWidget,), {})
sys.modules["kivy.uix.scrollview"].ScrollView = type("ScrollView", (_StubWidget,), {})
sys.modules["kivy.uix.popup"].Popup = type("Popup", (_StubWidget,), {})

# graphics 绘图指令桩（实例化即可）
class _GraphicInst:
    def __init__(self, *a, **kw):
        pass
for _g in ("Color", "Rectangle", "Ellipse", "Line"):
    setattr(sys.modules["kivy.graphics"], _g, _GraphicInst)

# clock & animation
sys.modules["kivy.clock"].Clock = FakeClock
sys.modules["kivy.animation"].Animation = _StubAnimation

# 让 `import kivy` / `from kivy import ...` 可用
sys.modules["kivy"] = kivy_pkg

import gacha_anim  # noqa: E402  (必须在 mock 之后)

passed, failed = [], []

def check(cond, name):
    if cond:
        passed.append(name)
        print(f"  ✓ {name}")
    else:
        failed.append(name)
        print(f"  ✗ {name}")

print("[A] 普通词条：玉简旋转 -> 定格 -> 回调")
clock = FakeClock()
gacha_anim.Clock = clock
callback_fired = [0]
anim = gacha_anim.GachaAnimation()
anim._event = None
anim.play_normal(callback=lambda: callback_fired.__setitem__(0, callback_fired[0] + 1))
clock.advance(2.0)  # 超过 duration 1.6s
check(callback_fired[0] == 1, "定格回调触发且仅触发一次")

print("\n[B] 天外之象：碎裂 -> 碎片位移 -> 自动停止 -> 回调")
clock2 = FakeClock()
gacha_anim.Clock = clock2
anim2 = gacha_anim.GachaAnimation()
cb2 = [0]
entry = gd.get_celestial_pool()[0]
anim2.play_celestial(entry, callback=lambda: cb2.__setitem__(0, cb2[0] + 1))
# 驱动碎片动画 1.2s（60fps → 72 帧）
for _ in range(80):
    clock2.advance(1 / 60)
check(cb2[0] == 1, "碎裂结束回调触发")
check(anim2._event is None, "碎片动画 1.2s 后自动停止(无泄漏)")

print("\n[D] 动画模块 import 完整性 + 关键方法")
check(hasattr(gacha_anim, "GachaAnimation"), "GachaAnimation 类存在")
check(hasattr(anim, "play_normal"), "play_normal 方法存在")
check(hasattr(anim, "play_celestial"), "play_celestial 方法存在")

print("\n[C] 模块背景接入数")
import module_bg
print(f"   背景映射: {len(module_bg.ModuleBackground._map)} 个模块")
check(len(module_bg.ModuleBackground._map) >= 5, "主界面+4模块背景已接入")

print("\n" + "="*40)
print(f"通过 {len(passed)} / 失败 {len(failed)}")
sys.exit(1 if failed else 0)
