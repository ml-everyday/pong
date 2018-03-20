import pygame
import numpy as np
import random
import sys
from pygame.locals import *

def main():
    pong = Pong()

class Pong:
    """
    Initialize and run a game of pong with two active players
    """
    def __init__(self):
        pygame.init()
        self.fps = pygame.time.Clock()

        self.width = 200
        self.height = 200
        self.ball_radius = 4
        self.pad_width = self.width//50
        self.pad_height = self.height//5
        self.half_pad_width = self.pad_width//2
        self.half_pad_height = self.pad_height//2
        self.score_panel_height = 50
        self.paddle_velocity = 8

        self.ball_pos = [0,0]
        self.ball_vel = [0,0]
        self.l_paddle_vel = 0
        self.r_paddle_vel = 0
        self.l_paddle_pos = [self.half_pad_width, self.height//2]
        self.r_paddle_pos = [self.width-1-self.half_pad_width, self.height//2]
        self.l_score = 0
        self.r_score = 0

        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.green = (0,255,0)

        self.window = pygame.display.set_mode((self.width, self.height+self.score_panel_height), 0, 32)
        pygame.display.set_caption("PONG")

        self.initialize_game()

    def initialize_game(self):
        self.spawn_ball(random.choice([True, False]))

        while True:
            self.update_game_position()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.keydown(event)
                elif event.type == KEYUP:
                    self.keyup(event)

            pygame.display.update()
            self.fps.tick(40)

    def spawn_ball(self, to_left):
        self.ball_pos = [self.width//2, self.height//2]
        vel_hor = random.randrange(1,4)
        vel_vert = random.randrange(1,4) * random.choice([-1, 1])

        if to_left:
            vel_hor = -vel_hor

        self.ball_vel = [vel_hor, vel_vert]

    def update_game_position(self):
        # move paddles
        self.move_paddle(self.l_paddle_pos, self.l_paddle_vel)
        self.move_paddle(self.r_paddle_pos, self.r_paddle_vel)

        # move ball
        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        self.draw_screen()
        
        # bounce ball off walls
        if int(self.ball_pos[1]) <= self.ball_radius:
            self.ball_vel[1] = -self.ball_vel[1]
        if int(self.ball_pos[1]) >= self.height + 1 - self.ball_radius:
            self.ball_vel[1] = -self.ball_vel[1]

        # bounce ball off paddles
        if int(self.ball_pos[0]) <= self.ball_radius + self.pad_width and int(self.ball_pos[1]) in range(self.l_paddle_pos[1] - self.half_pad_height,self.l_paddle_pos[1] + self.half_pad_height,1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) <= self.ball_radius + self.pad_width:
            self.r_score += 1
            self.spawn_ball(True)
        if int(self.ball_pos[0]) >= self.width + 1 - self.ball_radius - self.pad_width and int(self.ball_pos[1]) in range(self.r_paddle_pos[1] - self.half_pad_height,self.r_paddle_pos[1] + self.half_pad_height,1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) >= self.width + 1 - self.ball_radius - self.pad_width:
            self.l_score += 1
            self.spawn_ball(False)

    def move_paddle(self, paddle_pos, paddle_vel):
        paddle_pos_not_at_boundaries = paddle_pos[1] > self.half_pad_height \
                                       and paddle_pos[1] < self.height - self.half_pad_height
        paddle_pos_top_and_moving_down = paddle_pos[1] == self.half_pad_height \
                                         and paddle_vel > 0
        paddle_pos_bottom_and_moving_up = paddle_pos[1] == self.height - self.half_pad_height \
                                          and paddle_vel < 0
        if paddle_pos_not_at_boundaries or \
           paddle_pos_top_and_moving_down or \
           paddle_pos_bottom_and_moving_up:
           paddle_pos[1] += paddle_vel


    def draw_screen(self):
        self.window.fill(self.black)
        pygame.draw.line(self.window, self.white, [0, self.height + 1], [self.width, self.height + 1], 1)

        # draw ball
        pygame.draw.circle(self.window, self.white, self.ball_pos, self.ball_radius, 0)

        # draw paddles
        pygame.draw.polygon(self.window, self.green, [[self.l_paddle_pos[0] - self.half_pad_width, self.l_paddle_pos[1] - self.half_pad_height], \
                                            [self.l_paddle_pos[0] - self.half_pad_width, self.l_paddle_pos[1] + self.half_pad_height], \
                                            [self.l_paddle_pos[0] + self.half_pad_width, self.l_paddle_pos[1] + self.half_pad_height], \
                                            [self.l_paddle_pos[0] + self.half_pad_width, self.l_paddle_pos[1] - self.half_pad_height]], 0)
        pygame.draw.polygon(self.window, self.green, [[self.r_paddle_pos[0] - self.half_pad_width, self.r_paddle_pos[1] - self.half_pad_height], \
                                            [self.r_paddle_pos[0] - self.half_pad_width, self.r_paddle_pos[1] + self.half_pad_height], \
                                            [self.r_paddle_pos[0] + self.half_pad_width, self.r_paddle_pos[1] + self.half_pad_height], \
                                            [self.r_paddle_pos[0] + self.half_pad_width, self.r_paddle_pos[1] - self.half_pad_height]], 0)

        l_score_font = pygame.font.SysFont("Comic Sans MS", 20)
        l_label = l_score_font.render("Score " + str(self.l_score), 1, (255,255,0))
        self.window.blit(l_label, (30,20+self.height))

        r_score_font = pygame.font.SysFont("Comic Sans MS", 20)
        r_label = r_score_font.render("Score " + str(self.r_score), 1, (255,255,0))
        self.window.blit(r_label, (self.width-30-50,20+self.height))

    def keydown(self, event):
        if event.key == K_UP:
            self.r_paddle_vel = -self.paddle_velocity
        elif event.key == K_DOWN:
            self.r_paddle_vel = self.paddle_velocity
        elif event.key == K_w:
            self.l_paddle_vel = -self.paddle_velocity
        elif event.key == K_s:
            self.l_paddle_vel = self.paddle_velocity

    def keyup(self, event):
        if event.key in (K_w, K_s):
            self.l_paddle_vel = 0
        elif event.key in (K_UP, K_DOWN):
            self.r_paddle_vel = 0


if __name__ == "__main__":
    main()