import colorsys
import math
import random
import time


import numpy as np

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from PIL import Image, ImageDraw
from cmath import phase
from tqdm import tqdm
import sys

DIM_X = DIM_Y = 256


SEEDS = 1
start = time.time()


def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


def color_distance(color_1, color_2):
    dr = (color_1[0] - color_2[0]) ** 2
    dg = (color_1[1] - color_2[1]) ** 2
    db = (color_1[2] - color_2[2]) ** 2
    delta = (dr + dg + db) ** (1/2)
    return delta
    # color_1_rgb = sRGBColor(
    #     color_1[0] / 255, color_1[1] / 255, color_1[2] / 255)
    # color_2_rgb = sRGBColor(
    #     color_2[0] / 255, color_2[1] / 255, color_2[2] / 255)
    # color1_lab = convert_color(color_1_rgb, LabColor)
    # color2_lab = convert_color(color_2_rgb, LabColor)
    # return delta_e_cie2000(color1_lab, color2_lab)

def get_closest_color(color, list_of_colors):
    champion_distance = float('inf')
    champion_color = (0, 0, 0)
    for i in list_of_colors:
        current_distance = color_distance(color, i)
        if current_distance < champion_distance:
            champion_distance = current_distance
            champion_color = i
    return champion_color


def border_has_pixel(x, y, image_array, radius=1.5, p=2):
    found_pixels = []
    lower_x = max(0, normal_round(x-radius))
    upper_x = min(DIM_X - 1, normal_round(x+radius))+1
    lower_y = max(0, normal_round(y-radius))
    upper_y = min(DIM_Y - 1, normal_round(y+radius))+1
    for i in range(lower_x, upper_x):
        for j in range(lower_y, upper_y):
            if not image_array[i][j]:
                continue
            x_dist = abs(i-x)
            y_dist = abs(j-y)
            reg_dist = (x_dist ** p + y_dist ** p) ** (1/p)
            if reg_dist <= radius:
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
        pixel = remaining_pixels.pop()
        image_array[pixel[0]][pixel[1]] = color

    last_value = DIM_X * DIM_Y + 1

    img = Image.new('RGB', dim)
    draw = ImageDraw.Draw(img)


    repeat_count = 0
    for i in tqdm(range(last_value)):
        random.shuffle(remaining_pixels)
        # print(len(remaining_pixels))

        to_remove = False
        color_to_remove = False
        for idx, (x, y) in enumerate(remaining_pixels):
            # print(idx, x, y)
            # Nearest neighbor
            nn = border_has_pixel(x, y, image_array=image_array)
            if nn:
                color = get_closest_color(image_array[nn[0]][nn[1]],
                                          list_of_colors=color_list)
                color_to_remove = color
                # print(idx, x, y, color)
                image_array[x][y] = color
                to_remove = (x, y)
                break

        if to_remove:
            remaining_pixels.remove(to_remove)
        if color_to_remove:
            color_list.remove(color_to_remove)
        if last_value == len(remaining_pixels):
            repeat_count += 1
            # print(f'repeat {repeat_count}')
            print(f'Pixels left: {len(remaining_pixels)}')
            print(f'Colors left: {len(color_list)}\n')
        last_value = len(remaining_pixels)
        if i % 1000 == 0:
            for x in range(DIM_X):
                for y in range(DIM_Y):
                    draw.point((x, y), image_array[x][y])
            img.show()

    img.show()
    img.save("out.png")


main()

end = time.time()
print(end-start)