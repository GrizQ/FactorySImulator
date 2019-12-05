import numpy as np

class Consumer():
	count = 0

	def __init__(self, startTime, requirement):
		self.index = Consumer.count
		self.state = 0	# -1:failed; 0:waiting; 1:angry; 2:finished
		self.startTime = startTime
		self.requirement = requirement
		self.producing = np.zeros(requirement.size)
		Consumer.count += 1

	def __str__(self):
		return "Consumer ID: %d, Current State: %d, Srart Time: %d. created" % (self.index, self.state, self.startTime)

	def getState(self):
		return self.state

	def setState(self, newState):
		self.state = newState

	def getRequirement(self):
		return self.requirement

	def getProducing(self):
		return self.producing

	# if all requirement are done and no product is producing, set the state to 2(finished)
	def updateState(self):
		if (np.count_nonzero(self.requirement) == 0) and (np.count_nonzero(self.producing) == 0):
			# lalala: maybe self.State += 2 to differenciate leave happily and angrily
			self.setState(2)
		return self.state

	# called when a producer start producing item index
	def produceProduct(self, index):
		self.requirement[index] -= 1
		self.producing[index] += 1

	# called when a producer finish producing item index
	def finishProduct(self, index):
		self.producing[index] -= 1

	def needServe(self):
		return (np.count_nonzero(self.requirement) != 0)