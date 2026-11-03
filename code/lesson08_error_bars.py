"""误差棒怎么画，以及凭什么乘二。

第一部分：工具。给你一列记录，报出平均、毛边、乘二之后的范围。
第二部分：替第 07 课那句"乘二"做证。把一列记录反复抽十条取平均，看平均自己排成什么形状。
第三部分：同一个动作换成一列很歪的记录，钟形就不一定立刻出现了。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random


def fuzz(records, unit=""):
    n = len(records)
    mean = sum(records) / n
    spread = math.sqrt(sum((x - mean) ** 2 for x in records) / (n - 1))
    se = spread / math.sqrt(n)
    print(f"平均 {mean:.1f}{unit} ± {se:.1f}（毛边）")
    print(f"你敢报的范围：{mean - 2 * se:.1f} 到 {mean + 2 * se:.1f}{unit}")
    return mean, spread, se


def spread_of(record):
    n = len(record)
    m = sum(record) / n
    return math.sqrt(sum((x - m) ** 2 for x in record) / (n - 1))


def repeat_averages(data, k, runs):
    out = []
    for _ in range(runs):
        sample = random.choices(data, k=k)
        out.append(sum(sample) / k)
    return out


def histogram(values, bins=9, width=46):
    lo = min(values)
    hi = max(values)
    step = (hi - lo) / bins
    counts = [0] * bins
    for x in values:
        k = int((x - lo) / step)
        if k == bins:
            k = bins - 1
        counts[k] = counts[k] + 1

    biggest = max(counts)
    for i in range(bins):
        left = lo + i * step
        bar = "*" * max(1, int(round(counts[i] / biggest * width)))
        print(f"{left:6.1f}  {bar}  {counts[i]}")


taxi = [3, 5, 2, 4, 30, 3, 2, 5]
commute = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]

print("【第一部分：把误差棒画出来】")
fuzz(taxi, " 分钟")

print()
print("【第二部分：通勤这十天，抽十条取平均，重复两万遍】")
random.seed(7)
avgs = repeat_averages(commute, 10, 20000)
histogram(avgs)
se = 1.856
for mult in (1, 2, 3):
    inside = 0
    for a in avgs:
        if abs(a - 35.4) <= mult * se:
            inside = inside + 1
    print(f"±{mult} 倍毛边（±{mult * se:.1f} 分钟）之内：{inside / len(avgs) * 100:.1f}%")
print(f"预测的毛边 {spread_of(commute) / math.sqrt(10):.2f}，"
      f"实测两万条平均的散布 {spread_of(avgs):.2f}")

print()
print("【第三部分：换成那列很歪的等车记录，同样抽十条】")
random.seed(7)
avgs2 = repeat_averages(taxi, 10, 10000)
histogram(avgs2)
print(f"预测的毛边 {spread_of(taxi) / math.sqrt(10):.2f}，"
      f"实测一万条平均的散布 {spread_of(avgs2):.2f}")

print()
print("【第四部分：同一列歪记录，改抽一百条 —— 钟形回来了】")
random.seed(7)
avgs3 = repeat_averages(taxi, 100, 10000)
histogram(avgs3)
se100 = spread_of(taxi) / math.sqrt(100)
truth = sum(taxi) / len(taxi)
inside = 0
for a in avgs3:
    if abs(a - truth) <= 2 * se100:
        inside = inside + 1
print(f"±2 倍毛边（±{2 * se100:.1f} 分钟）之内：{inside / len(avgs3) * 100:.1f}%")
