import pygame
from pygame.locals import *
import numpy as np

from .pygamescene import *


class TestScene(PygameScene):


    def __init__(self, scene_runner, surface_size, bg_color):

        super().__init__(scene_runner, surface_size)

        self.bg_color = bg_color
        self.counter = 0
        self.next_scene = None


    def _update_frame(self, dt, mouse_postiion, mouse_pressed, keys_pressed, events):

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                elif event.key == K_SPACE:
                    self.scene_runner.switch_active_scene(self.next_scene)
                elif event.key == K_UP:
                    self.counter += 1
            elif event.type == QUIT:
                self.quit()

        self.scene_surface.fill(self.bg_color)
        pygame.draw.circle(self.scene_surface, (0, 0, 0), np.divide(self.scene_surface.get_size(), 2).tolist(), self.counter * 10)