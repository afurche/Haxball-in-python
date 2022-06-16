import pygame
import os
from network import Network
import pickle
from math import sqrt, cos, sin
from _thread import *
from typing import Tuple
from time import sleep
from football_pitch import FootballPitch
from game_ball import GameBall
from player import Player
from setup_variables import *


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
            self._football_pitch.player1.move_footballer(1)
        elif self._football_pitch.player_id == 2:
            self._football_pitch.player2.move_footballer(2)

    def communication_thread(self):
        """
        Separate thread for handling communication of the client with server.
        Communication works in a way that :]
        Server sends a tuple containing coordinates of the footballers of the opponent, coordinates of ball and game score
        Client sends coordinates of self footballers and the list with velocities that should be assinged to ball during collision
        """
        self._network.connect_to_server()
        self._football_pitch = self._network.football_pitch
        while self._game_run:
            if self._football_pitch.player_id == 1:
                message_to_send = (self._football_pitch.player1.get_players_coord(), self._football_pitch.player1.get_ball_push_velocities())
                received_message = self._network.send(message_to_send)
                self._football_pitch.player2.set_players_coord(received_message[0])
                self._football_pitch.ball.coord = received_message[1]
                if received_message[2] != self._football_pitch.scores:
                    self._football_pitch.scores = received_message[2]
                    self._football_pitch.reset_pitch_after_goal()
            elif self._football_pitch.player_id == 2:
                message_to_send = (self._football_pitch.player2.get_players_coord(), self._football_pitch.player2.get_ball_push_velocities())
                received_message = self._network.send(message_to_send)
                self._football_pitch.player1.set_players_coord(received_message[0])
                self._football_pitch.ball.coord = received_message[1]
                if received_message[2] != self._football_pitch.scores:
                    self._football_pitch.scores = received_message[2]
                    self._football_pitch.reset_pitch_after_goal()

    def game_loop(self):
        """
        Main loop of the game on client side
        """
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
