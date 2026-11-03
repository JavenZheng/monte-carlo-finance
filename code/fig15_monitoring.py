"""第 15 课配图（三）：你多久看一眼，决定你漏掉多少跌破。

生成 assets/fig15_monitoring.svg。和第 15 课第七部分同一套抽签（种子 7、
八千条路、每条切 1000 段当成"真实最低"），只是把"你看得到的那几个时刻"改成 4/12/52/250/1000 次。
"""

import math
import os
import random

from svgkit import Canvas

a, nfine, runs = 0.5, 1000, 8000
watches = [4, 12, 52, 250, 1000]


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


random.seed(7)
truth = 0
seen = {w: 0 for w in watches}
for _ in range(runs):
    pos = 0.0
    vals = [0.0]
    for _ in range(nfine):
        pos += random.gauss(0, math.sqrt(1.0 / nfine))
        vals.append(pos)
    if min(vals) <= -a:
        truth += 1
    for w in watches:
        if min(vals[::nfine // w]) <= -a:
            seen[w] += 1

base = truth / runs * 100
cont = 2 * norm_cdf(-a) * 100
rates = [seen[w] / runs * 100 for w in watches]

fig = Canvas(width=800, height=470,
             title='你少看，"跌破"就像没发生过',
             sub=f"八千条路、每条切 {nfine} 段（种子 7）；跌破线 −{a}"
                 "　·　柱内白字＝你看到的跌破，浅色是漏掉的个百分点")

fig.set_view(0.5, len(watches) + 0.5, 0, cont + 9, bottom=316)
fig.grid_y([0, 10, 20, 30, 40, 50, 60], "{:.0f}")
fig.frame()

fig.vbars(list(range(1, len(watches) + 1)), rates, color="#2f6fb0", gap=0.35)

fig.hline(base, color="#1a1a1a", width=1.6, dash="6 4")
fig.hline(cont, color="#7a7a7a", width=1.2, dash="2 4")

for i, (w, r) in enumerate(zip(watches, rates), start=1):
    fig.note_at(fig.X(i), fig.pb + 18, f"{w}", color="#5a5a5a", size=12.5, anchor="middle")
    fig.note_at(fig.X(i), fig.Y(r) + 24, f"{r:.1f}%", color="#ffffff", size=13.5, anchor="middle")
    fig.note_at(fig.X(i), fig.Y(r) + 44, f"漏 {base - r:.1f}", color="#dbe6f2", size=11.5,
                anchor="middle")

fig.note_at((fig.pl + fig.pr) / 2, 352, "一年看几次", color="#454545", size=12.5,
            anchor="middle")
fig.note_at(58, 378,
            f"黑虚线＝每段都看（{nfine} 次）算出的真值 {base:.1f}%；"
            f"灰点线＝连续地看的理论值 {cont:.1f}%",
            color="#454545", size=12.5)
fig.note_at(58, 398,
            f"连每段都看都比理论值低 {cont - base:.1f} 个百分点："
            "这条路你不可能看全，只能选择漏多少。",
            color="#454545", size=12.5)
fig.note_at(58, 418,
            '第 14 课那份保底合同"看 12 次报 6.82、看 500 次报 6.13"，'
            "差的就是这里漏掉的跌破折成的钱。",
            color="#c2410c", size=12.5)

fig.ylabel("跌破过的路径占几成")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig15_monitoring.svg")
print(fig.save(out))
print(f"    真值（{nfine} 段）{base:.1f}%；连续理论 {cont:.1f}%；"
      + "；".join(f"看 {w} 次 {r:.1f}%（漏 {base - r:.1f}）" for w, r in zip(watches, rates)))
