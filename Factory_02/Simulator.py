import pygame
import random
import time
import numpy as np

from Producer import Producer
from Consumer import Consumer
from Product import Product
from FactoryEvent import FactoryEvent

# set True to display the window, False to disable
display_window = True

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PRODUCER_WIDTH = 60
PRODUCER_HEIGHT = 60
CONSUMER_WIDTH = 36
CONSUMER_HEIGHT = 24

TIME_MAX1 = 60	# products finished in TIME_MAX1 will not be punished
PENALTY = 5
TIME_MAX2 = 120	# products finished between TIME_MAX1 and TIME_MAX2 will be punished and no products is allowed to be finished after TIME_MAX2

NUM_OF_PRODUCER = 9
NUM_OF_PRODUCT = 4
PRODUCE_TIME = np.array([4, 6, 5, 7])

PRODUCT_NAME = np.empty(shape = [NUM_OF_PRODUCT], dtype = str)
PRODUCT_PRODUCED = np.zeros(NUM_OF_PRODUCT)

producers = np.empty(shape = [NUM_OF_PRODUCER], dtype = Producer)
products = np.empty(shape = [NUM_OF_PRODUCT], dtype = Product)

def addNewEvent(time, eType, eArg):
	global factoryEvents
	i = 0
	pos = factoryEvents.size
	for i in range(0,factoryEvents.size):
		if time <= factoryEvents[i].time:
			pos = i
			break
	factoryEvents = np.insert(factoryEvents, pos, FactoryEvent(time, eType, eArg))
	print(factoryEvents[pos])
	
# lalala: read from file
def load_textures():

	global producer_texture
	producer_texture = pygame.image.load("res\\img\\dinosaur.jpg")
	producer_texture = pygame.transform.scale(producer_texture, (PRODUCER_WIDTH, PRODUCER_HEIGHT))

	# lalala show the requirement of each consumer
	global consumer_texture
	consumer_texture = pygame.image.load("res\\img\\pink_ghost.png")
	consumer_texture = pygame.transform.scale(consumer_texture, (CONSUMER_WIDTH, CONSUMER_HEIGHT))

def loadConsumers():
	global consumers, orderedConsumers, factoryEvents
	consumers = np.empty(shape = [0], dtype = Consumer)
	consumersFile = open('res\\data\\consumers.txt')
	consumersData = consumersFile.read().split('\n')
	for i in range(0,len(consumersData)):
		consumerDataStr = consumersData[i].split()
		consumerStartTime = int(consumerDataStr[0])
		consumerRequirement = np.zeros(NUM_OF_PRODUCT)
		for j in range(1,len(consumerDataStr)):
			consumerRequirement[j-1] = int(consumerDataStr[j])
		consumers = np.append(consumers, Consumer(consumerStartTime, consumerRequirement))
		print(consumers[i])
		addNewEvent(consumerStartTime, 0, i)
	consumersFile.close()
	orderedConsumers = np.empty(shape = [0], dtype = int)

# initialize the simulator
def init_window():
	global simulator_window
	WINDOW_CAPTION = "Factory Simulator"
	WINDOW_ICON = pygame.image.load("res\\img\\zaku.png")
	simulator_window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
	pygame.display.set_caption(WINDOW_CAPTION)
	pygame.display.set_icon(WINDOW_ICON)

	load_textures()
	pygame.init()
	simulator_window.fill(COLOR_WHITE)
	pygame.display.update()

# start simulate a day work: generate consumers and start time flies
# def start_simulator():

# 	# lalala add a start button
# 	# lalala reset pygame.time or set a start time
# 	pygame.display.update()

def init():

	global curTime, factoryEvents, simulator_state, credit, profit, idleProducers
	curTime = 0
	factoryEvents = np.empty(shape = [0], dtype = FactoryEvent)
	simulator_state = True
	credit = 100
	profit = 0
	idleProducers = np.empty(shape = [0], dtype = int)

	for i in range(0, NUM_OF_PRODUCER):
		producers[i] = Producer()
		idleProducers = np.append(idleProducers, producers[i].getIndex())
		print(producers[i])
	for i in range(0,NUM_OF_PRODUCT):
		products[i] = Product(PRODUCE_TIME[i])
		PRODUCT_NAME[i] = i
		print(products[i])
	loadConsumers()

# check if all work is or will be done
# if not, allocate new job for every idle producers
def updateProducers():
	global curTime, factoryEvents, idleProducers, consumers

	# if there has any work left, let all idle producers start working
	while hasWorkLeft():
		if hasIdleProducer():
			newState = greedyServe() # lalala: replaced by reinforcement learning later
			producerID = idleProducers[0]
			servingID = newState[0]
			producingID = newState[1]

			producers[producerID].setState(servingID, producingID) # change the serving and producing of the producer
			consumers[servingID].produceProduct(producingID) # tell the consumer an item is being produced
			addNewEvent(curTime + PRODUCE_TIME[producingID], 3, producerID) # add producer finish job event
			print("time: %d, producer %d start serving consumer %d, producing %d" % (curTime, producerID, producers[producerID].getServing(), producers[producerID].getProducing()))
			idleProducers = np.delete(idleProducers, 0)
		else:
			break

