
import colorsys
import math
import random
import time
import threading


import numpy as np


from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from PIL import Image, ImageDraw
from cmath import phase
from tqdm import tqdm
import sys


def normal_round(n):
    if n - np.floor(n) < 0.5:
        return int(np.floor(n))
    return int(np.ceil(n))


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


def get_closest_color(color, color_list):
    champion_distance = 999_999_999_999
    champion_color = (0, 0, 0)
    for i in color_list:
        current_distance = color_distance(color, i)
        if current_distance < champion_distance:
            champion_distance = current_distance
            champion_color = i
    return champion_color


# def is_perfect_square(x):

#     # Find floating point value of
#     # square root of x.
#     sr = np.sqrt(x)

#     # If square root is an integer
#     return (sr - np.floor(sr)) == 0


class ImageGeneration:
    def __init__(self, dim_x, dim_y, seeds, radius=1.5, p=2, min_value_color=0,
                 random_seed=None, progress_bar=True):
        if random_seed is not None:
            random.seed(random_seed)
        self.seeds = seeds
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.p = float(p)
        self.radius = float(radius)
        self.progress_bar = progress_bar

        self.img = Image.new('RGB', (dim_x, dim_y))
        self.draw = ImageDraw.Draw(self.img)

        self.color_list = self.populate_colors(unique_colors=dim_x*dim_y,
                                               min_value=min_value_color)
        random.shuffle(self.color_list)

        if dim_x * dim_y < 255 ** 3:
            self.color_list = set(self.color_list)

        self.image_array = []
        self.remaining_pixels = set()

        for x in range(dim_x):
            self.image_array.append([])
            for y in range(dim_y):
                self.image_array[x].append((-1, -1, -1))
                # remaining_pixels.append((x, y))

        for _ in range(seeds):
            color = self.color_list.pop()
            rand_x = random.randint(0, dim_x - 1)
            rand_y = random.randint(0, dim_y - 1)
            self.add_pixel(rand_x, rand_y, color)

    def add_pixel(self, x, y, color):
        self.image_array[x][y] = color
        lower_x = max(0, normal_round(x - self.radius))
        upper_x = min(self.dim_x - 1, normal_round(x + self.radius)) + 1
        lower_y = max(0, normal_round(y - self.radius))
        upper_y = min(self.dim_y - 1, normal_round(y + self.radius)) + 1

        for i in range(lower_x, upper_x):
            for j in range(lower_y, upper_y):
                if (i, j) in self.remaining_pixels \
                        or self.image_array[i][j][0] != -1:
                    continue
                x_dist = np.abs(i-x)
                y_dist = np.abs(j-y)
                reg_dist = np.power(
                    (np.power(x_dist, self.p)
                     + np.power(y_dist, self.p)), (1/self.p))
                if reg_dist <= self.radius:
                    self.remaining_pixels.add((i, j))

    def get_neighbor(self, x, y):
        neighbor_list = []
        lower_x = max(0, normal_round(x - self.radius))
        upper_x = min(self.dim_x - 1, normal_round(x + self.radius)) + 1
        lower_y = max(0, normal_round(y - self.radius))
        upper_y = min(self.dim_y - 1, normal_round(y + self.radius)) + 1

        for i in range(lower_x, upper_x):
            for j in range(lower_y, upper_y):
                if self.image_array[i][j][0] == -1:
                    continue
                x_dist = abs(i-x)
                y_dist = abs(j-y)
                reg_dist = (x_dist ** self.p + y_dist ** self.p) ** (1/self.p)
                if reg_dist <= self.radius:
                    neighbor_list.append((i, j))
        return random.choice(neighbor_list)

    # def methoddddd(self,
    #                lower_x: int,
    #                upper_x: int,
    #                lower_y: int,
    #                upper_y: int,
    #                x: int, y: int):
    #     neighbor_list = np.array([(-1, -1)])
    #     # !
    #     # !
    #     # !
    #     # ! Vectorize this
    #     # !
    #     # !
    #     # !
    #     for i in range(lower_x, upper_x):
    #         for j in range(lower_y, upper_y):
    #             if self.image_array[i][j][0] == -1:
    #                 continue
    #             x_dist = np.abs(i-x)
    #             y_dist = np.abs(j-y)

    #             reg_dist = (x_dist ** self.p + y_dist ** self.p) ** (1/self.p)
    #             # if reg_dist <= self.radius:
    #             #     return (i, j)
    #             if reg_dist <= self.radius:
    #                 # print(i, j)
    #                 neighbor_list = np.append(neighbor_list, (i, j))
    #     # !
    #     # !
    #     # !
    #     # ! Vectorize this
    #     # !
    #     # !
    #     # !
    #     # for i in range(5):
    #     #     print()
    #     # print(neighbor_list)
    #     # for i in range(5):
    #     #     print()
    #     neighbor_list = np.delete(neighbor_list, (-1, -1))
    #     print(neighbor_list)
    #     choice = random.choice(neighbor_list)
    #     return choice

    @classmethod
    def populate_colors(cls, max_pixel=255, unique_colors=256**2, min_value=0):
        """Returns evenly spaced colors"""
        all_colors = []
        max_value = max_pixel ** 3
        dim_1_colors = np.linspace(min_value, max_value, num=unique_colors)
        for i in dim_1_colors:
            red = int(i % max_pixel)
            green = int((i // max_pixel) % max_pixel)
            blue = int(i // (max_pixel ** 2))
            all_colors.append((red, green, blue))
        return all_colors

    def fit_colors(self):
        last_value = self.dim_x * self.dim_y - 1 - self.seeds

        if self.progress_bar:
            for i in tqdm(range(last_value)):
                self.propagate()
        else:
            for i in range(last_value):
                self.propagate()

            # if is_perfect_square(i):
            #     for x in range(self.dim_x):
            #         for y in range(self.dim_y):
            #             self.draw.point((x, y), self.image_array[x][y])
            #     self.save(f"image_tests/images/growth/{i}.png")
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                self.draw.point((x, y), self.image_array[x][y])

    def propagate(self):
        chosen = random.choice(tuple(self.remaining_pixels))
        x, y = chosen
        # print(len(remaining_pixels))

        neighbor = self.get_neighbor(*chosen)
        n_x, n_y = neighbor
        color = get_closest_color(
            self.image_array[n_x][n_y], self.color_list)
        self.add_pixel(x, y, color)

        self.remaining_pixels.remove(chosen)
        self.color_list.remove(color)

        # if is_perfect_square(i):
        #     for x in range(self.dim_x):
        #         for y in range(self.dim_y):
        #             self.draw.point((x, y), self.image_array[x][y])
        #     self.save(f"image_tests/images/growth/{i}.png")

    def show(self, *args, **kwargs):
        self.img.show(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.img.save(*args, **kwargs)


def grow(optional=None, progress_bar=True):
    # print(f'enter start {postfix}')
    # r = random.uniform(1.0, 5.0)
    # p = random.uniform(0.5, 5.0)
    r = 1.0
    p = 1.0
    dim_x = dim_y = 128
    seeds = 1
    start = time.time()
    image_generator = ImageGeneration(dim_x, dim_y,
                                      seeds, radius=r, p=p,
                                      random_seed=optional,
                                      progress_bar=progress_bar)
    image_generator.fit_colors()
    end = time.time()
    # print(dim_x * dim_y)
    print(f'{end-start}\n')
    image_generator.save(f"image_tests/temp/{dim_x}x{dim_y}_{optional}_radius_{r:.5f}_power_{p:.5f}.png")
    #     f"image_tests/images/out_min_power_{i}.png")
    # print(f'exit start {postfix}')
    # image_generator.show()


# image_generator = ImageGeneration(5, 5, 5, progress_bar=False)
# image_generator.fit_colors()
# num_threads = 2
# for i in range(num_threads):
#     progress_bar = (i == num_threads - 1)
#     seed_to_use = random.randint(0, 1_000_000_000)
#     thread = threading.Thread(target=grow, args=(seed_to_use, progress_bar))
#     thread.start()

seed_to_use = random.randint(0, 1_000_000_000)
grow(optional=seed_to_use)

# Speedup options:
# //Write in another language
# *Optimize for interpreter
# *JIT Compilation
# ?Parallelization
