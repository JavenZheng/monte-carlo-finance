"""导数回答'多一单位值多少钱'，泰勒展开回答'我用的这个近似差多少'。

第一部分：边际表——'多一块值多少'取决于你站在哪一块。
第二部分：顶点——多一块钱已经不划算的那一刻。
第三部分：一步读、前向读、中心读——曲率会让你读歪，读法能救回来。
第四部分：泰勒展开——每一项多大，误差约等于你扔掉的第一项。
第五部分：二阶项救命——平均一分不赚，中位只剩三成。
第六部分：近似带来的偏差和抽样带来的毛边是两回事，算力只治后者。
第七部分：练习核对。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random

COST = 8.0        # 一杯的硬成本
DEMAND_A = 120.0  # 定 1 元时一天理论能卖多少杯
DEMAND_B = 6.0    # 每涨 1 元少卖几杯


def demand(p):
    return DEMAND_A - DEMAND_B * p


def profit(p):
    """一天卖 p 元一杯，赚多少钱。"""
    return (p - COST) * demand(p)


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def forward(f, x, h):
    """往前挪一步读：把 [x, x+h] 这段的平均变化当成 x 这一点的答案。"""
    return (f(x + h) - f(x)) / h


def central(f, x, h):
    """前后各挪一步再平均：把 x 两侧的信息都用上。"""
    return (f(x + h) - f(x - h)) / (2 * h)


print("【第一部分：多一块钱值多少，要看你现在站在哪一块】")
print(f"  一杯硬成本 {COST:.0f} 元；定 10 元一天卖 {demand(10):.0f} 杯，每涨 1 元少卖 {DEMAND_B:.0f} 杯")
print("  定价      一天利润    涨 1 块之后    多一块值")
for p in [9, 10, 11, 12, 13, 14, 15, 16]:
    print(f"  {p:>4} 元  {profit(p):>10.0f}  {profit(p + 1):>12.0f}  {profit(p + 1) - profit(p):>+11.0f}")
print("  同样是'多一块'，在 10 元那档值 42 块，在 14 元那档倒亏 6 块。")
print("  这个'多一单位值多少钱'就叫导数，也就是老师傅嘴里的边际。")
print("  它不是一个数，是随你所在档位变化的一个数。")
print()
print("  把步子缩小看瞬时，还是 p=10 那一档：")
print(f"    一步读（涨满 1 块）      ：{(profit(11) - profit(10)) / 1:.1f}")
print(f"    小步读（涨 0.1 块）      ：{forward(profit, 10, 0.1):.1f}")
print(f"    两侧平均读（9.9 到 10.1）：{central(profit, 10, 0.1):.1f}")
print(f"    手算的瞬时值 168 − 12p 在 p=10：{168 - 12 * 10:.1f}")

print()
print("【第二部分：顶点就是'多一块值 0'那一档】")
best_p, best_v = None, -1.0
p = 8.0
while p <= DEMAND_A / DEMAND_B:
    if profit(p) > best_v:
        best_v, best_p = profit(p), p
    p += 0.1
print(f"  以 0.1 元为档，从 {COST:.0f} 元一档档试上去：最赚的是 {best_p:.1f} 元，一天 {best_v:.0f} 块")
print("  手算：利润 = (p−8)(120−6p)，展开是 −6p² + 168p − 960；令导数 168 − 12p = 0 → p = 14")
print(f"  核对（步子缩到 0.1 元来读）：p=13.9 时多一角值 {forward(profit, 13.9, 0.1):+.1f}，p=14.1 时值 {forward(profit, 14.1, 0.1):+.1f}")
print(f"  过了顶点每多一角都是负的：p=16 → {forward(profit, 16, 0.1):+.1f}")

print()
print("【第三部分：一步读出来的其实是'中点'的瞬时值】")
print(f"  利润是条下弯的曲线。在 p=10 涨满 1 块，读到 {(profit(11) - profit(10)):.0f}；")
print(f"  而 10 那一点的瞬时值是 {central(profit, 10, 0.001):.1f}，11 那一点是 {central(profit, 11, 0.001):.1f}。")
print(f"  答案在中间：10.5 那一点的瞬时值正好是 {central(profit, 10.5, 0.001):.1f}。")
print("  换个弯得更厉害的函数（f = e^x，在 x=2 处真导数 = e² = %.4f）：" % math.exp(2))
print("    步长      往前读        误差        两侧平均读      误差")
true_d = math.exp(2)
for h in [1.0, 0.5, 0.25, 0.125, 0.0625]:
    f_err = abs(forward(math.exp, 2, h) - true_d) / true_d * 100
    c_err = abs(central(math.exp, 2, h) - true_d) / true_d * 100
    print(f"    {h:<8.4f}  {forward(math.exp, 2, h):>8.4f}  {f_err:>8.1f}%   {central(math.exp, 2, h):>9.4f}  {c_err:>7.2f}%")
print("  步长减半：往前读的错减半，两侧平均读的错减到四分之一。")
print("  往前读是'一阶准'，两侧平均读是'二阶准'。多算一次调用，换来的是阶数。")

print()
print("【第四部分：泰勒展开——误差就是你扔掉的第一项】")
print("  e^x ≈ 1 + x + x²/2 + x³/6（尾巴一项比一项小，扔掉就有误差）")
print("    x        真值        1+x       差        1+x+x²/2      差")
for x in [0.01, 0.04, 0.1, 0.3, 0.5, 1.0]:
    truth = math.exp(x)
    one = 1 + x
    two = 1 + x + x * x / 2
    print(f"  {x:>6.2f}  {truth:>10.6f}  {one:>8.4f}  {truth - one:>+9.6f}   {two:>10.6f}  {truth - two:>+10.6f}")
print(f"  x=0.04 那一行：扔掉的第一项是 x²/2 = {0.04 ** 2 / 2:.6f}，实测误差 {math.exp(0.04) - 1.04:.6f}。")
print("  泰勒展开替你回答的问题只有一个：我用这个好算的式子代替那个难算的，会错多少？")
print("  答案不用重新推导，看一眼你扔掉的第一项有多大就够了。")

print()
print("【第五部分：二阶项不是学术点缀，它决定你属于哪一半】")
print("  先用第四部分那套读一下 ln(1+r)：它的前两项是 r − r²/2。")
print(f"    r=0.1：真值 {math.log(1.1):.6f}，r − r²/2 = {0.1 - 0.1 ** 2 / 2:.6f}，差 {math.log(1.1) - (0.1 - 0.1 ** 2 / 2):+.6f}（就是下一项 r³/3 = {0.1 ** 3 / 3:.6f}）")
print("  一笔钱 100，投 250 天，每天的平均涨跌是 0（不赚不赔的赌局），单日起伏 10%。")
print("  只按一阶想（把平均乘起来）：250 天后还是 100，结论是'不亏不赚'。")
random.seed(7)
ends = []
for _ in range(10000):
    v = 100.0
    for _ in range(250):
        v *= 1 + random.gauss(0, 0.10)
    ends.append(v)
ends.sort()
med = ends[len(ends) // 2]
below = sum(1 for e in ends if e < 100) / len(ends) * 100
theory = 100 * math.exp(-0.10 ** 2 * 250 / 2)
print(f"  实测（一万遍）：平均 {sum(ends) / len(ends):.1f}，中位 {med:.1f}，{below:.1f}% 的路径低于起点")
print(f"  二阶项给的预测：中位 ≈ 100 × e^(−250 × 0.10²/2) = 100 × e^(−1.25) = {theory:.1f}")
print(f"  平均那一行的诚实话：真值是 100，实测 {sum(ends) / len(ends):.1f}，因为这个平均自己的毛边就有 ±{spread(ends) / math.sqrt(len(ends)):.1f}（少数路径能翻好几倍，第 08 课那个厚尾毛病）")
print("  平均（一阶）说没事，中位（含二阶）说多数人亏钱。差的就是 −σ²T/2 那一项，")
print("  也就是第 10 课那个'波动拖累'——它不是新规矩，就是 e^x 那一行的第二项。")

print()
print("【第六部分：两种误差，只有一种能用算力买掉】")
MU, SD, DAYS = 0.004, 0.03, 30
print("  模型：每天乘 (1 + 平均 0.4% 起伏 3%)，看 30 天后终值的平均。")
print("  偷懒：把 30 天当一步，直接算 100 × (1 + 30×0.004)。")
truth_exact = 100 * (1 + MU) ** DAYS
one_step = 100 * (1 + DAYS * MU)
bias_one = one_step - truth_exact
print(f"  真值（精确算法）：{truth_exact:.2f}")
print(f"  一步近似      ：{one_step:.2f}  偏差 {bias_one:+.2f}（确定性的，跑多少遍都不会动）")
print("  把 30 天切成几段，每一段都用同样的偷懒法：")
for m in [1, 2, 4, 8, 16]:
    seg = 1 + (DAYS / m) * MU
    v = 100 * seg ** m
    print(f"    切 {m:>2} 段：{v:>7.2f}  偏差 {v - truth_exact:+.3f}")
print("  段数翻倍、偏差减半——一阶准。把第二项加回去（1 + x + x²/2，x=0.12）：")
two_order = 100 * (1 + DAYS * MU + (DAYS * MU) ** 2 / 2)
print(f"    {two_order:.2f}  偏差 {two_order - truth_exact:+.3f}——一次修正顶得上切几十段。")
print()
print("  再把它跑成模拟，看毛边随次数怎么变（真值同上）：")
for runs in [2000, 20000, 200000]:
    random.seed(7)
    vals = []
    for _ in range(runs):
        v = 100.0
        for _ in range(DAYS):
            v *= 1 + random.gauss(MU, SD)
        vals.append(v)
    est = sum(vals) / len(vals)
    se = spread(vals) / math.sqrt(runs)
    print(f"    {runs:>6} 遍：估计 {est:.2f} ± {se:.2f}（毛边）；近似偏差仍是 {bias_one:+.2f}")
print(f"  二十万遍时毛边已经比偏差小：此后总误差由那个 {abs(bias_one):.2f} 说了算，多加算力白加。")

print()
print("【第七部分：练习核对】")
print("  练习一：p=11 与 p=12 各涨一块；从 13 连涨两块到 15 一共值多少")
for p in [11, 12]:
    print(f"    p={p}：利润 {profit(p):.0f} → {profit(p + 1):.0f}，多一块值 {profit(p + 1) - profit(p):+.0f}")
print(f"    p=13 → p=15：利润 {profit(13):.0f} → {profit(15):.0f}，一共 {profit(15) - profit(13):+.0f}")
print(f"  练习二：x=0.1 → e^0.1 = {math.exp(0.1):.5f}；1+x = {1.1:.5f}；1+x+x²/2 = {1 + 0.1 + 0.005:.5f}")
print(f"    扔掉的第一项 x²/2 = {0.1 ** 2 / 2:.5f}，下一项 x³/6 = {0.1 ** 3 / 6:.6f}")
print("  练习三：f(99)=12.0、f(100)=15.8、f(101)=20.0 → 前向 %.1f、中心 %.1f、二阶导 %+.1f"
      % (20.0 - 15.8, (20.0 - 12.0) / 2, 20.0 - 2 * 15.8 + 12.0))
MU3, T3 = 0.005, 60
simple = 100 * (1 + T3 * MU3)
compound = 100 * (1 + MU3) ** T3
x3 = T3 * MU3
print(f"  练习四：100 块、60 天、日均 {MU3:.1%}。单利省事报 {simple:.2f}，复利真值 {compound:.2f}，差 {compound - simple:+.2f}")
print(f"    用扔掉的第一项预估：x = {x3:.2f}，x²/2 = {x3 ** 2 / 2:.5f}（即 {x3 ** 2 / 2 * 100:.2f} 块）；再加 x³/6 = {x3 ** 3 / 6:.5f} 合计 {x3 ** 2 / 2 * 100 + x3 ** 3 / 6 * 100:.2f} 块")
MU2, SD2 = 0.003, 0.06
print(f"  练习五：日均 +0.3%、起伏 6%、250 天。二阶近似中位 ≈ 100 × e^(250×({MU2} − 0.06²/2)) = "
      f"{100 * math.exp(250 * (MU2 - SD2 ** 2 / 2)):.1f}")
print(f"    平均的理论值：100 × 1.003^250 = {100 * 1.003 ** 250:.1f}")
random.seed(7)
ends5 = []
for _ in range(10000):
    v = 100.0
    for _ in range(250):
        v *= 1 + random.gauss(MU2, SD2)
    ends5.append(v)
ends5.sort()
below5 = sum(1 for e in ends5 if e < 100) / len(ends5) * 100
print(f"    实测（一万遍）：平均 {sum(ends5) / len(ends5):.1f} ± 毛边 {spread(ends5) / math.sqrt(len(ends5)):.1f}，"
      f"中位 {ends5[len(ends5) // 2]:.1f}，{below5:.1f}% 的路径低于起点")
