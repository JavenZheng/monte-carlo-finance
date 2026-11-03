"""工作日午餐预算。

改最上面五个数，重跑。
不需要装任何东西：浏览器里打开 https://jupyter.org/try ，把整段粘进去也能跑。
"""

elapsed_days = 11      # 这个月已经过了几个工作日
spent = 449            # 这些天午餐一共花了多少
workdays_left = 11     # 这个月还剩几个工作日
budget = 1000          # 你给自己的整月午餐预算
coffee = 8             # 你纠结的那件小事

daily = spent / elapsed_days
month_end = daily * (elapsed_days + workdays_left)
daily_cap = (budget - spent) / workdays_left
headroom = daily_cap - daily

print(f"过了 {elapsed_days} 个工作日，花了 {spent}，平均每天 {daily:.1f}")
print(f"照这个速度，月底落在 {month_end:.0f}，而你的预算是 {budget}")
print(f"剩下的 {workdays_left} 天，每天最多能花 {daily_cap:.1f}")
print(f"也就是比现在宽出 {headroom:.1f} —— 你想要的那杯是 {coffee}")
