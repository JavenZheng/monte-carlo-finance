"""第 14 课配图：把"你预期的涨幅"塞进定价，会得到一只可以随便拧的旋钮。

生成 assets/fig14_expectation_knob.svg。和第 14 课第五部分同一套抽签
（种子 7、二十万遍、起 100、年化起伏 20%、行权价 100、一年期），
只换"你预期它一年涨多少"这一个旋钮。
"""

import math
import os
import random

from svgkit import Canvas

S0, R, SIGMA, K, T = 100.0, 0.05, 0.20, 100.0, 1.0
runs = 200000

cases = [(0.0, "预期涨 0%", "你预期它一年纹丝不动"),
         (R, "预期涨 5%", "风险中性口径（该用的）"),
         (0.12, "预期涨 12%", "你预期一年涨 12%"),
         (0.20, "预期涨 20%", "你预期一年涨 20%")]

prices = {}
for drift, tag, note in cases:
    random.seed(7)
    vals = []
    for _ in range(runs):
        z = random.gauss(0, 1)
        st = S0 * math.exp((drift - SIGMA ** 2 / 2) * T + SIGMA * math.sqrt(T) * z)
        vals.append(math.exp(-R * T) * max(st - K, 0))
    prices[drift] = sum(vals) / len(vals)

fig = Canvas(width=800, height=470,
             title='同一份合同，只换"你预期的涨幅"，报价能走三倍',
             sub=f'一份"一年后按 {K:.0f} 买入"的权利（行权价 {K:.0f}、起价 {S0:.0f}、'
                 f'年化起伏 {SIGMA:.0%}、一年期）；各抽 {runs // 10000} 万遍（种子 7）')

fig.set_view(0.5, len(cases) + 0.5, 0, prices[0.20] * 1.30, bottom=320)
fig.grid_y([0, 5, 10, 15, 20, 25], "{:.0f}")
fig.frame()

for i, (drift, tag, note) in enumerate(cases, start=1):
    color = "#1a7f5f" if abs(drift - R) < 1e-9 else "#2f6fb0"
    fig.vbars([i], [prices[drift]], color=color, gap=0.45)
    fig.note_at(fig.X(i), fig.Y(prices[drift]) - 12, f"{prices[drift]:.2f}",
                color=color, size=15, anchor="middle")
    fig.note_at(fig.X(i), fig.pb + 20, tag, color="#1a1a1a", size=12.5, anchor="middle")
    fig.note_at(fig.X(i), fig.pb + 38, note, color="#7a7a7a", size=11, anchor="middle")

fig.hline(prices[R], color="#1a7f5f", width=1.4, dash="6 4")
fig.note_at(fig.pl + 10, fig.Y(prices[R]) - 11,
            "只有这一格是价格：它由复制成本给出", color="#1a7f5f", size=12.5,
            anchor="start")

fig.ylabel("这份权利今天值几块")

fig.note_at(64, 386,
            f"合同一个字没改，报价从 {prices[0.0]:.2f} 一路走到 {prices[0.20]:.2f}"
            f"（{prices[0.20] / prices[0.0]:.1f} 倍）——变的只是你嘴里那个预期。",
            color="#454545", size=12.5)
fig.note_at(64, 406,
            '所以"这个预期年化 12%，所以它值这个价"这句话里，那个 12% 是一只可以随便拧的旋钮。',
            color="#c2410c", size=12.5)
fig.note_at(64, 426,
            '定价的正确问法不是"我觉得多大概率会涨"，而是"要拼出这笔赔付，我今天得花几块"。',
            color="#1a7f5f", size=12.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig14_expectation_knob.svg")
print(fig.save(out))
for drift, tag, note in cases:
    print(f"    {tag}（{note}）→ {prices[drift]:.2f}")
print(f"    倍数 {prices[0.20] / prices[0.0]:.1f}")
