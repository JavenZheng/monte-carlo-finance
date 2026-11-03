"""第一次真模拟。

第一段复现第 01 课的便利贴实验：六条里爆一条，连发六条一条都没爆的概率。
第二段造一个还没发生过的月：每个工作日随机抽一顿饭钱，看月底落在哪儿。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import random


def a_round(rate, posts):
    """发 posts 条，每条爆的概率是 rate。一条都没爆返回 True。"""
    hits = 0
    for _ in range(posts):
        if random.random() < rate:
            hits = hits + 1
    return hits == 0


def all_quiet_rate(rate, posts, runs):
    """重复 runs 轮，返回其中"全空"的轮占多大比例。"""
    quiet = 0
    for _ in range(runs):
        if a_round(rate, posts):
            quiet = quiet + 1
    return quiet / runs


def one_month(low, high, workdays):
    """造一个没发生过的月：每个工作日的花销在 low 到 high 之间随机。"""
    total = 0
    for _ in range(workdays):
        total = total + random.uniform(low, high)
    return total


print("【第一段：把便利贴装进电脑】")
for runs in (10, 1000, 100000):
    random.seed(7)          # 每行都从同一条运气流开头，你看到的差别只来自轮数
    p = all_quiet_rate(1 / 6, 6, runs)
    print(f"演 {runs} 轮 → 全空占 {p * 100:.1f}%")

print()
print("【第二段：一个还没发生的月，演 1000 个】")
random.seed(7)
months = []
for _ in range(1000):
    months.append(one_month(25, 55, 22))

months.sort()
p10 = months[int(0.1 * len(months))]
p90 = months[int(0.9 * len(months))]
print(f"最省的月 {months[0]:.0f}，最贵的月 {months[-1]:.0f}")
print(f"平均 {sum(months) / len(months):.0f}")
print(f"一成的月低于 {p10:.0f}，九成的月不超过 {p90:.0f}")
