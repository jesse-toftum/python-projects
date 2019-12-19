from functools import lru_cache
import gc
import math
import random
import time

import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from sklearn import metrics


class SimpleTiming:
    def __init__(self,
                 plot=True,
                 print_out=True,
                 max_time: float = 60,
                 duration: float = 1,
                 n_iterator=None,
                 data_or_generator=None,
                 selector=None,
                 arg_dict={'n': 'n',
                           'item_choice': False,
                           'data': False},
                 ):

        # User options
        self.plot = plot
        self.print_out = print_out
        self.max_time = max_time
        self.duration = duration
        self.n_iterator = n_iterator
        self.data_or_generator = data_or_generator
        self.selector = selector
        self.arg_dict = arg_dict

        # Default Values
        self.x_vals = []
        self.y_vals = []
        self.shared_dict = dict()
        self.a = None
        self.b = None
        self.r_2 = None

        # Conditional setup
        if self.selector is None:
            self.selector = random.choice
        if self.n_iterator is None:
            self.n_iterator = self.built_in_iterator()
        self.uses_items = self.arg_dict['item_choice'] is not False
        self.uses_data = self.arg_dict['data'] is not False
        self.named_n = self.arg_dict['n']

        self.data_generator_exists = False
        if data_or_generator is not None:
            try:
                iterator = iter(data_or_generator)
            except TypeError:
                self.data_generator_exists = True
            else:
                self.data_generator_exists = False

        # Function lookup
        self.functions = {
            "log(n)": np.vectorize(lambda x, a, b: a * math.log2(x) + b),
            "log(n)^2": np.vectorize(lambda x, a, b: a * math.log2(x) ** 2 + b),
            "n": np.vectorize(lambda x, a, b: a * x + b),
            "n*log(n)": np.vectorize(lambda x, a, b: a * x * math.log2(x) + b),
            "n*log(n)^2": np.vectorize(lambda x, a, b: a * x * math.log2(x) ** 2 + b),
            "n^2": np.vectorize(lambda x, a, b: a * x ** 2 + b),
            "n^3": np.vectorize(lambda x, a, b: a * x ** 3 + b),
            "2^n": np.vectorize(lambda x, a, b: a * 2 ** x + b),
            # "n^a": np.vectorize(lambda x, a, b: x ** a + b),
            # "a^n": np.vectorize(lambda x, a, b: a ** x + b),
            "n!": np.vectorize(lambda x, a, b: a * math.factorial(x) + b),
        }

    def function_label(self, function_name):
        function_labels = {
            "log(n)": f'${self.b:.6f}+{self.a:.8f}$log$(n)$ with $r^2={self.r_2:.4f}$',
            "log(n)^2": f'${self.b:.6f}+{self.a:.8f}$log$(n)^2$ with $r^2={self.r_2:.4f}$',
            "n": f'${self.b:.6f}+{self.a:.8f}n$ with $r^2={self.r_2:.4f}$',
            "n*log(n)": f'${self.b:.6f}+{self.a:.8f}n$log$(n)$ with $r^2={self.r_2:.4f}$',
            "n*log(n)^2": f'${self.b:.6f}+{self.a:.8f}n$log$(n)^2$ with $r^2={self.r_2:.4f}$',
            "n^2": f'${self.b:.6f}+{self.a:.8f}n^2$ with $r^2={self.r_2:.4f}$',
            "n^3": f'${self.b:.6f}+{self.a:.8f}n^3$ with $r^2={self.r_2:.4f}$',
            "2^n": f'${self.b:.6f}+2^{self.a:.8f}x$ with $r^2={self.r_2:.4f}$',
            # "n^a": f'${self.b:.6f}+n^{self.a:.8f}$ with $r^2={self.r_2:.4f}$',
            # "a^n": f'${self.b:.6f}+{self.a:.8f}^n$ with $r^2={self.r_2:.4f}$',
            "n!": f'${self.b:.6f}+{self.a:.8f}n!$ with $r^2={self.r_2:.4f}$',
        }
        return function_labels[function_name]

    def built_in_iterator(self):
        n = 16
        while True:
            yield n
            n <<= 1

    def time_function(self,
                      function_to_time,
                      *args, **kwargs):
        iteration = 0
        previous_time = 0
        test_start = time.time()
        if self.data_generator_exists:
            data = self.data_or_generator

        if self.print_out:
            self.print_header()

        # Disable garbage collection so it doesn't interfere with timing
        gc.disable()
        while time.time() - self.max_time < test_start:
            try:
                n = next(self.n_iterator)
                self.shared_dict[self.named_n] = n

                if self.data_or_generator is None:
                    current_time = self.time_n(function_to_time,
                                               *args, **kwargs)

                else:
                    if self.arg_dict['item_choice'] is not False:
                        for item in self.selector(data):
                            time_for_n(**{self.arg_dict['item_choice']: item})

                self.x_vals.append(n)
                self.y_vals.append(current_time)
                if self.print_out:
                    self.print_info(n, current_time, previous_time, iteration)
                previous_time = current_time
                iteration += 1
            except StopIteration:
                # Iterator exhausted: stop the loop
                break

        # Re-enable garbage collection now that timing is done
        gc.enable()
        if self.plot:
            self.plot_and_fit(label=f'Samples from {function_to_time.__name__}')
            plt.style.use('ggplot')
            plt.legend()
            plt.show()

    def time_n(self, function_to_time, *args, **kwargs):

        # Repeat the timing of the function, but only until the number of
        # repetitions surpasses duration
        repetitions = 1
        elapsed = 0
        while elapsed < self.duration:
            repetitions *= 2
            start = time.process_time()
            for _ in range(repetitions):
                result = function_to_time(*args, **self.shared_dict, **kwargs)
            end = time.process_time()
            elapsed = end - start
        final_time = elapsed / repetitions  # / size

        # Do the same timing as before, but don't actually call the function
        # This basically calculates overhead just due to running loops
        repetitions = 1
        elapsed = 0
        while elapsed < self.duration:
            repetitions *= 2
            start = time.process_time()
            for _ in range(repetitions):
                # result = function_to_time(*args, **kwargs)
                pass
            end = time.process_time()
            elapsed = end - start
        overhead_time = elapsed / repetitions  # / size

        # Subtract the overhead
        timing_for_n = final_time - overhead_time

        # print(f"{function_to_time.__name__} ran in {timing_for_n:.8f} s")
        return timing_for_n

    @classmethod
    def print_header(cls):
        """
        Prints the header for the timings in an aligned manner.
        """
        print(f"{'Size':<16} {'Time (sec)':<16} {'Delta (sec)':<16} {'Ratio':<16}")

    def print_info(self, n, current_time, previous_time, iteration):
        """
        Prints information of the timings, in line with the other timings.
        """
        print(f"{n:<16} {current_time:<16.8f} ", end="")
        if iteration > 0:
            print(
                f"{current_time - previous_time:<16.8f} {current_time/previous_time:<16.8f}")
        else:
            print()

    def plot_and_fit(self, label):
        """
        Simultaneously plots recorded values and does its best to fit and plot an
        asymptotically accurate curve.
        """
        function_name, params, r2 = self.find_best_fit()
        print(f'Best fit found to be O({function_name})')
        plt.plot(self.x_vals, self.y_vals, label=label, linestyle='--')
        x_vals = np.linspace(self.x_vals[0], self.x_vals[-1], 1_000)
        y_vals = self.functions[function_name](x_vals, params[0], params[1])
        self.a = params[0]
        self.b = params[1]
        self.r_2 = r2
        plt.plot(x_vals,
                 y_vals,
                 label=self.function_label(function_name))

    def get_r_2(self, function, params):
        """
        Returns the coefficient of determination for a fit given the x values,
        the y values, the function, and the parameters of the function.
        """
        return metrics.r2_score(self.y_vals, function(self.x_vals, params[0], params[1]))

    def find_best_fit(self):
        """
        Calculates the line of best fit given x and y data.
        """
        best_r = float('-inf')
        best_function = ""
        best_params = ()
        for name, function in self.functions.items():
            try:
                params, _ = optimize.curve_fit(function,
                                               self.x_vals,
                                               self.y_vals,
                                               p0=[1, 1])
                current_r2 = self.get_r_2(function, params)
                # print(f'{name} gives {current_r2}')
                if current_r2 > best_r:
                    # print(f'New best! {name} replaces {best_function}, '
                    #       f'with {current_r2:.6f} > {best_r:.6f}')
                    best_function = name
                    best_params = params
                    best_r = current_r2
            except OverflowError:
                pass
        # print(best_function, best_params)
        return best_function, best_params, best_r



def fib(n):
    for _ in range(n):
        for _ in range(n):
            pass
    return n


SimpleTiming(duration=1, max_time=60).time_function(fib)
