import random
import math

class NeedleSimulator:
    def __init__(self, needle_count, needle_len, line_spacing, screen_width, screen_height):
        self.needle_count = needle_count
        self.needle_len = needle_len
        self.line_spacing = line_spacing
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def simulate(self):
        needles = []
        hit_count = 0
        lines_y = list(range(0, self.screen_height, self.line_spacing))

        for _ in range(self.needle_count):
            # 針中點座標
            x_center = random.uniform(0, self.screen_width)
            y_center = random.uniform(0, self.screen_height)
            # 針旋轉角度
            theta = random.uniform(0, math.pi)
            dx = (self.needle_len / 2) * math.cos(theta)
            dy = (self.needle_len / 2) * math.sin(theta)
            # 針頭/尾座標
            x0, y0 = x_center - dx, y_center - dy
            x1, y1 = x_center + dx, y_center + dy

            # 判斷相交
            # 在布豐投針實驗中，如果針剛好落在線上（重合），要不要算進「與線相交」的命中次數？
            # >>不計入
            # 這個幾何機率問題要求的是「針的中點與角度同時使得針穿越線」的機率。
            # 針剛好落在線上或一端壓線，在數學上是機率為 0 的事件（測度為零），所以通常不納入統計。
            crossed = any((y_l - y0) * (y_l - y1) < 0 for y_l in lines_y )
            if crossed: hit_count += 1
            needles.append(((x0, y0), (x1, y1), crossed))

        pi_estimate = (2 * self.needle_len * self.needle_count / (hit_count * self.line_spacing))
        
        return needles, lines_y, pi_estimate, hit_count
    

