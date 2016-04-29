#ver 0.2.1
#since 4.28.16
#by Spalynx
import tkinter as tk
import time

W_HEIGHT = 480
W_WIDTH = 640
SCORE = 0;
LIVES = 3;
ENEMIES = 20;
import SPiN_entities as spinE

class GameScreen(tk.Frame):
	def __init__(self, master=None):
		self.canvas = tk.Canvas(master, width= W_WIDTH, height = W_HEIGHT)
		self.characters = [spinE.Player("player", W_WIDTH/2, W_HEIGHT-60, self.canvas)]
		tk.Frame.__init__(self, master)
		self.pack()
		self.game_run()

    #builds all of the widgets to be placed on screen.
	def game_run(self):
		self.canvas.update()
		self.canvas.create_rectangle(10, W_HEIGHT-10, W_WIDTH-10, 10, 
				fill="black" , width=20, outline="grey", tag="background")
		
		self.characters[0].draw();
		self.canvas.pack()

		#init lives and scores
		self.draw_score()
		self.draw_lives()
		self.lives_iterate(0)
		self.score_iterate(0)

	def on_key_press (self, event):
		if event.keysym == "Left" or event.keysym == 'Right' or event.keysym == 'space':
			if event.keysym == 'space':
				self.score_iterate(-1)
			self.characters[0].key = event.keysym;

	def lives_iterate(self, i):
		global LIVES
		LIVES += i;
		self.canvas.itemconfigure(self.canvas.find_withtag("lives"),
			text="[" + str(LIVES) + "] your score")  
	def score_iterate(self, i):
		global SCORE
		SCORE += i;
		self.canvas.itemconfigure(self.canvas.find_withtag("score"), 
			text="[" + str(SCORE) + "] your score") 

	def draw_score(self):
		self.canvas.create_text(100,10,tag = "score", 
			text = "[0] your score", justify = tk.RIGHT, fill="red") 
	def draw_lives(self):
		self.canvas.create_text(W_WIDTH-100, 10, tag = "lives",
			text = "[]] lives left", justify = tk.LEFT, fill="red")