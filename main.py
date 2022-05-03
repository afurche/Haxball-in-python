import pygame
import os
from network import Network
import pickle
from math import sqrt, cos, sin

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 604
GAME_BALL_SIZE = 27
PLAYER_BALL_SIZE = 54
RED_TEAM_START_POSITIONS = [(200, 130), (200, 280), (200, 430)]
BLUE_TEAM_START_POSITIONS = [(950, 130), (950, 280), (950, 430)]
STANDARD_VELOCITY = 7
SPRINT_VELOCITY = 10


class BallObject:
    def __init__(self, start_x, start_y, ball_size):
        self._x = start_x
        self._y = start_y
        self._radius = ball_size / 2
        self._standard_velocity = STANDARD_VELOCITY
        self._sprint_velocity = SPRINT_VELOCITY

    @property
    def coord(self):
        return self._x, self._y

    def draw(self, screen, sprite):
        pygame.draw.circle(screen, color='black', center=self.coord, radius=self._radius)
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
    def sprint_velocity(self):
        return self._sprint_velocity

    @sprint_velocity.setter
    def sprint_velocity(self, new_velocity):
        self._sprint_velocity = new_velocity


class TeamPlayer(BallObject):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, PLAYER_BALL_SIZE)
        self._is_current = False

    def move(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self._x > 30:
            if keys[pygame.K_LSHIFT]:
                self._x -= self._sprint_velocity
            else:
                self._x -= self._standard_velocity

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self._x < 1170:
            if keys[pygame.K_LSHIFT]:
                self._x += self._sprint_velocity
            else:
                self._x += self._standard_velocity

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self._y > 30:
            if keys[pygame.K_LSHIFT]:
                self._y -= self._sprint_velocity
            else:
                self._y -= self._standard_velocity

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self._y < 574:
            if keys[pygame.K_LSHIFT]:
                self._y += self._sprint_velocity
            else:
                self._y += self._standard_velocity

    @property
    def is_current(self):
        return self._is_current

    @is_current.setter
    def is_current(self, new_is_current):
        self._is_current = new_is_current


class GameBall(BallObject):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, GAME_BALL_SIZE)
        self._angle = 0

    def move_automatic(self):
        self.y = int(cos(self._angle) * 100) + SCREEN_HEIGHT / 2
        self.x = int(sin(self._angle) * 100) + SCREEN_WIDTH / 2
        self._angle += 0.05


class Player:
    def __init__(self, team_start_position):
        self._team = [TeamPlayer(coord[0], coord[1]) for coord in team_start_position]
        self._team[0].is_current = True

    def move_footballer(self):
        for player in self._team:
            if player.is_current:
                player.move()

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


class FootballPitch:
    def __init__(self):
        self._player_id = 0
        self._player1 = Player(RED_TEAM_START_POSITIONS)
        self._player2 = Player(BLUE_TEAM_START_POSITIONS)
        self._ball = GameBall()

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

    def player_footballer_change(self):
        if self._player_id == 1:
            self._player1.change_to_player_closest_to_ball(self._ball.coord)
        elif self._player_id == 2:
            self._player2.change_to_player_closest_to_ball(self._ball.coord)


class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mini Football')
        self._background_sprite = pygame.image.load(os.path.join('assets', 'haxmap.png'))
        self._red_team_sprite = pygame.image.load(os.path.join('assets', 'red_player.png'))
        self._blue_team_sprite = pygame.image.load(os.path.join('assets', 'blue_player.png'))
        self._red_team_current_sprite = pygame.image.load(os.path.join('assets', 'red_player_current.png'))
        self._ball_sprite = pygame.image.load(os.path.join('assets', 'ball.png'))
        self._clock = pygame.time.Clock()
        self._game_run = True
        self._is_player_changing_footballer = False
        self._network = Network()
        self._football_pitch = self._network.football_pitch

    def player_change_event(self):
        if self._is_player_changing_footballer:
            self._football_pitch.player_footballer_change()
            self._is_player_changing_footballer = False

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if not self._is_player_changing_footballer:
                        self._is_player_changing_footballer = True

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
                    blue_player.draw(self._screen, self._red_team_current_sprite)
                else:
                    blue_player.draw(self._screen, self._blue_team_sprite)
                red_player.draw(self._screen, self._red_team_sprite)

    def blit_screen(self):
        self._screen.blit(self._background_sprite, self._background_sprite.get_rect())
        self._football_pitch.ball.draw(self._screen, self._ball_sprite)
        self.blit_players()
        pygame.display.update()

    def player_move(self):
        if self._football_pitch.player_id == 1:
            self._football_pitch.player1.move_footballer()
        elif self._football_pitch.player_id == 2:
            self._football_pitch.player2.move_footballer()

    def update_football_pitch(self, received_pitch):
        if self._football_pitch.player_id == 1:
            self._football_pitch.player2 = received_pitch.player2
        elif self._football_pitch.player_id == 2:
            self._football_pitch.player1 = received_pitch.player1

        # z tą piłką to trzeba będzie się dobrze zastanowić jak to ma działać xDDD
        self._football_pitch.ball = received_pitch.ball

    def game_loop(self):
        self._clock.tick(144)
        while self._game_run:
            self.update_football_pitch(self._network.send(self._football_pitch))
            self.blit_screen()
            self.event_catcher()
            self.player_move()
            self.player_change_event()
            self._football_pitch.ball.move_automatic()


if __name__ == '__main__':
    Game().game_loop()
