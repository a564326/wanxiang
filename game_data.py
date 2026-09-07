# -*- coding: utf-8 -*-
"""
万象词条录 —— 词条数据库
规则：负面词条仅限白色；蓝(rare)及以上全部纯正向。
"""

# 稀有度顺序（由低到高），用于判定"蓝以上"
RARITY_ORDER = ["white", "green", "blue", "purple", "gold", "celestial"]

# 稀有度显示名 + 颜色
RARITY_META = {
    "white":    {"name": "凡俗", "color": "#B0B0B0", "emoji": "○", "chance": 0.55},
    "green":    {"name": "精良", "color": "#4CAF50", "emoji": "●", "chance": 0.30},
    "blue":     {"name": "稀有", "color": "#2196F3", "emoji": "■", "chance": 0.12},
    "purple":   {"name": "史诗", "color": "#9C27B0", "emoji": "▲", "chance": 0.025},
    "gold":     {"name": "传说", "color": "#F1C40F", "emoji": "★", "chance": 0.005},
    "celestial": {"name": "神话", "color": "#FF6EC7", "emoji": "✦", "chance": 0.0001},
}

# 道统分类
SCHOOLS = ["剑", "丹", "阵", "符", "兽", "魔", "佛", "儒"]

# 装备槽位
SLOTS = ["头", "身", "手", "脚", "心"]

# ---------- 词条数据 ----------
# 每条: id, name, rarity, school, slot, effect, negative=False
WHITE = [
    ("w_speed", "疾行", "white", "剑", "脚", "移动速度+5%"),
    ("w_eye", "明眸", "white", "符", "头", "视野+10%"),
    ("w_ear", "聪耳", "white", "符", "头", "听觉范围+15%"),
    ("w_hand", "巧手", "white", "丹", "手", "采集产物+1"),
    ("w_breathe", "吐纳", "white", "儒", "心", "灵气恢复+3/时"),
    ("w_skin", "铜皮", "white", "身", "身", "受击伤害-2%"),
    ("w_bone", "铁骨", "white", "身", "身", "负重+10"),
    ("w_fire", "小火苗", "white", "丹", "手", "火焰伤害+5%"),
    ("w_water", "水感", "white", "丹", "心", "水中呼吸时间+20%"),
    ("w_jump", "轻身", "white", "剑", "脚", "跳跃高度+10%"),
    ("w_climb", "攀援", "white", "剑", "手", "攀爬速度+15%"),
    ("w_swim", "善泳", "white", "剑", "脚", "游泳速度+20%"),
    ("w_rest", "安眠", "white", "儒", "心", "休息恢复+10%"),
    ("w_eat", "暴食", "white", "丹", "身", "进食饱腹感+30%"),
    ("w_luck", "小幸运", "white", "儒", "心", "掉落率+1%"),
    ("w_memory", "过目", "white", "儒", "头", "记忆留存+10%"),
    ("w_talk", "善言", "white", "儒", "头", "交谈好感+5%"),
    ("w_trade", "小算盘", "white", "儒", "手", "交易价格+2%"),
    ("w_cold", "耐寒", "white", "身", "身", "寒冷伤害-10%"),
    ("w_heat", "耐热", "white", "身", "身", "炎热伤害-10%"),
    ("w_toxin", "微抗毒", "white", "丹", "身", "中毒伤害-15%"),
    ("w_bleed", "凝血", "white", "丹", "身", "流血伤害-10%"),
    ("w_fear", "无畏", "white", "佛", "心", "恐惧持续时间-20%"),
    ("w_focus", "专注", "white", "佛", "头", "引导中断率-10%"),
    ("w_heal", "自愈", "white", "丹", "心", "脱离战斗后回血+5%"),
    ("w_arrow", "稳手", "white", "剑", "手", "远程散射-10%"),
    ("w_knife", "利刃", "white", "剑", "手", "切割伤害+3%"),
    ("w_shield", "格挡", "white", "剑", "手", "格挡几率+3%"),
    ("w_run", "健步", "white", "剑", "脚", "冲刺消耗-10%"),
    # 负面（仅白色）
    ("w_lost", "路痴", "white", "头", "头", "迷路概率+20%", True),
    ("w_sleepy", "贪睡", "white", "儒", "心", "清晨状态延迟30分钟", True),
    ("w_tickle", "怕痒", "white", "身", "身", "被击中要害概率+5%", True),
    ("w_seasick", "晕船", "white", "剑", "脚", "乘船/飞行眩晕+30%", True),
    ("w_mosquito", "招蚊", "white", "身", "身", "野外持续掉血+1/秒", True),
    ("w_stutter", "口吃", "white", "儒", "头", "交谈有10%概率失败", True),
    ("w_glutton", "贪嘴", "white", "丹", "身", "进食消耗翻倍", True),
    ("w_noisy", "唠叨", "white", "儒", "头", "潜行被发现距离+20%", True),
    ("w_short", "惧高", "white", "剑", "脚", "高处坠落伤害+25%", True),
    ("w_dark", "畏光", "white", "佛", "头", "强光下命中-10%", True),
    ("w_left", "左撇子", "white", "剑", "手", "非惯用手装备效果-15%", True),
    ("w_thirst", "易渴", "white", "丹", "身", "水分消耗+30%", True),
    ("w_angry", "易怒", "white", "魔", "心", "受击后命中-5%持续10秒", True),
]

