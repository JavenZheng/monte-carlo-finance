# 蒙特卡洛与金融工程 · 零基础职场人版

**系列**：`quant-for-office-workers` ｜ **仓库**：`monte-carlo-finance`

一门写给**不写代码、没学过概率统计、金融术语也不懂**的职场人的课程。目标是把你带到能独立翻开
Paul Glasserman 的 *Monte Carlo Methods in Financial Engineering*（Springer, 2003）而不至于在第 3 页放弃。原书共 9 章、三个部分，外加三个附录；章节页码见 [原书章节索引](docs/book-index.md)。

> **状态**：第一期（15 课）**正文已全部写完** ✅ ｜ M-1 工具模块（01–04）✅ ｜ M0 数学与金融必备（05–15）✅ ｜ 第 04–15 课已配图（14 张，全部脚本生成）✅ ｜ 代码块数字全库逐行复核 ✅ ｜ 术语表与 15 张备忘卡已对齐 ✅ ｜ 配套浏览器 notebook：15 课全部就绪（每格的真实输出已嵌入文件）｜ **第一期已开源**；第二期（原书第 2–9 章）仍在规划

---

## 终点承诺

第一期结束时，你能够：

1. 在浏览器里用约 20 行 Python 模拟出一个不确定量的估计值；
2. **报出你的误差、解释它为什么是这个大小**，并区分"飘"（方差）与"偏"（偏差）；
3. 翻开原书第 1、2 章，认出每个符号，说清它在做什么，不再当天书读。

我们**不**承诺"从零到精通金融工程"。这门课的天花板是 **能算 + 能跑 + 能看懂原书在做什么**——严格证明一律放进【进阶框】，明确标注可跳过。

---

## 你的日常就是课件

这门课不用教科书语言开场。用的是一天班之后你真的会碰到的事：中午点的那单外卖要等多久、要不要充那个 200 块的会员、地铁早退 5 分钟晚到 20 分钟、月底那点工资怎么安排、自己那个不温不火的新媒体账号下一条能不能爆。

复杂概念先在生活里站稳，再上符号。

---

## 第一期路线图

### M-1 工具 · 让不写代码的人跑起第一个模拟（第 01–04 课）

| # | 课名 | 一句话 |
|---|---|---|
| **01** | **[六张便利贴：你其实已经会做蒙特卡洛了](docs/m1-tooling/01-six-sticky-notes.md)** ✅ | 不碰电脑，用便利贴做一次真模拟 |
| 02 | **[浏览器里的第一行代码](docs/m1-tooling/02-first-line-in-the-browser.md)** ✅ | print、变量、算式——零安装，做出一个改数就重算的账格子 |
| 03 | **[够用就好的三样](docs/m1-tooling/03-three-things-enough.md)** ✅ | 列表、循环、函数，用一周的午餐记录讲通 |
| 04 | **[你的第一个真模拟](docs/m1-tooling/04-your-first-real-simulation.md)** ✅ | 随机数、种子、造一个还没发生过的月并取平均 |

### M0 数学与金融最小必备（第 05–15 课）

| # | 课名 | 对应原书 |
|---|---|---|
| 05 | **[为什么"平均值"会骗你](docs/m0-foundations/05-why-the-average-fools-you.md)** ✅ | §1.1 |
| 06 | **[期望与方差：老板问"这方案稳不稳"时在问什么](docs/m0-foundations/06-expectation-and-spread.md)** ✅ | §1.1.3 |
| **07** | **[要测多少次，你才敢下结论](docs/m0-foundations/07-how-many-before-you-decide.md)** ✅ | **§1.1.3、附录 A** |
| 08 | **[那个"乘二"是从哪来的](docs/m0-foundations/08-where-the-times-two-comes-from.md)** ✅ | 附录 A |
| 09 | **[随机数其实是排队领号](docs/m0-foundations/09-making-random-variables.md)** ✅ | §2.1–2.2 |
| 10 | **[为什么股价跌不成负数](docs/m0-foundations/10-normal-and-lognormal.md)** ✅ | §2.3、§3.2 |
| 11 | **[一篮子公司为什么还会同一天倒霉](docs/m0-foundations/11-correlation-and-baskets.md)** ✅ | §2.3（多维正态） |
| 12 | **[知道明天下雨，就该重估单量](docs/m0-foundations/12-conditioning-and-control.md)** ✅ | §4.1 控制变量 |
| 13 | **[再多一块钱值不值](docs/m0-foundations/13-derivatives-and-error-tails.md)** ✅（微积分够用版：导数＝边际、泰勒展开＝误差近似） | §6.2 二阶方法、§7.1 有限差分 |
| 14 | **[明年的 30 块，今天值几块](docs/m0-foundations/14-pricing-by-discounted-expectation.md)** ✅（金融够用版：折现期望、复制与无套利、路径依赖只能演） | §1.2 定价原理、§6.4 障碍穿越 |
| 15 | **[醉汉回家的路：连续，却没有一段是直的](docs/m0-foundations/15-brownian-motion.md)** ✅（布朗运动直觉：二次变差、$\sqrt{t}$ 标度、期末与路上是两笔账） | §3.1 布朗运动、§3.2 几何布朗、§6.4 障碍穿越 |

