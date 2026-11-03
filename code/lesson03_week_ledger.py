"""把一列记录交给电脑：平均、最贵最省、超过线的那几天。

改 summarize(...) 括号里那一列数，就是你自己的记录了。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""


def summarize(records, line=45):
    n = len(records)
    total = sum(records)
    mean = total / n

    print(f"记了 {n} 天，总共 {total}，平均每天 {mean:.1f}")
    print(f"最贵那天 {max(records)}，比平均高 {max(records) - mean:.1f}")
    print(f"最省那天 {min(records)}，比平均低 {mean - min(records):.1f}")

    over = []
    for x in records:
        if x > line:
            over.append(x)
    print(f"超过 {line} 的有 {len(over)} 天：{over}")

    return mean


week = [38, 42, 29, 55, 41, 33, 47]
commute = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]

print("【一周午餐】")
summarize(week)
print()
print("【十天通勤，单位分钟，把线设成 40】")
summarize(commute, line=40)
