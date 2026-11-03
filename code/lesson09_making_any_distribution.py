"""排队领号：从一个 0 到 1 的均匀抽签，造出任何你想要的形状。

第一部分：离散三档（外卖送达时间）。
第二部分：连续均匀（区间里随挑）。
第三部分：指数（间隔多久来一单）。
第四部分：把你自己的历史记录当成可能性表，造出"未来的三十条"。
第五部分：练习一、二那两组数字。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random


def pick(u, table):
    """u 是 0 到 1 之间的抽签；table 是 [(上沿, 名字)]，从小到大排好。"""
    for edge, name in table:
        if u < edge:
            return name
    return table[-1][1]


def uniform_between(u, low, high):
    return low + (high - low) * u


def exponential(u, rate):
    return -math.log(1 - u) / rate


def future_total(records, k, runs):
    """从历史 records 里有放回抽 k 条，看这 k 条加起来是多少；重复 runs 次。"""
    out = []
    for _ in range(runs):
        drawn = random.choices(records, k=k)
        out.append(sum(drawn))
    out.sort()
    return out


print("【第一部分：三档送达时间】")
random.seed(7)
table = [(0.2, "快（20分钟）"), (0.7, "准点（30分钟）"), (1.0, "晚（50分钟）")]
counts = {"快（20分钟）": 0, "准点（30分钟）": 0, "晚（50分钟）": 0}
for _ in range(20000):
    counts[pick(random.random(), table)] += 1
for name, c in counts.items():
    print(f"{name}：{c / 20000 * 100:.1f}%")

print()
print("【第二部分：区间里随挑，25 到 55】")
random.seed(7)
values = [uniform_between(random.random(), 25, 55) for _ in range(20000)]
print(f"平均 {sum(values) / len(values):.2f}（理论 {(25 + 55) / 2}）")

print()
print("【第三部分：每隔多久来一单，平均每小时 6 单】")
random.seed(7)
gaps = [exponential(random.random(), 6) for _ in range(20000)]
print(f"平均间隔 {sum(gaps) / len(gaps) * 60:.1f} 分钟（理论 10 分钟）")
short = 0
for g in gaps:
    if g < 1 / 12:
        short += 1
print(f"不到 5 分钟就来一单的比例：{short / len(gaps) * 100:.1f}%")

print()
print("【第四部分：用你那七条播放量，造未来的三十条】")
plays = [820, 1200, 3400, 610, 950, 2100, 480]
random.seed(7)
totals = future_total(plays, 30, 10000)
p10 = totals[int(0.1 * len(totals))]
p50 = totals[int(0.5 * len(totals))]
p90 = totals[int(0.9 * len(totals))]
print(f"三十条的总播放：一成低于 {p10:.0f}，中位 {p50:.0f}，九成不超过 {p90:.0f}")
print(f"最常在哪个区间：{totals[int(0.25*len(totals))]:.0f} 到 {totals[int(0.75*len(totals))]:.0f}")

print()
print("【第五部分：练习那两题】")
random.seed(7)
table2 = [(0.3, "20分钟"), (0.8, "30分钟"), (1.0, "50分钟")]
counts2 = {"20分钟": 0, "30分钟": 0, "50分钟": 0}
for _ in range(20000):
    counts2[pick(random.random(), table2)] += 1
for name, c in counts2.items():
    print(f"{name}：{c / 20000 * 100:.1f}%")

random.seed(7)
gaps3 = [exponential(random.random(), 3) for _ in range(20000)]
hit = 0
for g in gaps3:
    if g < 10 / 60:
        hit += 1
print(f"平均每小时 3 单时：平均间隔 {sum(gaps3) / len(gaps3) * 60:.1f} 分钟，小于 10 分钟占 {hit / len(gaps3) * 100:.1f}%")