原书章节与页码对照见 [原书章节索引](docs/book-index.md)。

**[第 12 课（条件期望）](docs/m0-foundations/12-conditioning-and-control.md)是整个第一期的最高点**，也是原书控制变量与条件模拟技术的直接伏笔。**[第 15 课（布朗运动）](docs/m0-foundations/15-brownian-motion.md)收尾**——它一结束，原书第一部分（第 1–3 章）对你就是"可读"状态。

### 后续：第二期（制作中，还没有课文）

按原书真实结构走。**下面每一个模块目前都还没有内容**，你在本仓库能读到的只有上面第一期那 15 课。

| 模块 | 对应原书 | 状态 |
|---|---|---|
| M1 随机数与随机变量 | ch2 | 未开始 |
| M2 样本路径的生成 | ch3 | 未开始 |
| M3 方差缩减（全书心脏） | ch4 | 未开始 |
| M4 准蒙特卡洛 | ch5 | 未开始 |
| M5 离散化方法 | ch6 | 未开始 |
| M6 敏感性估计 Greeks | ch7 | 未开始 |
| M7 美式期权定价 | ch8 | 未开始 |
| M8 风险管理：在险价值与信用风险 | ch9 | 未开始 |
| 附录 A/B/C 的数学准备 | 附录 | 未开始 |

第一期里曾经没做完的那件事已经做完：配套 notebook **15 课全部就绪**，每格都跑过并把真实输出嵌进文件，你在 GitHub 上直接点开就能看到数字，不必自己运行。只有第 01 课是例外——那一课故意不用电脑，它的 notebook 只是给你在手机上翻页看的，末尾两格验算可以跳过。课文里的代码也始终可以直接看 `code/` 里对应的 `.py`，它们设计成整段粘进浏览器（Colab / JupyterLite）也能跑。

---

## 怎么跑代码

**第一节课起就不需要安装任何东西**——所有代码设计为可在浏览器直接运行（Colab / JupyterLite）。