GREEN = [
    ("g_sword", "剑心", "green", "剑", "手", "剑类伤害+12%"),
    ("g_pill", "丹心", "green", "丹", "心", "炼丹成功率+15%"),
    ("g_array", "阵眼", "green", "阵", "手", "阵法持续时间+20%"),
    ("g_talisman", "符骨", "green", "符", "手", "符箓效果+15%"),
    ("g_beast", "兽感", "green", "兽", "脚", "驯服成功率+20%"),
    ("g_demon", "魔血", "green", "魔", "心", "吸血+5%"),
    ("g_buddha", "佛心", "green", "佛", "心", "治疗效果+15%"),
    ("g_confucian", "儒骨", "green", "儒", "头", "经验获取+10%"),
    ("g_body", "炼体", "green", "身", "身", "最大生命+8%"),
    ("g_mana", "灵海", "green", "儒", "心", "最大灵气+12%"),
    ("g_regen", "回春", "green", "丹", "心", "每秒回血+2"),
    ("g_speed2", "迅捷", "green", "剑", "脚", "移动速度+12%"),
    ("g_crit", "会心", "green", "剑", "手", "暴击率+5%"),
    ("g_critdmg", "暴烈", "green", "剑", "手", "暴击伤害+20%"),
    ("g_armor", "坚甲", "green", "身", "身", "护甲+15%"),
    ("g_thorn", "反伤", "green", "身", "身", "受到近战伤害时反弹20%"),
    ("g_leech", "饮血", "green", "魔", "手", "造成物理伤害时回血+3%"),
    ("g_focus2", "凝神", "green", "佛", "头", "技能冷却-8%"),
    ("g_range", "远见", "green", "符", "头", "攻击距离+10%"),
    ("g_split", "分裂", "green", "剑", "手", "箭矢/弹道+1"),
    ("g_storm", "引雷体", "green", "丹", "心", "雷系伤害+25%，但被雷劈伤害+50%", True),
]

