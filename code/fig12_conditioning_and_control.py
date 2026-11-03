"""第 12 课配图：误差的两块，一块靠查清楚，一块靠找个几乎同涨同跌的辅助量。

生成 assets/fig12_conditioning_and_control.svg。左格是第四节的方差分解（单日
组内 36.7 + 组间 84.0），右格是第五节那张控制变量的表（ρ 从 0 到 0.9，各两万
遍，种子 7）。数字与课文第三、四、五节逐字一致。
"""

import math
import os
import random

from svgkit import Canvas, spread

RAIN_P, RAIN_MEAN, RAIN_SD = 0.3, 60.0, 8.0
FAIR_MEAN, FAIR_SD = 40.0, 5.0
DAYS = 30
runs = 20000

per_day = RAIN_P * RAIN_MEAN + (1 - RAIN_P) * FAIR_MEAN
within = RAIN_P * RAIN_SD ** 2 + (1 - RAIN_P) * FAIR_SD ** 2
between = RAIN_P * (RAIN_MEAN - per_day) ** 2 + (1 - RAIN_P) * (FAIR_MEAN - per_day) ** 2
total = within + between
share = between / total
month_all = math.sqrt(total * DAYS)
month_known = math.sqrt(within * DAYS)


def control(rho):
    """与 code/lesson12_conditioning_and_control.py 第三部分同一套抽签。"""
    random.seed(7)
    plain, fixed = [], []
    for _ in range(runs):
        common = random.gauss(0, 1)
        x = common
        y = rho * common + math.sqrt(1 - rho ** 2) * random.gauss(0, 1)
        plain.append(y)
        fixed.append(y - rho * x)
    return spread(plain), spread(fixed)


rhos = [0.0, 0.3, 0.5, 0.7, 0.9]
before, after = {}, {}
for r in rhos:
    before[r], after[r] = control(r)
cut = {r: (1 - after[r] / before[r]) * 100 for r in rhos}

fig = Canvas(width=800, height=470,
             title="你的误差分两块：一块查清楚就没了，一块要找个高相关的帮手",
             sub="左格：一天的起伏（方差）拆成组内和组间；右格：拿辅助量减一刀之后，"
                 "毛边还剩多少（两万遍，种子 7）")

# ---------------- 左格：方差分解 ----------------
fig.set_view(0, 2, 0, 132, left=64, right=372, top=88, bottom=316)
fig.grid_y([0, 40, 80, 120], "{:.0f}")
fig.frame()
fig.hline(within, color="#8a8a8a", width=1.2, dash="4 3")
fig.vbars([0.6], [total], color="#c2410c", gap=0.35, opacity=0.9)
fig.vbars([0.6], [within], color="#2f6fb0", gap=0.35, opacity=0.9)
fig.note_at(fig.X(0.6), fig.Y((within + total) / 2) + 4, f"组间 {share * 100:.1f}%",
            color="#ffffff", size=11.5, anchor="middle")
fig.note_at(fig.X(0.6), fig.Y(within / 2) + 4, f"组内 {(1 - share) * 100:.1f}%",
            color="#ffffff", size=11.5, anchor="middle")
fig.note_at(fig.X(1.12), fig.Y(total) + 4, f"整月晃 {month_all:.1f} 单",
            color="#1a1a1a", size=12.5)
fig.note_at(fig.X(1.12), fig.Y(within) - 10, f"知道天气，只剩 {month_known:.1f} 单",
            color="#8a8a8a", size=12.5)
fig.note_at(64, 352, "横轴：一天的起伏，平方之后（组内 + 组间）", color="#454545", size=12)

# ---------------- 右格：控制变量的平方律 ----------------
fig.set_view(0, 1, 0, 1.24, left=440, right=774, top=88, bottom=316)
fig.grid_x([0, 0.2, 0.4, 0.6, 0.8, 1.0], "{:.1f}")
fig.grid_y([0, 0.2, 0.4, 0.6, 0.8, 1.0], "{:.1f}")
fig.frame()
fig.hline(1.0, color="#8a8a8a", width=1.2, dash="4 3")
curve = [i / 200 for i in range(199)]
fig.plot(curve, [math.sqrt(1 - r ** 2) for r in curve], color="#2f6fb0", width=2.4)
fig.dots(rhos, [after[r] for r in rhos], color="#c2410c", r=4.4)
fig.note_at(fig.X(0.02), fig.Y(1.0) - 8, "一点没减", color="#8a8a8a", size=11.5)
fig.note_at(fig.pr - 10, fig.pt + 16, "起作用的是相关的平方", color="#1a1a1a",
            size=13, anchor="end")
fig.note_at(fig.pr - 10, fig.pt + 36,
            f"ρ=0.3 只降 {cut[0.3]:.1f}%，ρ=0.9 降 {cut[0.9]:.1f}%",
            color="#c2410c", size=12.5, anchor="end")
fig.note_at(440, 352, "横轴：辅助量和目标的相关度 ρ（蓝线＝理论，橙点＝两万遍实测）",
            color="#454545", size=12)

# ---------------- 图下三行 ----------------
fig.note_at(58, 378,
             f"左：组间占 {share * 100:.1f}%——把天气定下来，整月起伏从 {month_all:.1f} 掉到 "
             f"{month_known:.1f} 单（模拟实测 59.7 → 34.8，少 41.7%）。",
             color="#454545", size=12.5)
fig.note_at(58, 400,
            f"右：辅助量能省多少看的是相关的平方——ρ=0.3 只降 {cut[0.3]:.1f}%，"
            f"ρ=0.9 才降 {cut[0.9]:.1f}%。",
            color="#454545", size=12.5)
fig.note_at(58, 422,
            "所以：能查清楚的先查清楚（那是组间，不花算力）；要找帮手，就找几乎同涨同跌的那个，不然白干。",
            color="#c2410c", size=12.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig12_conditioning_and_control.svg")
print(fig.save(out))
print(f"    组内 {within:.1f} + 组间 {between:.1f} = {total:.1f}，组间占 {share * 100:.1f}%；"
      f"整月 {month_all:.1f} → {month_known:.1f} 单")
for r in rhos:
    print(f"    相关 {r:.1f}：减前 {before[r]:.3f} → 减后 {after[r]:.3f}（理论 {math.sqrt(1 - r ** 2):.3f}），"
          f"降 {cut[r]:.1f}%")
