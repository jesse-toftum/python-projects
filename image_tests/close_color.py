import pyximport; pyximport.install()

from color_test import ImageGeneration

import time
import random


def grow(optional=None, progress_bar=True):
    # print(f'enter start {postfix}')
    # r = random.uniform(1.0, 5.0)
    # p = random.uniform(0.5, 5.0)
    r = 1.0
    p = 1.0
    dim_x = 1920
    dim_y = 1080
    seeds = 1
    start = time.time()
    image_generator = ImageGeneration(dim_x, dim_y,
                                      seeds, radius=r, power=p,
                                      random_seed=optional,
                                      progress_bar=progress_bar)
    image_generator.fit_colors()
    end = time.time()
    # print(dim_x * dim_y)
    print(f'{end-start}\n')
    image_generator.save(
        f"image_tests/images/grow/1/{dim_x}x{dim_y}_{optional}_radius_"
        f"{r:.1f}_power_{p:.1f}_final.png")
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
