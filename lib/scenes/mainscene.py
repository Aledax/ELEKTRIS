import pygame
from pygame.locals import *

from lib.scenes.pygamescene import PygameScene
from lib.scenes.sceneconfig import *
from lib.scenes.mainconfig import *
from lib.scenes.mainassets import *
from lib.scenes.infinitescene import InfiniteScene

from lib.widgets.buttonwidget import ButtonWidget


class MainScene(PygameScene):


    def __init__(self, scene_runner):

        super().__init__(scene_runner, WINDOW_SIZE)

        self.infinite_button = ButtonWidget(WINDOW_CENTER, True, 0.5, 0.07, 'Start!', [self._start_infinite], [[]])

        # Animation state

        self.background_scroll = 0


    def _start_infinite(self):

        self.scene_runner.switch_active_scene(InfiniteScene(self.scene_runner), True)

    
    def _update_frame(self, dt, mouse_position, mouse_pressed, keys_pressed, events):

        self.infinite_button.update(mouse_position, mouse_pressed[0])

        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()

        # Background

        self.background_scroll = (self.background_scroll - BACKGROUND_SCROLL_SPEED * dt) % IMAGE_BG.get_height()
        for i in range(-1, int(WINDOW_HEIGHT / IMAGE_BG.get_height()) + 1):
            self.scene_surface.blit(IMAGE_BG, (0, self.background_scroll + i * IMAGE_BG.get_height()))

        # Widgets

        self.infinite_button.render(self.scene_surface)