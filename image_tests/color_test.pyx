#cython: language_level=3
import random
import time

import numpy as np
from numba.typed import List
# from libcpp cimport bool
from PIL import Image, ImageDraw
from tqdm import tqdm

from numba_funcs import get_closest_color, is_perfect_square, normal_round

# TODO: Break this code back down from class, then Cythonize it from there
cdef class ImageGeneration:
    def __init__(self,
                 dim_x, dim_y,
                 seeds,
                 radius=1.0, power=1.0,
                 min_value_color=0,
                 random_seed=None,
                 progress_bar=True):

        if random_seed is not None:
            random.seed(random_seed)
            self.random_seed = random_seed
        else:
            self.random_seed = 42
            random.seed(42)

        self.seeds = seeds
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.power = float(power)
        self.radius = float(radius)
        self.progress_bar = progress_bar

        self.img = Image.new('RGB', (dim_x, dim_y))
        self.draw = ImageDraw.Draw(self.img)

        self.color_list = self.populate_colors(unique_colors=dim_x*dim_y,
                                               min_value=min_value_color)
        random.shuffle(self.color_list)

        if dim_x * dim_y < 255 ** 3:
            self.color_list = set(self.color_list)

        # self.color_list = List()
        temp = List()
        for i in self.color_list:
            temp.append(i)
        self.color_list = temp
        del temp

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
                    (np.power(x_dist, self.power)
                     + np.power(y_dist, self.power)), (1/self.power))
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
                reg_dist = (x_dist ** self.power + y_dist **
                            self.power) ** (1/self.power)
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

    #             reg_dist = (x_dist**self.p + y_dist**self.p) ** (1/self.p)
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
                self.propagate(i)
        else:
            for i in range(last_value):
                self.propagate(i)

        for x in range(self.dim_x):
            for y in range(self.dim_y):
                self.draw.point((x, y), self.image_array[x][y])

    def propagate(self, iteration):
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

        # if is_perfect_square(iteration):
        #     for x in range(self.dim_x):
        #         for y in range(self.dim_y):
        #             self.draw.point((x, y), self.image_array[x][y])
        #     self.save(
        #         f"image_tests/images/grow/1/{self.dim_x}x{self.dim_y}_"
        #         f"{self.random_seed}_radius_{self.radius:.1f}_power_"
        #         f"{self.p:.1f}_{np.sqrt(iteration)}.png")

    def show(self, *args, **kwargs):
        self.img.show(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.img.save(*args, **kwargs)
