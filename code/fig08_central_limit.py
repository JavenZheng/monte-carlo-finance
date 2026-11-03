"""第 08 课配图：两万个"平均"排成钟形，而你手上那十天不是。

生成 assets/fig08_central_limit.svg。数据与第 08 课第二部分完全一致：
通勤十条，每次带放回抽十条取平均，重复两万遍（种子 7）。
蓝色柱子＝两万条平均的分堆；底部橙色短竖线＝原始那十条记录钉在横轴上。
"""

import math
import os
import random

from svgkit import Canvas, spread

commute = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]
unit = "分钟"
runs = 20000

mean = sum(commute) / len(commute)
se = spread(commute) / math.sqrt(len(commute))

random.seed(7)
avgs = [sum(random.choices(commute, k=10)) / 10 for _ in range(runs)]
measured = spread(avgs)

bins = 24
lo, hi = 24.0, 47.0
step = (hi - lo) / bins
counts = [0] * bins
for a in avgs:
    k = int((a - lo) / step)
    counts[min(bins - 1, max(0, k))] += 1

centers = [lo + (i + 0.5) * step for i in range(bins)]
top = max(counts) * 1.18

fig = Canvas(width=800, height=480,
             title='两万个"平均"排成钟形，你手上那十天不是',
             sub=f"通勤十条（{min(commute)}–{max(commute)} {unit}），每次抽十条取平均、重复 {runs} 遍（种子 7）"
                 f"　·　实测散布 {measured:.2f}，公式 σ/√n 给的毛边 {se:.2f}")
fig.set_view(lo, hi, 0, top)
fig.grid_x([25, 28, 31, 34, 37, 40, 43, 46], "{:.0f}")
fig.grid_y(list(range(0, int(top) + 1, 500)), "{:,.0f}")
fig.frame()

fig.vbars(centers, counts, color="#2f6fb0", gap=0.12)
fig.rug(commute, color="#c2410c")

fig.vline(mean, color="#1a1a1a", width=1.6)
for mult in (1, 2):
    fig.vline(mean - mult * se, color="#7a7a7a", dash="4 3")
    fig.vline(mean + mult * se, color="#7a7a7a", dash="4 3")

fig.note_at(fig.X(mean) + 6, fig.pt + 16, f"平均 {mean:.1f} {unit}", color="#1a1a1a", size=13)
fig.note_at(fig.pl + 14, fig.pt + 22,
            f"±1 倍毛边（±{se:.1f} {unit}）之内 70.2%", color="#454545", size=12.5)
fig.note_at(fig.pl + 14, fig.pt + 40,
            f"±2 倍毛边（±{2 * se:.1f} {unit}）之内 96.6%", color="#454545", size=12.5)
fig.note_at(fig.pl + 14, fig.pt + 58,
            f"橙竖线＝原始那十条，散在 {min(commute)} 到 {max(commute)}", color="#c2410c", size=12.5)

fig.xlabel(f'一个"十天"的平均（{unit}）')
fig.ylabel("两万条平均里，落在这一档的有几条")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig08_central_limit.svg")
saved = fig.save(out)
print(f"{saved}: 公式毛边 {se:.2f} / 实测散布 {measured:.2f}；"
      f"±1 倍覆盖 {sum(1 for a in avgs if abs(a - mean) <= se) / runs * 100:.1f}%，"
      f"±2 倍覆盖 {sum(1 for a in avgs if abs(a - mean) <= 2 * se) / runs * 100:.1f}%")
