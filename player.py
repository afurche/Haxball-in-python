from team_player import TeamPlayer
from typing import Tuple
from setup_variables import *
from math import sqrt


class Player:
    def __init__(self, team_start_position, game_ball):
        self._team = [TeamPlayer(coord[0], coord[1]) for coord in team_start_position]
        self._team[0].is_current = True
        self._team[1].is_goalkeeper = True
        self._game_ball = game_ball

    def move_footballer(self, player_id):
        for index, team_player in enumerate(self._team):
            player_goalkeeper_x = BLUE_TEAM_GOALKEEPER_X if player_id == 1 else RED_TEAM_GOALKEEPER_X
            player_defender_x = BLUE_TEAM_DEFENDER_X if player_id == 1 else RED_TEAM_DEFENDER_X
            if team_player.is_current:
                team_player.move()
            else:
                team_player.advanced_move_automatic(player_goalkeeper_x, player_defender_x, self._game_ball)

    @property
    def team(self):
        return self._team

    @property
    def current_player(self):
        for player in self._team:
            if player.is_current:
                return player

    def get_ball_push_velocities(self):
        return [team_player.ball_push_velocity for team_player in self._team]

    def is_goalkeeper_assigned(self):
        for team_player in self._team:
            if team_player.is_goalkeeper:
                return True
        return False

    def assign_position_for_off_ball_team_players(self):
        counter = 0
        for team_player in self._team:
            if not team_player.is_current:
                if counter == 0:
                    team_player.is_goalkeeper = True
                else:
                    team_player.is_goalkeeper = False
                counter += 1

    def change_to_player_closest_to_ball(self, ball_coord: (int, int)) -> None:
        distance_dict = {index: sqrt(abs(ball_coord[0] - player.coord[0]) ** 2 + abs(ball_coord[1] - player.coord[1]) ** 2) for index, player in enumerate(self._team)}
        min_distance_player_index = min(distance_dict, key=lambda k: distance_dict.get(k))
        tmp_old_current_player = self.current_player
        self.current_player.is_current = False
        if not self.is_goalkeeper_assigned():
            tmp_old_current_player.is_goalkeeper = True
        self._team[min_distance_player_index].is_current = True
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
            team_player.returned_to_goalkeeper_position = False
            team_player.returned_to_defender_position = False