# lalala: just a simply job allocate method, will implement reinforcement learning later
def greedyServe():
	global producers, consumers, orderedConsumers

	for i in range(0,orderedConsumers.size):
		if consumers[orderedConsumers[i]].needServe():
			servingID = orderedConsumers[i]
			break
	producingID = np.where(consumers[servingID].getRequirement() > 0)[0][0]
	return servingID, producingID

# update the state of all consumers in queue
def updateConsumers():
	global consumers, orderedConsumers, profit

	tempConsumers = orderedConsumers

	for i in range(0,orderedConsumers.size):
		if (consumers[orderedConsumers[i]].updateState()) == 2:
			tempConsumers = np.delete(tempConsumers, np.where(tempConsumers == orderedConsumers[i]))
			profit += 100
			print("consumer %d satisfied" % (orderedConsumers[i]))
	orderedConsumers = tempConsumers

def hasIdleProducer():
	global idleProducers
	return (idleProducers.size != 0)

# check if any consumer still have requirement not produced or being produced
def hasWorkLeft():
	global consumers, orderedConsumers
	for i in range(0,orderedConsumers.size):
		if consumers[orderedConsumers[i]].needServe():
			return True
	return False

def handleEvent(event):
	global curTime, factoryEvents, orderedConsumers, credit, idleProducers, consumers
	factoryEvents = np.delete(factoryEvents, 0)
	curTime = event.time
	eArg = event.eArg
	if event.eType == 0:
		orderedConsumers = np.append(orderedConsumers, eArg)
		addNewEvent(curTime + TIME_MAX1, 1, eArg)
		addNewEvent(curTime + TIME_MAX2, 2, eArg)
	elif event.eType == 1:
		if consumers[eArg].getState() != 2:
			consumers[eArg].setState(1)
			credit -= PENALTY
			print("time: %d, consumer %d is angry, change its state to %d" % (curTime, eArg, consumers[eArg].getState()))
	elif event.eType == 2:
		if consumers[eArg].getState() != 2:
			consumers[eArg].setState(-1)
			# stop here, failed
			credit -= 100
			print("time: %d, consumer %d left angrily, change its state to %d" % (curTime, eArg, consumers[eArg].getState()))
	elif event.eType == 3:
		# lalala: reinforcement learning here
		# something[producers[eArg].getProducing()] += 1
		consumers[producers[eArg].getServing()].finishProduct(producers[eArg].getProducing())
		producers[eArg].setState(-1, -1)
		idleProducers = np.append(idleProducers, producers[eArg].getIndex())

	updateProducers()
	updateConsumers()

def display_lalala():
	# lalala
	font_text = pygame.font.SysFont("Arial", 15)
	# show number of items
	# lalala use something like array
	for i in range(0,NUM_OF_PRODUCT):
		text_item = PRODUCT_NAME[i] + ": {:.0f}".format(PRODUCT_PRODUCED[i])
		surface_item = font_text.render(text_item, True, COLOR_BLACK)
		simulator_window.blit(surface_item, ((5 + (int)(i / 2)) * WINDOW_WIDTH / 8, 20 + 30 * (i % 2)))

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
	for i in range(0,NUM_OF_PRODUCER):
		simulator_window.blit(producer_texture, (i % 3 * gap + offset_x, (int)(i / 3) * gap + offset_y))
		font_text = pygame.font.SysFont("Arial", 15)
		text_producer_name = font_text.render("Producer {}".format(i), True, COLOR_BLACK)
		simulator_window.blit(text_producer_name, (i % 3 * gap + offset_x, (int)(i / 3) * gap + offset_y + text_offset))

def display_consumer():
	# lalala requirement
	# lalala change those parameters to global value maybe
	global orderedConsumers
	gap = 60
	offset_x = 50
	offset_y = 100
	text_offset = 30
	for i in range(0,orderedConsumers.size):
		simulator_window.blit(consumer_texture, (i % 5 * gap + offset_x + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset_y))
		font_text = pygame.font.SysFont("Arial", 10)
		text_consumer_name = font_text.render("Consumer {}".format(orderedConsumers[i]), True, COLOR_BLACK)
		simulator_window.blit(text_consumer_name, (i % 5 * gap + offset_x + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset_y + text_offset))

def update_window():
	global simulator_state

	simulator_window.fill(COLOR_WHITE)

	display_lalala()
	display_producer()
	display_consumer()

	for event in pygame.event.get():
		# finish if x clicked
		if event.type == pygame.QUIT:
			simulator_state = False
			pygame.quit()

	pygame.display.update()

def end_simulator():
	pygame.quit()

if __name__ == "__main__":
	init()
	if display_window:
		init_window()
	# start_simulator()	# lalala: add a start button before start and add a if statementf
	while factoryEvents.size > 0:
		handleEvent(factoryEvents[0])
		if display_window:
			update_window()
	if display_window:
		end_simulator()