BLUE = [
    ("b_jianlai", "剑来", "blue", "剑", "手", "每第6次攻击自动释放一次无消耗剑气"),
    ("b_break", "破法", "blue", "剑", "手", "攻击有20%概率无视目标30%护甲"),
    ("b_extra", "额外掉落", "blue", "丹", "手", "击杀精英敌人额外掉落1件物品"),
    ("b_counter", "自动反击", "blue", "身", "身", "被近战击中时自动反击一次80%伤害"),
    ("b_swallow", "灵气过肺", "blue", "儒", "心", "周围灵气自动缓慢转化为自身灵气"),
    ("b_immune_low", "低阶免疫", "blue", "佛", "心", "免疫低于自身一个大境界的控制效果"),
    ("b_double", "双修", "blue", "丹", "心", "修炼速度+25%，丹药效果+25%"),
    ("b_eye2", "天眼", "blue", "符", "头", "可看穿一切伪装与隐身"),
    ("b_portal", "缩地", "blue", "阵", "脚", "短距离传送冷却-40%"),
    ("b_tame", "万兽臣服", "blue", "兽", "心", "同等级及以下野兽初始好感为友善"),
    ("b_absorb", "炼化", "blue", "魔", "手", "击败敌人有概率直接吸收其一项属性"),
    ("b_ward", "法盾", "blue", "佛", "身", "每60秒自动获得一个吸收15%伤害的护盾"),
    ("b_chain", "连锁", "blue", "阵", "手", "攻击命中后可弹射至另一个目标"),
    ("b_seal", "封印", "blue", "符", "手", "攻击有概率使目标下一个技能施法失败"),
    ("b_enlighten", "顿悟", "blue", "儒", "头", "每完成一次突破，随机一项属性永久+1%"),
]

PURPLE = [
    ("p_jianyu", "剑域", "purple", "剑", "手", "展开剑域，域内所有剑类伤害+40%"),
    ("p_ignore", "无视品阶", "purple", "剑", "手", "攻击可忽略目标品阶带来的减伤"),
    ("p_rebirth", "涅槃", "purple", "佛", "心", "每场战斗首次致命伤害时自动复活并恢复50%生命"),
    ("p_plunder", "夺天", "purple", "魔", "心", "每击杀一个强敌，永久掠夺其1%最大属性"),
    ("p_fate", "改命", "purple", "儒", "头", "可指定修改自身一项命格属性"),
    ("p_causal", "因果", "purple", "佛", "心", "对造成过伤害的敌人，后续伤害+30%"),
    ("p_world", "洞天", "purple", "阵", "心", "自带一处可成长的随身洞天福地"),
    ("p_alchemy", "丹成", "purple", "丹", "手", "炼丹必定出极品，且额外产出一份副产物"),
    ("p_talisman", "万符", "purple", "符", "手", "同时使用符箓数量+3，符箓不占冷却"),
    ("p_summon", "召唤", "purple", "兽", "心", "可同时契约并召唤两只高阶灵兽"),
]

GOLD = [
    ("g_dadao", "大道可期", "gold", "儒", "心", "所有修炼瓶颈突破概率永久+50%"),
    ("g_qiyun", "气运加身", "gold", "儒", "头", "所有概率类事件（掉落/暴击/奇遇）结果恒定为有利"),
    ("g_yinian", "一念成法", "gold", "佛", "手", "消耗全部灵气，将任意一门术法临时提升至满阶"),
    ("g_immortal", "仙骨", "gold", "身", "身", "飞升所需积累减半，渡劫伤害-50%"),
    ("g_allknow", "万象通明", "gold", "儒", "头", "可瞬时推演并掌握任何一门技艺至当世顶峰"),
    ("g_create", "造化", "gold", "丹", "心", "可将任意两件物品融合，必出更高品阶产物"),
]

CELESTIAL = [
    ("c_tiandao", "我即天数", "celestial", "儒", "心",
     "你的意志可直接改写为一条天地规则，每日一次；每次改写后，天道雷罚威力逐次+50%", True),
    ("c_nowait", "飞升不用排队", "celestial", "佛", "心",
     "飞升时跳过天劫直接进入仙界；代价是仙界对你初始态度为敌视", True),
    ("c_wanjie", "万界归墟", "celestial", "魔", "心",
     "可将一整片小世界的灵气瞬间抽干化为己用；使用后该世界灵气枯竭百年", True),
    ("c_creation", "创生", "celestial", "丹", "心",
     "可凭空创造一件此前不存在的物品或生命；每次创造索取你等量的寿元", True),
    ("c_mingyun", "命不由天", "celestial", "佛", "心",
     "免疫一切因果律攻击、预言与诅咒；代价是也永远无法被任何人祝福或结契", True),
    ("c_woming", "我命由我", "celestial", "魔", "心",
     "死亡时自动逆转因果复活，每千年一次；复活后所有已装备词条过载降一阶", True),
    ("c_yuanzhu", "万象归源", "celestial", "儒", "心",
     "所有已装备词条效果翻倍，装备槽+3；每场大战后随机一条词条过载损坏", True),
    ("c_wodao", "我即是道", "celestial", "儒", "心",
     "你的一言一行皆可被天地承认为'道'；当你证道之日，天道将视你为叛徒并全力抹杀", True),
]

