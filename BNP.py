import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---- 參數設定 ----
d = 1.0       # 線與線間距
l = 0.5       # 針的長度，需滿足 l <= d
N = int(input("請輸入要投擲的針數量："))  # 使用者輸入

# ---- 畫布設定 ----
num_lines = 10  # 畫幾條平行線
line_positions = np.arange(0, num_lines * d, d)
fig, ax = plt.subplots(figsize=(10, 6))

# 設定圖的邊界與背景
ax.set_xlim(0, 10)
ax.set_ylim(0, d * num_lines)
ax.set_aspect('equal')
ax.set_title("Buffon's Needle Simulation")

# 畫出平行線
for y in line_positions:
    ax.plot([0, 10], [y, y], 'k-', linewidth=1)

# ---- 模擬投針 ----
hit_count = 0

for _ in range(N):
    # 隨機中心位置 (x, y)
    x_center = np.random.uniform(0, 10)
    y_center = np.random.uniform(0, d * num_lines)
    
    # 隨機角度 theta ∈ [0, π]
    theta = np.random.uniform(0, np.pi)
    
    # 針兩端位置
    dx = (l / 2) * np.cos(theta)
    dy = (l / 2) * np.sin(theta)
    x0, x1 = x_center - dx, x_center + dx
    y0, y1 = y_center - dy, y_center + dy
    
    # 判斷是否與任一平行線相交
    # 原理：若 y0 與 y1 落在不同區間，代表穿越了某條線
    y_min = min(y0, y1)
    y_max = max(y0, y1)
    crossed = any((y <= y_max and y >= y_min and (y - y0)*(y - y1) < 0) for y in line_positions)

    if crossed:
        hit_count += 1
        ax.plot([x0, x1], [y0, y1], color='red')
    else:
        ax.plot([x0, x1], [y0, y1], color='blue')

# ---- 顯示估算 π ----
if hit_count > 0:
    estimated_pi = (2 * l * N) / (hit_count * d)
    result_text = f"Estimated π ≈ {estimated_pi:.5f}  (命中 {hit_count}/{N})"
else:
    result_text = "No hits — 無法估算 π"

# 顯示結果文字
ax.text(0.5, d * num_lines + 0.5, result_text, fontsize=14)

plt.show()
