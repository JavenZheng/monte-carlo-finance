"""第 15 课配图（二）：期末在哪 vs 路上跌破过没有。

生成 assets/fig15_endpoint_vs_path.svg。和第 15 课第六部分同一套抽签（种子 7、
一万条路、每条切 500 段），图上画的是其中一条：期末几乎没动，路上却跌破过那条线。
旁边三个百分比也是同一轮抽签数出来的，不是另外编的。
"""

import math
import os
import random

from svgkit import Canvas

a, n, runs = 0.5, 500, 10000


def one_path():
    pos, lo = 0.0, 0.0
    seg = [0.0]
    for _ in range(n):
        pos += random.gauss(0, math.sqrt(1.0 / n))
        lo = min(lo, pos)
        seg.append(pos)
    return seg, pos, lo


random.seed(7)
finals, mins = [], []
for _ in range(runs):
    _, pos, lo = one_path()
    finals.append(pos)
    mins.append(lo)

p_fin = sum(1 for v in finals if v <= -a) / runs
p_min = sum(1 for v in mins if v <= -a) / runs
stay = [m for f, m in zip(finals, mins) if abs(f) <= 0.2]
p_stay = sum(1 for m in stay if m <= -a) / len(stay)

pick = next(i for i, (f, m) in enumerate(zip(finals, mins))
            if abs(f) <= 0.2 and m <= -0.75)

random.seed(7)
for _ in range(pick + 1):
    seg, end, low = one_path()
low_at = seg.index(low) / n

fig = Canvas(width=800, height=470,
             title=f"期末没跌破 ≠ 路上没跌破：这条路的期末是 {end:+.2f}，中途最低 {low:+.2f}",
             sub=f"一万条布朗路径之一（起点 0，切 {n} 段，种子 7，第 {pick + 1} 条）"
                 f"　·　横轴是时间，纵轴是累计涨跌幅")

fig.set_view(0, 1.34, min(low, -a) - 0.34, max(max(seg), 0) + 0.16, right=774, bottom=345)
fig.grid_x([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], "{:.1f}")
fig.grid_y([-1.0, -0.5, 0.0, 0.5], "{:.1f}")
fig.frame()
fig.zero_line(color="#c8c8c8")

fig.hline(-a, color="#c2410c", width=1.6, dash="6 4")
fig.note_at(fig.X(1.02), fig.Y(-a) - 10, f"那条线 −{a}", color="#c2410c", size=12.5)

fig.plot([i / n for i in range(n + 1)], seg, color="#2f6fb0", width=1.6)

fig.dots([1.0], [end], color="#2f6fb0", r=5)
fig.note_at(fig.X(1.02), fig.Y(end) - 4, f"期末 {end:+.2f}", color="#1a1a1a", size=12.5)
fig.note_at(fig.X(1.02), fig.Y(end) + 12, "按期末算：没跌破", color="#2f6fb0", size=12)
fig.dots([low_at], [low], color="#c2410c", r=5)
fig.note_at(fig.X(low_at) - 10, fig.Y(low) + 20, f"途中最低 {low:+.2f}", color="#c2410c",
            size=12.5, anchor="end")
fig.note_at(fig.X(low_at) - 10, fig.Y(low) + 36, "按路上算：跌破过", color="#c2410c",
            size=12, anchor="end")

fig.xlabel("时间（一年切成 500 段）")
fig.ylabel("累计涨跌幅")

fig.note_at(58, 385,
            f"一万条这样的路数下来：期末 ≤ −{a} 的 {p_fin * 100:.1f}%；"
            f"途中最低 ≤ −{a} 的 {p_min * 100:.1f}%——倍数 {p_min / p_fin:.2f}（反射原理给 2）",
            color="#454545", size=12.5)
fig.note_at(58, 405,
            f'而"期末没走远"（|期末| ≤ 0.2）的那些路里，中途跌破过 −{a} 的占 {p_stay * 100:.1f}%'
            f"——图上这条就是其中一条",
            color="#c2410c", size=12.5)
fig.note_at(58, 425,
            '任何只报"到期收益"的说法，报的都是第一行；赔付看的却是第二行。',
            color="#7a7a7a", size=12)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig15_endpoint_vs_path.svg")
print(fig.save(out))
print(f"    期末 ≤ −{a}：{p_fin * 100:.1f}%；途中最低 ≤ −{a}：{p_min * 100:.1f}%；"
      f"倍数 {p_min / p_fin:.2f}；|期末| ≤ 0.2 里跌破过 {p_stay * 100:.1f}%")
print(f"    图上这条：第 {pick + 1} 条，期末 {end:+.3f}，最低 {low:+.3f}（在 t = {low_at:.3f}）")
