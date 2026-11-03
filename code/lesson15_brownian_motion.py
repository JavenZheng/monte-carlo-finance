"""连续却处处不可导：把布朗运动摸出数感。

第一部分：把一分钟切成几段，终点分布不变，但路径越来越抖（第 08 课中心极限定理的又一次现身）。
第二部分：路径的"抖"有两种量法：一种按步长归零，一种不但不归零还收敛到一个固定的数。
第三部分：问"这一瞬间涨多快"——步子越小读数越大，永远不停下来（对照第 13 课 e^x 会收敛）。
第四部分：把窗口缩小，幅度只按根号缩：放大多少倍都还是抖，找不到一段是直的。
第五部分：醉汉回家：几乎一定会回来，但"平均要多久"这个数买不起。
第六部分：期末在哪 vs 途中跌破过没有——途中那一档的概率正好是期末的两倍。
第七部分：你多久看一眼，决定你漏掉多少跌破（回接第 14 课那张步长表）。
第八部分：练习核对。
浏览器里打开 https://jupyter.org/try 整段粘进去也能跑。
"""

import math
import random


def spread(vals):
    n = len(vals)
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def bm(steps):
    """一条 [0, 1] 上的布朗路径（用 steps 段近似），返回每一段的增量。"""
    return [random.gauss(0, math.sqrt(1.0 / steps)) for _ in range(steps)]


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


print("【第一部分：切成几段，终点不变，路径变抖】")
print("  一分钟的价格从 0 出发走到结束；把它切成 n 段，每段的起伏按 1/√n 缩。")
for n, runs in [(10, 40000), (100, 40000), (1000, 4000)]:
    random.seed(7)
    ends, highs = [], []
    for _ in range(runs):
        d = bm(n)
        ends.append(sum(d))
        pos, hi = 0.0, 0.0
        for x in d:
            pos += x
            if pos > hi:
                hi = pos
        highs.append(hi)
    print(f"    n = {n:>5}：终点 平均 {sum(ends) / len(ends):+.3f}、起伏 {spread(ends):.3f}"
          f"（理论 0 与 1.000）；  路上最高点 平均 {sum(highs) / len(highs):.3f}"
          f"（段数拉到连续时是 0.798）")
print("  → 终点那一格永远是同一个分布（第 08 课）；变的是中间：段数越多，路上越高越抖。")
print("    终点你算得准，路上发生了什么你一点都不知道。")

print()
print("【第二部分：'抖'有两种量法，一种归零，一种不归零】")
print("  把每条路上的起伏加起来（总长度），再把平方加起来（二次变差），各演两百条取平均：")
qv_mean = {}
for n in [100, 1000, 10000]:
    random.seed(7)
    tot, qv = [], []
    for _ in range(200):
        d = bm(n)
        tot.append(sum(abs(x) for x in d))
        qv.append(sum(x * x for x in d))
    qv_mean[n] = sum(qv) / len(qv)
    print(f"    切 {n:>5} 段：总长度 平均 {sum(tot) / len(tot):6.2f}；   平方和 平均 {qv_mean[n]:.3f}"
          f"（理论 1.000）")
print("  → 总长度随段数变多一路涨（永不收敛，所以'这条路多长'没有答案）；")
print("    平方和却不跟着步长消失，稳定在 1，也就是时间 T。这一条是 Itô 那一项的来源，")
print("    也是第 10 课、第 13 课、第 14 课三次出现的那个 σ²/2 的出处。")

print()
print("【第三部分：'这一瞬间涨多快'有没有答案？】")
print("  在 t=0.5 处问斜率 (W(0.5+h) − W(0.5)) / h，每档步长演两万遍，取绝对值的平均：")
print("      步长 h     斜率平均绝对值     乘上 √h 之后     理论 √(2/π) = 0.798")
for k in range(1, 8):
    h = 2.0 ** -k
    random.seed(7)
    slopes = [abs(random.gauss(0, math.sqrt(h))) / h for _ in range(20000)]
    m_ = sum(slopes) / len(slopes)
    print(f"    {h:.5f}     {m_:>10.3f}          {m_ * math.sqrt(h):>7.3f}")
print("  → 第 13 课里 e^x 的读数随步长收敛到 7.3891；这里的读数随步长一路往上涨，")
print("    涨的速率是 1/√h——步子减半、读数乘 1.41。它不收敛，所以'这一瞬间多快'没有答案。")

