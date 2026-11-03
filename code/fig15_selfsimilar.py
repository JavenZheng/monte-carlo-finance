"""第 15 课配图（一）：放大多少倍都还是抖——同一条路的三格。

生成 assets/fig15_selfsimilar.svg。一条切 4000 段的布朗路径（种子 7），
左格看整段，中格放大 4 倍，右格放大 8 倍；每格上下都按本段自己的幅度铺满，
所以三格的锯齿看起来一样密。

底下那行 √ 的账不靠这一条路（单条路的幅度很飘），用的是第 15 课第四部分那个动作：
每种窗口长度各演四千遍取平均。
"""

import math
import os
import random

from svgkit import Canvas

steps = 4000
random.seed(7)
pos = 0.0
vals = [0.0]
for _ in range(steps):
    pos += random.gauss(0, math.sqrt(1.0 / steps))
    vals.append(pos)


def mean_range(t, reps=4000, sub=200):
    """窗口长度 t 里，一条路"最高点减最低点"的平均（第 15 课第四部分的量法）。"""
    random.seed(7)
    out = []
    for _ in range(reps):
        p = hi = lo = 0.0
        for _ in range(sub):
            p += random.gauss(0, math.sqrt(t / sub))
            hi = max(hi, p)
            lo = min(lo, p)
        out.append(hi - lo)
    return sum(out) / len(out)


windows = [(0, 4000, "整段", 1.0), (1500, 2500, "放大 4 倍", 0.25), (1750, 2250, "放大 8 倍", 0.125)]
single = []
for i0, i1, name, t in windows:
    seg = [v - vals[i0] for v in vals[i0:i1 + 1]]
    single.append(max(seg) - min(seg))

avg = {t: mean_range(t) for t in (1.0, 0.25, 0.125)}

fig = Canvas(width=800, height=430,
             title="同一条路：放大 4 倍、放大 8 倍，锯齿一样密",
             sub=f"一条切 {steps} 段的布朗路径（种子 7）　·　每格上下按本段自己的幅度铺满，"
                 "所以看不出'放大后变直'")

left = 58
gap = 30
panel_w = (800 - 26 - left - 2 * gap) / 3

for idx, ((i0, i1, name, t), rng) in enumerate(zip(windows, single)):
    x0, x1 = i0 / steps, i1 / steps
    seg = [v - vals[i0] for v in vals[i0:i1 + 1]]
    pl = left + idx * (panel_w + gap)
    fig.set_view(x0, x1, min(seg) - 0.10 * rng, max(seg) + 0.10 * rng,
                 left=pl, right=pl + panel_w, top=96, bottom=316)
    fig.grid_x([x0 + (x1 - x0) * f for f in (0.25, 0.5, 0.75)], "{:.2f}")
    fig.frame()
    fig.plot([x0 + (x1 - x0) * j / (len(seg) - 1) for j in range(len(seg))], seg,
             color="#2f6fb0", width=1.5)
    fig.zero_line()
    fig.note_at(pl, 78, name, color="#1a1a1a", size=14)
    fig.note_at(pl, 352, f"窗口长度 {t:.3f}", color="#7a7a7a", size=11.5)
    fig.note_at(pl, 368, f"这一段自己：幅度 {rng:.3f}", color="#c2410c", size=11.5)

fig.note_at(left, 402,
            f"√ 的账要平均着算（每种窗口各演四千遍）：长度 1.000 幅度 {avg[1.0]:.3f}；"
            f"0.250 → {avg[0.25]:.3f}（÷ {avg[1.0] / avg[0.25]:.2f}）；"
            f"0.125 → {avg[0.125]:.3f}（再 ÷ {avg[0.25] / avg[0.125]:.2f}）",
            color="#454545", size=12.5)
fig.note_at(left, 420,
            "缩 4 倍只除以 2、缩 8 倍再除以 1.41：都是开根号，不是 4 和 8——所以永远找不到一段是直的",
            color="#7a7a7a", size=12)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig15_selfsimilar.svg")
print(fig.save(out))
print(f"    单条路三格：{' / '.join(f'{r:.3f}' for r in single)}")
print(f"    四千遍平均：{' / '.join(f'{avg[t]:.3f}' for t in (1.0, 0.25, 0.125))}")
