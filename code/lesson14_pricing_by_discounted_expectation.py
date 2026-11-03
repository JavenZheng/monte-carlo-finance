"""定价 = 把未来的每一笔钱按可能性加权，再折回今天。

第一部分：今天的 100 块和明年的 100 块不是同一个数（折现）。
第二部分：把可能性也加权进去：期望折现，并用模拟核对。
第三部分：复制——为什么定价不听你心里的概率（一张两档的表）。
第四部分：原书的正主：一份"锁价权利"值多少钱，模拟价对上了公式价。
第五部分：把"你预期的涨幅"塞进定价会得到什么数。
第六部分：路径依赖的合同：必须一天一天演，顺带看步长带来的偏差（第 13 课）。
第七部分：把第 12 课的控制变量用在这个定价上。
第八部分：练习核对。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random

S0 = 100.0     # 今天的价
R = 0.05       # 无风险利率（一年）
SIGMA = 0.20   # 年化起伏


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black_scholes(s, k, r, sigma, t):
    d1 = (math.log(s / k) + (r + sigma ** 2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def sim_terminal(runs, drift, sigma, t, strike):
    """只看最后一天：GBM 的终值是一次抽签，payoff 折回今天。"""
    out = []
    for _ in range(runs):
        z = random.gauss(0, 1)
        st = S0 * math.exp((drift - sigma ** 2 / 2) * t + sigma * math.sqrt(t) * z)
        out.append(math.exp(-R * t) * max(st - strike, 0))
    return out


def sim_terminal_and_underlying(runs, drift, sigma, t, strike):
    """同上，但把到期价本身也留着当辅助量。"""
    pay = []
    und = []
    for _ in range(runs):
        z = random.gauss(0, 1)
        st = S0 * math.exp((drift - sigma ** 2 / 2) * t + sigma * math.sqrt(t) * z)
        pay.append(math.exp(-R * t) * max(st - strike, 0))
        und.append(st)
    return pay, und


def sim_path(steps, runs, drift, sigma, t, barrier, payout):
    """一天一天演：整条路径最低点不低于 barrier 才赔付。返回 (定价, 毛边)。"""
    dt = t / steps
    vals = []
    for _ in range(runs):
        s = S0
        low = s
        for _ in range(steps):
            s *= math.exp((drift - sigma ** 2 / 2) * dt + sigma * math.sqrt(dt) * random.gauss(0, 1))
            if s < low:
                low = s
        vals.append(math.exp(-R * t) * payout if low >= barrier else 0.0)
    return sum(vals) / len(vals), spread(vals) / math.sqrt(len(vals))


print("【第一部分：今天的钱和明年的钱不是同一个数】")
print("  一笔钱放在 T 年后，今天的等价 = 未来那笔 ÷ (1+r)^T")
print("    金额    1 年后      2 年后      5 年后")
for r in [0.03, 0.05, 0.08]:
    row = [10000 / (1 + r) ** T for T in [1, 2, 5]]
    print(f"  利率 {r:.0%}  " + "  ".join(f"{v:>8.0f}" for v in row))
print("  一年一付和一月一付也不一样：每月 25 块、连发 12 个月，按年利率 5% 摊成月利率 0.417% 折：")
mr = 0.05 / 12
pv = sum(25 / (1 + mr) ** m for m in range(1, 13))
print(f"    名义一共 {25 * 12} 块，折回今天是 {pv:.1f} 块；如果一次拖到年底才付，只值 {300 / 1.05:.1f} 块")
print(f"    早拿到这件事值 {pv - 300 / 1.05:.1f} 块")
print("  → 折现这件事替你回答的问题：**未来那一笔钱，今天该按几块记账。**")

print()
print("【第二部分：把可能性也加权进去】")
print("  新项目：明年有六成概率回 12 万，四成概率只回 4 万。无风险利率 5%。")
p_low, pv_low, pv_high = 0.4, 4.0, 12.0
exp_pay = (1 - p_low) * pv_high + p_low * pv_low
print(f"  第 06 课的期望：E = 0.6 × 12 + 0.4 × 4 = {exp_pay:.1f} 万")
print(f"  折回今天：{exp_pay:.1f} ÷ 1.05 = {exp_pay / 1.05:.3f} 万")
random.seed(7)
draws = [pv_high if random.random() < 0.6 else pv_low for _ in range(20000)]
mean = sum(draws) / len(draws)
se = spread(draws) / math.sqrt(len(draws))
print(f"  模拟两万遍核对：平均 {mean:.3f} 万 ± 毛边 {se:.3f} 万（第 07 课那台机器）")
print("  → **定价 = 折现 × 期望**，两件事各管一半：折现管时间，期望管不确定。")

print()
print("【第三部分：为什么定价不听你心里的概率】")
print("  一张合同：某股票今天 100，明年要么涨 30%（变 130）要么跌 30%（变 70）。")
print("  合同写：涨到 130 付你 30，跌到 70 一分不给。")
up, dn, pay_up, pay_dn = 130.0, 70.0, 30.0, 0.0
delta = (pay_up - pay_dn) / (up - dn)
cash = (up * pay_dn - dn * pay_up) / (up - dn) / (1 + R)   # 负数表示借入
borrowed = -cash
owed_mature = borrowed * (1 + R)
replica = delta * S0 + cash
print(f"  复制它只需两笔：买 {delta:.2f} 股（花 {delta * S0:.2f} 元），同时借入 {borrowed:.2f} 元，到期连本带利还 {owed_mature:.2f} 元。")
print(f"  到期核对：涨到 130 → {delta:.2f}×130 − {owed_mature:.2f} = {delta * up - owed_mature:.2f}；跌到 70 → {delta:.2f}×70 − {owed_mature:.2f} = {delta * dn - owed_mature:.2f}")
print(f"  这套拼法今天的成本 = {delta:.2f}×100 − {borrowed:.2f} = {replica:.3f} 元")
print()
print(f"  你心里觉得涨的概率是 60%，于是你会报：(0.6×30 + 0.4×0) ÷ 1.05 = "
      f"{(0.6 * pay_up + 0.4 * pay_dn) / (1 + R):.3f}")
q = ((1 + R) - dn / S0) / ((up - dn) / S0)
print(f"  而市场那个拼法隐含的概率是 q = (1.05 − 0.70) ÷ (1.30 − 0.70) = {q:.4f}，不是你的 0.60")
print(f"  用 q 算回来：({q:.4f}×30) ÷ 1.05 = {q * pay_up / (1 + R):.3f}——和复制成本是同一个数")
gap = (0.6 * pay_up) / (1 + R) - replica
print(f"  你的报价比复制成本高 {gap:+.3f} 元：谁肯按 17.14 卖，别人花 {replica:.2f} 拼一份就能白拿这 {gap:.2f} 元，所以这个价在市场上留不住。")
print("  → 定价的正确问法不是'我觉得多大概率会涨'，而是'**要拼出这笔赔付，今天得花几块**'。")

print()
print("【第四部分：一份锁价权利值多少钱（模拟对上公式）】")
print(f"  条件：今天价 {S0:.0f}、行权价 {S0:.0f}、年化起伏 {SIGMA:.0%}、一年期、无风险利率 {R:.0%}。")
print("  赔付 = max(到期价 − 100, 0)，折回今天。")
for runs in [2000, 20000, 200000]:
    random.seed(7)
    vals = sim_terminal(runs, R, SIGMA, 1.0, S0)
    m_ = sum(vals) / len(vals)
    print(f"    {runs:>6} 遍：定价 {m_:.2f} ± 毛边 {spread(vals) / math.sqrt(runs):.2f}")
bs = black_scholes(S0, S0, R, SIGMA, 1.0)
print(f"  公式给的价格（进阶框那条）：{bs:.4f}")
print(f"  两种折现口径：连续复利 e^(-0.05) = {math.exp(-R):.4f}，一年一结 1/1.05 = {1 / (1 + R):.4f}，"
      f"差 {1 / (1 + R) - math.exp(-R):.4f}")
print("  → 这就是原书第 1 章说的：价格是那个期望，而期望算不出来时就用蒙特卡洛去抽。")

print()
print("【第五部分：把'你预期的涨幅'塞进去会得到什么数】")
prices = {}
for drift, tag in [(0.0, "你预期它一年纹丝不动"), (R, "风险中性口径（该用的）"),
                   (0.12, "你预期一年涨 12%"), (0.20, "你预期一年涨 20%")]:
    random.seed(7)
    vals = sim_terminal(200000, drift, SIGMA, 1.0, S0)
    m_ = sum(vals) / len(vals)
    prices[drift] = m_
    print(f"    预期涨幅 {drift:.0%}：{tag} → 报出 {m_:.2f}")
print(f"  同一份合同，只因为换了'你预期的涨幅'，报价从 {prices[0.0]:.2f} 一路走到 {prices[0.20]:.2f}"
      f"（{prices[0.20] / prices[0.0]:.1f} 倍）。")
print("  而第三节那张两档表已经告诉你：市场按复制成本成交，不按你的预期成交。")
print("  风险中性那套口径的意思就是——**把预期的那一格换成无风险利率，让复制关系成立。**")

print()
print("【第六部分：路径依赖的合同，只能一天一天演】")
print("  合同：一年内这条价格曲线最低点不低于 85，年底付你 10 块；碰到 85 以下就一分不给。")
step_prices = {}
for steps in [125, 250, 500]:
    random.seed(7)
    v, e = sim_path(steps, 20000, R, SIGMA, 1.0, 85.0, 10.0)
    step_prices[steps] = (v, e)
    print(f"    一年切 {steps:>3} 步：定价 {v:.3f} ± 毛边 {e:.3f}")
diff = step_prices[125][0] - step_prices[500][0]
diff_se = math.sqrt(step_prices[125][1] ** 2 + step_prices[500][1] ** 2)
print(f"  步数越细、报价越低——因为你只在自己算的那几个时刻去看价格，中间漏掉的下跌看不见。")
print(f"  125 步到 500 步差了 {diff:.3f}，而这个差的抽样毛边只有 ±{diff_se:.3f}：这段差不是运气，是步长。")
print("  这正是第 13 课那个离散化偏差：它不随模拟次数下降，只随步长变化。")
random.seed(7)
p100k, e100k = sim_path(250, 100000, R, SIGMA, 1.0, 85.0, 10.0)
print(f"  同样 250 步（近似误差一样），只加次数：两万遍 {step_prices[250][0]:.3f} ± {step_prices[250][1]:.3f}，"
      f"十万遍 {p100k:.3f} ± {e100k:.3f}")
print(f"  次数加五倍，毛边只缩到 {e100k / step_prices[250][1]:.2f} 倍——正好是 1/√5 = {1 / math.sqrt(5):.2f}；"
      f"而'步子太粗'带来的那一段偏差一分不动，要修它只能加步数。")

print()
print("【第七部分：第 12 课那招在这里真能用上】")
print("  辅助量取'到期价本身'：它的平均值不用模拟就知道，是 100 × e^0.05 = "
      f"{100 * math.exp(R):.3f}。")
random.seed(7)
pay, und = sim_terminal_and_underlying(200000, R, SIGMA, 1.0, S0)
n = len(pay)
mp = sum(pay) / n
mu = sum(und) / n
sp = spread(pay)
su = spread(und)
cov = sum((a - mp) * (b - mu) for a, b in zip(pay, und)) / (n - 1)
rho = cov / (sp * su)
a_star = cov / (su ** 2)
adj = [p - a_star * (u - 100 * math.exp(R)) for p, u in zip(pay, und)]
print(f"    赔付与到期价的相关：{rho:.3f}；最优系数 a = {a_star:.3f}")
print(f"    不用辅助量：{mp:.3f} ± 毛边 {sp / math.sqrt(n):.3f}")
print(f"    用辅助量校正：{sum(adj) / n:.3f} ± 毛边 {spread(adj) / math.sqrt(n):.3f}")
print(f"    毛边降到 {(spread(adj) / sp) * 100:.0f}%，理论 √(1−ρ²) = {math.sqrt(1 - rho ** 2) * 100:.0f}%")
print(f"    公式价 {bs:.3f}：校正后的估计离它 {abs(sum(adj) / n - bs):.3f}，原来的估计离它 {abs(mp - bs):.3f}")

print()
print("【第八部分：练习核对】")
print("  练习一：三年后 5 万、年利率 4% → 现值 "
      f"{50000 / 1.04 ** 3:,.0f} 元；名义 50000 打的是 {50000 / 1.04 ** 3 / 50000:.1%}")
print("  练习二：0.7×9 + 0.3×2 = "
      f"{0.7 * 9 + 0.3 * 2:.1f} 万，除以 1.05 → {(0.7 * 9 + 0.3 * 2) / 1.05:.3f} 万")
u2, d2_, p2 = 120.0, 80.0, 25.0
dl = (p2 - 0) / (u2 - d2_)
bo = (u2 * 0 - d2_ * p2) / (u2 - d2_) / (1 + R)
print(f"  练习三：涨 120 付 25、跌 80 付 0 → 买 {dl:.3f} 股、借 {abs(bo):.2f}，复制成本 {dl * S0 - abs(bo):.3f}；"
      f"隐含概率 q = {((1 + R) - d2_ / S0) / ((u2 - d2_) / S0):.4f}")
print(f"    核对低档：0.625 股到期值 {dl * d2_:.1f}，今天借入 {dl * d2_ / (1 + R):.2f}；"
      f"高档 {dl * u2:.1f} − {dl * d2_:.1f} = {dl * (u2 - d2_):.1f}")
wrong = ((1 + R) - d2_) / (u2 - d2_)
print(f"    常见错误：拿绝对价去套公式 → (1.05 − 80) ÷ (120 − 80) = {wrong:.2f}，一个负概率")
bs110 = black_scholes(S0, 110, R, SIGMA, 1.0)
print("  练习四：行权价改成 110（其余不变）的公式价 → "
      f"{bs110:.3f}；模拟二十万遍核对（种子 7）：")
random.seed(7)
v110 = sim_terminal(200000, R, SIGMA, 1.0, 110.0)
m110, e110 = sum(v110) / len(v110), spread(v110) / math.sqrt(len(v110))
print(f"    {m110:.3f} ± {e110:.3f}；离公式 {abs(m110 - bs110):.2f}，"
      f"是毛边的 {abs(m110 - bs110) / e110:.1f} 倍")
print("  练习五：同一份保底合同，一年只按月看 12 次、按周看 52 次（两万遍）：")
coarse = {}
for steps in [12, 52]:
    random.seed(7)
    v, e = sim_path(steps, 20000, R, SIGMA, 1.0, 85.0, 10.0)
    coarse[steps] = v
    print(f"    一年看 {steps:>2} 次：定价 {v:.3f} ± 毛边 {e:.3f}")
print(f"    对照第六部分：一年看 500 次是 {step_prices[500][0]:.2f}；"
      f"看 12 次比看 500 次贵出 {coarse[12] - step_prices[500][0]:.2f}")
