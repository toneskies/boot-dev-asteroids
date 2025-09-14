import pygame
from constants import *
from shot import *

class Weapon():
    def __init__(self):
        self.weapon_names = list(WEAPONS.keys())
        self.weapon_index = 0
        self.set_weapon(self.weapon_names[self.weapon_index])
    
    def set_weapon(self, name):
        self.weapon = WEAPONS[name]
        self.name = name

    def next_weapon(self):
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapon_names):
            self.weapon_index = 0
        self.set_weapon(self.weapon_names[self.weapon_index])

    def get_cooldown(self):
        return self.weapon["cooldown"]

    def shoot(self, position, rotation):
        if self.name == "single":
            Shot(position, rotation)
        elif self.name == "double":
            Shot(position, rotation, offset=(15, 0))
            Shot(position, rotation, offset=(-15, 0))
        elif self.name == "scatter":
            Shot(position, rotation, angle_offset=20)
            Shot(position, rotation)
            Shot(position, rotation, angle_offset=-20)