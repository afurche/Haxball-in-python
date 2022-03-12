import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 604
BALL_SIZE = 27


class Game:
    def __init__(self):

        self._game_run = True

        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mini Football')
        self._background_sprite = pygame.image.load(os.path.join('assets', 'haxmap.png'))
        self._janne_ahonen = pygame.image.load(os.path.join('assets', 'JanneAhonen.jpg'))
        self._ball_sprite = pygame.image.load(os.path.join('assets', 'ball.png'))
        self._red_player_sprite = pygame.image.load(os.path.join('assets', 'red_player.png'))
        self._blue_player_sprite = pygame.image.load(os.path.join('assets', 'blue_player.png'))
        self._clock = pygame.time.Clock()

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_run = False

    def blit_background(self):
        self._screen.blit(self._background_sprite, self._background_sprite.get_rect())
        self._screen.blit(self._ball_sprite, (SCREEN_WIDTH / 2 - (BALL_SIZE / 2), SCREEN_HEIGHT / 2 - (BALL_SIZE / 2)))
        self._screen.blit(self._red_player_sprite, (200, 280))
        self._screen.blit(self._red_player_sprite, (200, 430))
        self._screen.blit(self._red_player_sprite, (200, 130))

        self._screen.blit(self._blue_player_sprite, (950, 280))
        self._screen.blit(self._blue_player_sprite, (950, 430))
        self._screen.blit(self._blue_player_sprite, (950, 130))
        pygame.display.update()

    def game_loop(self):
        while self._game_run:
            self.blit_background()
            self.event_catcher()


if __name__ == '__main__':
    Game().game_loop()
