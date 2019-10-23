#	pygame
import pygame
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

simulator_state = True

CREDIT = 100
PROFIT = 0
NUM_OF_PRODUCERS = 5	# this can be changed by reinforcement learning
NUM_OF_CONSUMERS = 12
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

class Consumer():
	def __init__(self, chosen):
		super(Consumer, self).__init__()
		self.chosen = False
		
def load_textures():
	global producer_texture
	producer_texture = pygame.image.load("res\\img\\dinosaur.jpg")
	producer_texture = pygame.transform.scale(producer_texture, (60, 60))
	global consumer_texture
	consumer_texture = pygame.image.load("res\\img\\pink_ghost.png")
	consumer_texture = pygame.transform.scale(consumer_texture, (27, 18))

# initialize the simulator
def init_simulator():
	pygame.init()
	simulator_window.fill(COLOR_WHITE)
	pygame.display.update()

# start simulate a day work: generate consumers and start time flies
def start_simulator():

	# lalala
	pygame.display.update()
	
def display_producer():
	# lalala
	gap = 100
	offset = 100
	text_offset = 65
	for i in range(0,NUM_OF_PRODUCERS):
		simulator_window.blit(producer_texture, (i % 3 * gap + offset, (int)(i / 3) * gap + offset))
		font_text = pygame.font.SysFont("Arial", 15)
		text_producer_name = font_text.render("Producer {}".format(i), True, COLOR_BLACK)
		simulator_window.blit(text_producer_name, (i % 3 * gap + offset, (int)(i / 3) * gap + offset + text_offset))

def display_consumer():
	# lalala
	gap = 60
	offset = 100
	text_offset = 30
	for i in range(0,NUM_OF_CONSUMERS):
		simulator_window.blit(consumer_texture, (i % 5 * gap + offset + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset))
		font_text = pygame.font.SysFont("Arial", 10)
		text_consumer_name = font_text.render("Consumer {}".format(i), True, COLOR_BLACK)
		simulator_window.blit(text_consumer_name, (i % 5 * gap + offset + WINDOW_WIDTH / 2, (int)(i / 5) * gap + offset + text_offset))

def update_simulator():

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			simulator_state = False
			pygame.quit()
	simulator_window.fill(COLOR_WHITE)

	# lalala
	# credit and profit
	font_text = pygame.font.SysFont("Arial", 15)
	text_credit = font_text.render("Credit: {}".format(CREDIT), True, COLOR_BLACK)
	text_profit = font_text.render("Profit: {}".format(PROFIT), True, COLOR_BLACK)
	simulator_window.blit(text_credit, (7 * WINDOW_WIDTH / 8, 20))
	simulator_window.blit(text_profit, (7 * WINDOW_WIDTH / 8, 50))
	# create a timer on the top middle of the window
	font_timer = pygame.font.SysFont("Times New Roman", 30)
	timer = "{:.0f}".format(pygame.time.get_ticks() / 1000)
	text_timer = font_timer.render(timer, True, COLOR_BLACK)
	simulator_window.blit(text_timer, (WINDOW_WIDTH / 2, 20))

	display_producer()
	display_consumer()

	pygame.display.update()
	

def end_simulator():
	pygame.quit()

if __name__ == "__main__":
	load_textures()
	init_simulator()
	start_simulator()	# lalala: add a start button before start and add a if statement
	producers = np.empty(shape = [NUM_OF_PRODUCERS], dtype = Producer)
	for i in range(0,NUM_OF_PRODUCERS):
		producers[i] = Producer(i)

	while simulator_state:	# lalala time.time() - START_TIME < DAY_TIME
		update_simulator()
	end_simulator()
