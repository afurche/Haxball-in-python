import pygame
import os
from network import Network
import pickle
from math import sqrt, cos, sin
from _thread import *
from typing import Tuple
from time import sleep

SCREEN_WIDTH, SCREEN_HEIGHT, PITCH_HEIGHT = 1200, 654, 604  # need to add bottom strip for score_board
GAME_BALL_SIZE = 27
PLAYER_BALL_SIZE = 54
RED_TEAM_START_POSITIONS = [(350, 130), (350, 280), (350, 430)]
BLUE_TEAM_START_POSITIONS = [(850, 130), (850, 280), (850, 430)]
STANDARD_VELOCITY = 5
GAME_BALL_STRAIGHT_VELOCITY = 6
GAME_BALL_DIAGONAL_VELOCITY = 3
GAME_BALL_KICK_STRAIGHT_VELOCITY = 10
GAME_BALL_KICK_DIAGONAL_VELOCITY = 6
BOTTOM_SCORE_STRIP_COLOR = (101, 143, 96)


class BallObject:
    def __init__(self, start_x, start_y, ball_size):
        self._x = start_x
        self._y = start_y
        self._radius = ball_size / 2
        self._standard_velocity = STANDARD_VELOCITY
        self._circle = None  # represents pygame circle object

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

    def move(self, ball):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._x > 30:

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._x > 30:
                self._x -= self._standard_velocity / 2
                self._y -= self.standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self._x -= self._standard_velocity / 2
                self._y += self.standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._x -= self._standard_velocity
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [-GAME_BALL_KICK_STRAIGHT_VELOCITY, 0]
                    else:
                        ball.current_velocity = [-GAME_BALL_STRAIGHT_VELOCITY, 0]

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self._x < 1170:

            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._x < 1170:
                self._x += self._standard_velocity / 2
                self._y -= self.standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self._x += self._standard_velocity / 2
                self._y += self.standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._x += self._standard_velocity
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [GAME_BALL_KICK_STRAIGHT_VELOCITY, 0]
                    else:
                        ball.current_velocity = [GAME_BALL_STRAIGHT_VELOCITY, 0]

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._y > 30:

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._y > 30:
                self._y -= self._standard_velocity / 2
                self._x -= self._standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self._y -= self._standard_velocity / 2
                self._x += self._standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, -GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [GAME_BALL_DIAGONAL_VELOCITY, -GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._y -= self._standard_velocity
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [0, -GAME_BALL_KICK_STRAIGHT_VELOCITY]
                    else:
                        ball.current_velocity = [0, -GAME_BALL_STRAIGHT_VELOCITY]

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self._y < 574:

            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._y < 574:
                self._y += self._standard_velocity / 2
                self._x -= self._standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [-GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [-GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self._y += self._standard_velocity / 2
                self._x += self._standard_velocity / 2
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [GAME_BALL_KICK_DIAGONAL_VELOCITY, GAME_BALL_KICK_DIAGONAL_VELOCITY]
                    else:
                        ball.current_velocity = [GAME_BALL_DIAGONAL_VELOCITY, GAME_BALL_DIAGONAL_VELOCITY]

            else:
                self._y += self._standard_velocity
                if self._touches_ball:
                    if keys[pygame.K_SPACE]:
                        ball.current_velocity = [0, GAME_BALL_KICK_STRAIGHT_VELOCITY]
                    else:
                        ball.current_velocity = [0, GAME_BALL_STRAIGHT_VELOCITY]

    @property
    def is_current(self):
        return self._is_current

    @is_current.setter
    def is_current(self, new_is_current):
        self._is_current = new_is_current
        if new_is_current:
            self.returned_to_start_position = False

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
        if ((self.x < 0 + GAME_BALL_SIZE + 50) and (self.y < 290 or self.y > 340)) or ((self.x > SCREEN_WIDTH - GAME_BALL_SIZE - 50) and (self.y < 270 or self.y > 340)):
            return True
        else:
            return False

    def check_y_axis_field_collision(self):
        if (self.y < 0 + GAME_BALL_SIZE + 30) or (self.y > SCREEN_HEIGHT - GAME_BALL_SIZE - 30):
            return True
        else:
            return False

    def ball_movement(self):
        print(self.current_velocity)
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


class Player:
    def __init__(self, team_start_position, game_ball):
        self._team = [TeamPlayer(coord[0], coord[1]) for coord in team_start_position]
        self._team[0].is_current = True
        self._game_ball = game_ball

    def move_footballer(self):
        for player in self._team:
            if player.is_current:
                player.move(self._game_ball)
            else:
                player.move_automatic(self._game_ball)

    @property
    def team(self):
        return self._team

    @property
    def current_player(self):
        for player in self._team:
            if player.is_current:
                return player

    def change_to_player_closest_to_ball(self, ball_coord: (int, int)) -> None:
        distance_dict = {index: sqrt(abs(ball_coord[0] - player.coord[0]) ** 2 + abs(ball_coord[1] - player.coord[1]) ** 2) for index, player in enumerate(self._team)}
        min_distance_player_index = min(distance_dict, key=lambda k: distance_dict.get(k))
        self.current_player.is_current = False
        self._team[min_distance_player_index].is_current = True
        self._team[min_distance_player_index].horizontal_strategy = self._team[(min_distance_player_index + 1) % len(self._team)].horizontal_strategy
        print(f"Index: {min_distance_player_index}{self._team[min_distance_player_index].horizontal_strategy},  Index:{(min_distance_player_index + 1) % len(self._team)}{self._team[(min_distance_player_index + 1) % len(self._team)].horizontal_strategy}")

    def get_players_coord(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return tuple(team_player.coord for team_player in self._team)

    def set_players_coord(self, player_coord: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]):
        for team_player, coord in zip(self._team, player_coord):
            team_player.coord = coord

    def change_strategy(self):
        for team_player in self._team:
            if not team_player.is_current:
                team_player.returned_to_start_position = False
                team_player._horizontal_strategy = not team_player.horizontal_strategy

    def reset_team_after_goal(self, coord_list):
        for team_player, coord in zip(self._team, coord_list):
            team_player.coord = coord


class FootballPitch:
    def __init__(self):
        self._player_id = 0
        self._ball = GameBall()
        self._player1 = Player(RED_TEAM_START_POSITIONS, self._ball)
        self._player2 = Player(BLUE_TEAM_START_POSITIONS, self._ball)
        self._player1_score = 0
        self._player2_score = 0

    @property
    def player1(self):
        return self._player1

    @property
    def player2(self):
        return self._player2

    @property
    def ball(self):
        return self._ball

    @property
    def player_id(self):
        return self._player_id

    @player_id.setter
    def player_id(self, player_id):
        self._player_id = player_id

    def set_player_id(self, player_id):
        self._player_id = player_id

    @player1.setter
    def player1(self, player1):
        self._player1 = player1

    @player2.setter
    def player2(self, player2):
        self._player2 = player2

    @ball.setter
    def ball(self, ball):
        self._ball = ball

    @property
    def player1_score(self):
        return self._player1_score

    @player1_score.setter
    def player1_score(self, new_score):
        self._player1_score = new_score

    @property
    def player2_score(self):
        return self._player2_score

    @player2_score.setter
    def player2_score(self, new_score):
        self._player2_score = new_score

    @property
    def scores(self):
        return self._player1_score, self._player2_score

    @scores.setter
    def scores(self, new_scores):
        self._player1_score = new_scores[0]
        self._player2_score = new_scores[1]

    def player_footballer_change(self):
        if self._player_id == 1:
            self._player1.change_to_player_closest_to_ball(self._ball.coord)
        elif self._player_id == 2:
            self._player2.change_to_player_closest_to_ball(self._ball.coord)

    def player_strategy_change(self):
        if self._player_id == 1:
            self._player1.change_strategy()
        else:
            self._player2.change_strategy()

    def check_player_collisions_with_ball(self):
        if self._player_id == 1:
            player_tmp = self._player1
        else:
            player_tmp = self._player2

        for team_player in player_tmp.team:
            if team_player.circle.colliderect(self._ball.circle):
                team_player.touches_ball = True
            else:
                team_player.touches_ball = False

    def reset_pitch_after_goal(self):
        self._player1.reset_team_after_goal(RED_TEAM_START_POSITIONS)
        self._player2.reset_team_after_goal(BLUE_TEAM_START_POSITIONS)
        self._ball.reset_ball_after_goal()


class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mini Football')
        self._screen.fill(BOTTOM_SCORE_STRIP_COLOR)
        self._background_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'haxmap.png')), (SCREEN_WIDTH, PITCH_HEIGHT))
        self._red_team_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_player.png')), (PLAYER_BALL_SIZE, PLAYER_BALL_SIZE))
        self._blue_team_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player.png')), (PLAYER_BALL_SIZE, PLAYER_BALL_SIZE))
        self._red_team_current_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_player_current.png')), (PLAYER_BALL_SIZE, PLAYER_BALL_SIZE))
        self._blue_team_current_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_player_current.png')), (PLAYER_BALL_SIZE, PLAYER_BALL_SIZE))
        self._ball_sprite = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ball.png')), (GAME_BALL_SIZE, GAME_BALL_SIZE))
        self._clock = pygame.time.Clock()
        self._game_run = True
        self._is_player_changing_footballer = False
        self._network = Network()
        self._football_pitch = None
        self._last_send_message = None
        self._last_received_message = None
        self._is_player_changing_strategy = False

    def player_change_event(self):
        if self._is_player_changing_footballer:
            self._football_pitch.player_footballer_change()
            self._is_player_changing_footballer = False

    def player_change_strategy(self):
        if self._is_player_changing_strategy:
            self._football_pitch.player_strategy_change()
            self._is_player_changing_strategy = False

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if not self._is_player_changing_footballer:
                        self._is_player_changing_footballer = True
                if event.key == pygame.K_q:
                    self._is_player_changing_strategy = True

    def blit_players(self):
        for red_player, blue_player in zip(self._football_pitch.player1.team, self._football_pitch.player2.team):
            if self._football_pitch.player_id == 1:
                if red_player.is_current:
                    red_player.draw(self._screen, self._red_team_current_sprite)
                else:
                    red_player.draw(self._screen, self._red_team_sprite)
                blue_player.draw(self._screen, self._blue_team_sprite)
            elif self._football_pitch.player_id == 2:
                if blue_player.is_current:
                    blue_player.draw(self._screen, self._blue_team_current_sprite)
                else:
                    blue_player.draw(self._screen, self._blue_team_sprite)
                red_player.draw(self._screen, self._red_team_sprite)

    def blit_scoreboard(self):
        self._screen.blit(pygame.font.Font(None, 45).render(f"RED {self._football_pitch.player1_score}:{self._football_pitch.player2_score} BLUE", False, '#FFFFFF'), (500, 615))

    def blit_screen(self):
        self._screen.fill(BOTTOM_SCORE_STRIP_COLOR)
        self._screen.blit(self._background_sprite, self._background_sprite.get_rect())
        self.blit_players()
        self._football_pitch.ball.draw(self._screen, self._ball_sprite)
        self.blit_scoreboard()
        pygame.display.update()

    def player_move(self):
        if self._football_pitch.player_id == 1:
            self._football_pitch.player1.move_footballer()
        elif self._football_pitch.player_id == 2:
            self._football_pitch.player2.move_footballer()

    def communication_thread(self):
        self._network.connect_to_server()
        self._football_pitch = self._network.football_pitch
        while self._game_run:
            if self._football_pitch.player_id == 1:
                message_to_send = (self._football_pitch.player1.get_players_coord(), self._football_pitch.ball.coord)
                self._last_send_message = message_to_send
                received_message = self._network.send(message_to_send)
                self._football_pitch.player2.set_players_coord(received_message[0])
                if self._last_send_message[1] != received_message[1]:
                    self._football_pitch.ball.coord = received_message[1]
                if received_message[2] != self._football_pitch.scores:
                    self._football_pitch.scores = received_message[2]
                    self._football_pitch.reset_pitch_after_goal()
            elif self._football_pitch.player_id == 2:
                message_to_send = (self._football_pitch.player2.get_players_coord(), self._football_pitch.ball.coord)
                self._last_send_message = message_to_send
                received_message = self._network.send(message_to_send)
                self._football_pitch.player1.set_players_coord(received_message[0])
                if self._last_send_message[1] != received_message[1]:
                    self._football_pitch.ball.coord = received_message[1]
                if received_message[2] != self._football_pitch.scores:
                    self._football_pitch.scores = received_message[2]
                    self._football_pitch.reset_pitch_after_goal()

    def game_loop(self):
        start_new_thread(self.communication_thread, ())
        while self._game_run:
            self._clock.tick(30)
            if self._football_pitch is not None:
                self.blit_screen()
                self.event_catcher()
                self.player_move()
                self.player_change_strategy()
                self.player_change_event()
                self._football_pitch.check_player_collisions_with_ball()
                self._football_pitch.ball.ball_movement()


if __name__ == '__main__':
    Game().game_loop()
