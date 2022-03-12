import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 604
GAME_BALL_SIZE = 27
PLAYER_BALL_SIZE = 54
RED_TEAM_START_POSITIONS = [(200, 130), (200, 280), (200, 430)]
BLUE_TEAM_START_POSITIONS = [(950, 130), (950, 280), (950, 430)]


class BallObject:
    def __init__(self, start_x, start_y, sprite_path, ball_size):
        self._x = start_x
        self._y = start_y
        self._sprite = pygame.image.load(sprite_path)
        self._radius = ball_size / 2

    @property
    def coord(self):
        return self._x, self._y

    @property
    def sprite(self):
        return self._sprite

    def draw(self, screen):
        pygame.draw.circle(screen, color='black', center=self.coord, radius=self._radius)
        screen.blit(self.sprite, tuple(coord - self._radius for coord in self.coord))

    def move(self):
        pass


class TeamPlayer(BallObject):
    def __init__(self, start_x, start_y, team_color):
        super().__init__(start_x, start_y, os.path.join('assets', f'{team_color}_player.png'), PLAYER_BALL_SIZE)


class GameBall(BallObject):
    def __init__(self):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, os.path.join('assets', 'ball.png'), GAME_BALL_SIZE)


class Game:
    def __init__(self):

        self._game_run = True

        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mini Football')
        self._background_sprite = pygame.image.load(os.path.join('assets', 'haxmap.png'))
        self._ball = GameBall()
        self._red_team = [TeamPlayer(coord[0], coord[1], 'red') for coord in RED_TEAM_START_POSITIONS]
        self._blue_team = [TeamPlayer(coord[0], coord[1], 'blue') for coord in BLUE_TEAM_START_POSITIONS]
        self._janne_ahonen = pygame.image.load(os.path.join('assets', 'JanneAhonen.jpg'))
        self._clock = pygame.time.Clock()

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    #Blit Janne Ahonen
                    self._screen.blit(self._janne_ahonen, self._janne_ahonen.get_rect())
                    pygame.display.update()

    def blit_players(self):
        for red_player, blue_player in zip(self._red_team, self._blue_team):
            red_player.draw(self._screen)
            blue_player.draw(self._screen)

    def blit_screen(self):
        self._screen.blit(self._background_sprite, self._background_sprite.get_rect())
        self._ball.draw(self._screen)
        self.blit_players()
        pygame.display.update()

    def game_loop(self):
        while self._game_run:
            self.blit_screen()
            self.event_catcher()


if __name__ == '__main__':
    Game().game_loop()
