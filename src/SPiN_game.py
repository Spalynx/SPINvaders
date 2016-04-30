#file	-	SPiN_game.py
#pack	-	SPiNvaders
#ver	- 	0.2.5
#since 	-	4.28.16
#author	-	Spalynx

import SPiN_entities as spinE
import tkinter as tk
import time

W_HEIGHT = 480
W_WIDTH = 640

''' This is one of the three top level classes used by SPiN.py class.
#	GameScreen is the overall class for starting the game, while TitleScreen,
#		and ScoreScreen control the starting and ending screens respectively.
#
#	GameScreen extends tk.Frame and implements a tk.Canvas within, and places
#		entities on the canvas and within it's master array.
'''

class GameScreen(tk.Frame):
	SCORE = 0;	LIVES = 3;	ENEMIES = 40;
	characters = None;	 canvas = None;
	
	def __init__(self, master=None):
		''' Inits the canvas, and the main entities list. '''

		self.canvas = tk.Canvas(master, width= W_WIDTH, height = W_HEIGHT)
		self.characters = [spinE.Player("player", W_WIDTH/2, W_HEIGHT-60, self.canvas, self)]
		tk.Frame.__init__(self, master)
		self.pack()
		self.game_run()

	def game_run(self):
		''' Creates the background and it's border, and draws all entities, then scoreboard. '''

		self.canvas.update()
		self.canvas.create_rectangle(10, W_HEIGHT-10, W_WIDTH-10, 10,
				fill="black" , width=20, outline="grey", tag="background")
		e = EnemyHandler(self.ENEMIES, self)

		#draws all characters
		self.characters[0].draw();
		e.draw()
		self.canvas.pack()

		#init lives and score
		self.draw_score()
		self.draw_lives()
		self.lives_iterate(0)
		self.score_iterate(0)

	def on_key_press (self, event):
		'''Event handler for keypress, ships the key straight to the player for decisions. '''
			#TODO: Make Event handling happen in the player class; this method requires constant updating.
			#TODO: Allow mouse movement and clicks, because no matter how retro you get, mice are neato.
		
		if event.keysym == "Left" or event.keysym == 'Right' or event.keysym == 'space':
			#if it's left/right/space send to player, else no thanks.
		
			if event.keysym == 'space':
				#spammers are not very fun.
				self.score_iterate(-1)
			self.characters[0].key = event.keysym;
		else:
			return

	def lives_iterate(self, i):
		'''Adds a value to the lives in the class, if they go below zero, the game ends.'''

		self.LIVES += i;
		self.canvas.itemconfigure(self.canvas.find_withtag("lives"),
			text="[" + str(self.LIVES) + "] your score")
	def score_iterate(self, i):
		'''Adds a value to the score in the class, if they go below zero, the game ends.'''
		self.SCORE += i;
		
		#Updates the lives printed on screen.
		self.canvas.itemconfigure(self.canvas.find_withtag("score"),
			text="[" + str(self.SCORE) + "] your score")

	def draw_score(self):
		'''Draws the score to screen, this should only be called once per game.'''
		self.canvas.create_text(100,10,tag = "score",
			text = "[0] your score", justify = tk.RIGHT, fill="red")
	def draw_lives(self):
		'''Draws the lives to screen, this should only be called once per game.'''
		self.canvas.create_text(W_WIDTH-100, 10, tag = "lives",
			text = "[]] lives left", justify = tk.LEFT, fill="red")
	def end_game():
		''' You just lost! This function sends you to the high score screen.'''
		ScoreScreen(SCORE)

class EnemyHandler:
	enemysize = 20
	characters = None
	count = 0

	def __init__(self, enemycount: int, parent: GameScreen):
		'''Building enemycount amount of enemies, setting their positions and names.'''
		self.characters = parent.characters
		self.count = enemycount

		for x in range (0, self.count):
			column = x//10;	row = x - column*10; #Row strips the leading tens num, column strips the ones num.
			print(": " + str(row))
			#Creates enemies in the correct location, and adds to the characters list. 
			self.characters.append( spinE.Enemy(x, 	30 + row*(self.enemysize + 10),
						30 + column*(self.enemysize + 10), 
						parent.canvas, parent, self.enemysize) )
			#consider calculating the x and y info inside the enemy class.

	def draw(self):
		import string
		for char in self.characters:
			if(str.find(char.name, "enemy") >= 0):
				#if enemy is in the tag, draw it.
				print("{" + str(char.posx) + " , " + str(char.posy) + "}")
				char.draw()

