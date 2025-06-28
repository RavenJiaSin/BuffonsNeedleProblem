import pygame
import pygame_gui
from config import *
from simulator import NeedleSimulator
from gui import BuffonGUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Buffon's Needle Simulator - OOP GUI")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    gui = BuffonGUI(screen, manager)

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gui.button:
                    try:
                        count, length, spacing = gui.get_input_values()
                        if length > spacing:
                            gui.set_simulation_result([], [], None, 0, count)
                        else:
                            sim = NeedleSimulator(count, length, spacing, WIDTH, DRAW_AREA_HEIGHT)
                            needles, lines_y, pi_val, hit = sim.simulate()
                            gui.set_simulation_result(needles, lines_y, pi_val, hit, count)
                    except:
                        gui.set_simulation_result([], [], None, 0, 0)

        gui.draw()
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
