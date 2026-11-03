"""把"每天的涨跌"连起来：为什么价格只能为正，为什么平均值比中位数大。

第一部分：把涨跌当成"几块钱"直接加到价格上 → 会跑出负价格。
第二部分：把涨跌当成"百分之几"乘上去 → 永远为正，但形状一边长尾巴。
第三部分：同样 ±50，加减和乘除的答案不一样。
第四部分：平均一模一样、起伏翻倍，你的典型结果反而变差（波动拖累）。
第五部分：log 把一串乘法变成一串加法，于是理论值和模拟值能对上。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random


def add_price(start, daily_sd, days, runs):
    """每天的涨跌当成"几块钱"，正态，直接加。返回每条路径的终值和中途最低点。"""
    ends = []
    lows = []
    for _ in range(runs):
        p = start
        low = start
        for _ in range(days):
            p += random.gauss(0, daily_sd)
            if p < low:
                low = p
        ends.append(p)
        lows.append(low)
    return ends, lows


def mult_price(start, mean_r, sd_r, days, runs):
    """每天的涨跌当成"百分之几"，正态，乘上去。返回每条路径的终值。"""
    out = []
    for _ in range(runs):
        p = start
        for _ in range(days):
            p *= 1 + random.gauss(mean_r, sd_r)
        out.append(p)
    return out


def quantile(sorted_vals, q):
    return sorted_vals[int(q * len(sorted_vals))]


def histogram(values, bins=9, width=44):
    lo = min(values)
    hi = max(values)
    step = (hi - lo) / bins
    counts = [0] * bins
    for x in values:
        k = int((x - lo) / step)
        if k == bins:
            k = bins - 1
        counts[k] = counts[k] + 1
    biggest = max(counts)
    for i in range(bins):
        left = lo + i * step
        bar = "*" * max(1, int(round(counts[i] / biggest * width)))
        print(f"{left:7.0f}  {bar}  {counts[i]}")


print("【第一部分：把涨跌当成几块钱直接加】")
random.seed(7)
adds, lows = add_price(100, 5, 250, 10000)
neg = 0
for v in adds:
    if v < 0:
        neg += 1
ever = 0
for v in lows:
    if v < 0:
        ever += 1
adds.sort()
print("起点 100，每天 ±5 块钱乱晃（平均 0），一年 250 天，跑一万遍：")
print(f"  终值是负数的：{neg} 遍，占 {neg / len(adds) * 100:.1f}%")
print(f"  中途跌破过零的：{ever} 遍，占 {ever / len(lows) * 100:.1f}%")
print(f"  最惨的一遍：{adds[0]:.1f} 元")
print(f"  一成低于 {quantile(adds, 0.1):.0f}，中位 {quantile(adds, 0.5):.0f}，九成不超过 {quantile(adds, 0.9):.0f}")

print()
print("【第二部分：把涨跌当成百分之几乘上去】")
random.seed(7)
mults = mult_price(100, 0.0, 0.02, 250, 10000)
mults.sort()
print("起点 100，每天平均涨 0%、起伏 2%，一年 250 天，跑一万遍：")
print(f"  最惨的一遍：{mults[0]:.2f} 元（没有一遍是负的）")
print(f"  一成低于 {quantile(mults, 0.1):.1f}，中位 {quantile(mults, 0.5):.1f}，九成不超过 {quantile(mults, 0.9):.1f}")
print(f"  一万遍的平均：{sum(mults) / len(mults):.1f}")
below = 0
for v in mults:
    if v < 100:
        below += 1
print(f"  一年后比起点还低的：占 {below / len(mults) * 100:.1f}%")
print("  一万条路径的终值排成什么形状：")
histogram(mults)

print()
print("【第三部分：同样 ±50，加减和乘除不是一回事】")
print(f"先跌 50% 再涨 50%：100 × 0.5 × 1.5 = {100 * 0.5 * 1.5:.1f}")
print(f"先涨 50% 再跌 50%：100 × 1.5 × 0.5 = {100 * 1.5 * 0.5:.1f}")
print(f"而 ±50 块钱来回：100 + 50 − 50 = {100 + 50 - 50}")

print()
print("【第四部分：平均一样、起伏翻倍，典型结果反而更差】")
random.seed(7)
calm = mult_price(100, 0.001, 0.02, 250, 10000)
calm.sort()
random.seed(7)
wild = mult_price(100, 0.001, 0.04, 250, 10000)
wild.sort()
print("两个都是每天平均涨 0.1%，一年 250 天，各跑一万遍：")
print(f"  起伏 2%：中位 {quantile(calm, 0.5):.1f}，平均 {sum(calm) / len(calm):.1f}，亏钱的占 {sum(1 for v in calm if v < 100) / len(calm) * 100:.1f}%")
print(f"  起伏 4%：中位 {quantile(wild, 0.5):.1f}，平均 {sum(wild) / len(wild):.1f}，亏钱的占 {sum(1 for v in wild if v < 100) / len(wild) * 100:.1f}%")
random.seed(7)
flat10 = mult_price(100, 0.0, 0.10, 250, 10000)
flat10.sort()
print(f"再把起伏拉到 10%、平均涨 0%：中位 {quantile(flat10, 0.5):.1f}，平均 {sum(flat10) / len(flat10):.1f}")
print(f"  理论给的中位：100 × e^(−0.10² ÷ 2 × 250) = {100 * math.exp(-0.10 ** 2 / 2 * 250):.1f}")

print()
print("【第五部分：log 把一串乘法变成一串加法】")
random.seed(7)
one = [random.gauss(0.001, 0.02) for _ in range(250)]
p = 100.0
for r in one:
    p *= 1 + r
direct = math.log(p / 100)
added = 0
for r in one:
    added += math.log(1 + r)
print(f"一条路径：连乘完再取 log = {direct:.4f}；把每天的 log(1+r) 加起来 = {added:.4f}")
print("同一个数。所以日收益近似正态时，'log(终值 ÷ 起点)'就是那个钟形。")
theory = 250 * 0.001 - 0.02 ** 2 / 2 * 250
print(f"起伏 2%、平均每天涨 0.1%，一年的中位理论值：100 × e^{theory:.3f} = {100 * math.exp(theory):.1f}")
