import socket
from _thread import *
from football_pitch import FootballPitch
from player import Player
from setup_variables import *
import pickle
import pygame
import os


class GameServer:
    def __init__(self, football_pitch):
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Server view')
        self._background_sprite = pygame.image.load(os.path.join('assets', 'haxmap.png'))
        self._red_team_sprite = pygame.image.load(os.path.join('assets', 'red_player.png'))
        self._blue_team_sprite = pygame.image.load(os.path.join('assets', 'blue_player.png'))
        self._ball_sprite = pygame.image.load(os.path.join('assets', 'ball.png'))
        self._clock = pygame.time.Clock()
        self._football_pitch = football_pitch
        self._view_run = True

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._view_run = False

    def blit_players(self):
        for red_player, blue_player in zip(self._football_pitch.player1.team, self._football_pitch.player2.team):
            red_player.draw(self._screen, self._red_team_sprite)
            blue_player.draw(self._screen, self._blue_team_sprite)

    def blit_screen(self):
        self._screen.blit(self._background_sprite, self._background_sprite.get_rect())
        self._football_pitch.ball.draw(self._screen, self._ball_sprite)
        self.blit_players()
        pygame.display.update()

    def game_server_loop(self):
        """
        Handles the loop of the server view of the game also handles ball movement in the game
        :return:
        """
        while self._view_run:
            self._clock.tick(30)
            self._football_pitch.ball.ball_movement()
            self.blit_screen()
            self.event_catcher()


class Server:
    def __init__(self):
        self._server = "172.16.128.171"
        self._port = 5556
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._current_client_id = 0
        self._goal_was_added = False
        self._player1_push_velocities = [[0, 0], [0, 0], [0, 0]]
        self._player2_push_velocities = [[0, 0], [0, 0], [0, 0]]
        try:
            self._sock.bind((self._server, self._port))
        except socket.error as err:
            print(err)
        self._football_pitch = FootballPitch()

    def add_goals_if_scored_goal(self):
        if self._football_pitch.ball.x > 1150 and 270 < self._football_pitch.ball.y < 340 and not self._goal_was_added:
            self._football_pitch.player1_score += 1
            self._goal_was_added = True
            self._player1_push_velocities = [[0, 0], [0, 0], [0, 0]]
            self._player2_push_velocities = [[0, 0], [0, 0], [0, 0]]
            self._football_pitch.ball.reset_ball_after_goal()
        elif self._football_pitch.ball.x < 50 and 270 < self._football_pitch.ball.y < 340 and not self._goal_was_added:
            self._football_pitch.player2_score += 1
            self._player1_push_velocities = [[0, 0], [0, 0], [0, 0]]
            self._player2_push_velocities = [[0, 0], [0, 0], [0, 0]]
            self._goal_was_added = True
            self._football_pitch.ball.reset_ball_after_goal()
        elif self._goal_was_added:
            self._goal_was_added = False

    def client_thread(self, conn, client_id):
        """
        Thread function used for handling a client on a server, server receives and sends data to client

        """
        self._football_pitch.player_id = client_id + 1
        conn.send(pickle.dumps(self._football_pitch))
        while True:
            try:
                data = pickle.loads(conn.recv(512))

                if not data:
                    print(f"Client{client_id} disconnected with server !")
                    break

                if client_id == 0:
                    self._football_pitch.player1.set_players_coord(data[0])

                    self._player1_push_velocities = data[1]

                    message = (self._football_pitch.player2.get_players_coord(), self._football_pitch.ball.coord, self._football_pitch.scores)
                    conn.sendall(pickle.dumps(message))

                elif client_id == 1:
                    self._football_pitch.player2.set_players_coord(data[0])

                    self._player2_push_velocities = data[1]

                    message = (self._football_pitch.player1.get_players_coord(), self._football_pitch.ball.coord, self._football_pitch.scores)
                    conn.sendall(pickle.dumps(message))

            except Exception as e:
                print(f"Server error ! :, {e}")
                break

        print(f"Connection with client {client_id} ended")
        self._current_client_id -= 1
        conn.close()

    def game_server_thread(self):
        game_server = GameServer(self._football_pitch)
        game_server.game_server_loop()

    def ball_handling_thread(self):
        """
        Responsible for handling assignment of proper velocities of game ball and for handling scored goals,
        Ball movement is handled in the game_server_loop method of GameServer
        If the ball has a collision with a team player its velocity is changed to proper value received from client.
        """
        while True:
            for index, team_player in enumerate(self._football_pitch.player1.team + self._football_pitch.player2.team):
                if team_player.circle.colliderect(self._football_pitch.ball.circle):
                    if index < 3:
                        if self._player1_push_velocities[index] != [0, 0]:
                            self._football_pitch.ball.current_velocity = self._player1_push_velocities[index]
                    else:
                        print(index % 3)
                        if self._player2_push_velocities[index % 3] != [0, 0]:
                            self._football_pitch.ball.current_velocity = self._player2_push_velocities[index % 3]

            self.add_goals_if_scored_goal()
            print('')

    def server_run(self):
        """
        Main loop of server
        """
        self._sock.listen(2)
        print("Server Started")
        start_new_thread(self.game_server_thread, ())
        start_new_thread(self.ball_handling_thread, ())
        while True:
            connection, address = self._sock.accept()
            print("Connected to:", address)
            start_new_thread(self.client_thread, (connection, self._current_client_id))
            self._current_client_id += 1


if __name__ == '__main__':
    Server().server_run()
