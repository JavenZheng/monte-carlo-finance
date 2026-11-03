"""第 11 课配图：分散的地板——前十只砍掉四成，后面买的是手续费。

生成 assets/fig11_diversification.svg。三条实线是式子 √(ρ + (1−ρ)/n)，
橙色那三个圆点是第 11 课第三部分真去模拟出来的篮子起伏（种子 7、两万天、n = 1/2/10/50），
虚线是"加到无穷多只也消不掉的地板" √ρ。
"""

import math
import os
import random

from svgkit import Canvas, spread


def basket_sd(rho, n, days):
    out = []
    for _ in range(days):
        common = random.gauss(0, 1)
        total = 0
        for _ in range(n):
            total += math.sqrt(rho) * common + math.sqrt(1 - rho) * random.gauss(0, 1)
        out.append(total / n)
    return spread(out)


ns = list(range(1, 101))
rhos = [0.0, 0.3, 0.7]
curves = {r: [math.sqrt(r + (1 - r) / n) for n in ns] for r in rhos}

random.seed(7)
measured = []
for n in [1, 2, 10, 50]:
    measured.append((n, basket_sd(0.3, n, 20000)))

fig = Canvas(width=800, height=470,
             title="分散有地板：前十只砍掉四成，第一百只只砍 9%",
             sub="篮子起伏 ÷ 单只起伏＝1；三条线是式子 √(ρ + (1−ρ)/n)，"
                 "橙点是相关 0.3 时真模拟出来的篮子（种子 7、两万天）")

fig.set_view(0, 100, 0, 1.06, bottom=330)
fig.grid_x([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], "{:.0f}")
fig.grid_y([0, 0.2, 0.4, 0.6, 0.8, 1.0], "{:.1f}")
fig.frame()

colors = {0.0: "#2f6fb0", 0.3: "#c2410c", 0.7: "#4d7a4d"}
for r in rhos:
    fig.plot(ns, curves[r], color=colors[r], width=2.2)
    floor = math.sqrt(r)
    fig.hline(floor, color=colors[r], width=1.1, dash="4 4")

fig.dots([n for n, _ in measured], [v for _, v in measured], color="#c2410c", r=4.6)

fig.label(10, curves[0.3][9], f"10 只：{curves[0.3][9]:.3f}", color="#c2410c", size=12.5,
          anchor="middle", dx=0, dy=-12)
fig.label(78, curves[0.3][77], f"100 只：{curves[0.3][99]:.3f}", color="#c2410c", size=12.5,
          anchor="start", dx=6, dy=-12)
fig.label(1, 1.0, "1 只：1.000", color="#1a1a1a", size=12.5, anchor="start", dx=8, dy=-6)
fig.label(10, curves[0.0][9], f"ρ=0 时 10 只：{curves[0.0][9]:.3f}", color="#2f6fb0",
          size=12, anchor="middle", dx=10, dy=-12)
fig.label(10, curves[0.7][9], f"ρ=0.7 时 10 只：{curves[0.7][9]:.3f}", color="#4d7a4d",
          size=12, anchor="middle", dx=10, dy=-12)

fig.legend([(colors[0.0], None, "相关 0"), (colors[0.3], None, "相关 0.3"),
            (colors[0.7], None, "相关 0.7（同色虚线＝地板 √ρ）")],
           fig.pr - 16, fig.pt + 20, anchor="end")

fig.xlabel("篮子里有几只（等权）")
fig.ylabel("篮子起伏 ÷ 单只起伏")

fig.note_at(64, 380,
            "相关 0.3 这一格：1 只 1.000 → 10 只 0.608 → 100 只 0.554，而地板是 0.548——"
            "加到第一百只，只比第十只少了 9%。",
            color="#454545", size=12.5)
fig.note_at(64, 400,
            "换成每天 2% 的单只起伏：1 只 2.00% → 10 只 1.22% → 100 只 1.11%，"
            "再怎么加也到不了 1.10% 以下。",
            color="#c2410c", size=12.5)
fig.note_at(64, 420,
            '地板是那个共同的"大环境"给的：你能摊掉的是各自的小运气，摊不掉一起动的那一份。',
            color="#7a7a7a", size=12)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig11_diversification.svg")
print(fig.save(out))
print(f"    相关 0.3 实测：{'；'.join(f'{n} 只 {v:.3f}' for n, v in measured)}")
print(f"    理论：{'；'.join(f'{n} 只 {math.sqrt(0.3 + 0.7 / n):.3f}' for n in [1, 2, 10, 50])}")
