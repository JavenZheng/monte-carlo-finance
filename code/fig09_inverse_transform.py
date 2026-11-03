"""第 09 课配图：一条一米长的队伍，切段就是三档，反解就是曲线。

生成 assets/fig09_inverse_transform.svg。左格是"队伍位置 u → 等多久"这条映射
本身（每小时 6 单的指数间隔，加上第三节那三档送达的台阶）；右格是把这条队伍
抽两万遍落出来的形状。种子 7，数字与课文第三、四节逐字一致。
"""

import math
import os
import random

from svgkit import Canvas

runs = 20000
rate = 6.0                 # 平均每小时 6 单
mean_min = 60 / rate       # 理论平均间隔 10 分钟

random.seed(7)
us = [random.random() for _ in range(runs)]
gaps = [-math.log(1 - u) / rate * 60 for u in us]

measured = sum(gaps) / len(gaps)
short = sum(1 for g in gaps if g < 5) / len(gaps)
under_mean = sum(1 for g in gaps if g < measured) / len(gaps)
u5 = 1 - math.exp(-5 / mean_min)        # 曲线穿过 5 分钟时的队伍位置
tail10 = -math.log(0.10) * mean_min     # 队伍最后 10% 从几分钟起

fig = Canvas(width=800, height=470,
             title="一条一米长的队伍：切段是三档，反解是曲线",
             sub=f"左格：抽到队伍上哪个位置（横轴）→ 就等多久（纵轴，分钟）；"
                 f"右格：把这条队伍抽两万遍落出来的形状（种子 7）")

# ---------------- 左格：映射本身 ----------------
fig.set_view(0, 1, 0, 56, left=58, right=392, top=88, bottom=316)
fig.band(0, u5, color="#c2410c", opacity=0.07)
fig.grid_x([0, 0.2, 0.4, 0.6, 0.8, 1.0], "{:.1f}")
fig.grid_y([0, 10, 20, 30, 40, 50], "{:.0f}")
fig.frame()

fig.dots([u for u, g in zip(us[::67], gaps[::67]) if g <= 50],
         [g for g in gaps[::67] if g <= 50], color="#2f6fb0", r=1.9, opacity=0.32)
line_u = [i / 400 * 0.9933 for i in range(401)]
fig.plot(line_u, [-math.log(1 - u) * mean_min for u in line_u], color="#2f6fb0", width=2.4)
fig.plot([0, 0.2, 0.2, 0.7, 0.7, 1.0], [20, 20, 30, 30, 50, 50],
         color="#c2410c", width=2.0, dash="6 4")
fig.vline(u5, color="#c2410c", width=1.3, dash="4 3", y0=0, y1=5)
fig.hline(5, color="#c2410c", width=1.3, dash="4 3")
fig.dots([u5], [5], color="#c2410c", r=4.2)

fig.note_at(fig.X(0.95), fig.Y(40), "一小时 6 单：抽到哪儿，就等多久",
            color="#2f6fb0", size=12.5, anchor="end")
fig.note_at(fig.X(0.02), fig.Y(20) - 8, "快（20 分钟）", color="#c2410c", size=11.5)
fig.note_at(fig.X(0.22), fig.Y(30) - 8, "准点（30 分钟）", color="#c2410c", size=11.5)
fig.note_at(fig.X(0.72), fig.Y(50) - 8, "晚（50 分钟）", color="#c2410c", size=11.5)
fig.note_at(fig.pl + 10, fig.Y(14), f"队伍前 {u5 * 100:.1f}%（橙色那一段），",
            color="#c2410c", size=12.5)
fig.note_at(fig.pl + 10, fig.Y(14) + 18, "全落在 5 分钟以内", color="#c2410c", size=12.5)
fig.note_at(58, 352, "横轴：队伍上的位置（0 是队头，1 是队尾）", color="#454545", size=12)

# ---------------- 右格：抽出来的形状 ----------------
lo, hi, bins = 0.0, 45.0, 45
counts = [0] * bins
over = 0
for g in gaps:
    if g >= hi:
        over += 1
        continue
    counts[int(g)] += 1

fig.set_view(lo, hi, 0, max(counts) * 1.18, left=452, right=774, top=88, bottom=316)
fig.band(0, 5, color="#c2410c", opacity=0.07)
fig.grid_x([0, 5, 10, 15, 20, 25, 30, 35, 40, 45], "{:.0f}")
fig.grid_y([t for t in range(0, max(counts) + 1, 500) if t % 1000 == 0], "{:,}")
fig.frame()
fig.vbars([i + 0.5 for i in range(bins)], counts, color="#2f6fb0", gap=0.12)
mean_top = max(counts) * 0.72
fig.vline(measured, color="#1a7f5f", width=1.6, dash="6 4", y0=0, y1=mean_top)
fig.note_at(fig.X(0.4), fig.pt + 16, f"不到 5 分钟：{short * 100:.1f}%",
            color="#c2410c", size=13)
fig.note_at(fig.X(measured) + 7, fig.Y(mean_top) - 8, f"平均 {measured:.1f} 分钟",
            color="#1a7f5f", size=12.5)
fig.note_at(452, 352, f"横轴：两单之间隔了几分钟（超过 {hi:.0f} 分钟的 {over} 条没画进来）",
            color="#454545", size=12)

# ---------------- 图下三行 ----------------
fig.note_at(58, 378,
            f"左边那条线就是全部秘密：队伍前 {u5 * 100:.1f}% 映到 5 分钟以内，"
            f"而最后 10% 那一段从 {tail10:.1f} 分钟起还没头。",
            color="#454545", size=12.5)
fig.note_at(58, 400,
            f"抽两万遍，机器自己报的数和它说的对上：平均间隔 {measured:.1f} 分钟，"
            f"不到 5 分钟占 {short * 100:.1f}%。",
            color="#454545", size=12.5)
fig.note_at(58, 422,
            f"比平均短的占 {under_mean * 100:.1f}%——平均值是被少数长间隔抬上去的。"
            f"同一个平均，可以配完全不同的形状。",
            color="#c2410c", size=12.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig09_inverse_transform.svg")
print(fig.save(out))
print(f"    平均间隔 {measured:.1f} 分钟；不到 5 分钟 {short * 100:.1f}%"
      f"（理论 {u5 * 100:.1f}%）；比平均短 {under_mean * 100:.1f}%；"
      f"最后 10% 从 {tail10:.1f} 分钟起；超过 {hi:.0f} 分钟 {over} 条")
