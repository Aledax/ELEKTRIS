import pygame

from lib.scenes.sceneconfig import *


if __name__ == '__main__':

    window_surface = pygame.display.set_mode(WINDOW_SIZE)

    from lib.scenes.elektrisscenerunner import *

    scene_runner = ElektrisSceneRunner(window_surface, True, False)
    scene_runner.switch_to_main_scene(False)
    scene_runner.loop()