ENTRIES = {
    "white": WHITE,
    "green": GREEN,
    "blue": BLUE,
    "purple": PURPLE,
    "gold": GOLD,
    "celestial": CELESTIAL,
}

def all_entries():
    result = []
    for r in RARITY_ORDER:
        for e in ENTRIES.get(r, []):
            d = dict(zip(["id", "name", "rarity", "school", "slot", "effect"], e[:6]))
            if len(e) > 6:
                d["negative"] = e[6]
            result.append(d)
    return result

def get_entries_by_rarity(rarity):
    return [dict(zip(["id", "name", "rarity", "school", "slot", "effect"], e[:6])) for e in ENTRIES.get(rarity, [])]

def get_normal_pool():
    pool = []
    for r in ["white", "green", "blue", "purple", "gold"]:
        pool.extend(get_entries_by_rarity(r))
    return pool

def get_celestial_pool():
    return get_entries_by_rarity("celestial")

def roll_rarity():
    import random
    r = random.random()
    cum = 0
    for rarity in RARITY_ORDER[:-1]:
        cum += RARITY_META[rarity]["chance"]
        if r < cum:
            return rarity
    return "celestial"

# 境界系统
REALMS = [
    {"name": "练气", "pool_max": "green", "slots": 2},
    {"name": "筑基", "pool_max": "green", "slots": 3},
    {"name": "金丹", "pool_max": "blue",  "slots": 4},
    {"name": "元婴", "pool_max": "blue",  "slots": 5},
    {"name": "化神", "pool_max": "purple","slots": 6},
    {"name": "炼虚", "pool_max": "purple","slots": 7},
    {"name": "渡劫", "pool_max": "gold",  "slots": 8},
    {"name": "大乘", "pool_max": "celestial","slots": 9},
]

def realm_index(realm_name):
    for i, r in enumerate(REALMS):
        if r["name"] == realm_name:
            return i
    return 0

def available_rarities(realm_name):
    idx = realm_index(realm_name)
    cap = REALMS[idx]["pool_max"]
    cap_idx = RARITY_ORDER.index(cap)
    return RARITY_ORDER[:cap_idx + 1]

# 道统羁绊
BONDS = {
    "剑": {"name": "剑道", "desc": "同系≥3：剑类伤害+20%；≥5：剑气自动护主"},
    "丹": {"name": "丹道", "desc": "同系≥3：丹药效果+30%；≥5：自动炼丹"},
    "阵": {"name": "阵道", "desc": "同系≥3：阵法范围+30%；≥5：阵法永续"},
    "符": {"name": "符道", "desc": "同系≥3：符箓冷却-25%；≥5：符箓不耗灵气"},
    "兽": {"name": "御兽", "desc": "同系≥3：灵兽属性+25%；≥5：可共存召唤"},
    "魔": {"name": "魔道", "desc": "同系≥3：吸血+10%；≥5：击杀回满"},
    "佛": {"name": "佛道", "desc": "同系≥3：治疗效果+25%；≥5：免疫负面"},
    "儒": {"name": "儒道", "desc": "同系≥3：经验+20%；≥5：顿悟概率翻倍"},
}

GOLD_COLOR = "#F1C40F"
BG_DARK = "#0a0a1a"
CELESTIAL_COLOR = RARITY_META["celestial"]["color"]

# 向后兼容别名（供 gacha_anim / main 引用）
GOLD = GOLD_COLOR
RARITY_COLOR = {r: meta["color"] for r, meta in RARITY_META.items()}
