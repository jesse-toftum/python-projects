"""
A (fairly) simple timing class
"""
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
                 plot: bool = True,
                 print_out: bool = True,
                 max_time: float = 60,
                 duration: float = 1,
                 n_iterator=None,
                 data_or_generator=None,
                 selector=None,
                 arg_dict=None,
                 skip_fits=None
                 ):
        """
        Initializer for SimpleTiming

        Parameters
        ----------
        plot : bool, optional
            Whether to plot recorded values with best fit, by default True
        print_out : bool, optional
            Whether to print out table data, by default True
        max_time : float, optional
            Maximum number of seconds allowed of time before continuing to
            another iteration of timing, by default 60
        duration : float, optional
            Minimum number of seconds required for timing an individual
            iteration of `n`, by default 1
        n_iterator : [type], optional
            If `None`, times in powers of 2, from n=2^4 to n=2^30. Either a
            generator that yields numbers or a collection that can be iterated
            over. By default None
        data_or_generator : [type], optional
            Optional data field that can be pushed to the function to be timed.
            By default None
        selector : [type], optional
            If `None`, defaults to `random.choice` as the selector. Used to
            select the item that is passed to the function that is timed.
            By default None
        arg_dict : dict, optional
            If `None`, defaults to `{'n': 'n',
                             'item': False,
                             'data': False}`.
            Used to specify where a function would take a parameter for varying
            `n`, where it would take data it would use (like sorting), or where
            it would take an item (like searching). By default None
        skip_fits : list, optional
            If `None`, defaults to ,`['n!', 'a^n', 'n^a']`. The `time_function`
            method does not attempt to fit these functions. By default None
        """
        # User options
        self.plot = plot
        self.print_out = print_out
        self.max_time = max_time
        self.duration = duration
        self.data_or_generator = data_or_generator
        self.selector = selector
        self.arg_dict = arg_dict
        self.skip_fits = skip_fits

        # Default Values
        self.x_vals = [int]
        self.y_vals = [int]
        self.shared_dict = dict()
        self.alpha = None
        self.beta = None
        self.r_2 = None
        self.data = None

        # Conditional setup
        if self.arg_dict is None:
            self.arg_dict = {'n': 'n',
                             'item': False,
                             'data': False}
        if self.skip_fits is None:
            self.skip_fits = ['n!', 'a^n', 'n^a']
        if self.selector is None:
            self.selector = random.choice
        self.function_takes_item = self.arg_dict['item'] is not False
        self.function_takes_data = self.arg_dict['data'] is not False
        self.function_takes_n = self.arg_dict['n'] is not False

        if n_iterator is not None:
            try:
                _ = iter(n_iterator)
            except TypeError:
                self.n_iterator = n_iterator
            else:
                self.n_iterator = iter(n_iterator)
        else:
            self.n_iterator = iter([2 ** i for i in range(4, 31)])

        self.data_generator_exists = False
        if data_or_generator is not None:
            try:
                _ = iter(data_or_generator)
            except TypeError:
                self.data_generator_exists = True
            else:
                self.data_generator_exists = False

        self.multiples = ['seconds', 'milliseconds', 'nanoseconds']

        # Function lookup
        self.functions = {
            "log(n)": np.vectorize(lambda x, a, b: a * math.log2(x) + b),
            "log(n)^2": np.vectorize(lambda x, a, b:
                                     a * math.log2(x) ** 2 + b),
            "n": np.vectorize(lambda x, a, b: a * x + b),
            "n*log(n)": np.vectorize(lambda x, a, b: a * x * math.log2(x) + b),
            "n*log(n)^2": np.vectorize(lambda x, a, b:
                                       a * x * math.log2(x) ** 2 + b),
            "n^2": np.vectorize(lambda x, a, b: a * x ** 2 + b),
            "n^3": np.vectorize(lambda x, a, b: a * x ** 3 + b),
            "n^4": np.vectorize(lambda x, a, b: a * x ** 4 + b),
            "2^n": np.vectorize(lambda x, a, b: a * 2 ** x + b),
            "n^a": np.vectorize(lambda x, a, b: x ** a + b),
            "a^n": np.vectorize(lambda x, a, b: a ** x + b),
            "n!": np.vectorize(lambda x, a, b: a * math.factorial(x) + b),
        }

        # Remove functions that should be skipped
        for i in self.skip_fits:
            if i in self.skip_fits:
                del self.functions[i]

    def function_label(self, function_name):
        function_labels = {
            "log(n)": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot $log$(n)$'
                       f' with $r^2={self.r_2:.4f}$'),
            "log(n)^2": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot $(n)^2$'
                         f' with $r^2={self.r_2:.4f}$'),
            "n": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot n$'
                  ' with $r^2={self.r_2:.4f}$'),
            "n*log(n)": (f'${self.beta:.6f}+{self.alpha:.8f}'
                         f'\\cdot n \\cdot $log$(n)$'
                         f' with $r^2={self.r_2:.4f}$'),
            "n*log(n)^2": (f'${self.beta:.6f}+{self.alpha:.8f}'
                           '\\cdot n \\cdot $log$(n)^2$'
                           f' with $r^2={self.r_2:.4f}$'),
            "n^2": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot n^2$'
                    f' with $r^2={self.r_2:.4f}$'),
            "n^3": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot n^3$'
                    f' with $r^2={self.r_2:.4f}$'),
            "n^4": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot n^4$'
                    f' with $r^2={self.r_2:.4f}$'),
            "2^n": (f'${self.beta:.6f}+2^{self.alpha:.8f}x$'
                    f' with $r^2={self.r_2:.4f}$'),
            "n^a": (f'${self.beta:.6f}+n^{self.alpha:.8f}$'
                    f' with $r^2={self.r_2:.4f}$'),
            "a^n": (f'${self.beta:.6f}+{self.alpha:.8f}^n$'
                    f' with $r^2={self.r_2:.4f}$'),
            "n!": (f'${self.beta:.6f}+{self.alpha:.8f}\\cdot n!$'
                   f' with $r^2={self.r_2:.4f}$'),
        }
        # Remove functions that should be skipped
        for i in self.skip_fits:
            if i in self.skip_fits:
                del function_labels[i]

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

        if self.print_out:
            self.print_header()

        # Disable garbage collection so it doesn't interfere with timing
        gc.disable()
        while time.time() - self.max_time < test_start:
            try:
                n = next(self.n_iterator)
                if self.function_takes_n:
                    self.shared_dict[self.arg_dict['n']] = n

                if self.data_or_generator is None:
                    current_time = self.time_n(function_to_time,
                                               *args, **kwargs)

                else:
                    if self.data_generator_exists:
                        self.data = self.data_or_generator(n)
                    else:
                        self.data = self.data_or_generator
                    if self.function_takes_data:
                        self.shared_dict[self.arg_dict['data']] = self.data

                    current_time = self.time_n(function_to_time,
                                               *args, **kwargs)

                self.x_vals.append(n)
                self.y_vals.append(current_time)
                if self.print_out:
                    self.print_info(n, current_time, previous_time, iteration)
                previous_time = current_time
                iteration += 1
            except StopIteration:
                # Iterator exhausted: stop the loop
                break
            except (KeyboardInterrupt, MemoryError) as _:
                break

        # Re-enable garbage collection now that timing is done
        gc.enable()
        if self.plot:
            iteration = 0
            while max(self.y_vals) < 0.005:
                self.y_vals = [i * 1000 for i in self.y_vals]
                iteration += 1
            self.plot_and_fit(
                label=f'Samples from {function_to_time.__name__}')
            plt.style.use('ggplot')
            plt.xlabel("n")
            plt.ylabel(f"Time in {self.multiples[iteration]}")
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
                try:
                    if self.function_takes_item:
                        item = self.selector(self.data)
                        self.shared_dict[self.arg_dict['item']] = item
                    function_to_time(*args, **self.shared_dict, **kwargs)
                except StopIteration:
                    # Iterator exhausted: stop the loop
                    break
            end = time.process_time()
            elapsed = end - start
        final_time = elapsed / repetitions

        # Do the same timing as before, but don't actually call the function
        # This basically calculates overhead just due to running loops
        repetitions = 1
        elapsed = 0
        while elapsed < self.duration:
            repetitions *= 2
            start = time.process_time()
            for _ in range(repetitions):
                try:
                    if self.function_takes_item:
                        item = self.selector(self.data)
                        self.shared_dict[self.arg_dict['item']] = item
                    # function_to_time(*args, **self.shared_dict, **kwargs)
                except StopIteration:
                    # Iterator exhausted: stop the loop
                    break
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
        print(f"{'Size':<16} {'Time (sec)':>16}"
              f" {'Delta (sec)':>16} {'Ratio':>16}")

    @classmethod
    def print_info(cls, n, current_time, previous_time, iteration):
        """
        Prints information of the timings, in line with the other timings.
        """
        print(f"{n:<16} {current_time:>16.8f} ", end="")
        if iteration > 0:
            print(
                f"{current_time - previous_time:>16.8f}"
                f" {current_time/previous_time:>16.8f}")
        else:
            print()

    def plot_and_fit(self, label):
        """
        Simultaneously plots recorded values and does its best to fit and plot
        an asymptotically accurate curve.
        """
        function_name, params, r2 = self.find_best_fit()
        print(f'Best fit found to be O({function_name})')
        plt.plot(self.x_vals, self.y_vals, label=label, linestyle='--')
        x_vals = np.linspace(self.x_vals[0], self.x_vals[-1], 1_000)
        y_vals = self.functions[function_name](x_vals, params[0], params[1])
        self.alpha = params[0]
        self.beta = params[1]
        self.r_2 = r2
        plt.plot(x_vals,
                 y_vals,
                 label=self.function_label(function_name))

    def get_r_2(self, function, params):
        """
        Returns the coefficient of determination for a fit given the x values,
        the y values, the function, and the parameters of the function.
        """
        return metrics.r2_score(self.y_vals,
                                function(self.x_vals, params[0], params[1]))

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


def linear_contains(data, item):
    for i in range(len(data)):
        if data[i] == item:
            return True
    return False


def binary_contains(data, item):
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == item:
            return True
        if data[mid] < item:
            low = mid + 1
        else:
            high = mid - 1
    return False


SimpleTiming(
    data_or_generator=lambda x: range(x),
    arg_dict={
        "n": False,
        "data": "data",
        "item": "item"
    },
    n_iterator=[100 * i for i in range(1, 301)],
    duration=1,
    max_time=600).time_function(binary_contains)
