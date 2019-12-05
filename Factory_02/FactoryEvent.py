import numpy as np

class FactoryEvent:

	# eType:
	# 0	consumer coming
	# 1	consumer angry
	# 2	consumer leave(failed to order all products on time)
	# 3 producer finish job
	def __init__(self, time, eType, eArg):
		self.time = time
		self.eType = eType
		self.eArg = eArg

	def __str__(self):
		return "time: %d, Event Type: %d, Event Argument: %d. created" % (self.time, self.eType, self.eArg)