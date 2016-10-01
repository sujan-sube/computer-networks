import numpy as np
from asyncio import Queue

# set global variables (tick duration set to 1ms)
TICK_DURATION = 10**-3
TICKS = 100
SERVICE_TIME = None
DASH = '---------------------------'

# calculate exponential random variable
def expon_var(lam):
  U = np.random.random_sample(size=1)
  X = -1 * (1 / lam) * np.log(1 - U)
  return float(X)

# implementation of M/D/1 queue
def md1(action, q, i, service_tick):
  if action == 'gen':
    q.put_nowait(i)
  elif action == 'service':
    if q.empty() is False:
      if i == 1 or service_tick < i:
        service_tick = i + SERVICE_TIME

      if i == service_tick:
        service_tick = i + SERVICE_TIME
        q.get_nowait()

      print("SERVICE TICK: ", service_tick)

  return q, service_tick

# implementation of M/D/1/K queue
def md1k(action, q, i, service_tick):
  pass

def main(queue_type):
  if queue_type == 'md1':
    queue_fns = md1
  elif queue_type == 'md1k':
    queue_fns = md1k
  else:
    print("Unknown queue type!")
    return

  # declare variables for simulation
  server_queue = Queue()
  repetition = 1
  lower = 0.2
  upper = 0.3
  step_size = 0.1
  C = 10**6
  L = 2000
  # K = None
  global SERVICE_TIME 
  SERVICE_TIME = int((float(L) / C) / TICK_DURATION)

  for rho in np.arange(lower, upper, step_size):
    print("RHO: ", rho)
    for repeat in range(0, repetition, 1):
      print("REPETITION: ", repeat)
      print(DASH)
      inter_arrival_tick = 1
      service_tick = 1

      # network simulation loop
      for i in range(1, TICKS + 1, 1):
        lam = rho * C / L
        print("\nTICK: ", i)

        # packet generation and inter-arrival time calculation
        if i == inter_arrival_tick:
          server_queue, service_tick = queue_fns('gen', server_queue, i, service_tick)
          inter_arrival_tick = i + int(round(expon_var(lam) / TICK_DURATION, 0))
          print("INTERARRIVAL:", inter_arrival_tick)

        # service packets
        server_queue, service_tick = queue_fns('service', server_queue, i, service_tick)

        # print packets in queue
        print("PACKETS IN QUEUE: ", server_queue.qsize())


# Network queue type and parameter selection
main(queue_type='md1')
