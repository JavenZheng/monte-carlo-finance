"""两个方案，一个问长期，一个问脾气。

期望 = 每种结果按它的机会掺在一起；起伏（标准差）= 结果离那个掺好的数有多远。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math


def expectation(outcomes, probs):
    total = 0
    for x, p in zip(outcomes, probs):
        total = total + x * p
    return total


def spread(outcomes, probs):
    m = expectation(outcomes, probs)
    v = 0
    for x, p in zip(outcomes, probs):
        v = v + (x - m) ** 2 * p
    return math.sqrt(v)


offers = [
    ("A 铁饭碗", [12000], [1.0]),
    ("B 高提成", [15000, 7500], [0.6, 0.4]),
    ("C 大起大落", [20000, 8000], [0.5, 0.5]),
]

for name, outcomes, probs in offers:
    m = expectation(outcomes, probs)
    s = spread(outcomes, probs)
    print(f"{name}：长期每月 {m:.0f}，脾气 ±{s:.0f}")

print()
print("【期望可以永远拿不到：一颗骰子】")
die = [1, 2, 3, 4, 5, 6]
p = [1 / 6] * 6
print(f"期望 {expectation(die, p)}，起伏 {spread(die, p):.2f}")
