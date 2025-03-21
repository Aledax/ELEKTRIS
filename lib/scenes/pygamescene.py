import sys
import pygame
from pygame.locals import *


class PygameSceneRunner:

    
    def __init__(self, screen_size):

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.window_surface = pygame.display.set_mode(screen_size)
        self.active_scene = None

    
    def switch_active_scene(self, active_scene):

        self.active_scene = active_scene
    

    def loop(self):

        while True:

            if self.active_scene is None:
                continue

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            keys_pressed = pygame.key.get_pressed()
            events = pygame.event.get()

            self.active_scene._update_frame(mouse_position, mouse_pressed, keys_pressed, events)
            self.window_surface.blit(self.active_scene.scene_surface, (0, 0))
            pygame.display.update()

            self.clock.tick(self.fps)


class PygameScene:

    
    def __init__(self, scene_runner, surface_size):

        self.scene_runner = scene_runner
        self.scene_surface = pygame.surface.Surface(surface_size).convert_alpha()


    def quit(self):
        
        pygame.quit()
        sys.exit()


    def _update_frame(self, mouse_postiion, mouse_pressed, keys_pressed, events):

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            elif event.type == QUIT:
                self.quit()