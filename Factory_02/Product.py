class Product():
	count = 0

	def __init__(self, produceTime):
		self.index = Product.count
		self.produceTime = produceTime
		Product.count += 1

	def __str__(self):
		return "Product Type ID: %d, Produce Time needed: %d. created" % (self.index, self.produceTime)