import pygame

from ..utils.pygameplus import *
from .mainconfig import *


# Images


IMAGE_BG = pygame.transform.scale_by(
    pygame.image.load(asset_path(os.path.join('images', 'spacebg0.png'))), 0.25).convert_alpha()