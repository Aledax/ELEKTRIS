import pygame

from lib.utils.pygameplus import *
from lib.scenes.infiniteconfig import *


# Images


IMAGE_BG = pygame.transform.scale_by(
    pygame.image.load(asset_path(os.path.join('images', 'space-bg-3.png'))), 0.25).convert_alpha()


# Fonts


FONT_SCORE = pygame.font.Font(asset_path(os.path.join('fonts', 'DAGGERSQUARE.otf')), FONT_SCORE_SIZE)


# Sounds


BGM_PATH = asset_path(os.path.join('sounds', 'gatorgambol.mp3'))

SOUND_SELECT = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'flick1.ogg')))

SOUND_HOLD = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'crank1.wav')))

SOUND_PLACE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'snap1.wav')))
SOUND_PLACE.set_volume(0.5)

SOUND_SCORE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'ding3.wav')))
SOUND_SCORE.set_volume(0.2)

SOUND_LOSE = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'incorrect1.wav')))

SOUND_RESTART = pygame.mixer.Sound(asset_path(os.path.join('sounds', 'wipe1.wav')))