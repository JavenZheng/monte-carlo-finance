"""把你的真实记录粘进去，得到这个数字的成色。

第 07 课配套。只用标准库，本地装了 Python 就能跑，不需要 numpy、不需要联网。

    python3 code/lesson07_your_own_numbers.py

你可以直接改下面那一行 records：通勤分钟、日支出、每日曝光量、打开率百分比都可以。
"""

import math

# ↓↓↓ 把你自己的记录粘在这里 ↓↓↓
records = [34, 41, 29, 38, 45, 31, 37, 40, 26, 33]
unit = "分钟"


def describe(values):
    n = len(values)
    mean = sum(values) / n
    spread = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1))
    fuzz = spread / math.sqrt(n)
    return mean, spread, fuzz


if __name__ == "__main__":
    mean, spread, fuzz = describe(records)

    print(f"记录条数：       {len(records)}")
    print(f"你的平均：       {mean:.1f} {unit}")
    print(f"单次起伏：       {spread:.1f} {unit}")
    print(f"这个数字的毛边： {fuzz:.1f} {unit}")
    print(f"真实水平大概落在 {mean - 2 * fuzz:.0f} 到 {mean + 2 * fuzz:.0f} {unit} 之间")

    # 想比较两组记录（比如两条路线、两种标题写法），把第二组粘在这里再跑一次
    print("\n想比较两组的话，把两组各自的毛边加起来，再看你观察到的差距有没有大过它。")
