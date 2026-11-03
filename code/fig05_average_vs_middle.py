"""第 05 课配图：三组数排成三条队，看平均站在哪儿。

生成 assets/fig05_average_vs_middle.svg。数据就是课文第四节那三列（播放量七条、
通勤十条、等车八条），三个数（平均、排在中间那条、低于平均占几成）用
code/lesson05_where_the_average_sits.py 的同一套算法现算，与课文逐字一致。
"""

import os

from svgkit import Canvas

groups = [
    ("你的七条内容（播放量）", [820, 1200, 3400, 610, 950, 2100, 480], "次", 380, 3600,
     [500, 1000, 2000, 3000]),
    ("你十天的通勤（分钟）", [34, 41, 29, 38, 45, 31, 37, 40, 26, 33], "分钟", 22, 48,
     [25, 30, 35, 40, 45]),
    ("你八次打车的等车时间", [3, 5, 2, 4, 30, 3, 2, 5], "分钟", -1, 33,
     [0, 5, 10, 15, 20, 25, 30]),
]

fig = Canvas(width=800, height=480,
             title='同一个"平均"，三组数说的是三句话',
             sub="每条记录钉在横轴上；蓝实线＝平均，黑虚线＝排在中间那条，"
                 "橙色那一块＝低于平均的那几条")

LEFT, RIGHT = 64, 774
for idx, (name, records, unit, lo, hi, ticks) in enumerate(groups):
    top = 108 + idx * 106
    bottom = top + 58
    fig.set_view(lo, hi, 0, 1, left=LEFT, right=RIGHT, top=top, bottom=bottom)
    mean = sum(records) / len(records)
    middle = sorted(records)[len(records) // 2]
    below = sum(1 for x in records if x < mean) / len(records)

    fig.band(lo, mean, color="#c2410c", opacity=0.06)
    fig.plot([lo, hi], [0.5, 0.5], color="#d8d8d8", width=1.2)
    for t in ticks:
        px = fig.X(t)
        fig.parts.append(f'<line x1="{px:.1f}" y1="{bottom:.1f}" x2="{px:.1f}" '
                         f'y2="{bottom + 4:.1f}" stroke="#c8c8c8"/>')
        fig.note_at(px, bottom + 17, f"{t:,}", color="#8a8a8a", size=10.5, anchor="middle")
    fig.dots(records, [0.5] * len(records), color="#2f6fb0", r=5.4, opacity=0.85)
    fig.vline(mean, color="#2f6fb0", width=2.2, y0=0.06, y1=0.94)
    fig.vline(middle, color="#1a1a1a", width=1.8, dash="5 3", y0=0.06, y1=0.94)

    fig.note_at(LEFT, top - 10, name, color="#1a1a1a", size=13)
    fig.note_at(RIGHT, top - 10,
                f"平均 {mean:.1f}{unit}　中间那条 {middle}{unit}　低于平均 {below * 100:.0f}%",
                color="#454545", size=12.5, anchor="end")

fig.note_at(58, 418,
            "第一组和第三组：蓝线被右边那一条拽走了，黑虚线还站在人堆里"
            "——低于平均占七十一和八十八。",
            color="#454545", size=12.5)
fig.note_at(58, 438,
            "那个平均描述的是这一列的总量，不是你典型的一次。",
            color="#454545", size=12.5)
fig.note_at(58, 458,
            '第二组：两条线几乎重合、低于平均正好五成——这组数老老实实，'
            '"我通勤平均三十五分钟"可以放心说出口。',
            color="#1a7f5f", size=12.5)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                   "fig05_average_vs_middle.svg")
print(fig.save(out))
for name, records, unit, _, _, _ in groups:
    mean = sum(records) / len(records)
    middle = sorted(records)[len(records) // 2]
    below = sum(1 for x in records if x < mean) / len(records)
    print(f"    {name}：平均 {mean:.1f}{unit}，中间那条 {middle}{unit}，"
          f"低于平均 {below * 100:.0f}%，最大 {max(records)} 比平均高 {max(records) - mean:.1f}")
