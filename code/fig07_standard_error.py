"""第 07 课配图：根号税——毛边只按 1/√条数 缩。

生成 assets/fig07_standard_error.svg。数据就是正文那十条通勤记录，
曲线是公式 σ/√n，点是"真去抽 n 条取平均、重复四千遍"量出来的散布（种子 7）。
两者贴在一起，就是第 07 课那条式子的证据。
"""

import math
import os
import random

from svgkit import Canvas, spread

records = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]
unit = "分钟"
n_max = 40
reps = 4000

mean_all = sum(records) / len(records)
sigma = spread(records)

ns = list(range(1, n_max + 1))
curve = [sigma / math.sqrt(n) for n in ns]

measured = []
random.seed(7)
for n in ns:
    avgs = [sum(random.choices(records, k=n)) / n for _ in range(reps)]
    measured.append(spread(avgs))

fig = Canvas(width=780, height=470,
             title="毛边只按 1/√条数 往下走",
             sub=f"十条通勤记录，平均 {mean_all:.1f} {unit}，单次起伏 σ = {sigma:.1f} {unit}"
                 "　·　每个条数都真抽 4000 遍（种子 7）")
fig.set_view(0.4, n_max + 0.6, 0, 6.4)
fig.grid_x([1, 5, 10, 15, 20, 25, 30, 35, 40])
fig.grid_y([0, 1, 2, 3, 4, 5, 6], "{:.0f}")
fig.frame()

fig.plot(ns, curve, color="#2f6fb0", width=2.4)
fig.dots(ns, measured, color="#c2410c", r=3.2, opacity=0.85)

fig.label(10, sigma / math.sqrt(10), f"记 10 天：毛边 {sigma / math.sqrt(10):.1f} {unit}",
          color="#1a1a1a", size=13, anchor="end", dx=-8, dy=16)
fig.label(40, sigma / math.sqrt(40), f"记 40 天：{sigma / math.sqrt(40):.1f} {unit}",
          color="#1a1a1a", size=13, anchor="end", dx=-6, dy=-8)

fig.hline(0, color="#d8d8d8", dash="1 0")
fig.xlabel("记了几天（用来算平均的条数 n）")
fig.ylabel(f"平均的毛边（{unit}）")
fig.legend([("#2f6fb0", None, "公式 σ/√n"), ("#c2410c", "dot", "真抽四千遍量出来的")],
           fig.pr - 16, fig.pt + 20, anchor="end")
fig.note_at(fig.pr - 16, fig.pt + 44,
            "条数翻四倍，毛边才减半",
            color="#7a7a7a", anchor="end")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fig07_standard_error.svg")
saved = fig.save(out)
print(f"{saved}: n=10 公式 {sigma / math.sqrt(10):.2f} / 实测 {measured[9]:.2f}；"
      f"n=40 公式 {sigma / math.sqrt(40):.2f} / 实测 {measured[-1]:.2f}")
