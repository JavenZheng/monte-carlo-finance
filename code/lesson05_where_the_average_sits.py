"""你的那个平均，描述了你几天？

把一列记录交给它，它告诉你三件事：平均是多少、排在中间那条是多少、
这一列里有几条在平均以下。最后那个数才是判断"平均有没有骗你"的关键。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""


def where_average_sits(records, unit=""):
    n = len(records)
    mean = sum(records) / n
    ordered = sorted(records)
    middle = ordered[n // 2]

    below = 0
    for x in records:
        if x < mean:
            below = below + 1

    print(f"一共 {n} 条。平均 {mean:.1f}{unit}，排在中间那条 {middle}{unit}")
    print(f"低于平均的有 {below} 条，占 {below / n * 100:.0f}%")
    print(f"最多的一条 {ordered[-1]}，它比平均高 {ordered[-1] - mean:.1f}")
    return mean


plays = [820, 1200, 3400, 610, 950, 2100, 480]
commute = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]
taxi = [3, 5, 2, 4, 30, 3, 2, 5]

print("【你最近七条内容的播放量】")
where_average_sits(plays, " 次")
print()
print("【十天通勤，分钟】")
where_average_sits(commute, " 分钟")
print()
print("【八次打车等车，分钟】")
where_average_sits(taxi, " 分钟")
