import pygame
import random
import math
pygame.init()

class DrawInformation:  # instead of making various global variables, made this class
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [                  # Different shades of gray for differentiating the blocks
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 30)      # Font & Size
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)  # Font & Size

	SIDE_PAD = 100   # In px i.e. side padding of 50px left & 50px right
	TOP_PAD = 150    # In px i.e. top padding of 150px left to draw controls

	def __init__(self, width, height, lst):  # lst is the starting list that we want to sort (or say blocks)
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height)) # IN pygame we need to setup a window on which we'll draw everything on
		pygame.display.set_caption("Sorting Algorithm Visualization") # caption for the window
		self.set_list(lst)  # calling set_list(lst) method

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))  # setting width of every block ;
																	#len(lst) is the number of blocks we have ; rounded off that value b/c we can't have fraction of block
		
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) # this is kind of height of one unit of block, 
														#this will be multiplied to get the actual height of particular block on the screen keeping in mind the highest and lowest block present
		
		self.start_x = self.SIDE_PAD // 2  #from where we start drawing blocks with x coordinate; used //2 to get whole number


def draw(draw_info, algo_name, ascending): 
	draw_info.window.fill(draw_info.BACKGROUND_COLOR) # filling the window with BACKGROUND_COLOUR

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))   # from where on the coordinate system the above text will render on screen 

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))  # from where on the coordinate system the above text will render on screen 

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))  # from where on the coordinate system the above text will render on screen 

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:   #TO see the swapping and updates in list 
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)   

	for i, val in enumerate(lst):  # to get the index as well as the value of the particular element
		x = draw_info.start_x + i * draw_info.block_width   #(x,y) for top-left corner of the block, because we draw it from the top-left corner to down and right direction
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]  #colour of the blocks; this is done so that every adjacent block is different colour from neighbour

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))   # Drawing the blocks or say rectangle

	if clear_bg:  # To see the swapping and updates in list while sorting is happeming
		pygame.display.update()


def generate_starting_list(n, min_val, max_val): #To generate the starting lst; n=no. of element in lst; min_val & max_val are min and max possible value
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)  #generating random values b/w min and max_val inclusively
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst   # we make this variable so that we don't have to write draw_info.lst multiple times

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]  #Swapping Variables  
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)  # Redrawing the list, in arguement we've also passed the color of the swapping blocks 
				yield True  #So that while sorting is being done, other keys retain there functionality

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True) # Redrawing the list
			yield True

	return lst
# Similarly We could write any other Sorting Algo code which works as a generator then we are good to go.

def main():
	run = True   #for the main loop of the program
	clock = pygame.time.Clock()  # To regulate how fast the loop will be running

	n = 50  #no of blocks in list
	min_val = 0  # min value of block
	max_val = 100 # max value of block

	lst = generate_starting_list(n, min_val, max_val)  # generating the lst
	draw_info = DrawInformation(1000, 600, lst)  #creating the obj, to create the pygame window, with 1000=width;600=height;lst is the list of blocks
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:     # this loop will be constantly running in background otherwise program would just stop
		clock.tick(60)   #60fps here it means it representa the max no. of times this loop can run in 1 second

		if sorting:
			try:
				next(sorting_algorithm_generator)  #we gonna keep calling the generator until its done
			except StopIteration:   # Once we're done sorting the list, then stop
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():  
			if event.type == pygame.QUIT:#if we click X at top right, then it closes pygame window by coming out of the loop b/c of run==false
				run = False

			if event.type != pygame.KEYDOWN:  # Event when no key is pressed, then the loop continues
				continue

			if event.key == pygame.K_r:   #Event when R is pressed, Resetting the blocks
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:  # Event when Space is pressed
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)  #creating generator object
			elif event.key == pygame.K_a and not sorting: # Event when a is pressed, for Ascending
				ascending = True
			elif event.key == pygame.K_d and not sorting: # Event when d is pressed, for Descending
				ascending = False
			elif event.key == pygame.K_i and not sorting: # Event when i is pressed, for Insertion Sort
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting: # Event when b is pressed, for Bubble Sort
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
	pygame.quit()

if __name__ == "__main__":
	main()

	