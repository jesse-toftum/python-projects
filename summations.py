import math
from matplotlib import pyplot as plt

def integrate(lower_bound, upper_bound, num_terms, function):
    current_bound = lower_bound
    summed = 0
    delta_x = (upper_bound - lower_bound) / num_terms
    while current_bound < upper_bound:
        summed += (function(current_bound) * delta_x)
        current_bound += delta_x
    return summed

def integrate_trap(lower_bound, upper_bound, num_terms, function):
    delta_x = (upper_bound - lower_bound) / num_terms
    summed = 0
    i = 1
    while i < num_terms:
        summed += (function(lower_bound + i * delta_x))
        i += 1
    return (delta_x / 2) * (function(lower_bound) + 2 * summed + function(upper_bound))



f = lambda x: (x ** 2) - 4
correct_answer = -10 - (2/3)
x_vals = [i for i in range(10, 1_000)]
y_vals_normal = [abs(integrate(-2, 2, i, f)-correct_answer) for i in x_vals]
y_vals_trap = [abs(integrate_trap(-2, 2, i, f)-correct_answer) for i in x_vals]

plt.style.use('ggplot')
plt.grid(True, which="both")
plt.loglog(x_vals, y_vals_normal)
plt.loglog(x_vals, y_vals_trap)
plt.show()