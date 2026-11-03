"""两件事一起晃：相关系数怎么算，以及为什么买了十只不等于风险除以十。

第一部分：先核对量尺。造两列已知相关度的数，看你算出来的相关系数对不对。
第二部分：两个数加起来，起伏不是相加——把第 06 课欠的那一项补上。
第三部分：一篮子的起伏怎么来。同一个大环境 + 各自的小运气，n 只等权。
第四部分：分散的地板。加到第十只很有用，加到第一百只几乎没用。
第五部分：相关系数自己也有毛边。两条毫不相干的记录，八天能算出多高的相关？
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def corr(xs, ys):
    """两列数有多"一起动"：-1 到 1。"""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sx = spread(xs)
    sy = spread(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n - 1) / (sx * sy)


def market_pair(rho, n):
    """造 n 天的两列数，让它们的相关大约是 rho：共同的"大环境"加各自的"小运气"。"""
    xs = []
    ys = []
    for _ in range(n):
        common = random.gauss(0, 1)
        xs.append(math.sqrt(rho) * common + math.sqrt(1 - rho) * random.gauss(0, 1))
        ys.append(math.sqrt(rho) * common + math.sqrt(1 - rho) * random.gauss(0, 1))
    return xs, ys


def basket_sd(rho, n, days):
    """n 只资产等权合成一个篮子，看这个篮子每天的起伏（单只起伏按 1 算）。"""
    out = []
    for _ in range(days):
        common = random.gauss(0, 1)
        total = 0
        for _ in range(n):
            total += math.sqrt(rho) * common + math.sqrt(1 - rho) * random.gauss(0, 1)
        out.append(total / n)
    return spread(out)


print("【第一部分：先核对量尺】")
random.seed(7)
for target in [0.0, 0.3, 0.7, 0.9]:
    xs, ys = market_pair(target, 20000)
    print(f"  设定相关 {target:.1f} → 实测 corr {corr(xs, ys):.3f}")

print()
print("【第二部分：两个加起来，起伏不是相加】")
random.seed(7)
for r in [0.0, 0.3, 0.7, 1.0]:
    xs, ys = market_pair(r, 20000)
    summed = [x + y for x, y in zip(xs, ys)]
    theory = math.sqrt(1 + 1 + 2 * r)
    print(f"  两者相关 {r:.1f}：加起来的起伏 实测 {spread(summed):.3f} / 理论 {theory:.3f}（各自起伏都是 1.000）")

print()
print("【第三部分：一篮子的起伏】")
random.seed(7)
rho = 0.3
for n in [1, 2, 10, 50]:
    measured = basket_sd(rho, n, 20000)
    theory = math.sqrt(rho + (1 - rho) / n)
    print(f"  {n:>2} 只、彼此相关 {rho}：篮子起伏 实测 {measured:.3f} / 理论 {theory:.3f}（单只 = 1.000）")

print()
print("【第四部分：分散的地板】")
for r in [0.0, 0.3, 0.7]:
    one = 1.0
    ten = math.sqrt(r + (1 - r) / 10)
    hundred = math.sqrt(r + (1 - r) / 100)
    floor = math.sqrt(r)
    print(f"  相关 {r:.1f}：1 只 {one:.3f} → 10 只 {ten:.3f} → 100 只 {hundred:.3f}；地板（无穷多只）{floor:.3f}")
print("  换算成每天 2% 的单只起伏：相关 0.3 时，1 只 2.00% → 10 只 1.22% → 100 只 1.11%，再怎么加也到不了 1.10% 以下。")
print("  两份收入等权（n = 2）时，合计起伏是多少倍的一份收入：")
for r in [0.7, 0.3, 0.1]:
    print(f"    相关 {r:.1f} → {math.sqrt(r + (1 - r) / 2):.3f}")

print()
print("【第五部分：相关系数自己也有毛边】")
for days in [8, 30, 100]:
    random.seed(7)
    big = 0
    trials = 5000
    values = []
    for _ in range(trials):
        a, b = market_pair(0.0, days)
        c = corr(a, b)
        values.append(abs(c))
        if abs(c) > 0.5:
            big += 1
    values.sort()
    print(f"  两条毫不相干的记录、各 {days} 天：|相关| > 0.5 的占 {big / trials * 100:.1f}%，一半的情况会算出 {values[trials // 2]:.2f} 以上")
