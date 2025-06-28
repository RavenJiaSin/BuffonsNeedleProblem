import pygame
import pygame_gui
from config import *

class BuffonGUI:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.setup_ui()
        self.result_lines = []
        self.needles = []
        self.lines_y = []

    def setup_ui(self):
        # 建立輸入欄位
        self.needle_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(30, 510, 120, 30), self.manager)
        self.length_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(30, 560, 120, 30), self.manager)
        self.spacing_input = pygame_gui.elements.UITextEntryLine(pygame.Rect(30, 610, 120, 30), self.manager)
        self.needle_input.set_text("500")
        self.length_input.set_text("40")
        self.spacing_input.set_text("50")
        self.button = pygame_gui.elements.UIButton(pygame.Rect(WIDTH//2 - 60, 660, 120, 30), "模擬", self.manager)

    def get_input_values(self):
        return (
            int(self.needle_input.get_text()),
            float(self.length_input.get_text()),
            int(self.spacing_input.get_text())
        )

    def set_simulation_result(self, needles, lines_y, pi_value, hit_count, total):
        self.needles = needles
        self.lines_y = lines_y
        if pi_value:
            self.result_lines = [
                "計算過程：",
                "π ≈ (2 × 針長 × 投擲次數) ÷ (命中次數 × 線距)",
                f"    = (2 × {self.length_input.get_text()} × {total}) ÷ ({hit_count} × {self.spacing_input.get_text()})",
                f"    ≈ {pi_value:.5f}"
            ]
        else:
            self.result_lines = ["No hits — 無法估算 π"]

    def draw(self):
        self.screen.fill(WHITE)

        # 畫線
        for y in self.lines_y:
            pygame.draw.line(self.screen, BLACK, (0, y), (WIDTH, y), 1)

        # 畫針
        for start, end, crossed in self.needles:
            color = RED if crossed else BLUE
            pygame.draw.line(self.screen, color, start, end, 2)

        # 顯示文字
        for i, line in enumerate(self.result_lines):
            text_surface = FONT.render(line, True, BLACK)
            self.screen.blit(text_surface, (350, 510 + i * 30))

        # 中文標籤
        self.screen.blit(FONT.render("針數量", True, BLACK), (160, 515))
        self.screen.blit(FONT.render("針長度", True, BLACK), (160, 565))
        self.screen.blit(FONT.render("橫線間距", True, BLACK), (160, 615))