print()
print("【第四部分：窗口缩一半，幅度只除以 1.41——放大多少倍都还是抖】")
print("  在一段长度为 t 的时间里，最高点减最低点（这段路的幅度）平均多大：")
amp = {}
for t in [1.0, 0.5, 0.25, 0.125, 0.0625]:
    random.seed(7)
    ranges = []
    for _ in range(4000):
        pos, hi, lo = 0.0, 0.0, 0.0
        for x in bm(200):
            pos += x * math.sqrt(t)
            if pos > hi:
                hi = pos
            if pos < lo:
                lo = pos
        ranges.append(hi - lo)
    amp[t] = sum(ranges) / len(ranges)
keys = [1.0, 0.5, 0.25, 0.125, 0.0625]
for i, t in enumerate(keys):
    ratio = "" if i == 0 else f"    上一档是本档的 {amp[keys[i - 1]] / amp[t]:.3f} 倍"
    print(f"    窗口 {t:.4f}：幅度平均 {amp[t]:.3f}{ratio}")
print(f"  → 时间缩一半，幅度只除以 √2 = 1.414（实测 {amp[1.0] / amp[0.5]:.3f}、"
      f"{amp[0.5] / amp[0.25]:.3f}、{amp[0.25] / amp[0.125]:.3f}、{amp[0.125] / amp[0.0625]:.3f}）。")
print("  → 永远找不到'小到看起来是直的'那一档：这条路在任意尺度上一样抖（自相似）。")

