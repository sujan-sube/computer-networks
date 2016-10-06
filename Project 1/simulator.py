import numpy as np
from asyncio import Queue
from matplotlib import pyplot as p

# set global variables (tick duration set to 1 ms)
TICK_DURATION = 10**-3
TICKS = 100000
SERVICE_TIME = 0
DASH = '---------------------------'
AVG_NUM_PACKETS = 0
AVG_SOJOURN_TICK = 0
IDLE_TICK = 0
TOTAL_PACKETS = 0


# calculate exponential random variable
def expon_var(lam):
  U = np.random.random_sample(size=1)
  X = -1 * (1 / lam) * np.log(1 - U)
  return float(X)

# implementation of M/D/1 queue
def md1(action, q, i, service_tick):

  # handle generate packet request
  if action == 'gen':
    q.put_nowait(i)
    global TOTAL_PACKETS
    TOTAL_PACKETS += 1

  # handle service packet request
  elif action == 'service':
    if q.empty() is False:
      if i == 1 or service_tick < i:
        service_tick = i + SERVICE_TIME

      if i == service_tick:
        # service_tick = i + SERVICE_TIME
        global AVG_SOJOURN_TICK
        AVG_SOJOURN_TICK = ((TOTAL_PACKETS - 1) / TOTAL_PACKETS) * AVG_SOJOURN_TICK + (i - q.get_nowait()) / TOTAL_PACKETS
        print("AVG_SOJOURN_TIME: ", AVG_SOJOURN_TICK)

      global AVG_NUM_PACKETS
      AVG_NUM_PACKETS += q.qsize()
      print("SERVICE TICK: ", service_tick)

    elif q.empty() is True:
      global IDLE_TICK
      IDLE_TICK += 1

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
  global IDLE_TICK
  global AVG_NUM_PACKETS
  global AVG_SOJOURN_TICK
  global TOTAL_PACKETS
  SERVICE_TIME = int((float(L) / C) / TICK_DURATION)

  for rho in np.arange(lower, upper, step_size):
    print("RHO: ", rho)
    for repeat in range(0, repetition, 1):
      print("REPETITION: ", repeat)
      print(DASH)

      # reset variables for each simulation
      inter_arrival_tick = 1
      service_tick = 1
      IDLE_TICK = 0
      AVG_NUM_PACKETS = 0
      AVG_SOJOURN_TICK = 0
      TOTAL_PACKETS = 0

      # network simulation loop
      for i in range(1, TICKS + 1, 1):
        lam = rho * C / L
        print("\nTICK: ", i)

        # packet generation and inter-arrival time calculation
        if i == inter_arrival_tick:
          server_queue, service_tick = queue_fns('gen', server_queue, i, service_tick)
          inter_arrival_tick = i + int(np.ceil(expon_var(lam) / TICK_DURATION))
          print("INTERARRIVAL:", inter_arrival_tick)

        # service packets
        server_queue, service_tick = queue_fns('service', server_queue, i, service_tick)

        # print packets in queue
        print("PACKETS IN QUEUE: ", server_queue.qsize())

      AVG_NUM_PACKETS /= TICKS


# Network queue type and parameter selection
main(queue_type='md1')

print(DASH)
print("E[n]: ", AVG_NUM_PACKETS)
print("E[t]: ", AVG_SOJOURN_TICK)
print("P_idle: ", IDLE_TICK)

# Test Random Exponential Variable
# mylist = []
# lam = 0.2 * 10**6 / 2000
# for i in range(1, 1000):
#   mylist.append(expon_var(lam) / 10**-3)

# print(mylist)
# p.hist(mylist, 30)
# p.show()
