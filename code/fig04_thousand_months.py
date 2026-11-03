"""第 04 课配图：把一台机器开一千次，得到一千个还没发生过的月。

横轴是"这个月花掉多少"，纵轴是"一千个月里有几个落在这一档"。
五条竖线就是课文里那三行输出：最省、一成、平均、九成、最贵。

数字全部由本机实测抄下来（random.seed(7)），与课文逐字一致。

    python3 code/fig04_thousand_months.py   # → assets/fig04_thousand_months.svg
"""

import math
import os
import random

from svgkit import Canvas

LOW, HIGH, WORKDAYS = 25, 55, 22


def one_month(low, high, workdays):
    total = 0
    for _ in range(workdays):
        total = total + random.uniform(low, high)
    return total


random.seed(7)
months = []
for _ in range(1000):
    months.append(one_month(LOW, HIGH, WORKDAYS))
months.sort()
p10 = months[int(0.1 * len(months))]
p90 = months[int(0.9 * len(months))]
mean = sum(months) / len(months)
lo, hi = months[0], months[-1]

BIN = 10
start = math.floor(lo / BIN) * BIN
edges = list(range(start, int(math.ceil(hi / BIN)) * BIN + BIN, BIN))
counts = [0] * (len(edges) - 1)
for v in months:
    counts[min(int((v - start) // BIN), len(counts) - 1)] += 1
peak = max(counts)

BLUE, ORANGE, GREY, GREEN = "#2f6fb0", "#c2410c", "#8a8a8a", "#1a7f5f"
fig = Canvas(800, 424,
             title='一千个还没发生过的月',
             sub='每天 25 到 55 元、22 个工作日，把这台机器开一千次。横轴：这个月的总额；纵轴：这样的月有几个。')

fig.set_view(start - 8, edges[-1] + 8, 0, peak * 1.42, left=62, right=774, top=96, bottom=296)
fig.frame()
fig.grid_x(list(range(750, 1001, 50)), label_fmt="{:.0f}")
fig.grid_y([t for t in range(0, peak + 30, 30)], label_fmt="{:.0f}")

fig.band(p10, p90, color=BLUE, opacity=0.07)

base = fig.Y(0)
for i, c in enumerate(counts):
    x0, x1 = fig.X(edges[i]), fig.X(edges[i + 1])
    y = fig.Y(c)
    fig.parts.append(f'<rect x="{x0 + 1:.1f}" y="{y:.1f}" width="{x1 - x0 - 2:.1f}" '
                     f'height="{base - y:.1f}" fill="{BLUE}" opacity="0.72"/>')

marks = [(lo, f"最省 {lo:.0f}", GREY, 116, "start", 7),
         (p10, f"一成的月低于 {p10:.0f}", BLUE, 138, "start", 7),
         (mean, f"平均 {mean:.0f}", ORANGE, 116, "end", -7),
         (p90, f"九成的月不超过 {p90:.0f}", BLUE, 160, "end", -7),
         (hi, f"最贵 {hi:.0f}", GREY, 116, "end", -7)]
for v, text, color, py, anchor, dx in marks:
    fig.parts.append(f'<line x1="{fig.X(v):.1f}" y1="{fig.pt + 4:.1f}" x2="{fig.X(v):.1f}" '
                     f'y2="{base:.1f}" stroke="{color}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    fig.note_at(fig.X(v) + dx, py, text, color=color, size=12.5, anchor=anchor)

fig.note_at(62, 342, f"这一千个月都没发生过，但你记录了它们：最省 {lo:.0f}、最贵 {hi:.0f}、平均 {mean:.0f}。",
             color="#454545", size=12.5)
fig.note_at(62, 366, f"把中间那八成圈出来（图上那块淡蓝）：一成的月低于 {p10:.0f}，九成的月不超过 {p90:.0f}。",
             color="#454545", size=12.5)
fig.note_at(62, 390, "两头各只有一千分之一，换一次种子就飘；中间那几根线（一成、平均、九成）几乎不动。",
             color="#7a7a7a", size=12)

path = fig.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fig04_thousand_months.svg"))

print(f"最省的月 {lo:.0f}，最贵的月 {hi:.0f}")
print(f"平均 {mean:.0f}")
print(f"一成的月低于 {p10:.0f}，九成的月不超过 {p90:.0f}")
print(f"分档起点 {start}，档数 {len(counts)}，最挤的一档 {peak} 个")
print(path)