print()
print("【第五部分：醉汉回家——一定回，但等不起】")
print("  一维醉汉每步向左向右各一半概率。看他多少步之内回到出发的那个路口：")
for cap, runs in [(100, 20000), (500, 20000), (2000, 8000), (10000, 3000)]:
    random.seed(7)
    back, times = 0, []
    for _ in range(runs):
        pos = 0
        for step in range(1, cap + 1):
            pos += 1 if random.random() < 0.5 else -1
            if pos == 0:
                back += 1
                times.append(step)
                break
    med = sorted(times)[len(times) // 2]
    theory = 1 - math.comb(2 * (cap // 2), cap // 2) / 2 ** (2 * (cap // 2))
    print(f"    最多等 {cap:>6} 步：回来的占 {back / runs * 100:.1f}%（理论 {theory * 100:.1f}%）；"
          f"回来的中位步数 {med:>5}；平均步数（截在这个上限）{sum(times) / len(times):>8.0f}")
print("  → 上限放大，回来的比例往 1 走（一维醉汉几乎一定会回家）；")
print("    但'平均多少步'跟着上限一起涨：这个平均不存在。第 05 课那个厚尾毛病的最凶版本。")

print()
print("【第六部分：期末在哪 vs 途中跌破过没有】")
print("  一万条路径，每条切 500 段（起点 0）。既看期末值，也看途中最低点：")
a, n, runs = 0.5, 500, 10000
random.seed(7)
finals, mins = [], []
for _ in range(runs):
    pos, lo = 0.0, 0.0
    for x in bm(n):
        pos += x
        if pos < lo:
            lo = pos
    finals.append(pos)
    mins.append(lo)
p_fin = sum(1 for v in finals if v <= -a) / runs
p_min = sum(1 for v in mins if v <= -a) / runs
stay = [m for f, m in zip(finals, mins) if abs(f) <= 0.2]
print(f"    期末 ≤ −{a}：{p_fin * 100:.1f}%（钟形表给 {norm_cdf(-a) * 100:.1f}%）；"
      f"   途中最低 ≤ −{a}：{p_min * 100:.1f}%（两倍应是 {2 * norm_cdf(-a) * 100:.1f}%）；"
      f"   倍数 {p_min / p_fin:.2f}")
print(f"    '期末没走远'（|期末| ≤ 0.2）的那些路径里，途中跌破 −{a} 的占 {sum(1 for m in stay if m <= -a) / len(stay) * 100:.1f}%")
print("  → 途中跌破过的概率正好是期末低于那档的两倍（反射原理，进阶框给式子）。")
print(f"    实测倍数不到 2.00 是因为这条路由 500 段近似，中间漏掉的下跌看不见——这正是第七部分要量的那件事。")
print("    第 14 课那份保底合同的道理全在这一行里：'期末没跌破'从来不代表'路上没跌破过'。")

print()
print("【第七部分：你多久看一眼，决定你漏掉多少跌破】")
print("  同样的路（切 1000 段当成'真实最低'），只在你看得到的那几个时刻检查有没有跌破 −0.5：")
nfine, runs2 = 1000, 8000
watches = [4, 12, 52, 250, 1000]
random.seed(7)
truth = 0
seen = {w: 0 for w in watches}
for _ in range(runs2):
    pos = 0.0
    vals = [0.0]
    for x in bm(nfine):
        pos += x
        vals.append(pos)
    if min(vals) <= -a:
        truth += 1
    for w in watches:
        marks = vals[::nfine // w]
        if min(marks) <= -a:
            seen[w] += 1
base = truth / runs2
print(f"    每段都看（1000 次）算真值：跌破过的占 {base * 100:.1f}%"
      f"（这条路连续地看是 {2 * norm_cdf(-a) * 100:.1f}%，连 1000 段都还漏 {(2 * norm_cdf(-a) - base) * 100:.1f} 个百分点）")
for w in watches:
    print(f"    一年看 {w:>4} 次：你看到的跌破 {seen[w] / runs2 * 100:.1f}%"
          f"（漏了 {(base - seen[w] / runs2) * 100:.1f} 个百分点）")
print("  → 看的人越少，'跌破'越像没发生，那份保底合同就越贵。第 14 课那张表")
print("    （12 次 6.821、500 次 6.134）就是这么来的：粗步长不是算得慢一点，是算错了方向。")

print()
print("【第八部分：练习核对】")
random.seed(7)
d100 = bm(100)
print(f"  练习一：切 100 段的一条路径，平方和 = {sum(x * x for x in d100):.3f}；"
      f"同一切法演两百条的平均 = {qv_mean[100]:.3f}；切 10000 段的平均 = {qv_mean[10000]:.3f}（理论都是 1.000）")
h = 0.01
random.seed(7)
sl = [abs(random.gauss(0, math.sqrt(h))) / h for _ in range(20000)]
print(f"  练习二：h = 0.01 时斜率平均绝对值 = {sum(sl) / len(sl):.3f}，"
      f"理论 0.798/√h = {0.7978845608 / math.sqrt(h):.3f}；"
      f"h 减半到 0.005 时读数应乘 √2 = {math.sqrt(2):.3f}")
print(f"  练习三：整段（窗口 1.0）幅度实测 {amp[1.0]:.3f}，窗口 1/16 实测 {amp[0.0625]:.3f}；"
      f"1/√16 = {1 / 4:.3f}，实测比值 {amp[0.0625] / amp[1.0]:.3f}")
p1 = sum(1 for v in finals if v <= -1.0) / runs
m1 = sum(1 for v in mins if v <= -1.0) / runs
print(f"  练习四：把线改成 −1.0 → 期末 ≤ −1.0 占 {p1 * 100:.1f}%，"
      f"途中最低 ≤ −1.0 占 {m1 * 100:.1f}%，倍数 {m1 / p1:.2f}"
      f"（钟形表给期末 15.9%、两倍是 31.7%）")
print("  练习五：一笔钱投 250 个交易日、日均 0、单日起伏 2%（一万遍，看的是累计涨跌幅）：")
random.seed(7)
days, sd, runs5 = 250, 0.02, 10000
no_loss, never_5, never_10, both = 0, 0, 0, 0
for _ in range(runs5):
    pos, lo = 0.0, 0.0
    for _ in range(days):
        pos += random.gauss(-sd * sd / 2, sd)
        if pos < lo:
            lo = pos
    if pos >= 0:
        no_loss += 1
        if lo >= -0.05:
            both += 1
    if lo >= -0.05:
        never_5 += 1
    if lo >= -0.10:
        never_10 += 1
print(f"    期末不亏（累计涨跌幅 ≥ 0）：{no_loss / runs5 * 100:.1f}%；"
      f"全年从没跌破 −5%：{never_5 / runs5 * 100:.1f}%；从没跌破 −10%：{never_10 / runs5 * 100:.1f}%")
print(f"    '期末不亏'的这些人里，全年从没跌破 −5% 的只有 {both / no_loss * 100:.1f}%"
      f"（其余 {(1 - both / no_loss) * 100:.1f}% 中途跌破过）")
print(f"    为什么'不亏'不到一半：日均 0 说的是简单收益，对数口径每年被波动拖累扣掉 "
      f"{sd * sd / 2 * days * 100:.1f}%（第 10 课那个 σ²/2）；"
      f"按钟形表算期末 ≥ 0 的概率是 "
      f"{(1 - norm_cdf(sd * sd / 2 * days / (sd * math.sqrt(days)))) * 100:.1f}%")
