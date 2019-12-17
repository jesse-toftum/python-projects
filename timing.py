import math
import numpy as np
import time

from matplotlib import pyplot as plt
from scipy import optimize
from sklearn import metrics


REPETITIONS = 1000
DURATION = 1000
SIZE = 1023
PLOT = True
LIMIT = 2 ** 8
MULT = 2

def main():
    # choice = int(input("Enter choice (0-10): "))
    for choice in range(9, 10):
        if choice == 0:
            print("Time single binary search for last element in array")
            print(f"{time_binary_search_1(SIZE)} msecs\n")
        elif choice == 1:
            print(f"Time {REPETITIONS} searches, average them")
            print(f"{time_binary_search_2(SIZE)} msecs\n")
        elif choice == 2:
            print(f"Time loop itself doing {REPETITIONS} searches, average them")
            print(f"{time_binary_search_3(SIZE)} msecs\n")
        elif choice == 3:
            print(f"Time loop itself doing {REPETITIONS} searches, average them, subtract overhead")
            print(f"{time_binary_search_4(SIZE, True)} msecs\n")
        elif choice == 4:
            print(f"Time loop itself for {DURATION} msecs, average them, subtract overhead")
            print(f"{time_binary_search_5(SIZE, True)} msecs\n")
        elif choice == 5:
            print(f"Time loop itself for {DURATION} msecs looking up all items, average, subtract overhead")
            print(f"{time_binary_search_6(SIZE, True)} msecs\n")
        elif choice == 6:
            print(f"Time loop itself for {DURATION} msecs looking up all items, average, subtract overhead using a process timer")
            print(f"{time_binary_search_7(SIZE, True)} msecs\n")
        elif choice == 7:
            print(f"Time loop itself for {DURATION} msecs, average them, subtract overhead for various sizes")
            size = 16
            print(f"{'Size':<16} {'Time (msec)':<16} {'Delta (msec)':<16} {'Ratio':<16}")
            previous_time = 0
            x_vals = []
            y_vals = []
            iteration = 0
            while size < LIMIT:
                size *= MULT
                size = round(size)
                current_time = time_binary_search_5(size - 1)
                print(f"{size:<16} {current_time:<16.8f} ", end="")
                if iteration > 0:
                    print(f"{current_time - previous_time:<16.8f} {current_time/previous_time:<16.8f}")
                else:
                    print()
                previous_time = current_time
                x_vals.append(size)
                y_vals.append(current_time)
                iteration += 1
            if PLOT:
                plt.plot(x_vals, y_vals, label="test1")
            print()
        elif choice == 8:
            print(f"Time loop itself for {DURATION} msecs looking up all items, average, subtract overhead for various sizes")
            size = 16
            print(f"{'Size':<16} {'Time (msec)':<16} {'Delta (msec)':<16} {'Ratio':<16}")
            previous_time = 0
            x_vals = []
            y_vals = []
            iteration = 0
            while size < LIMIT:
                size *= MULT
                size = round(size)
                current_time = time_binary_search_6(size - 1)
                print(f"{size:<16} {current_time:<16.8f} ", end="")
                if iteration > 0:
                    print(f"{current_time - previous_time:<16.8f} {current_time/previous_time:<16.8f}")
                else:
                    print()
                previous_time = current_time
                x_vals.append(size)
                y_vals.append(current_time)
                iteration += 1
            if PLOT:
                plt.plot(x_vals, y_vals, label="test2")
            print()
        elif choice == 9:
            print(f"Time loop itself for {DURATION} msecs looking up all items, average, subtract overhead using a process timer for various sizes")
            size = 16
            print(f"{'Size':<16} {'Time (msec)':<16} {'Delta (msec)':<16} {'Ratio':<16}")
            previous_time = 0
            x_vals = []
            y_vals = []
            iteration = 0
            while size < LIMIT:
                size *= MULT
                size = round(size)
                current_time = time_binary_search_7(size - 1)
                print(f"{size:<16} {current_time:<16.8f} ", end="")
                if iteration > 0:
                    print(f"{current_time - previous_time:<16.8f} {current_time/previous_time:<16.8f}")
                else:
                    print()
                previous_time = current_time
                x_vals.append(size)
                y_vals.append(current_time)
                iteration += 1
            if PLOT:

                plt.plot(x_vals, y_vals, label="test3")
            print()
        elif choice == 10:
            print("Average time for linear search for last element for various sizes")
            size = 16
            print(f"{'Size':<16} {'Time (msec)':<16} {'Delta (msec)':<16} {'Ratio':<16}")
            previous_time = 0
            x_vals = []
            y_vals = []
            iteration = 0
            while size < LIMIT:
                size *= MULT
                size = round(size)
                current_time = time_linear_search_1(size - 1)
                print(f"{size:<16} {current_time:<16.8f} ", end="")
                if iteration > 0:
                    print(f"{current_time - previous_time:<16.8f} {current_time/previous_time:<16.8f}")
                else:
                    print()
                previous_time = current_time
                x_vals.append(size)
                y_vals.append(current_time)
                iteration += 1
            if PLOT:
                plt.plot(x_vals, y_vals, label="test4")
    if PLOT:
        plt.legend()
        plt.show()

def linear_search(data, item):
    for idx, itm in enumerate(data):
        if itm == item:
            return idx
    return -1

def binary_search(data, item):
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == item:
            return mid
        elif data[mid] < item:
            low = mid + 1
        else:
            high = mid - 1
    return -(low + 1)

def m_secs(time_amount):
    return time_amount * 1000

