from ball import BallObject
from setup_variables import *
import pygame


class TeamPlayer(BallObject):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, PLAYER_BALL_SIZE)
        self._is_current = False
        self._start_x = start_x
        self._start_y = start_y
        self._move_backward = False
        self.returned_to_start_position = False
        self._is_moving_automatically = False
        self._horizontal_strategy = True
        self._touches_ball = False
        self._ball_push_velocity = [0, 0]
        self._is_goalkeeper = False  # if False is defender of current player
        self._returned_to_goalkeeper_position = False
        self._returned_to_defender_position = False

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._x > 30:

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._x > 30:
                self._x -= self._standard_velocity / 2
                self._y -= self.standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self._x -= self._standard_velocity / 2
                self._y += self.standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._x -= self._standard_velocity
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [-GAME_BALL_KICK_STRAIGHT_VELOCITY, 0]
                else:
                    self._ball_push_velocity = [-GAME_BALL_STRAIGHT_VELOCITY, 0]

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self._x < 1170:

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._x < 1170:
                self._x += self._standard_velocity / 2
                self._y -= self.standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self._x += self._standard_velocity / 2
                self._y += self.standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._x += self._standard_velocity
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [GAME_BALL_KICK_STRAIGHT_VELOCITY, 0]
                else:
                    self._ball_push_velocity = [GAME_BALL_STRAIGHT_VELOCITY, 0]

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._y > 30:

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._y > 30:
                self._y -= self._standard_velocity / 2
                self._x -= self._standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self._y -= self._standard_velocity / 2
                self._x += self._standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._y -= self._standard_velocity
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [0, -GAME_BALL_KICK_STRAIGHT_VELOCITY]
                else:
                    self._ball_push_velocity = [0, -GAME_BALL_STRAIGHT_VELOCITY]

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self._y < 574:

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._y < 574:
                self._y += self._standard_velocity / 2
                self._x -= self._standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self._y += self._standard_velocity / 2
                self._x += self._standard_velocity / 2
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                else:
                    self._ball_push_velocity = [GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._y += self._standard_velocity
                if keys[pygame.K_SPACE]:
                    self._ball_push_velocity = [0, GAME_BALL_KICK_STRAIGHT_VELOCITY]
                else:
                    self._ball_push_velocity = [0, GAME_BALL_STRAIGHT_VELOCITY]

    @property
    def is_current(self):
        return self._is_current

    @is_current.setter
    def is_current(self, new_is_current):
        self._is_current = new_is_current
        self.returned_to_start_position = False
        self._is_goalkeeper = False
        self._returned_to_goalkeeper_position = False
        self._returned_to_defender_position = False

    @property
    def is_goalkeeper(self):
        return self._is_goalkeeper

    @is_goalkeeper.setter
    def is_goalkeeper(self, is_gk):
        self._is_goalkeeper = is_gk

    @property
    def returned_to_goalkeeper_position(self):
        return self._returned_to_goalkeeper_position

    @returned_to_goalkeeper_position.setter
    def returned_to_goalkeeper_position(self, n):
        self._returned_to_goalkeeper_position = n

    @property
    def returned_to_defender_position(self):
        return self._returned_to_defender_position

    @returned_to_defender_position.setter
    def returned_to_defender_position(self, n):
        self._returned_to_defender_position = n

    @property
    def horizontal_strategy(self):
        return self._horizontal_strategy

    @horizontal_strategy.setter
    def horizontal_strategy(self, strategy):
        self._horizontal_strategy = strategy

    @property
    def touches_ball(self):
        return self._touches_ball

    @touches_ball.setter
    def touches_ball(self, tb):
        self._touches_ball = tb

    @property
    def ball_push_velocity(self):
        return self._ball_push_velocity

    def move_automatic(self, ball):
        if self._horizontal_strategy:
            if self.returned_to_start_position:
                if self.x <= self._start_x + 150 and not self._move_backward:
                    self.x += 5
                    if self._touches_ball:
                        if self.x < ball.x:
                            ball.current_velocity = [10, 0]
                elif self.x >= self._start_x + 150 and not self._move_backward:
                    self._move_backward = True
                elif self.x > self._start_x - 150 and self._move_backward:
                    self.x -= 5
                    if self._touches_ball:
                        if self.x > ball.x:
                            ball.current_velocity = [-10, 0]
                elif self.x <= self._start_x - 150 and self._move_backward:
                    self._move_backward = False
            else:
                if self.y < self._start_y - 5:
                    self.y += 5
                    if self._touches_ball:
                        ball.current_velocity = [0, 5]
                elif self.y > self._start_y + 5:
                    self.y -= 5
                    if self._touches_ball:
                        ball.current_velocity = [0, -5]
                else:
                    if self.x < self._start_x - 5:
                        self.x += 5
                        if self._touches_ball:
                            ball.current_velocity = [5, 0]
                    elif self.x > self._start_x + 5:
                        self.x -= 5
                        if self._touches_ball:
                            ball.current_velocity = [-5, 0]
                    else:
                        self.returned_to_start_position = True
        else:
            if self.returned_to_start_position:
                if self.y <= self._start_y + 100 and not self._move_backward:
                    self.y += 5
                    if self._touches_ball:
                        ball.current_velocity = [0, 10]
                elif self.y >= self._start_y + 100 and not self._move_backward:
                    self._move_backward = True
                elif self.y > self._start_y - 100 and self._move_backward:
                    self.y -= 5
                    if self._touches_ball:
                        ball.current_velocity = [0, -10]
                elif self.y <= self._start_y - 100 and self._move_backward:
                    self._move_backward = False
            else:
                if self.y < self._start_y - 5:
                    self.y += 5
                    if self._touches_ball:
                        ball.current_velocity = [0, 5]
                elif self.y > self._start_y + 5:
                    self.y -= 5
                    if self._touches_ball:
                        ball.current_velocity = [0, -5]
                else:
                    if self.x < self._start_x - 5:
                        self.x += 5
                        if self._touches_ball:
                            ball.current_velocity = [5, 0]
                    elif self.x > self._start_x + 5:
                        self.x -= 5
                        if self._touches_ball:
                            ball.current_velocity = [-5, 0]
                    else:
                        self.returned_to_start_position = True

    def advanced_move_automatic(self, player_goal_x_coord, player_defender_x_coord, ball):
        if self._is_goalkeeper:
            if self._returned_to_goalkeeper_position:
                if self.y > GOAL_UP_Y - PLAYER_BALL_SIZE - 20 and not self._move_backward:
                    self.y -= 2
                elif self.y <= GOAL_UP_Y - (PLAYER_BALL_SIZE + 20) and not self._move_backward:
                    self._move_backward = True
                elif self.y < GOAL_BOTTOM_Y + PLAYER_BALL_SIZE + 20 and self._move_backward:
                    self.y += 2
                elif self.y >= GOAL_BOTTOM_Y + PLAYER_BALL_SIZE + 20 and self._move_backward:
                    self._move_backward = False
            else:
                if self.y > (PITCH_HEIGHT / 2) + 5:
                    self.y -= 5
                elif self.y < (PITCH_HEIGHT / 2) - 5:
                    self.y += 5
                else:
                    if player_goal_x_coord < SCREEN_WIDTH / 2:
                        if self.x > player_goal_x_coord + 5:
                            self.x -= 5
                        else:
                            self._returned_to_goalkeeper_position = True
                            print("GOALKEEPER SET")
                    else:
                        if self.x < player_goal_x_coord - 5:
                            self.x += 5
                        else:
                            self._returned_to_goalkeeper_position = True
                            print("GOALKEEPER SET")

        else:
            if self._returned_to_defender_position:
                if self.y > ball.y + 2:
                    self.y -= 2
                elif self.y < ball.y - 2:
                    self.y += 2
            else:
                if self.y > (PITCH_HEIGHT / 2) + 5:
                    self.y -= 5
                elif self.y < (PITCH_HEIGHT / 2) - 5:
                    self.y += 5
                else:
                    if player_defender_x_coord < SCREEN_WIDTH / 2:
                        if self.x > player_defender_x_coord + 5:
                            self.x -= 5
                        else:
                            self._returned_to_defender_position = True
                            print("DEFENDER SET")
                    else:
                        if self.x < player_defender_x_coord - 5:
                            self.x += 5
                        else:
                            self._returned_to_defender_position = True
                            print("DEFENDER SET")
