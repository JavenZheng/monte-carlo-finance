"""第 13 课配图：两种误差，只有一种能用算力买掉。

左格：同一套模拟把次数从 2,000 加到 200,000，毛边（误差棒）按 √次数 缩，
      而"把 30 天当一步算"带来的那 0.72 偏差纹丝不动。
右格：把 30 天切成 1/2/4/8/16 段，偏差一段一段减半；把 x²/2 加回去，一次就够。

数字全部由本机实测抄下来（每段前 random.seed(7)），与课文逐字一致。

    python3 code/fig13_bias_vs_noise.py   # → assets/fig13_bias_vs_noise.svg
"""

import math
import os
import random

from svgkit import Canvas, spread

MU, SD, DAYS = 0.004, 0.03, 30
truth = 100 * (1 + MU) ** DAYS
lazy = 100 * (1 + DAYS * MU)
bias = lazy - truth

runs_list = [2000, 20000, 200000]
est, se = [], []
for runs in runs_list:
    random.seed(7)
    vals = []
    for _ in range(runs):
        v = 100.0
        for _ in range(DAYS):
            v *= 1 + random.gauss(MU, SD)
        vals.append(v)
    est.append(sum(vals) / len(vals))
    se.append(spread(vals) / math.sqrt(runs))

segs = [1, 2, 4, 8, 16]
bias_seg = [100 * (1 + (DAYS / m) * MU) ** m - truth for m in segs]
x = DAYS * MU
two_order = 100 * (1 + x + x * x / 2) - truth

BLUE, ORANGE, GREEN = "#2f6fb0", "#c2410c", "#1a7f5f"
fig = Canvas(800, 470,
             title='毛边越跑越小，偏差一步不让',
             sub='左边：同一个模型只加次数。右边：同一个偷懒法只切段——或者把扔掉的那一项加回去。')

# ---------------- 左格：毛边 vs 偏差 ----------------
fig.set_view(-0.45, 2.75, 111.70, 113.45, left=62, right=398, top=104, bottom=322)
fig.frame()
fig.grid_y([112.0, 112.5, 113.0], label_fmt="{:.1f}")
fig.hline(truth, color=GREEN, width=2.0, dash="7 4")
fig.hline(lazy, color=ORANGE, width=2.0, dash="7 4")

for i, (n, e, s) in enumerate(zip(runs_list, est, se)):
    px, py = fig.X(i), fig.Y(e)
    top, bot = fig.Y(e + s), fig.Y(e - s)
    fig.parts.append(f'<line x1="{px:.1f}" y1="{top:.1f}" x2="{px:.1f}" y2="{bot:.1f}" '
                     f'stroke="{BLUE}" stroke-width="1.8"/>')
    for yy in (top, bot):
        fig.parts.append(f'<line x1="{px - 5:.1f}" y1="{yy:.1f}" x2="{px + 5:.1f}" y2="{yy:.1f}" '
                         f'stroke="{BLUE}" stroke-width="1.8"/>')
    fig.dots([i], [e], color=BLUE, r=4.4)
    fig.label(i, e - s, f"±{s:.2f}", color=BLUE, size=12, anchor="start", dx=8, dy=16)
    fig.note_at(px, fig.pb + 20, f"{n:,} 遍", color="#454545", size=12, anchor="middle")

fig.label(2.72, truth, f"真值 {truth:.2f}", color=GREEN, size=12.5, anchor="end", dy=-7)
fig.label(-0.40, lazy, f"偷懒一步算：{lazy:.2f}", color=ORANGE, size=12.5, anchor="start", dy=17)
ax = fig.X(2.55)
fig.parts.append(f'<line x1="{ax:.1f}" y1="{fig.Y(truth):.1f}" x2="{ax:.1f}" y2="{fig.Y(lazy):.1f}" '
                 f'stroke="{ORANGE}" stroke-width="1.6"/>')
for yy in (fig.Y(truth), fig.Y(lazy)):
    fig.parts.append(f'<path d="M {ax - 4:.1f} {yy + (3 if yy == fig.Y(truth) else -3):.1f} '
                     f'L {ax:.1f} {yy:.1f} L {ax + 4:.1f} {yy + (3 if yy == fig.Y(truth) else -3):.1f}" '
                     f'fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
fig.label(2.55, (truth + lazy) / 2, f"差 {abs(bias):.2f}", color=ORANGE, size=12, anchor="start", dx=7)
fig.note_at(62, 96, "① 只加次数：误差棒缩，橙线不动", color="#3a3a3a", size=13)

# ---------------- 右格：切段 vs 补项 ----------------
fig.set_view(-0.75, 6.6, -0.02, 0.82, left=452, right=780, top=104, bottom=322)
fig.frame()
fig.grid_y([0.2, 0.4, 0.6, 0.8], label_fmt="{:.1f}")
heights = [abs(b) for b in bias_seg]
fig.vbars(range(5), heights, color=BLUE, gap=0.30, opacity=0.85)
fig.plot(list(range(5)), heights, color="#b6b6b6", width=1.4, dash="4 3")
fig.vbars([5.7], [abs(two_order)], color=ORANGE, gap=0.30, opacity=0.95)
ty = fig.Y(abs(two_order))
fig.parts.append(f'<line x1="{fig.X(5.7) - 11:.1f}" y1="{ty:.1f}" x2="{fig.X(5.7) + 11:.1f}" '
                 f'y2="{ty:.1f}" stroke="{ORANGE}" stroke-width="3"/>')
for i, (m, b) in enumerate(zip(segs, bias_seg)):
    fig.label(i, heights[i], f"{b:+.3f}", color=BLUE, size=11.5, anchor="middle", dy=-13)
    fig.note_at(fig.X(i), fig.pb + 20, f"切 {m} 段", color="#454545", size=11.5, anchor="middle")
fig.note_at(fig.X(5.7), fig.pb + 20, "加回 x²/2", color=ORANGE, size=11.5, anchor="middle")
fig.label(5.7, abs(two_order), f"{two_order:+.3f}", color=ORANGE, size=11.5, anchor="middle", dy=-8)
fig.note_at(452, 96, "② 只切段：偏差每次减半，减不到零", color="#3a3a3a", size=13)

# ---------------- 底部三行 ----------------
fig.note_at(26, 372, "左：毛边按 √次数 缩——2,000 遍 ±0.41，二十万遍只剩 ±0.04；"
                     "橙线那 0.72（=0.12²/2 × 本金）与次数无关，加十倍算力它一步不让。",
             color="#454545", size=12.5)
fig.note_at(26, 396, "右：把 30 天切成段，段数翻倍、偏差减半（-0.723 → -0.023），这是一阶的，永远在路上下。",
             color="#454545", size=12.5)
fig.note_at(26, 420, "而把扔掉的那一项加回去（1 + x + x²/2），一次就从 0.723 掉到 0.003——一次修正顶得上切一百段。",
             color="#454545", size=12.5)
fig.note_at(26, 446, "这就是原书把第 4 章（方差缩减）和第 6 章（离散化）分成两章的原因：一笔治毛边，一笔治偏差，两笔不能互抵。",
             color="#7a7a7a", size=12)

path = fig.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fig13_bias_vs_noise.svg"))

print("真值 %.4f  偷懒 %.2f  偏差 %+.4f" % (truth, lazy, bias))
for n, e, s in zip(runs_list, est, se):
    print(f"{n:>6} 遍：估计 {e:.2f} ± {s:.2f}")
print(" ".join(f"{b:+.3f}" for b in bias_seg), f" 二阶 {two_order:+.3f}")
print(path)
