import colorsys
import random


import numpy as np

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from PIL import Image, ImageDraw
from cmath import phase
from tqdm import tqdm
import sys

DIM_X = DIM_Y = 64

SEEDS = 1


def color_distance(color_1, color_2):
    color_1_rgb = sRGBColor(
        color_1[0] / 255, color_1[1] / 255, color_1[2] / 255)
    color_2_rgb = sRGBColor(
        color_2[0] / 255, color_2[1] / 255, color_2[2] / 255)
    color1_lab = convert_color(color_1_rgb, LabColor)
    color2_lab = convert_color(color_2_rgb, LabColor)
    return delta_e_cie2000(color1_lab, color2_lab)



def border_has_pixel(x, y, image_array, radius=1.5, p=2):
    found_pixels = []
    for i in range(max(0, int(x-radius)), max(DIM_X - 1, int(x+radius))):
        for j in range(max(0, int(y-radius)), max(DIM_Y - 1, int(y+radius))):
            x_dist = abs(i-x)
            y_dist = abs(j-y)
            reg_dist = (x_dist ** p + y_dist ** p) ** (1/p)
            if reg_dist <= radius and image_array[i][j]:
                found_pixels.append((i, j))
    if found_pixels:
        return random.choice(found_pixels)
    return False


def populate_colors(dim_x, dim_y, max_pixel=255, unique_colors=256**2):
    """Returns evenly spaced colors"""
    all_colors = []
    max_value = max_pixel ** 3
    dim_1_colors = np.linspace(0, max_value, num=unique_colors)
    for i in dim_1_colors:
        red = int(i % max_pixel)
        green = int((i // max_pixel) % max_pixel)
        blue = int(i // (max_pixel ** 2))
        all_colors.append((red, green, blue))
    return all_colors


def main():
    color_list = populate_colors(DIM_X, DIM_Y, unique_colors=DIM_X*DIM_Y)
    print(len(color_list))
    print(DIM_X * DIM_Y)
    dim = (DIM_X, DIM_Y)

    image_array = []
    remaining_pixels = []
    for x in range(DIM_X):
        image_array.append([])
        for y in range(DIM_Y):
            image_array[x].append(False)
            remaining_pixels.append((x, y))

    random.shuffle(color_list)
    random.shuffle(remaining_pixels)

    for _ in range(SEEDS):
        color = color_list.pop()
        rand_x = random.randint(0, DIM_X-1)
        rand_y = random.randint(0, DIM_Y-1)
        image_array[rand_x][rand_y] = color

    while remaining_pixels:
        random.shuffle(remaining_pixels)
        print(len(remaining_pixels))

        to_remove = False

        for idx, (x, y) in enumerate(remaining_pixels):
            result = border_has_pixel(x, y, image_array=image_array)
            if result:
                image_array[x][y] = color_list.pop()
                to_remove = idx
                break

        if to_remove:
            del remaining_pixels[to_remove]

    print()
    print(len(remaining_pixels))
    img = Image.new('RGB', dim)
    draw = ImageDraw.Draw(img)

    for x in range(DIM_X):
        for y in range(DIM_Y):
            draw.point((x, y), image_array[x][y])

    img.show()
    img.save("out.png")


main()
