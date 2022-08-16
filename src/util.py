def str_to_rgb(str_rgb_color: str) -> tuple:
    return tuple([int(color) for color in str_rgb_color.split(", ")])