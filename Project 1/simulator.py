import numpy as np
import matplotlib.pyplot as p
from scipy.stats import expon

# exponential distribution bounded between 0 and 1
def expon_dist():
  x = np.linspace(expon.ppf(0.01), expon.ppf(0.99), 1000)
  dist_array = expon.pdf(x, scale=1)
  p.hist(dist_array, 100)
  print(x)
  print(dist_array)
  p.show()

def random_expon():
  packets_per_sec = 2
  beta = 1 / packets_per_sec
  U = np.random.exponential(beta, (100, 1))
  X = -1 * beta * np.log(1 - U)
  print(U)
  print(X)
  print(np.average(U))
  p.hist(U, 100)
  p.show()

def trunc_expon_dist():
  # http://docs.scipy.org/doc/scipy/reference/tutorial/stats/continuous_truncexpon.html
  # http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncexpon.html#scipy.stats.truncexpon


# expon_dist()
random_expon()


# Histogram of unbounded random exponential variable
# n = 1000
# scale = 1.0

# dist_array = np.random.exponential(1.0, (n, 1))

# print(dist_array)

# p.figure()
# p.hist(dist_array, 100)
# p.show()
