import simulator
from matplotlib import pyplot as plt
import numpy as np

def main():
  rho, result = simulator.main(queue_type='md1')
  result = np.array(result)
  x = rho
  en = result[:, 0]
  et = result[:, 1]
  p_idle = result[:, 2]

  print("E[n]: ", en)
  print("E[t]: ", et)
  print("E[n]/E[t]: ", np.divide(en, et))

  plt.figure(1)
  plt.subplots_adjust(hspace=0.65)

  # Rho vs E[n] Plot
  plt.subplot(311)
  plt.grid(True)
  plt.title('Rho vs E[n] Plot')
  plt.xlabel('Rho')
  plt.ylabel('Time (s)')
  plt.plot(x, en, 'ro-')

  # Rho vs E[t] Plot
  plt.subplot(312)
  plt.grid(True)
  plt.title('Rho vs E[t] Plot')
  plt.xlabel('Rho')
  plt.ylabel('Time (s)')
  plt.plot(x, et, 'bo-')

  # Rho vs P_idle Plot
  plt.subplot(313)
  plt.grid(True)
  plt.title('Rho vs P_idle Plot')
  plt.xlabel('Rho')
  plt.ylabel('Percentage (%)')
  plt.plot(x, p_idle, 'go-')
  plt.show()


if __name__ == '__main__':
  main()
