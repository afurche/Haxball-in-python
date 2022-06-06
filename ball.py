from setup_variables import *
import pygame


class BallObject:
    def __init__(self, start_x, start_y, ball_size):
        self._x = start_x
        self._y = start_y
        self._radius = ball_size / 2
        self._standard_velocity = STANDARD_VELOCITY
        self._circle = pygame.Rect(self._x - self._radius, self._y - self._radius, self._radius * 2, self._radius * 2)

    @property
    def coord(self):
        return self._x, self._y

    @coord.setter
    def coord(self, coord):
        self._x = coord[0]
        self._y = coord[1]

    def draw(self, screen, sprite):
        self._circle = pygame.draw.circle(screen, color='black', center=self.coord, radius=self._radius)
        screen.blit(sprite, tuple(coord - self._radius for coord in self.coord))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, move_val):
        self._x = move_val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, move_val):
        self._y = move_val

    @property
    def standard_velocity(self):
        return self._standard_velocity

    @standard_velocity.setter
    def standard_velocity(self, new_velocity):
        self._standard_velocity = new_velocity

    @property
    def circle(self):
        return self._circle
