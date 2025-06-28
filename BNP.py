import pygame
import pygame_gui
import random
import math

# --- 初始化 ---
pygame.init()
pygame.display.set_caption("Buffon's Needle Simulator")
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))


# --- GUI 元件區域設定 ---
input_rect = pygame.Rect(20, 500, 300, 180)
result_rect = pygame.Rect(340, 500, 640, 180)
draw_area_rect = pygame.Rect(0, 0, WIDTH, 480)

# --- 建立輸入欄位 ---
needle_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(30, 510, 120, 30),
    manager=manager
)
needle_input.set_text("500")

length_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(30, 560, 120, 30),
    manager=manager
)
length_input.set_text("40")

spacing_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(30, 610, 120, 30),
    manager=manager
)
spacing_input.set_text("50")

# --- 建立標籤 ---
font = pygame.font.SysFont("Microsoft JhengHei", 20)
def draw_labels():
    screen.blit(font.render("針數量", True, (0, 0, 0)), (160, 515))
    screen.blit(font.render("針長度", True, (0, 0, 0)), (160, 565))
    screen.blit(font.render("橫線間距", True, (0, 0, 0)), (160, 615))

# --- 建立送出按鈕 ---
submit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(WIDTH//2 - 60, 660, 120, 30),
    text='submit',
    manager=manager
)

# --- 投針模擬函數 ---
def simulate(needle_count, needle_len, line_spacing):
    needles = []
    hit_count = 0
    lines_y = list(range(0, draw_area_rect.height, line_spacing))

    for _ in range(needle_count):
        x_center = random.uniform(0, WIDTH)
        y_center = random.uniform(0, draw_area_rect.height)
        theta = random.uniform(0, math.pi)
        dx = (needle_len / 2) * math.cos(theta)
        dy = (needle_len / 2) * math.sin(theta)
        x0, y0 = x_center - dx, y_center - dy
        x1, y1 = x_center + dx, y_center + dy

        crossed = any(y <= max(y0, y1) and y >= min(y0, y1) and (y - y0)*(y - y1) < 0 for y in lines_y)
        if crossed:
            hit_count += 1
        needles.append(((x0, y0), (x1, y1), crossed))

    estimated_pi = (2 * needle_len * needle_count / (hit_count * line_spacing)) if hit_count > 0 else None
    return needles, lines_y, estimated_pi, hit_count

# 初始狀態
needles = []
lines_y = []
pi_result = None
hit_count = 0
needle_count = 0

# --- 主迴圈 ---
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == submit_button:
                # 讀取參數
                try:
                    needle_count = int(needle_input.get_text())
                    needle_len = float(length_input.get_text())
                    line_spacing = int(spacing_input.get_text())
                    if needle_len > line_spacing:
                        raise ValueError("針長不可大於線距")
                    needles, lines_y, pi_result, hit_count = simulate(needle_count, needle_len, line_spacing)
                except Exception as e:
                    pi_result = None
                    needles = []
                    lines_y = []
                    hit_count = 0

    # --- 畫圖區 ---
    for y in lines_y:
        pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), 2)

    for start, end, crossed in needles:
        color = (255, 0, 0) if crossed else (200, 200, 200)
        pygame.draw.line(screen, color, start, end, 2)

    # --- 顯示結果區 ---
    result_text_lines = []

    if pi_result:
        result_text_lines = [
            "計算過程：",
            "π = (2 × 針長 × 投擲次數) ÷ (命中次數 × 線距)",
            f"    = (2 × {needle_len} × {needle_count}) ÷ ({hit_count} × {line_spacing})",
            f"    = {pi_result:.5f}"
        ]
    elif needle_count > 0:
        result_text_lines = ["No hits — 無法估算 π"]

    # 顯示多行文字
    for i, line in enumerate(result_text_lines):
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (350, 510 + i * 30))  # 每行往下移動

    draw_labels()
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
