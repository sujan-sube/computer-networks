import numpy as np
import random
from node_class import *

# set global variables (tick duration set to 10 nanosecond)
TICK_DURATION = 10**-8
TICKS = 10000000
SERVICE_TIME = 0
DASH = '---------------------------'
SUCCESSFUL_PACKETS = 0
TOTAL_PACKET_DELAY = 0
VERBOSE = False


# calculate inter_arrival_time using exponential random variable
def inter_arrival_time(lam):
  U = np.random.random_sample(size=1)
  X = -1 * (1 / lam) * np.log(1 - U)
  return (X / TICK_DURATION)

def main(average_arrival, n_computers, reps):

  # declare variables for simulation
  repetition = reps
  S = 2 * 10**8
  W = 10**6
  L = 1500 * 8
  WAIT_TIME = int(512 / (W * TICK_DURATION))
  A_range = average_arrival
  N_range = n_computers
  global PROPOGATION_TIME
  global SERVICE_TIME
  global SUCCESSFUL_PACKETS
  global TOTAL_PACKET_DELAY
  output = [0, 0]
  final_result = []

  for N in N_range:
    print("N: ", N)
    # set service time (small dependence on N)
    PROPOGATION_TIME = int((10 * (N - 1) / float(S)) / TICK_DURATION)
    SERVICE_TIME = int((float(L) / W) / TICK_DURATION + PROPOGATION_TIME)

    if VERBOSE:
      print("Propogation Time: ", PROPOGATION_TIME)
      print("Service Time: ", SERVICE_TIME)

    for A in A_range:
      print("A: ", A)
      # reset output variable for new simulation
      output = [0, 0]

      for repeat in range(0, repetition, 1):
        print("REPETITION: ", repeat)
        print(DASH)

        # reset variables for each simulation
        medium_busy = False
        medium_busy_in_tick = 0
        medium_free_in_tick = 0
        medium_collision_tick = 0
        transmitting_node = None
        SUCCESSFUL_PACKETS = 0
        TOTAL_PACKET_DELAY = 0
        node_list = [Node(int(inter_arrival_time(A))) for i in range(N)]

        if VERBOSE:
          num = 1
          for node in node_list:
            print("Node {0}: ".format(num), node.next_arrival_tick)
            num += 1

        # network simulation loop
        for i in range(1, TICKS + 1, 1):

          # perform operations at each node
          for node in node_list:

            # calculate next packet arrival time for each node and populate nodes
            if node.gen_next_packet(i):
              node.add_packet(i + inter_arrival_time(A))

            # check if node is done waiting or backoff and set status to IDLE
            node.done_wait_time(i)
            node.done_backoff_time(i)

            # check if any node is ready to transmit
            if node.empty() is False and node.check_status(Status.IDLE):
              if medium_collision_tick != 0:
                node.backoff(i + medium_busy_in_tick, WAIT_TIME)

              elif medium_busy_in_tick != 0:
                node.backoff(i + medium_busy_in_tick, WAIT_TIME)
                transmitting_node.backoff(i + medium_busy_in_tick, WAIT_TIME)
                transmitting_node = None
                medium_collision_tick = medium_busy_in_tick
                medium_free_in_tick = medium_busy_in_tick
                medium_busy_in_tick = 0

              elif medium_busy:
                wait_tick = i + random.randint(0, WAIT_TIME)
                node.wait(wait_tick)

                if VERBOSE:
                  print("\nTICK: ", i)
                  print("WAIT TICK: ", wait_tick)

              elif medium_busy is False:
                node.begin_transmit(i + SERVICE_TIME)
                transmitting_node = node
                medium_busy_in_tick = PROPOGATION_TIME + i

                if VERBOSE:
                  print("\nTICK: ", i)
                  print("SERVICE TICK: ", i + SERVICE_TIME)

            # check if any node successfully transmitted
            if node.check_successful_transmit(i) and node.check_status(Status.TRANSMITTING):
              transmitting_node = None
              TOTAL_PACKET_DELAY += i - node.remove_packet()
              SUCCESSFUL_PACKETS += 1
              medium_free_in_tick = PROPOGATION_TIME + i

              if VERBOSE:
                print("\nTICK: ", i)
                print("SUCCESSFUL_PACKETS: ", SUCCESSFUL_PACKETS)

            # check if medium is in collision
            if i == medium_collision_tick:
              medium_collision_tick = 0

            # check if medium has become busy
            if i == medium_busy_in_tick:
              medium_busy = True
              medium_busy_in_tick = 0

            # check if medium will become free
            if i == medium_free_in_tick:
              medium_busy = False
              medium_free_in_tick = 0

        # performance metrics can only be caluclated if SUCCESSFUL_PACKETS is not 0
        if SUCCESSFUL_PACKETS != 0:
          output[0] += (SUCCESSFUL_PACKETS * L) / (TICK_DURATION * TICKS)
          output[1] += TOTAL_PACKET_DELAY * TICK_DURATION / SUCCESSFUL_PACKETS

      output = [x / repetition for x in output]
      final_result.append(output)
  return final_result


if __name__ == '__main__':
  # CSMA/CD protocol type and parameter selection
  print(main(average_arrival=[6], n_computers=[20, 40, 60, 80, 100], reps=5))
