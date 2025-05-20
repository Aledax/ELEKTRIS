import sys
import time
import pygame
from pygame.locals import *

from lib.utils.pygameplus import *


pygame.font.init()
pygame.mixer.init()


class PygameSceneRunner:

    
    def __init__(self, window_surface, debug=False, fps_cap=True):

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.window_surface = window_surface
        self.active_scene = None
        self.debug = debug
        self.fps_cap = fps_cap
        self.previous_frame_time = time.perf_counter()

    
    # Override this if you want a custom transition!
    def switch_active_scene(self, active_scene):

        self.active_scene = active_scene


    # Override this if you want non-scene-specific functionality, like custom transitions!
    def _update_frame(self, dt, mouse_position, mouse_pressed, keys_pressed, events):

        pass
    

    def loop(self):

        while True:

            if self.active_scene is None:
                continue

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            keys_pressed = pygame.key.get_pressed()
            events = pygame.event.get()
            
            current_time = time.perf_counter()
            dt = current_time - self.previous_frame_time
            self.previous_frame_time = current_time

            self.active_scene._update_frame(dt, mouse_position, mouse_pressed, keys_pressed, events)
            self._update_frame(dt, mouse_position, mouse_pressed, keys_pressed, events)
            self.window_surface.blit(self.active_scene.scene_surface, (0, 0))
            if self.debug:
                debug(self.window_surface, (20, 20), str(int(round(1 / dt))))
            pygame.display.update()

            if self.fps_cap:
                self.clock.tick(self.fps)


class PygameScene:

    
    def __init__(self, scene_runner, surface_size):

        self.scene_runner = scene_runner
        self.scene_surface = pygame.surface.Surface(surface_size).convert_alpha()


    def quit(self):
        
        pygame.quit()
        sys.exit()


    # Override this!
    def _update_frame(self, mouse_postiion, mouse_pressed, keys_pressed, events):

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            elif event.type == QUIT:
                self.quit()