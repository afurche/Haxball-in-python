from player import Player
from game_ball import GameBall
from typing import Tuple
from setup_variables import *


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
