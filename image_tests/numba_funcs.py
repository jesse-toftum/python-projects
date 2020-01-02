
import numpy as np
from numba import njit


@njit
def normal_round(n):
    if n - np.floor(n) < 0.5:
        return int(np.floor(n))
    return int(np.ceil(n))


@njit
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


@njit
def get_closest_color(color, color_list):
    champion_distance = 999_999_999_999
    champion_color = (0, 0, 0)
    for i in color_list:
        current_distance = color_distance(color, i)
        if current_distance < champion_distance:
            champion_distance = current_distance
            champion_color = i
    return champion_color


@njit
def is_perfect_square(x):

    # Find floating point value of
    # square root of x.
    sr = np.sqrt(x)

    # If square root is an integer
    return (sr - np.floor(sr)) == 0
