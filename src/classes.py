from operator import ne
import sys
import math
import neat
import time
import pygame
from typing import Sequence

from config import *
from cdtypes import *

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((display_width, display_height))
        self.finish: bool = False
        self.score: int = 0
        self.current_generation: int = 1
        self.cars : list = []
        self.genomes: list = []
        self.nets: list = []
        self.scores = []

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

    def add_car(self, car) -> None:
        self.cars.append(GroupSingle(car))
    
    def remove_car(self, car_index: int) -> None:
        self.cars.pop(car_index)
        self.genomes.pop(car_index)
        self.nets.pop(car_index) 
    
    def add_reward_lines(self) -> None:
        for reward_line_position in reward_line_positions:
            pygame.draw.line(self.screen, reward_line_color, (reward_line_position[0], reward_line_position[1]), (reward_line_position[2], reward_line_position[3]), 2)
            pygame.display.update()

    def info(self, current_generation: int, cars_left: int, score: int, best_score: int) -> None:
        font: Font = pygame.font.Font(font_config, 24)

        gen_info: Surface = font.render(f"Gen: {str(current_generation)}", False, text_color)
        gen_info_rect: Rect = gen_info.get_rect()
        gen_info_rect.center = (info_start_position_x_coord, info_start_position_y_coord)
        self.screen.blit(gen_info, gen_info_rect)

        cars_left_info: Surface = font.render(f"Cars left: {str(cars_left)}", False, text_color)
        cars_left_rect: Rect = gen_info.get_rect()
        cars_left_rect.center = (info_start_position_x_coord, info_start_position_y_coord + 30)
        self.screen.blit(cars_left_info, cars_left_rect)

        score_info: Surface = font.render(f"Score: {score} [Best: {best_score}] [Target: {target_score}]", False, text_color)
        score_info_rect: Rect = gen_info.get_rect()
        score_info_rect.center = (info_start_position_x_coord, info_start_position_y_coord + 60)
        self.screen.blit(score_info, score_info_rect)

    def run(self, genomes, config_txt: str) -> None:

        for _, genome in genomes:
            self.add_car(Car(self))
            self.genomes.append(genome)
            self.nets.append(neat.nn.FeedForwardNetwork.create(genome, config_txt))
            genome.fitness = 0


        self.running: bool = True
        self.start_time = time.time()

        while self.running:
            self.events()

            self.screen.blit(pygame.image.load(track_spritesheet), (0, 0))  
            if add_reward_lines:
                self.add_reward_lines()   

            self.info(self.current_generation, len(self.cars), self.score, max(self.scores) if len(self.scores) > 0 else self.score)

            if self.score >= target_score:
                self.running = False
                break

            if len(self.cars) == 0:
                self.current_generation += 1
                self.scores.append(self.score)
                self.score = 0
                break
            else:
                self.score += 1

            # if self.finish:
            #     current_generation += 1
            #     self.cars.clear()
            #     self.genomes.clear()
            #     self.nets.clear()
            #     self.finish = False

            for i, car in enumerate(self.cars):
                if car.sprite.is_crashed:
                    self.genomes[i].fitness -= 1
                    self.remove_car(i)
                else:
                    self.genomes[i].fitness += 1
                    if car.sprite.reward_line_passed:
                        self.genomes[i].fitness += 3
                        car.reward_line_passed = False

            for i, car in enumerate(self.cars):
                output = self.nets[i].activate(car.sprite.data())
                if output[0] > 0.7:
                    car.sprite.direction = 1
                if output[1] > 0.7:
                    car.sprite.direction = -1
                if output[0] <= 0.7 and output[1] <= 0.7:
                    car.sprite.direction = 0

            for car in self.cars:
                car.draw(self.screen)
                car.update()

            pygame.display.update()


