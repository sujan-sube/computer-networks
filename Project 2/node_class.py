from asyncio import Queue
import random

# status code of Nodes
class Status:

  IDLE = 0
  TRANSMITTING = 1
  WAIT = 2
  BACKOFF = 3
  WAIT_SLOT = 4
  POST_WAIT_SLOT = 5

# represents each Node on the network
class Node:

  def __init__(self, inter_arrival_tick):
    self.queue = Queue()
    self.next_arrival_tick = inter_arrival_tick
    self.service_tick = 0
    self.wait_tick = 0
    self.backoff_tick = 0
    self.backoff_value = 0
    self.status = Status.IDLE

  def check_status(self, status_code):
    if self.status == status_code:
      return True
    else:
      return False

  def set_status(self, status_code):
    self.status = status_code

  def add_packet(self, inter_arrival_tick):
    self.queue.put_nowait(self.next_arrival_tick)
    self.next_arrival_tick = inter_arrival_tick

  def remove_packet(self):
    self.service_tick = 0
    self.status = Status.IDLE
    self.backoff_value = 0
    return self.queue.get_nowait()

  def empty(self):
    if self.queue.empty():
      return True
    else:
      return False

  def gen_next_packet(self, current_tick):
    if self.next_arrival_tick == current_tick:
      return True
    else:
      return False

  def begin_transmit(self, service_tick):
    self.service_tick = service_tick
    self.status = Status.TRANSMITTING

  def wait(self, wait_tick):
    self.wait_tick = wait_tick
    self.status = Status.WAIT

  def wait_slot(self, wait_slot_tick):
    self.wait_tick = wait_slot_tick
    self.status = Status.WAIT_SLOT

  def done_wait_time(self, current_tick):
    if self.wait_tick == current_tick:
      if self.status == Status.WAIT:
        self.status = Status.IDLE
      elif self.status == Status.WAIT_SLOT:
        self.status = Status.POST_WAIT_SLOT

  def backoff(self, current_tick, wait_time):
    if self.backoff_value > 10:
      self.queue.get_nowait()
      self.backoff_value = 0
      self.status = Status.IDLE
    else:
      self.backoff_value += 1
      self.backoff_tick = int(current_tick + random.randint(0, 2**self.backoff_value - 1) * wait_time)
      self.status = Status.BACKOFF

  def done_backoff_time(self, current_tick):
    if self.status == Status.BACKOFF:
      if self.backoff_tick == current_tick:
        self.status = Status.IDLE

  def check_successful_transmit(self, current_tick):
    if self.service_tick == current_tick:
      return True
    else:
      return False
