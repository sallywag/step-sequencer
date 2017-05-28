import pygame
from pygame.locals import *
import winsound
import sys 

#CLASSES ------
class MyRect(Rect):
	def __init__(self, location, size, type):
		super().__init__(location, size)
		self.type = type #type can be a note like 
#CLASSES ------          #c, c#, etc. It can also
                         #be full or empty in regards
#FUNCTIONS ------        #to the pianoroll
def getKeyboard(x_loc, keysize): 
	keys     = ['c' , 'c#', 'd', 'd#', 'e', 
	            'f' , 'f#', 'g', 'g#', 'a',
                'a#',  'b', 'c2']
	num_keys = 13
                       
	for y_loc in range(0, num_keys*keysize[1], keysize[1]):
		yield MyRect((x_loc, y_loc+keysize[1]), keysize, keys.pop())
		
def getPianoroll(x_loc, boxsize, num_columns):
	num_boxes = 13
	for i in range(num_columns):
		column = []
		for y_loc in range(0, num_boxes*boxsize[1], boxsize[1]):
			column.append(MyRect((x_loc, y_loc+boxsize[1]), boxsize, 'empty'))
		
		x_loc += boxsize[0]
		yield column
	
def drawKeyboard(image, valid_types, keyboard):
	for key in keyboard:
		if key.type in valid_types:
			DISPLAYSURF.blit(image, (key.left, key.top))
			
def drawPianoroll(image, valid_types, pianoroll):
	for column in pianoroll:
		for square in column:
			if square.type in valid_types:
				DISPLAYSURF.blit(image, (square.left, square.top))
			
def highlight(piece, color, line_width):
	pygame.draw.line(DISPLAYSURF, color, (piece.left, piece.top), 
		             (piece.left + piece.width, piece.top), line_width)
					 
	pygame.draw.line(DISPLAYSURF, color, (piece.left, piece.top), 
		             (piece.left, piece.top + piece.height), line_width)
					 
	pygame.draw.line(DISPLAYSURF, color, 
		             (piece.left + piece.width, piece.top), 
		             (piece.left + piece.width, piece.top + piece.height), 
						                                       line_width)			 
	pygame.draw.line(DISPLAYSURF, color, 
		             (piece.left, piece.top + piece.height), 
		             (piece.left + piece.width, piece.top + piece.height), 
						                                       line_width)
															   
def playsound(note, sound_dict):
	winsound.PlaySound(sound_dict[note], winsound.SND_ASYNC)
	
def playPianoroll(pianoroll, sound_dict, pianoroll_dict, image):
	DISPLAYSURF.blit(image, (35,0)) #FIX
	pygame.display.update()
	
	for column in pianoroll:
		for index in range(len(column)):
			if column[index].type == 'full':
				playsound(pianoroll_dict[index], sound_dict)
				highlight(column[index], GREEN, 3) #FIX SLOPPY
				pygame.display.update()
				
		pygame.time.delay(250)
#FUNCTIONS ------
	
#GLOBALS ------wid  hei 
WINDOWSIZE  = (640, 480)
MARGIN      = 32
DISPLAYSURF = pygame.display.set_mode(WINDOWSIZE) #create surface object to
FPS         = 30                                  #draw on of size WINDOWSIZE
FPSCLOCK    = pygame.time.Clock()
#GLOBALS ------

#COLORS ------
BLACK = (0, 0,   0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
#COLORS ------

def main():
	pygame.init()
	pygame.display.set_caption('Keyboard')
	
	#IMAGES ------
	white_key_img = pygame.image.load('images/white.png').convert()
	black_key_img = pygame.image.load('images/black.png').convert()
	empty_img     = pygame.image.load('images/empty.png').convert()
	full_img      = pygame.image.load('images/full.png').convert()
	playing_img   = pygame.image.load('images/playing.png').convert()
	#IMAGES ------
	
	#OBJECTS/VARIABLES ------
	key_size       = (64, 32)
	box_size       = (32, 32)
	keyboard_xloc  = 32  #where keyboard starts on x axis
	pianoroll_xloc = 128 #where pianoroll starts on x axis
	num_columns    = 9
	white_keys     = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c2'] #used to generate keyboard
	black_keys     = ['c#', 'd#', 'f#', 'g#', 'a#']            #used to generate keyboard
	sound_dict     = {'c' : 'sounds/c.wav' , 'c#': 'sounds/c#.wav', #map MyRect type
				 	  'd' : 'sounds/d.wav' , 'd#': 'sounds/d#.wav', #to a sound file
				  	  'e' : 'sounds/e.wav' , 'f' : 'sounds/f.wav' ,
					  'f#': 'sounds/f#.wav', 'g' : 'sounds/g.wav' ,
					  'g#': 'sounds/g#.wav', 'a' : 'sounds/a.wav' ,
					  'a#': 'sounds/a#.wav', 'b' : 'sounds/b.wav' ,
					  'c2': 'sounds/c2.wav'}
	pianoroll_dict = { 12:'c' , 11:'c#' ,  10:'d' , #map integer to MyRect type
	                    9:'d#',  8:'e'  ,   7:'f' ,
                        6:'f#',  5:'g'  ,   4:'g#', 
					    3:'a' ,  2:'a#' ,   1:'b' ,
					    0:'c2'}	
					   
	keyboard       = list(getKeyboard(keyboard_xloc, key_size)) #generate a list representing the keyboard
	pianoroll      = list(getPianoroll(pianoroll_xloc, box_size, num_columns)) #generate a list representing
	#OBJECTS/VARIABLES ------												   #the pianoroll
	
	while True:
		DISPLAYSURF.fill(BLACK)
		
		#DRAWIMAGES ------
		drawKeyboard(white_key_img, white_keys, keyboard)
		drawKeyboard(black_key_img, black_keys, keyboard) ##FIX
		drawPianoroll(empty_img, ('empty'), pianoroll)
		drawPianoroll(full_img, ('full'), pianoroll)
		#DRAWIMAGES ------
		
		
		#HIGHLIGHT ------
		for key in keyboard:
			if key.collidepoint(pygame.mouse.get_pos()):
				highlight(key, BLUE, 3)
				
		for column in pianoroll:
			for square in column:
				if square.collidepoint(pygame.mouse.get_pos()):
					highlight(square, BLUE, 3)
		#HIGHLIGHT ------
		
		#EVENT LOOP ------
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			elif event.type == KEYDOWN and event.key == K_SPACE:
				playPianoroll(pianoroll, sound_dict, pianoroll_dict, playing_img)
				
			elif event.type == KEYDOWN and event.key == K_LEFT:
				if num_columns != 1:
					num_columns -= 1
					pianoroll    = list(getPianoroll(pianoroll_xloc, box_size, num_columns))
					
			elif event.type == KEYDOWN and event.key == K_RIGHT:
				if num_columns != 15:
					num_columns += 1
					pianoroll    = list(getPianoroll(pianoroll_xloc, box_size, num_columns))
				
			elif event.type == MOUSEBUTTONUP:
				for key in keyboard: #FIXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
					if key.collidepoint(pygame.mouse.get_pos()): # fix 
						playsound(key.type, sound_dict)
				for column in pianoroll: #tooo slow!!! make a rect onto of rect to click
					for square in column:
						if square.collidepoint(pygame.mouse.get_pos()): #FIX SLOW
							if square.type == 'empty':
								square.type = 'full'
							else:
								square.type = 'empty'
		#EVENT LOOP ------
				
		pygame.display.update()
		FPSCLOCK.tick(FPS)
	
if __name__ == '__main__':
	main()