class Car(Sprite):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game: Game = game
        self.original_image: Surface = pygame.image.load(car_spritesheet)
        self.image: Surface = self.original_image
        self.rect: Rect = self.image.get_rect(center = (car_position_x_coord, car_position_y_coord))
        self.rotation_velocity: int = car_rotation_velocity
        self.vel_vector: Vector2 = Vector2(1, 0)
        self.direction: int = car_direction
        self.angle: int = car_angle
        self.is_crashed: bool = False
        self.reward_line_passed: bool = False
        # self.drive_state: bool = False
        self.track_passed: bool = False
        self.radars: list[list[int]] = []

    def events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def movement(self) -> None:
        keys: Sequence[bool] = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            self.drive_state = False
            self.direction = 0

        if keys[pygame.K_UP]:
            self.drive_state = True

        if keys[pygame.K_RIGHT]:
            self.direction = 1

        if keys[pygame.K_LEFT]:
            self.direction = -1

    def drive(self) -> None:
        # if self.drive_state:
        #   self.rect.center += self.vel_vector * 6
        self.rect.center += self.vel_vector * car_speed

    def rotate(self) -> None:
        if self.direction == 1:
            self.angle -= self.rotation_velocity
            self.vel_vector.rotate_ip(self.rotation_velocity)
        if self.direction == -1:
            self.angle += self.rotation_velocity
            self.vel_vector.rotate_ip(-self.rotation_velocity)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center = self.rect.center)

    def radar(self, radar_angle: int) -> None:
        range: int = 0
        x_coord: int = int(self.rect.center[0])
        y_coord: int = int(self.rect.center[1])

        while not self.game.screen.get_at((x_coord, y_coord)) == pygame.Color(grass_color[0], grass_color[1], grass_color[2]) and range < radar_range:
            range += 1
            x_coord = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * range)
            y_coord = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * range)

        if development_mode:
            pygame.draw.line(self.game.screen, radar_line_color, self.rect.center, (x_coord, y_coord), 1)
            pygame.draw.circle(self.game.screen, radar_sensor_color, (x_coord, y_coord), 3)

        dist: int = int(math.sqrt(math.pow(self.rect.center[0] - x_coord, 2) + math.pow(self.rect.center[1] - y_coord, 2)))

        self.radars.append([radar_angle, dist])

    def collision(self) -> None:
        range: int = 35
        collision_point_right: list[int, int] = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * range),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * range)]
        collision_point_left: list[int, int] = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * range),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 22)) * range)]


        if self.game.screen.get_at(collision_point_right) == pygame.Color(grass_color[0], grass_color[1], grass_color[2]) \
                or self.game.screen.get_at(collision_point_left) == pygame.Color(grass_color[0], grass_color[1], grass_color[2]):
            self.is_crashed = True
        
        if self.game.screen.get_at(collision_point_right) == pygame.Color(finish_line_color[0], finish_line_color[1], finish_line_color[2]) \
                or self.game.screen.get_at(collision_point_left) == pygame.Color(finish_line_color[0], finish_line_color[1], finish_line_color[2]):
            self.game.finish = True
        
        if self.game.screen.get_at(collision_point_right) == pygame.Color(reward_line_color[0], reward_line_color[1], reward_line_color[2]) \
                or self.game.screen.get_at(collision_point_left) == pygame.Color(reward_line_color[0], reward_line_color[1], reward_line_color[2]):
            self.game.reward_line_passed = True
        
        if development_mode:
            pygame.draw.circle(self.game.screen, car_sensor_color, collision_point_right, 4)
            pygame.draw.circle(self.game.screen, car_sensor_color, collision_point_left, 4)
   
    def data(self) -> list[int]:
        input = [0 for _ in range(0, len(car_radar_angles))]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])

        return input
    
    def done(self) -> None:
        if self.is_crashed:
            print("Car crashed!")
            print(f"Time: {round((time.time() - self.game.start_time), 1)}s")
            pygame.quit()
        
        if self.track_passed and not self.is_crashed:
            print("Car successfully passed the track!")
            print(f"Time: {round((time.time() - self.game.start_time), 1)}s")
            pygame.quit()

    def update(self) -> None:
        # self.movement()
        self.radars.clear()
        self.drive()
        self.rotate()
        
        for radar_angle in car_radar_angles:
            self.radar(radar_angle)

        self.collision()
        # self.done()