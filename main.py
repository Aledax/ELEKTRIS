from lib.scenes.elektrisscenerunner import *
from lib.scenes.sceneconfig import *


if __name__ == '__main__':

    scene_runner = ElektrisSceneRunner(WINDOW_SIZE, True, False)

    # Must be imported after PygameSceneRunner instantiation

    from lib.scenes.mainscene import *
    main_scene = MainScene(scene_runner)

    scene_runner.switch_active_scene(main_scene, False)
    scene_runner.loop()