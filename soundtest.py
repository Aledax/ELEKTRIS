import pygame
import time

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

sound = pygame.mixer.Sound("assets//sounds//flick1.wav")

for i in range(10):
    print(f"Play {i+1}")
    sound.stop()
    sound.play()
    time.sleep(0.5)  # vary this to 2–3s to see if delay affects it