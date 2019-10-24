# lalala add something can recogonize which consumer is being served now

#	pygame
import pygame
import random
import numpy as np
import time

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# lalala
# window parameter
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_CAPTION = "Factory Simulator"
WINDOW_ICON = pygame.image.load("res\\img\\zaku.png")
simulator_window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)
pygame.display.set_icon(WINDOW_ICON)

PRODUCER_WIDTH = 60
PRODUCER_HEIGHT = 60
CONSUMER_WIDTH = 36
CONSUMER_HEIGHT = 24

simulator_state = True

DAY_TIME = 600	# total work time
TIME_MAX1 = 60	# products finished in TIME_MAX1 will not be punished
TIME_MAX2 = 120	# products finished between TIME_MAX1 and TIME_MAX2 will be punished and no products is allowed to be finished after TIME_MAX2
PENALTY = 5	# the penalty of each product finished between TIME_MAX1 and TIME_MAX2
NUM_OF_ITEM = 4
START_TIME = time.time()	# lalala change later
generate_rate = 0.01	# lalala change later add a generate consumer function later

consumerINDEX = 0	# lalala

class Producer():
	index = -1
	producing = -1
	start_time = 0

	def __init__(self, index):
		self.index = index
		self.producing = -1
		temp = "This is producer %d, currently producing %d" % (self.index, self.producing)
		print(temp)
		
	def changeState(self, producing):
		if self.producing == -1:
			self.producing = producing
			if producing != -1:
				self.start_time = pygame.time.get_ticks()
			temp = "State of producer %d have been changed to produce item %d, start at self.start_time: %d" % (self.index, self.producing, self.start_time)
			print(temp)
			global profit
			profit -= 100# lalala read from file and add an if statement
			return True
		else:
			print("i am busy")
			return False

	# lalala thinking about a smarter update function
	def updateState(self):
		produceTime = 5	# lalala read from file later and add an if statement
		if self.producing != (-1) and (pygame.time.get_ticks() - self.start_time) > (produceTime * 1000):
			item_amount[self.producing] += 1
			print("an item %d finished" % self.producing)
			self.producing = -1

# lalala thinking about a smarter update function
def updateProducer():
	for i in range(0,num_of_producer):
		producers[i].updateState()

class Consumer():
	index = 0
	requirement = 0	# lalala u know what u should do
	chosen = False
	start_time = 0
	punished = False

	def __init__(self, requirement, start_time):
		global consumerINDEX
		super(Consumer, self).__init__()
		self.index = consumerINDEX
		consumerINDEX += 1
		self.requirement = requirement
		self.start_time = start_time
		global num_of_consumer
		num_of_consumer += 1

	def setChosen(self, chosen):
		self.chosen = chosen
	def setPunished(self):
		self.punished = True
	def isPunished(self):
		return self.punished
	def isChosen(self):
		return self.chosen
	def getRequirement(self):
		return self.requirement
	def getIndex(self):
		return self.index
	def getStartTime(self):
		return self.start_time

# lalala rewrite!
def generateConsumer():
	global consumers, num_of_consumer
	requirement = random.randint(1,3)
	consumers = np.append(consumers, Consumer(requirement, pygame.time.get_ticks()))

# lalala rewrite!
def updateConsumer():
	global consumers, num_of_consumer, item_amount, credit, profit
	for i in range(0,num_of_consumer):
		if consumers[i].isPunished():
			if pygame.time.get_ticks() - consumers[i].getStartTime() >= (TIME_MAX2 * 1000):
				print("lalala exit la")
		else:
			if pygame.time.get_ticks() - consumers[i].getStartTime() >= (TIME_MAX1 * 1000):
				credit -= 5
				consumers[i].setPunished()
				print("consumer %d is angry now" %(i))
		if consumers[i].isChosen():
			if item_amount[1] >= consumers[i].getRequirement():
				item_amount[1] -= consumers[i].getRequirement()
				profit += 500
				num_of_consumer -= 1
				consumers = np.delete(consumers, i)
				break
		
def load_textures():
	global producer_texture
	producer_texture = pygame.image.load("res\\img\\dinosaur.jpg")
	producer_texture = pygame.transform.scale(producer_texture, (PRODUCER_WIDTH, PRODUCER_HEIGHT))

	# lalala show the requirement of each consumer, show different texture when a consumer is selected
	global consumer_texture
	consumer_texture = pygame.image.load("res\\img\\pink_ghost.png")
	consumer_texture = pygame.transform.scale(consumer_texture, (CONSUMER_WIDTH, CONSUMER_HEIGHT))

# initialize the simulator
def init_simulator():
	global credit, profit, num_of_producer, num_of_consumer, item_name, item_amount
	credit = 100
	profit = 0
	num_of_producer = 5	# lalala read from file later and can be changed by reinforcement learning 
	num_of_consumer = 0
	item_name = np.array(["ITEM A", "ITEM B", "ITEM C", "ITEM D"])	# lalala read from xml later
	item_amount = np.zeros(NUM_OF_ITEM)	# lalala i forget what i wanna to write

	pygame.init()
	simulator_window.fill(COLOR_WHITE)
	pygame.display.update()

# start simulate a day work: generate consumers and start time flies
def start_simulator():

	# lalala add a start button
	# lalala reset pygame.time or set a start time
	pygame.display.update()
	
