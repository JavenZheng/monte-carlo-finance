"""两种写法其实一模一样好，只发几条会有多容易骗到你。

第 07 课配套。这是本课程第一个真正的蒙特卡洛：不推导，直接让电脑把
"你再抽一次签"这件事演两万个遍，数一数其中有多少遍你会误以为看到了改进。

    python3 code/lesson07_how_often_you_get_beaten.py

想换成你自己的场景，只改下面三个数：平均、起伏、每种各测几条。
"""

import numpy as np

LEVEL = 3000      # 两种写法其实一样好，真实水平都是这个数
SPREAD = 2000     # 单条围绕平均的起伏
GAP_YOU_SAW = 500 # 你手上那个"新写法高出 500"


def beaten_odds(each, trials=20000, seed=7):
    """如果两种写法其实一样，只各发 each 条，有多大概率看出 GAP_YOU_SAW 的假差距。"""
    rng = np.random.default_rng(seed)
    old = rng.normal(LEVEL, SPREAD, (trials, each)).mean(axis=1)
    new = rng.normal(LEVEL, SPREAD, (trials, each)).mean(axis=1)
    leads = new - old
    return np.mean(leads >= GAP_YOU_SAW), np.mean(np.abs(leads) >= GAP_YOU_SAW)


if __name__ == "__main__":
    print(f"单条起伏 {SPREAD}，你看到的假差距 {GAP_YOU_SAW}\n")
    print(f"{'每种各发':>8} | {'看高出500的概率':>14} | {'看出任何500差距':>15}")
    print("-" * 50)
    for each in [9, 30, 100, 128]:
        one_way, two_way = beaten_odds(each)
        print(f"{each:>8} | {one_way * 100:>13.0f}% | {two_way * 100:>14.0f}%")

    print("\n读法：第一列是你愿意发多少条；后面两列是「其实什么都没变」时，")
    print("你仍然会被骗的概率。条数涨十几倍，被骗的概率才降下来——这就是根号税。")
