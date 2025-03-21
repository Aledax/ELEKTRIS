from lib.scenes.pygamescene import *
from lib.scenes.testscene import *


if __name__ == '__main__':

    # Initialize scene runner
    window_size = (1280, 720)
    scene_runner = PygameSceneRunner(window_size)

    # Initialize scenes
    colors = [(200, 50, 50), (50, 200, 50), (50, 50, 200)]
    scene_count = len(colors)
    scenes = [TestScene(scene_runner, window_size, colors[i]) for i in range(scene_count)]
    for i in range(scene_count):
        scenes[i].next_scene = scenes[(i + 1) % scene_count]

    # Start scene runner
    scene_runner.switch_active_scene(scenes[0])
    scene_runner.loop()