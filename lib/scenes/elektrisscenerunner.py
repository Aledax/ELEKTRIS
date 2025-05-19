from lib.scenes.pygamescene import *
from lib.scenes.elektrisconfig import *
from lib.scenes.elektrisassets import *


class ElektrisSceneRunner(PygameSceneRunner):


    TRANSITION_NONE = 0
    TRANSITION_FORWARDS = 1
    TRANSITION_BACKWARDS = 2


    def __init__(self, screen_size, debug=False, fps_cap=True):

        super().__init__(screen_size, debug, fps_cap)

        self.transition_state = ElektrisSceneRunner.TRANSITION_NONE
        self.transition_stopwatch = 0
        self.queued_active_scene = None


    def switch_active_scene(self, active_scene, transition):
        
        if transition:
            self.transition_state = ElektrisSceneRunner.TRANSITION_FORWARDS
            self.queued_active_scene = active_scene
            SOUND_TRANSITION.play()
        else:
            self.active_scene = active_scene


    def _update_frame(self, dt, mouse_position, mouse_pressed, keys_pressed, events):

        if self.transition_state == ElektrisSceneRunner.TRANSITION_NONE:
            return
        
        self.transition_stopwatch = min(self.transition_stopwatch + dt, TRANSITION_TIME)

        if self.transition_stopwatch == TRANSITION_TIME:

            self.transition_stopwatch = 0

            if self.transition_state == ElektrisSceneRunner.TRANSITION_FORWARDS:
                self.active_scene = self.queued_active_scene
                self.queued_active_scene = None
                self.transition_state = ElektrisSceneRunner.TRANSITION_BACKWARDS
                SOUND_TRANSITION.play()

            else:
                self.transition_state = ElektrisSceneRunner.TRANSITION_NONE

        if self.transition_state == ElektrisSceneRunner.TRANSITION_NONE:
            return
        
        transition_width = TRANSITION_PROGRESS_FUNCTION(self.transition_stopwatch) * WINDOW_WIDTH
        if self.transition_state == ElektrisSceneRunner.TRANSITION_BACKWARDS:
            transition_width = WINDOW_WIDTH - transition_width
        transition_width /= 2
        
        pygame.draw.rect(self.active_scene.scene_surface, TRANSITION_COLOR, (0, 0, transition_width, WINDOW_HEIGHT))
        pygame.draw.rect(self.active_scene.scene_surface, TRANSITION_COLOR, (WINDOW_WIDTH - transition_width, 0, transition_width, WINDOW_HEIGHT))