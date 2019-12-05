class Producer():
	count = 0

	def __init__(self):
		self.index = Producer.count
		self.serving = -1 # -1:not serving anyone; other numbers: index of consumer serving
		self.producing = -1	# -1:idle; other numbers: index of product producing
		Producer.count += 1

	def __str__(self):
		return "Producer ID: %d, Current State: %d, Serving Consumer: %d. created" % (self.index, self.producing, self.serving)

	def getIndex(self):
		return self.index

	def getProducing(self):
		return self.producing

	def getServing(self):
		return self.serving

	def setState(self, newServing, newProducing):
		self.serving = newServing
		self.producing = newProducing