`notebooks/` 里是逐课的浏览器版配套（markdown 引导 + 一格一格的代码），**15 课全都在**。每一格里跑出来的数字都已经嵌在文件里，你在 GitHub 上点开就能读到，不用自己运行；想自己动手就整段粘进 [https://jupyter.org/try](https://jupyter.org/try) 或 Colab，按 `Shift + Enter` 逐格跑。数字与课文印的逐字一致（种子钉在 7）。每一课的 `code/lessonNN_*.py` 也都可以整段粘进一个单元格跑。

本地运行可选。下面这份清单是 `code/` 里的全部脚本，右边是我这台机器（Python 3.12）跑一遍的秒数：

```bash
python3 code/lesson02_lunch_budget.py            # 0.1 秒
python3 code/lesson03_week_ledger.py             # 0.0 秒
python3 code/lesson04_first_real_simulation.py   # 0.1 秒
python3 code/lesson05_where_the_average_sits.py  # 0.0 秒
python3 code/lesson06_expectation_and_spread.py  # 0.0 秒
python3 code/lesson07_your_own_numbers.py        # 0.0 秒
python3 code/lesson07_how_often_you_get_beaten.py # 3.8 秒，需要 numpy
python3 code/lesson08_error_bars.py              # 0.1 秒
python3 code/lesson09_making_any_distribution.py # 0.1 秒
python3 code/lesson10_normal_and_lognormal.py    # 3.0 秒
python3 code/lesson11_correlation_and_basket.py  # 1.4 秒
python3 code/lesson12_conditioning_and_control.py # 0.8 秒
python3 code/lesson13_derivatives_and_error_terms.py  # 3.4 秒
python3 code/lesson14_pricing_by_discounted_expectation.py  # 17 秒
python3 code/lesson15_brownian_motion.py         # 11 秒
```

除第 07 课那个 `how_often` 之外，全部只用标准库，不需要装 numpy。钉住随机种子（每段前的 `random.seed(7)`）之后，同一份代码每次给你同一个数——课文里印的数字就是这么抄下来的，你可以逐字核对。

课程里的图全部由脚本生成，想重新出图：

```bash
python3 code/fig04_thousand_months.py    # → assets/fig04_thousand_months.svg
python3 code/fig05_average_vs_middle.py  # → assets/fig05_average_vs_middle.svg
python3 code/fig06_expectation_and_spread.py  # → assets/fig06_expectation_and_spread.svg
python3 code/fig07_standard_error.py     # → assets/fig07_standard_error.svg
python3 code/fig08_central_limit.py      # → assets/fig08_central_limit.svg
python3 code/fig09_inverse_transform.py  # → assets/fig09_inverse_transform.svg
python3 code/fig10_volatility_drag.py    # → assets/fig10_volatility_drag.svg
python3 code/fig11_diversification.py    # → assets/fig11_diversification.svg
python3 code/fig12_conditioning_and_control.py  # → assets/fig12_conditioning_and_control.svg
python3 code/fig13_bias_vs_noise.py      # → assets/fig13_bias_vs_noise.svg
python3 code/fig14_expectation_knob.py   # → assets/fig14_expectation_knob.svg
python3 code/fig15_selfsimilar.py        # → assets/fig15_selfsimilar.svg
python3 code/fig15_endpoint_vs_path.py   # → assets/fig15_endpoint_vs_path.svg
python3 code/fig15_monitoring.py         # → assets/fig15_monitoring.svg
```

这些出图脚本是**作者的工具**，不是课程内容；读者打开 `assets/` 里现成的图就够了。第 01–03 课是工具课，手上还没有可实测的数据可画，所以那三节刻意不出图。

需要 Python 3.10+。装不装都不影响你跟着课程走。

---

## 每节课的固定结构

```
一、你手上有一个真实的困惑（来自你的一天，不来自教材目录）
二、先用大白话把那个关键念头立住（整节可以不出现符号）
三、再给式子，并且先说这个式子替你回答什么问题
四、用它判断你眼前这件事算不算数
五、它能帮你做的三类现实决定（含"要不要开始 / 只有预算能测多细"）
六、把你自己的数字粘进去算（可运行的工具，不是演示）
七、不信式子？让电脑演一遍（蒙特卡洛的第一个正确用法）
八、一件要提醒你的事
九、练习：全是决策题，答案里有现实后果
十、一句话 ＋ 下一课预告
【进阶框】严格版本（可跳过，不影响下一课）
备忘卡 ＋ 原书对应
```

## 写法约定（长期遵守，也请你监督）

这些约定来自第一轮样课被推翻的原因，不是我凭空定的。

1. **不断线。** 一个想法用完整的段落说完，不靠括号、破折号、加粗、脚注把读者从思路上掀下去。加粗只在"这一句是读者要带走的结论"时使用。
2. **先日子，后名字。** 先用你听得懂的说法讲透（"这个数字的毛边"），术语和符号放到后面作为对照，绝不提前当门槛。一页里的新术语不超过两个。
3. **不自说自话。** 写不出清楚解释的句子就是不该存在的句子。宁可删掉，也不留"直觉上是这样……"这类含混过渡。
4. **式子必须先交代它替你回答什么问题。** 变形、读法、口诀都不算解释。
5. **平视。** 不写"初学者必踩的坑""你这样读不懂论文"这类俯视或吓唬的语气。读者是聪明的成年人，只是暂时不知道。
6. **每节课都要有一个读者走出教室就能用的东西**：一次真实决策、一段能改数字的脚本、一句敢说出口的话。做不到就重写这一节。
7. 展示性代码不收录。跑出来的每个数字都必须在本地实测过。

---

## 仓库结构

```
docs/m1-tooling/        编程工具课（01–04）
docs/m0-foundations/    数学与金融预备课（05–15）
docs/book-index.md      原书 9 章 + 3 附录的章节页码索引
code/                   可运行 .py 脚本与配图生成脚本
notebooks/              浏览器可直接跑的配套 notebook
assets/                 自绘图（一律由脚本生成）
glossary.md             术语中英对照 + 符号词典
LICENSE.md              双许可条款（正文 CC BY-NC-SA 4.0 / 代码 MIT）
_config.yml、_layouts/  GitHub Pages 站点配置与手机版式（只影响在线阅读，不影响课文本身）
```

---

## 两条长期原则

**① 版权红线。** 原书是 Springer 版权作品。本课程所有公式自行排版、所有图自行用代码生成、正文零复制，引用只到"章/节"层级。**建议购买正版**支持作者。

**② 诚实的难度。** 生活类比给的是直觉，给不了证明。我们在每一节里明说"你现在只拿到了直觉，证明在进阶框"，绝不假装 599 页的 monograph 能被比喻替代。

---

## 许可

- 正文（`docs/**`、`assets/**`、本 README）：**CC BY-NC-SA 4.0**
- 代码（`code/**`、`notebooks/**`）：**MIT**

两段的完整条款与"原书不在本仓库许可范围内"的说明，见 [LICENSE.md](LICENSE.md)。

---

## 关于作者

一位在 CBD 上班的普通白领，白天点外卖挤地铁，业余经营自己的新媒体账号。零基础入学，把踩过的坑全部写下来。
