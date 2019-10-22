import numpy as np
import time

NUM_OF_PRODUCERS = 5	#
DAY_TIME = 600	# total work time
TIME_MAX1 = 60	# products finished in TIME_MAX1 will not be punished
TIME_MAX2 = 120	# products finished between TIME_MAX1 and TIME_MAX2 will be punished and no products is allowed to be finished after TIME_MAX2
PENALTY = 5	# the penalty of each product finished between TIME_MAX1 and TIME_MAX2
START_TIME = time.time()


class Producer():
	def __init__(self, index):
		self.index = index
		self.state = 0
		temp = "This is producer %d, the current state is %d" % (self.index, self.state)
		print(temp)
		
	def changeState(self, state):
		self.state = state
		if state != 0:
			self.start_time = time.time() - START_TIME
		temp = "State of producer %d have been changed to state %d, start at self.start_time: %d" % (self.index, self.state, self.start_time)
		print(temp)

if __name__ == "__main__":
	
	producers = np.empty(shape = [NUM_OF_PRODUCERS], dtype = Producer)
	for i in range(0,NUM_OF_PRODUCERS):
		producers[i] = Producer(i)