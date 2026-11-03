"""知道一件事，就该换另一件事的算法：条件期望与控制变量。

第一部分：全期望公式。把"下个月单量"按天气拆开算一遍，再让模拟核对。
第二部分：天气预报值钱在哪。把已经知道的事定下来，毛边能少一半。
第三部分：控制变量。用一件"相关但你已经知道"的事去减，误差只剩根号下(1−ρ²)。
第四部分：方差分解。总起伏 = 组内起伏 + 组间起伏，看哪一块才是大头。
第五部分：分组过头会反噬。组平均是用几条记录估的，那部分毛边演多少遍都不会小。
第六部分：把"下个月发几条"从已知改成随机，看月总量的起伏涨多少。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random

RAIN_P = 0.3
RAIN_MEAN, RAIN_SD = 60.0, 8.0
FAIR_MEAN, FAIR_SD = 40.0, 5.0
DAYS = 30


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def one_month_random_weather():
    """老老实实模拟一个月：每天连天气一起抽。"""
    total = 0
    for _ in range(DAYS):
        if random.random() < RAIN_P:
            total += random.gauss(RAIN_MEAN, RAIN_SD)
        else:
            total += random.gauss(FAIR_MEAN, FAIR_SD)
    return total


def one_month_known_weather(rain_days):
    """你已经知道这个月有几天雨：天气这一层不再抽，只抽每天单量。"""
    total = 0
    for _ in range(rain_days):
        total += random.gauss(RAIN_MEAN, RAIN_SD)
    for _ in range(DAYS - rain_days):
        total += random.gauss(FAIR_MEAN, FAIR_SD)
    return total


def control(rho, runs):
    """要估的量 Y，和一个你已经知道平均值的辅助量 X，两者相关 rho。
    X 平均固定为 0，所以"减掉 a 倍的 (X − 0)"是合法的：它不减掉真值，只减掉噪声。"""
    plain = []
    fixed = []
    for _ in range(runs):
        common = random.gauss(0, 1)
        x = common
        y = rho * common + math.sqrt(1 - rho ** 2) * random.gauss(0, 1)
        plain.append(y)
        fixed.append(y - rho * (x - 0))
    return spread(plain), spread(fixed)


print("【第一部分：先按天气把期望拆开算】")
per_day = RAIN_P * RAIN_MEAN + (1 - RAIN_P) * FAIR_MEAN
print(f"  雨天 {RAIN_MEAN:.0f} 单、晴天 {FAIR_MEAN:.0f} 单、下雨概率 {RAIN_P}：")
print(f"  拆开来算的日期望 = {RAIN_P} × {RAIN_MEAN:.0f} + {1 - RAIN_P} × {FAIR_MEAN:.0f} = {per_day:.1f}")
print(f"  一个月（{DAYS} 天）= {DAYS * per_day:.0f} 单")
random.seed(7)
months = [one_month_random_weather() for _ in range(20000)]
print(f"  让电脑演两万遍：平均 {sum(months) / len(months):.1f} 单（和上面同一个数）")

print()
print("【第二部分：知道下个月有 12 天雨，值多少】")
random.seed(7)
blind = [one_month_random_weather() for _ in range(20000)]
rain_days = 12
random.seed(7)
foreseen = [one_month_known_weather(rain_days) for _ in range(20000)]
print(f"  不知道天气、每天现抽：月总量 平均 {sum(blind) / len(blind):.1f}，起伏 {spread(blind):.1f} 单")
print(f"  已知这个月有 {rain_days} 天雨：月总量 平均 {sum(foreseen) / len(foreseen):.1f}，起伏 {spread(foreseen):.1f} 单")
print(f"  期望多了 {sum(foreseen) / len(foreseen) - sum(blind) / len(blind):.1f} 单，起伏少了 {(1 - spread(foreseen) / spread(blind)) * 100:.1f}%")
print(f"  （前提是这 {rain_days} 天是你真知道的：预报、排班、合同。不能是 30 × 0.3 算出来的。）")

print()
print("【第三部分：控制变量，能省多少全看相关】")
print("  （辅助量和目标的起伏都归一为 1；a 取最优值 ρ）")
for rho in [0.0, 0.3, 0.5, 0.7, 0.9]:
    random.seed(7)
    before, after = control(rho, 20000)
    theory = math.sqrt(1 - rho ** 2)
    print(f"  相关 {rho:.1f}：毛边 减前 {before:.3f} → 减后 {after:.3f}；理论 √(1−ρ²) = {theory:.3f}")

print()
print("【第四部分：总起伏 = 组内 + 组间】")
within = RAIN_P * RAIN_SD ** 2 + (1 - RAIN_P) * FAIR_SD ** 2
between = RAIN_P * (RAIN_MEAN - per_day) ** 2 + (1 - RAIN_P) * (FAIR_MEAN - per_day) ** 2
print(f"  单日：组内（雨天/晴天各自内部还晃）= {within:.1f}")
print(f"  单日：组间（今天到底下不下雨）= {between:.1f}")
print(f"  加起来 = {within + between:.1f}；组间占 {(between / (within + between)) * 100:.1f}%")
print(f"  一个月（{DAYS} 天）：{(within + between) * DAYS:.0f}，开根号 = {math.sqrt((within + between) * DAYS):.1f} 单")
print(f"  和第二部分实测的 {spread(blind):.1f} 单是同一个数。")

print()
print("【第五部分：组平均是你估出来的，那部分毛边演多少遍都不会小】")
for m in [3, 8, 30]:
    random.seed(7)
    means = []
    for _ in range(20000):
        sample = [random.gauss(RAIN_MEAN, RAIN_SD) for _ in range(m)]
        means.append(sum(sample) / m)
    print(f"  用 {m:>2} 条雨天记录估'雨天平均单量'：毛边 {spread(means):.2f} 单；乘到 {rain_days} 天上 → ±{spread(means) * rain_days:.1f} 单")

print()
print("【第六部分：把'发几条'从已知改成随机（第 09 课那七条播放量）】")
plays = [820, 1200, 3400, 610, 950, 2100, 480]
random.seed(7)
fixed22 = [sum(random.choices(plays, k=22)) for _ in range(20000)]
random.seed(7)
n_unknown = [sum(random.choices(plays, k=random.randint(14, 30))) for _ in range(20000)]
print(f"  已知下个月发 22 条：月总播放 平均 {sum(fixed22) / len(fixed22):.0f}，起伏 {spread(fixed22):.0f}")
print(f"  条数在 14 到 30 之间随机：平均 {sum(n_unknown) / len(n_unknown):.0f}，起伏 {spread(n_unknown):.0f}")
print(f"  期望几乎没变，起伏多了 {(spread(n_unknown) / spread(fixed22) - 1) * 100:.1f}%")