def time_binary_search_1(size):
    data = [i for i in range(size)]

    start = time.time()
    binary_search(data, size-1)
    stop = time.time()
    final_time = stop - start
    return m_secs(final_time)

def time_binary_search_2(size):
    data = [i for i in range(size)]
    final_time = 0
    for i in range(REPETITIONS):
        start = time.time()
        binary_search(data, size-1)
        stop = time.time()
        final_time += stop - start
    return m_secs(final_time) / REPETITIONS

def time_binary_search_3(size):
    data = [i for i in range(size)]
    start = time.time()
    for i in range(REPETITIONS):
        binary_search(data, size-1)
    stop = time.time()
    final_time = m_secs(stop - start) / REPETITIONS

    return final_time

def time_binary_search_4(size, display_sanity=False):
    data = [i for i in range(size)]

    start = time.time()
    for i in range(REPETITIONS):
        binary_search(data, size-1)
    stop = time.time()
    final_time = m_secs(stop - start) / REPETITIONS

    overhead_start = time.time()
    for i in range(REPETITIONS):
        # binary_search(data, size-1)
        pass
    overhead_stop = time.time()
    overhead_time = m_secs(overhead_stop - overhead_start) / REPETITIONS

    if display_sanity:
        print(f"    Total avg:    {final_time} msecs")
        print(f"    Overhead avg: {final_time} msecs")


    return final_time - overhead_time

def time_binary_search_5(size, display_sanity=False):
    data = [i for i in range(size)]

    repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        start = time.time()
        for i in range(repetitions):
            binary_search(data, size-1)
        stop = time.time()
        elapsed = m_secs(stop - start)
    final_time = elapsed / repetitions

    # repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        overhead_start = time.time()
        for i in range(repetitions):
            # binary_search(data, size-1)
            pass
        overhead_stop = time.time()
        elapsed = m_secs(overhead_stop - overhead_start)
    overhead_time = elapsed / repetitions

    if display_sanity:
        print(f"    Total avg:    {final_time} msecs")
        print(f"    Overhead avg: {final_time} msecs")


    return final_time - overhead_time

def time_binary_search_6(size, display_sanity=False):
    data = [i for i in range(size)]

    repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        start = time.time()
        for i in range(repetitions):
            for item in data:
                binary_search(data, item)
        stop = time.time()
        elapsed = m_secs(stop - start)
    final_time = elapsed / repetitions / size

    # repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        overhead_start = time.time()
        for i in range(repetitions):
            for item in data:
                # binary_search(data, item)
                pass
        overhead_stop = time.time()
        elapsed = m_secs(overhead_stop - overhead_start)
    overhead_time = elapsed / repetitions / size

    if display_sanity:
        print(f"    Total avg:    {final_time} msecs")
        print(f"    Overhead avg: {final_time} msecs")


    return final_time - overhead_time

def time_binary_search_7(size, display_sanity=False):
    data = [i for i in range(size)]

    repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        start = time.process_time()
        for i in range(repetitions):
            for item in data:
                binary_search(data, item)
        stop = time.process_time()
        elapsed = m_secs(stop - start)
    final_time = elapsed / repetitions / size

    # repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        overhead_start = time.process_time()
        for i in range(repetitions):
            for item in data:
                # binary_search(data, item)
                pass
        overhead_stop = time.process_time()
        elapsed = m_secs(overhead_stop - overhead_start)
    overhead_time = elapsed / repetitions / size

    if display_sanity:
        print(f"    Total avg:    {final_time} msecs")
        print(f"    Overhead avg: {final_time} msecs")


    return final_time - overhead_time

def time_linear_search_1(size, display_sanity=False):
    data = [i for i in range(size)]

    repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        start = time.process_time()
        for i in range(repetitions):
            for item in data:
                linear_search(data, item)
        stop = time.process_time()
        elapsed = m_secs(stop - start)
    final_time = elapsed / repetitions / size

    # repetitions = 1
    elapsed = 0
    while elapsed < DURATION:
        repetitions *= 2
        overhead_start = time.process_time()
        for i in range(repetitions):
            for item in data:
                # linear_search(data, item)
                pass
        overhead_stop = time.process_time()
        elapsed = m_secs(overhead_stop - overhead_start)
    overhead_time = elapsed / repetitions / size

    if display_sanity:
        print(f"    Total avg:    {final_time} msecs")
        print(f"    Overhead avg: {final_time} msecs")


    return final_time - overhead_time

def o_linear(x, a, b):
    return a * x + b

def o_quadratic(x, a, b):
    return a * x ** 2 + b

def o_cubic(x, a, b):
    return a * x ** 3 + b

def o_exponential(x, a, b):
    return a ** x + b

def o_power(x, a, b):
    return x ** a + b

def o_factorial(x, a, b):
    return a * math.factorial(x) + b

def o_logn(x, a, b):
    return a * math.log2(x) + b

def o_lognsquared(x, a, b):
    return a * math.log2(x) ** 2 + b

def o_nlognsquared(x, a, b):
    return a * x * math.log2(x) ** 2 + b

def r2(function, params, x_data, y_data):
    return metrics.r2_score(y_data, function(x_data, params[0], params[1]))

def find_best_fit(x_data, y_data):
    best_r = float('-inf')
    best_function = ""
    best_params = ()
    for name, function in functions.items():
        params, params_covariance = optimize.curve_fit(function, x_data, y_data)
        print(r2(function, params, x_data, y_data))

functions = {"n*log(n)": lambda x, a, b: a * x * math.log2(x) + b,
             "log(n)": lambda x, a, b: a * math.log2(x) + b,
             }
# $\mathcal{O}$
main()