def display_lalala():
	# lalala
	font_text = pygame.font.SysFont("Arial", 15)
	# show number of items
	# lalala use something like array
	for i in range(0,NUM_OF_ITEM):
		text_item = item_name[i] + ": {:.0f}".format(item_amount[i])
		surface_item = font_text.render(text_item, True, COLOR_BLACK)
		simulator_window.blit(surface_item, ((5 + (int)(i / 2)) * WINDOW_WIDTH / 8, 20 + 30 * (i % 2)))

	# text_items = np.array(["ITEM A: %d" % item_amount[0], "ITEM B: %d" % item_amount[1], "ITEM C: %d" % item_amount[2], "ITEM D: %d" % item_amount[3]])
	# surface_itemA = font_text.render(text_items[0], True, COLOR_BLACK)
	# surface_itemB = font_text.render(text_items[1], True, COLOR_BLACK)
	# surface_itemC = font_text.render(text_items[2], True, COLOR_BLACK)
	# surface_itemD = font_text.render(text_items[3], True, COLOR_BLACK)
	# simulator_window.blit(surface_itemA, (5 * WINDOW_WIDTH / 8, 20))
	# simulator_window.blit(surface_itemB, (5 * WINDOW_WIDTH / 8, 50))
	# simulator_window.blit(surface_itemC, (6 * WINDOW_WIDTH / 8, 20))
	# simulator_window.blit(surface_itemD, (6 * WINDOW_WIDTH / 8, 50))

	# credit and profit
	# lalala add something like a bar
	text_credit = font_text.render("Credit: {}".format(credit), True, COLOR_BLACK)
	text_profit = font_text.render("Profit: {}".format(profit), True, COLOR_BLACK)
	simulator_window.blit(text_credit, (7 * WINDOW_WIDTH / 8, 20))
	simulator_window.blit(text_profit, (7 * WINDOW_WIDTH / 8, 50))
	# create a timer on the top middle of the window
	# lalala maybe add a clock
	font_timer = pygame.font.SysFont("Times New Roman", 30)
	timer = "{:.0f}".format(pygame.time.get_ticks() / 1000)
	text_timer = font_timer.render(timer, True, COLOR_BLACK)
	simulator_window.blit(text_timer, (WINDOW_WIDTH / 2, 20))

def display_producer():
	# lalala timer
	# lalala change those parameters to global value maybe
	gap = 100
	offset_x = 50
	offset_y = 100
	text_offset = 65
	# lalala add a if statement to differentiate (not)working producer by changing texture
	for i in range(0,num_of_producer):
		simulator_window.blit(producer_texture, (i % 3 * gap + offset_x, (int)(i / 3) * gap + offset_y))
		font_text = pygame.font.SysFont("Arial", 15)
		text_producer_name = font_text.render("Producer {}".format(i), True, COLOR_BLACK)
		simulator_window.blit(text_producer_name, (i % 3 * gap + offset_x, (int)(i / 3) * gap + offset_y + text_offset))

def display_consumer():
	# lalala requirement
	# lalala change those parameters to global value maybe
	global consumers
	gap = 60
	offset_x = 50
	offset_y = 100
	text_offset = 30
	for i in range(0,num_of_consumer):
		simulator_window.blit(consumer_texture, (i % 5 * gap + offset_x + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset_y))
		font_text = pygame.font.SysFont("Arial", 10)
		text_consumer_name = font_text.render("Consumer {}".format(consumers[i].getIndex()), True, COLOR_BLACK)
		simulator_window.blit(text_consumer_name, (i % 5 * gap + offset_x + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset_y + text_offset))

def update_simulator():

	simulator_window.fill(COLOR_WHITE)

	display_lalala()
	display_producer()
	display_consumer()

	for event in pygame.event.get():
		# finish if x clicked
		if event.type == pygame.QUIT:
			simulator_state = False
			pygame.quit()


		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = pygame.mouse.get_pos()

			# check if a producer is clicked
			gap = 100
			offset_x = 50
			offset_y = 100
			text_offset = 65
			for i in range(0,num_of_producer):
				if mouse_pos[0] > (i % 3 * gap + offset_x) and mouse_pos[0] < (i % 3 * gap + offset_x + PRODUCER_WIDTH):
					if mouse_pos[1] > ((int)(i / 3) * gap + offset_y) and mouse_pos[1] < ((int)(i / 3) * gap + offset_y + PRODUCER_HEIGHT):
						pause = True
						while pause:
							for event in pygame.event.get():
								# lalala add a full screen panel
								if event.type == pygame.MOUSEBUTTONUP:
									producers[i].changeState(1)
									pause = False

			# check if a consumer is clicked
			gap = 60
			offset_x = 50
			offset_y = 100
			text_offset = 30
			for i in range(0,num_of_consumer):
				if mouse_pos[0] > (i % 5 * gap + offset_x + WINDOW_WIDTH / 2) and mouse_pos[0] < (i % 5 * gap + offset_x + WINDOW_WIDTH / 2 + CONSUMER_WIDTH):
					if mouse_pos[1] > ((int)(i / 5) * gap + offset_y) and mouse_pos[1] < ((int)(i / 5) * gap + offset_y + CONSUMER_HEIGHT):
						consumers[i].setChosen(True)

	pygame.display.update()
	

def end_simulator():
	pygame.quit()

if __name__ == "__main__":
	load_textures()
	init_simulator()
	start_simulator()	# lalala: add a start button before start and add a if statement
	global producers, consumers
	producers = np.empty(shape = [num_of_producer], dtype = Producer)
	consumers = np.empty(shape = [num_of_consumer], dtype = Consumer)
	for i in range(0,num_of_producer):
		producers[i] = Producer(i)
	while simulator_state and (pygame.time.get_ticks() / 1000 < DAY_TIME):
		# lalala change!
		if random.random() < generate_rate:
			generateConsumer()

		updateProducer()	# lalala thinking about a smarter update function
		updateConsumer()
		update_simulator()
	end_simulator()
