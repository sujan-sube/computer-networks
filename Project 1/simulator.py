import numpy as np
from asyncio import Queue
from matplotlib import pyplot as plt

# set global variables (tick duration set to 1 ms)
TICK_DURATION = 10**-4
TICKS = 10000
SERVICE_TIME = 0
DASH = '---------------------------'
AVG_NUM_PACKETS = 0
AVG_SOJOURN_TICK = 0
IDLE_TICK = 0
TOTAL_PACKETS = 0
PACKET_LOSS = 0
QUEUE_MAX = None
VERBOSE = False


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
        global AVG_SOJOURN_TICK
        AVG_SOJOURN_TICK = ((TOTAL_PACKETS - 1) / TOTAL_PACKETS) * AVG_SOJOURN_TICK + (i - q.get_nowait()) / TOTAL_PACKETS

        if VERBOSE:
          print("AVG_SOJOURN_TIME: ", AVG_SOJOURN_TICK)

      global AVG_NUM_PACKETS
      AVG_NUM_PACKETS += q.qsize()

      if VERBOSE:
        print("SERVICE TICK: ", service_tick)

    elif q.empty() is True:
      global IDLE_TICK
      IDLE_TICK += 1

  return q, service_tick

# implementation of M/D/1/K queue
def md1k(action, q, i, service_tick):

  # handle generate packet request
  if action == 'gen':
    if q.qsize() < QUEUE_MAX:
      q.put_nowait(i)
      global TOTAL_PACKETS
      TOTAL_PACKETS += 1
    elif q.qsize() >= QUEUE_MAX:
      global PACKET_LOSS
      PACKET_LOSS += 1

  # handle service packet request
  elif action == 'service':
    if q.empty() is False:
      if i == 1 or service_tick < i:
        service_tick = i + SERVICE_TIME

      if i == service_tick:
        global AVG_SOJOURN_TICK
        AVG_SOJOURN_TICK = ((TOTAL_PACKETS - 1) / TOTAL_PACKETS) * AVG_SOJOURN_TICK + (i - q.get_nowait()) / TOTAL_PACKETS

        if VERBOSE:
          print("AVG_SOJOURN_TIME: ", AVG_SOJOURN_TICK)

      global AVG_NUM_PACKETS
      AVG_NUM_PACKETS += q.qsize()

      if VERBOSE:
        print("SERVICE TICK: ", service_tick)

    elif q.empty() is True:
      global IDLE_TICK
      IDLE_TICK += 1

  return q, service_tick

def main(queue_type, rho_lower, rho_upper, reps, K=None):
  if queue_type == 'md1':
    queue_fns = md1
  elif queue_type == 'md1k':
    queue_fns = md1k
  else:
    print("Unknown queue type!")
    return

  # declare variables for simulation
  server_queue = Queue()
  repetition = reps
  lower = rho_lower
  upper = rho_upper
  step_size = 0.1
  C = 10**6
  L = 2000
  global SERVICE_TIME
  global IDLE_TICK
  global AVG_NUM_PACKETS
  global AVG_SOJOURN_TICK
  global TOTAL_PACKETS
  global PACKET_LOSS
  global QUEUE_MAX
  QUEUE_MAX = K
  SERVICE_TIME = int((float(L) / C) / TICK_DURATION)
  rho_range = np.arange(lower, upper, step_size)
  output = [0, 0, 0, 0]
  final_result = []

  for rho in rho_range:
    print("RHO: ", rho)

    # reset output variable for new rho
    output = [0, 0, 0, 0]

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
      PACKET_LOSS = 0
      server_queue = Queue()

      # network simulation loop
      for i in range(1, TICKS + 1, 1):
        lam = rho * C / L
        if VERBOSE:
          print("\nTICK: ", i)

        # packet generation and inter-arrival time calculation
        if i == inter_arrival_tick:
          server_queue, service_tick = queue_fns('gen', server_queue, i, service_tick)
          inter_arrival_tick = i + int(np.ceil(expon_var(lam) / TICK_DURATION))
          if VERBOSE:
            print("INTERARRIVAL:", inter_arrival_tick)

        # service packets
        server_queue, service_tick = queue_fns('service', server_queue, i, service_tick)

        # print packets in queue
        if VERBOSE:
          print("PACKETS IN QUEUE: ", server_queue.qsize())

      AVG_NUM_PACKETS /= TICKS
      output[0] += AVG_NUM_PACKETS
      output[1] += AVG_SOJOURN_TICK * TICK_DURATION
      output[2] += IDLE_TICK / TICKS
      output[3] += PACKET_LOSS / TOTAL_PACKETS

    output = [x / repetition for x in output]
    final_result.append(output)
  return rho_range, final_result


if __name__ == '__main__':
  # Network queue type and parameter selection
  rho, results = main(queue_type='md1k', rho_lower=0.5, rho_upper=1.6, reps=5, K=10) 

  i = 0
  for result in results:
    print(DASH)
    print("RHO: ", rho[i])
    print("E[n]: ", result[0])
    print("E[t]: ", result[1])
    print("P_idle: ", result[2])
    print("P_loss: ", result[3])
    i += 1

  # Test Random Exponential Variable
  # mylist = []
  # lam = 0.2 * 10**6 / 2000
  # for i in range(1, 10000):
  #   mylist.append(expon_var(lam) / TICK_DURATION)

  # print(mylist)
  # plt.hist(mylist, 100)
  # plt.show()
