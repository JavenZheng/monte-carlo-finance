"""第 06 课配图：三份 offer，期望、脾气，和那条固定支出线。

生成 assets/fig06_expectation_and_spread.svg。数据就是课文第四、五节那三份方案
（A 铁饭碗 12000 稳、B 高提成 15000/7500、C 大起大落 20000/8000），期望和脾气
用课文那两个函数现算，与课文逐字一致。
"""

import math
import os

from svgkit import Canvas

plans = [
    ("A 铁饭碗", [12000], [1.0]),
    ("B 高提成", [15000, 7500], [0.6, 0.4]),
    ("C 大起大落", [20000, 8000], [0.5, 0.5]),
]
FIXED = 9000.0
LEFT, RIGHT = 64, 774
LO, HI = 4000.0, 22000.0
TOP0, ROW, GAP = 104, 74, 18


def expectation(outcomes, probs):
    return sum(x * p for x, p in zip(outcomes, probs))


def spread(outcomes, probs):
    m = expectation(outcomes, probs)
    return math.sqrt(sum((x - m) ** 2 * p for x, p in zip(outcomes, probs)))


fig = Canvas(width=800, height=500,
             title="三份 offer：期望一样，脾气不一样，落到你身上更不一样",
             sub="圆是可能的结果，圆越大代表那种月份越常；橙实线＝掺出来的期望，"
                 "灰括号＝脾气（离期望一般多远）")

for idx, (name, outcomes, probs) in enumerate(plans):
    top = TOP0 + idx * (ROW + GAP)
    bottom = top + ROW
    fig.set_view(LO, HI, 0, 1, left=LEFT, right=RIGHT, top=top, bottom=bottom)
    m = expectation(outcomes, probs)
    s = spread(outcomes, probs)

    if s > 0:
        fig.plot([m - s, m + s], [0.5, 0.5], color="#8a8a8a", width=1.6)
        for edge in (m - s, m + s):
            fig.vline(edge, color="#8a8a8a", width=1.6, y0=0.38, y1=0.62)
    for x, p in zip(outcomes, probs):
        fig.dots([x], [0.5], color="#2f6fb0", r=26 * math.sqrt(p), opacity=0.5)
        fig.note_at(fig.X(x), fig.Y(0.5) + 4, f"{x:,}", color="#12385c", size=12.5,
                    anchor="middle")
        if p < 1:
            fig.note_at(fig.X(x), fig.Y(0.5) + 22, f"{p * 10:.0f} 成的月份",
                        color="#454545", size=11.5, anchor="middle")
    fig.vline(m, color="#c2410c", width=2.6, y0=0.05, y1=0.95)
    fig.dots([m], [0.5], color="#c2410c", r=3.4)

    fig.note_at(LEFT, top - 10, name, color="#1a1a1a", size=13)
    fig.note_at(RIGHT, top - 10,
                f"长期每月 {m:,.0f}　脾气 ±{s:,.0f}",
                color="#454545", size=12.5, anchor="end")

axis_bottom = TOP0 + 2 * (ROW + GAP) + ROW
fig.set_view(LO, HI, 0, 1, left=LEFT, right=RIGHT, top=TOP0, bottom=axis_bottom)
for t in [5000, 10000, 15000, 20000]:
    px = fig.X(t)
    fig.parts.append(f'<line x1="{px:.1f}" y1="{axis_bottom:.1f}" x2="{px:.1f}" '
                     f'y2="{axis_bottom + 4:.1f}" stroke="#c8c8c8"/>')
    fig.note_at(px, axis_bottom + 17, f"{t:,}", color="#8a8a8a", size=10.5, anchor="middle")
px = fig.X(FIXED)
fig.parts.append(f'<line x1="{px:.1f}" y1="{TOP0 - 4:.1f}" x2="{px:.1f}" '
                 f'y2="{axis_bottom:.1f}" stroke="#b91c1c" stroke-width="1.6" '
                 f'stroke-dasharray="6 4"/>')
fig.note_at(px - 8, TOP0 + 14, f"每月固定支出 {FIXED:,.0f}", color="#b91c1c", size=12.5,
            anchor="end")

fig.note_at(58, 434,
            "橙线是\"掺很多遍之后每次摊到的数\"，它常常不在任何一个可能的月份上："
            "B 的期望 12000 那一格，一个月都不会出现。",
            color="#454545", size=12.5)
fig.note_at(58, 454,
            "A 和 B 的橙线落在同一条竖线上，脾气一个 ±0、一个 ±3674。"
            "期望相同，人生不同——这就是第二个数存在的理由。",
            color="#454545", size=12.5)
fig.note_at(58, 474,
            "红虚线才是生活：固定支出 9000。B 有四成的月份落在它左边，C 有一半。期望看不见这件事。",
            color="#b91c1c", size=12.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig06_expectation_and_spread.svg")
print(fig.save(out))
for name, outcomes, probs in plans:
    m = expectation(outcomes, probs)
    s = spread(outcomes, probs)
    below = sum(p for x, p in zip(outcomes, probs) if x < FIXED)
    print(f"    {name}：期望 {m:.0f}，脾气 ±{s:.0f}，落在固定支出左边的机会 {below * 100:.0f}%")
