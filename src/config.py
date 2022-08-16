import json

from util import str_to_rgb

target_score: int = 1600
track_level: int = 3
number_of_generations: int = 30
development_mode: bool = True
replace_old_model: bool = False
add_reward_lines: bool = False

# Checkpoint filename prefix
checkpoint_location = "./checkpoint"
filename_prefix = "neat-checkpoint-"

# Font file
font_config: str = "./font/FreeSansBold.ttf"

# JSON configuration file
with open("./config/game_config.json") as config_file:
    json_config: json = json.load(config_file)
    config_file.close()

# TXT configuration file, NEAT
txt_config: str = "./config/neat_config.txt"

# Display configuration
fps: int = json_config["display"]["fps"]
display_width: int = json_config["display"]["width"]
display_height: int = json_config["display"]["height"]

# Spritesheet configuration
car_spritesheet: str = json_config["spritesheet"]["car"]
track_spritesheet: str = json_config["spritesheet"]["tracks"][track_level - 1]

# Layer configuration
car_layer: int = json_config["layer"]["car"]
track_layer: int = json_config["layer"]["track"]

# Car configuration
car_speed: int = json_config["car"]["speed"]
car_angle: int = json_config["car"]["angle"]
car_rotation_velocity: float = json_config["car"]["rotation-velocity"]
car_direction: int = json_config["car"]["direction"]
car_radar_angles: list[int] = json_config["car"]["radar"]["angles"]["ultra-wide"]
collision_range: int = json_config["car"]["collision"]["range"]

# Track configuration
car_position_x_coord: int = json_config["track"][f"lvl-{track_level}-setup"]["car-position"]["x-coord"]
car_position_y_coord: int = json_config["track"][f"lvl-{track_level}-setup"]["car-position"]["y-coord"]
radar_range: int = json_config["track"][f"lvl-{track_level}-setup"]["radar-range"]
reward_line_positions: list[list[int]] = json_config["track"][f"lvl-{track_level}-setup"]["reward-line-positions"]
info_start_position_x_coord: int = json_config["track"][f"lvl-{track_level}-setup"]["info-start-position"]["x-coord"]
info_start_position_y_coord: int = json_config["track"][f"lvl-{track_level}-setup"]["info-start-position"]["y-coord"]

# Color configuration
grass_color: tuple = str_to_rgb(json_config["color"]["grass"])
finish_line_color: tuple = str_to_rgb(json_config["color"]["finish-line"])
car_sensor_color: tuple = str_to_rgb(json_config["color"]["car-sensor"])
radar_line_color: tuple = str_to_rgb(json_config["color"]["radar-line"])
radar_sensor_color: tuple = str_to_rgb(json_config["color"]["radar-sensor"])
reward_line_color: tuple = str_to_rgb(json_config["color"]["reward-line"])
text_color: tuple = str_to_rgb(json_config["color"]["text"])
