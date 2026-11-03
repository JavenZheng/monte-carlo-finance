"""第 10 课配图：同一个平均，两种人生（波动拖累）。

生成 assets/fig10_volatility_drag.svg。和第 10 课第四部分同一套抽签：
起 100、每天平均涨 0.1%、一年 250 天、各跑一万遍（种子 7），只把起伏从 2% 换成 4%。
两格用同一把尺子（横轴 0 到 280，纵轴同一格数），所以"中位线往左跑"是看得见的。
"""

import math
import os
import random

from svgkit import Canvas

days, runs, mean_r = 250, 10000, 0.001


def mult_price(start, sd_r):
    random.seed(7)
    out = []
    for _ in range(runs):
        p = start
        for _ in range(days):
            p *= 1 + random.gauss(mean_r, sd_r)
        out.append(p)
    return out


def quantile(vals, q):
    return sorted(vals)[int(q * len(vals))]


calm = mult_price(100, 0.02)
wild = mult_price(100, 0.04)

stats = {}
for name, vals in (("起伏 2%", calm), ("起伏 4%", wild)):
    stats[name] = dict(
        med=quantile(vals, 0.5),
        avg=sum(vals) / len(vals),
        loss=sum(1 for v in vals if v < 100) / len(vals) * 100,
        vals=vals)

lo, hi, bins = 0.0, 280.0, 28
step = (hi - lo) / bins
hists = {}
over = {}
peak = 0
for name, vals in ((k, v["vals"]) for k, v in stats.items()):
    counts = [0] * bins
    o = 0
    for x in vals:
        if x > hi:
            o += 1
        counts[min(bins - 1, max(0, int(x / step)))] += 1
    hists[name] = counts
    over[name] = o
    peak = max(peak, max(counts))

fig = Canvas(width=800, height=450,
             title="同一个平均，两种人生",
             sub="起 100，每天平均涨 0.1%、一年 250 天，各跑一万遍（种子 7）；两格同一把尺子"
                 "　·　实线＝中位（你会遇到的那一次），灰虚线＝平均")

left = 56
gap = 34
panel_w = (800 - 26 - left - gap) / 2
top = peak * 1.16

for idx, name in enumerate(("起伏 2%", "起伏 4%")):
    st = stats[name]
    pl = left + idx * (panel_w + gap)
    fig.set_view(lo, hi, 0, top, left=pl, right=pl + panel_w, top=92, bottom=322)
    fig.grid_x([0, 50, 100, 150, 200, 250], "{:.0f}")
    fig.grid_y([t for t in range(0, int(top), 250) if t % 500 == 0], "{:,.0f}")
    fig.frame()
    fig.band(lo, 100, color="#c2410c", opacity=0.07)
    fig.vbars([lo + (i + 0.5) * step for i in range(bins)], hists[name],
              color="#2f6fb0", gap=0.1)
    fig.vline(100, color="#c2410c", width=1.2, dash="3 3")
    fig.vline(st["med"], color="#1a1a1a", width=1.8)
    fig.vline(st["avg"], color="#7a7a7a", width=1.2, dash="5 4")
    fig.note_at(pl, 74, name, color="#1a1a1a", size=14)
    fig.note_at(fig.X(st["med"]) - 6, fig.pt + 18, f"中位 {st['med']:.1f}",
                color="#1a1a1a", size=12.5, anchor="end")
    fig.note_at(fig.X(st["avg"]) + 6, fig.pt + 34, f"平均 {st['avg']:.1f}",
                color="#7a7a7a", size=12.5)
    fig.note_at(fig.X(50), fig.pt + 54, f"比本金低：{st['loss']:.1f}%",
                color="#c2410c", size=12.5, anchor="middle")
    fig.note_at(pl + panel_w - 6, fig.pb - 8,
                f"最右一格含超过 {hi:.0f} 的 {over[name]} 条", color="#7a7a7a", size=11,
                anchor="end")

fig.note_at(left + panel_w / 2, 360, "一年后值多少（本金 100）", color="#454545", size=12.5,
            anchor="middle")
fig.note_at(left + panel_w + gap + panel_w / 2, 360, "一年后值多少（本金 100）",
            color="#454545", size=12.5, anchor="middle")
fig.note_at(58, 386,
            f"两格的平均几乎重合（{stats['起伏 2%']['avg']:.1f} 对 {stats['起伏 4%']['avg']:.1f}），"
            f"中位却往左跑了 {stats['起伏 2%']['med'] - stats['起伏 4%']['med']:.1f} 块"
            f"（{stats['起伏 2%']['med']:.1f} → {stats['起伏 4%']['med']:.1f}）",
            color="#454545", size=12.5)
fig.note_at(58, 406,
            f"亏钱的面积（橙色那一块）从 {stats['起伏 2%']['loss']:.1f}% 涨到 "
            f"{stats['起伏 4%']['loss']:.1f}%：报表上什么都没变，你手上的人生变了。",
            color="#c2410c", size=12.5)
fig.note_at(58, 426,
            "这就是波动拖累：起伏在指数上偷偷扣掉 σ²/2，平均看不见它，中位看得见。",
            color="#7a7a7a", size=12)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig10_volatility_drag.svg")
print(fig.save(out))
for name in ("起伏 2%", "起伏 4%"):
    st = stats[name]
    print(f"    {name}：中位 {st['med']:.1f}，平均 {st['avg']:.1f}，亏钱的占 {st['loss']:.1f}%")
