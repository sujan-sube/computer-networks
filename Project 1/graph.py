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
    i = 0
    result = [None] * len(K)
    for K_val in K:
      rho, result[i] = simulator.main(queue_type, rho_lower, rho_upper, reps, K_val)
      result[i] = np.array(result[i])
      i += 1

    # setup variables for generating graph
    x = rho
    en = []
    et = []
    p_idle = []
    p_loss = []

    # parse desired output variables from simulation results
    for i in range(0, len(K), 1):
      en.append(result[i][:, 0])
      et.append(result[i][:, 1])
      p_idle.append(result[i][:, 2])
      p_loss.append(result[i][:, 3])

    # Rho vs E[n] Plot
    plt.figure(1)
    plt.grid(True)
    plt.title('Rho vs E[n] Plot')
    plt.xlabel('Rho')
    plt.ylabel('Number of Packets')
    for i in range(0, len(K), 1):
      plt.plot(x, en[i], label='K = {0}'.format(K[i]), linewidth=2, marker='.')
    plt.legend(loc='upper left')

    # Rho vs E[t] Plot
    plt.figure(2)
    plt.grid(True)
    plt.title('Rho vs E[t] Plot')
    plt.xlabel('Rho')
    plt.ylabel('Time (s)')
    for i in range(0, len(K), 1):
      plt.plot(x, et[i], label='K = {0}'.format(K[i]), linewidth=2, marker='.')
    plt.legend(loc='upper left')

    # Rho vs P_idle Plot
    plt.figure(3)
    plt.grid(True)
    plt.title('Rho vs P_idle Plot')
    plt.xlabel('Rho')
    plt.ylabel('Percentage')
    for i in range(0, len(K), 1):
      plt.plot(x, p_idle[i], label='K = {0}'.format(K[i]), linewidth=2, marker='.')
    plt.legend(loc='upper right')

    # Rho vs P_loss Plot
    plt.figure(4)
    plt.grid(True)
    plt.title('Rho vs P_loss Plot')
    plt.xlabel('Rho')
    plt.ylabel('Percentage')
    for i in range(0, len(K), 1):
      plt.plot(x, p_loss[i], label='K = {0}'.format(K[i]), linewidth=2, marker='.')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
  # main(queue_type='md1', rho_lower=0.2, rho_upper=1.0, reps=5)
  main(queue_type='md1k', rho_lower=0.5, rho_upper=1.6, reps=5, K=[10, 25, 50])
