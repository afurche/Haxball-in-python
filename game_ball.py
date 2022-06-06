from ball import BallObject
from setup_variables import *


class GameBall(BallObject):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, PITCH_HEIGHT / 2, GAME_BALL_SIZE)
        self._current_directional_velocity = [0, 0]  # first value represent current speed in x axis and second represent current speed in y axis

    @property
    def current_velocity(self):
        return self._current_directional_velocity

    @property
    def vel_x(self):
        return self._current_directional_velocity[0]

    @vel_x.setter
    def vel_x(self, new_x):
        self._current_directional_velocity[0] = new_x

    @property
    def vel_y(self):
        return self._current_directional_velocity[1]

    @vel_y.setter
    def vel_y(self, new_y):
        self._current_directional_velocity[1] = new_y

    @current_velocity.setter
    def current_velocity(self, new_vel):
        self._current_directional_velocity = new_vel

    def check_x_axis_field_collision(self):
        if ((self.x < 0 + GAME_BALL_SIZE + 50) and (self.y < GOAL_UP_Y or self.y > GOAL_BOTTOM_Y)) or ((self.x > SCREEN_WIDTH - GAME_BALL_SIZE - 50) and (self.y < GOAL_UP_Y or self.y > GOAL_BOTTOM_Y)):
            return True
        else:
            return False

    def check_y_axis_field_collision(self):
        if (self.y < 0 + GAME_BALL_SIZE + 30) or (self.y > SCREEN_HEIGHT - GAME_BALL_SIZE - 30):
            return True
        else:
            return False

    def ball_movement(self):
        if self.check_x_axis_field_collision():
            self.vel_x = self.vel_x * (-1)
        if self.check_y_axis_field_collision():
            self.vel_y = self.vel_y * (-1)

        if abs(self.vel_x) != 0:
            self.x += self.vel_x
            if self.vel_x >= 0:
                self.vel_x = self.vel_x - 0.05 * self.vel_x
            else:
                self.vel_x = self.vel_x + 0.05 * (self.vel_x * (-1))

        if abs(self.vel_y) != 0:
            self.y += self.vel_y
            if self.vel_y >= 0:
                self.vel_y = self.vel_y - 0.05 * self.vel_y
            else:
                self.vel_y = self.vel_y + 0.05 * (self.vel_y * (-1))

    def reset_ball_after_goal(self):
        self.coord = (SCREEN_WIDTH / 2, PITCH_HEIGHT / 2)
        self.vel_x = 0
        self.vel_y = 0
