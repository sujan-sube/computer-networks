import simulator
from matplotlib import pyplot as plt
import numpy as np

def main(queue_type, rho_lower, rho_upper, reps, K=None):

  if queue_type == 'md1':
    rho, result = simulator.main(queue_type, rho_lower, rho_upper, reps)
    result = np.array(result)
    x = rho
    en = result[:, 0]
    et = result[:, 1]
    p_idle = result[:, 2]

    # verify output data
    print("E[n]: ", en)
    print("E[t]: ", et)
    print("E[n]/E[t]: ", np.divide(en, et))
    print("lamda: ", np.multiply(rho, 500))

    # Rho vs E[n] Plot
    plt.figure(1)
    plt.grid(True)
    plt.title('Rho vs E[n] Plot')
    plt.xlabel('Rho')
    plt.ylabel('Number of Packets')
    plt.plot(x, en, 'ro-')

    # Rho vs E[t] Plot
    plt.figure(2)
    plt.grid(True)
    plt.title('Rho vs E[t] Plot')
    plt.xlabel('Rho')
    plt.ylabel('Time (s)')
    plt.plot(x, et, 'bo-')

    # Rho vs P_idle Plot
    plt.figure(3)
    plt.grid(True)
    plt.title('Rho vs P_idle Plot')
    plt.xlabel('Rho')
    plt.ylabel('Percentage')
    plt.plot(x, p_idle, 'go-')
    plt.show()

  elif queue_type == 'md1k':
    pass


if __name__ == '__main__':
  main(queue_type='md1', rho_lower=0.2, rho_upper=1.0, reps=5)

  # ideal graphs of et and en
  # rho = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  # en = [0.223466, 0.364898, 0.530792, 0.752433, 1.057987, 1.502712, 2.425331, 4.939016]
  # et = [2249.98568, 2437.48928, 2666.72975, 3010.01476, 3514.00485, 4290.28775, 6048.87477, 10965.4439]
  # plt.figure(1)
  # plt.subplot(211)
  # plt.plot(rho, en, 'ro-')
  # plt.subplot(212)
  # plt.plot(rho, et, 'bo-')
  # plt.show()
