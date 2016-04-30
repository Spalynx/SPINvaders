#file	-	SPiN_entity.py
#pack	-	SPiNvaders
#ver	- 	0.2.5
#since 	-	4.28.16
#author	-	Spalynx

import tkinter as tk
import time

W_HEIGHT = 480
W_WIDTH = 640

''' Extended by: Player, Missle, Enemy, Barrier
#	This class handles basic values of the derived character.
#	It is entirely up to the derived class to update and fill these values
		ESPECIALLY posx/posy with every movement!
'''
class Character:
	name = "";		#Tag to be used in the canvas, I might refactor this to be called tag.
	posx = 0;		#X value on the canvas -> UPDATE THIS ALWAYS <-
	posy = 0;		#Y value on canvas, same as posx.
	canvas = None		#The canvas it rests, I might have just grabbed it from parent, but I use this too much.
	alive = True		#Boolean value if the item is alive or not.
	fired = []		#
	parent = None 		#In most cases, should be GameScreen; Missle will have player or enemy as it's parent.

	def __init__(self):
		import warnings as w
		w.warn("Player: No constructor params: Dude, just init it with values.", SyntaxWarning)

	def __init__(self, n: str, x: int, y: int, c: tk.Canvas, parent):
		''' Filling variables, nothing else.'''
		self.posx = x
		self.posy = y
		self.name = n
		self.canvas = c
		self.parent = parent

	def draw(self):
		'''Draws the character to the canvas. Since this should be mostly abstract, it's just a box.'''
		self.canvas.create_rectangle(self.posx, self.posy,self.posx+30,self.posy+30, tag=self.name,fill="blue")
	def move(self):
		'''Since I'm making psuedo abstract class, I'm just filling this fn with a death checker'''
		if(not self.alive):
			self.death()
	def death(self):
		'''Kills the character, this should draw an explosion or something later.'''
		self.alive = False
		#TODO: EXPLOSIONS!

	def set_pos(self, x, y):
		'''Accessor: Allows easy setting of the player's position.'''
		self.posx = x
		self.posy = y

	def check_death(self):
		''' "Conscious, am I dead?" - Dory'''
		return

	def fire_missle(self):
		''' Fires a missle. This fn checks to see if you have fired too many missles.
			if you have, it whiffs the shot, and flashes,
			if you have not, it creates a missle, adds it to the fired array, and sets it to move.
		'''

		if(len(self.fired) < 4):
			self.fired.append(Missle(self, len(self.fired)))
		else:
			#Whiffs the shot, produces a red box.
			#TODO: Consider simply flashing the player box red.
			self.canvas.create_rectangle(self.posx, self.posy, self.posx+30, self.posy+10, fill="red", tag="whiff")
			self.canvas.after(100, self.whiff_missle)
	def whiff_missle(self):
		''' Simply deletes the box created in fire missle's whiff case. '''
		#TODO: Insert sound here.
		self.canvas.delete("whiff") #might need to get the item

''' This class represents the player controlled entity in the program.
#	The player is allowed sideways movement and the ability to fire a missle.
#	Every time the player fires a missle, the game subtracts points, in an attempt to
		deterr spammers.
#	This class also internally handles missle handling, I might eventually move that up
		to the parent.
'''
class Player(Character):
	misslecount = 0
	key = ''

	def __init__(self):
		''' Sets some basic values if you're lazy. '''
		self.name = "player"
		self.posx = 20
		self.posy = W_HEIGHT - 50
	def __init__(self, n: str, x: int, y: int, c: tk.Canvas, par):
		''' Sets the values with the superclasses' constructor. '''
		Character.__init__(self,n,x,y,c,par)
		self.move()

	def move(self):
		''' Moves the player based on user input. This also handles death checking each frame of input. '''
		
		#checks if the player is dead, if it is, input is not accepted.
		self.check_death();
		if(self.alive):
			offset = W_WIDTH/50
			
			#Actions performed from input
			if self.key == "Left" and self.posx > 25:
				self.posx -= offset
				self.canvas.move("player", -offset, 0)
			elif self.key == 'Right' and self.posx < W_WIDTH-60:
				self.posx += offset
				self.canvas.move("player", offset, 0)
			elif self.key == 'space':
				self.fire_missle()



			self.key = "" #fun fact: without this line, autofire
			self.canvas.after(16, self.move) #~60FPS on movement

	#REFACTOR: fire_missle and whiff_missle sent to superclass.

	#TODO: do
	def check_death(self):
		return

''' This class represents the enemy entity, multiples of this are handled by their '''
class Enemy(Character):
	misslecount = 0
	size = 0
	key = ''

	def __init__(self):
		''' Sets some basic values if you're lazy. '''
		self.name = "enemy"
		self.posx = 20
		self.posy = W_HEIGHT - 50
	def __init__(self, n: str, x: int, y: int, c: tk.Canvas, par, size:int):
		''' Sets the values with the superclasses' constructor. '''
		self.size = size
		Character.__init__(self,n,x,y,c,par)
		self.move()
	def __init__(self, enemynum: int, x: int, y: int, c: tk.Canvas, par, size: int):
		''' Sets the values with the superclasses' constructor. Creates the name based upon enemy index. '''
		n = self.get_enemy_name(enemynum);
		self.size = size
		Character.__init__(self,n,x,y,c,par)
		self.move()

	def get_enemy_name(self, enemynum: int) -> str:
		''' Given the number, creates a string name of the enemy. '''
		return "enemy" + str(enemynum);
	def draw(self):
		'''Draws the character to the canvas. Since this should be mostly abstract, it's just a box.'''
		self.canvas.create_rectangle(self.posx, self.posy,self.posx+self.size,self.posy+self.size, tag=self.name,fill="orange")
class Missle(Character):
	UPMOVE = None 		#IF true the missle flies up, otherwise it flies down.
	parent = None		#This is already in Character, I might delete, or keep for verbosity.
	
	#TODO: Specify errors for no param constructor.
	def __init__(self,parent, listnum):
		''' Fills variables in the parent, and decides which way it should move.'''
		self.canvas = parent.canvas
		self.name = parent.name[:1] + "_mis" + str(parent.misslecount)
		self.posx = parent.posx + 15
		self.parent = parent;
		self.listnum = listnum
		
		#If the parent's name is player it moves up, otherwise, it moves down.
		if parent.name == "player":
			self.UPMOVE = True
			self.posy = parent.posy + 15
		else:
			self.UPMOVE = False
			self.posy = parent.posy - 35
		
		#The missle should always move.
		self.draw()
		self.move()
	
	def draw(self):
		''' Draws the missle to screen, x10*y20 dimensions. '''
		#TODO: picture of a missle.
		self.canvas.create_rectangle(self.posx, self.posy, self.posx+10, self.posy+20, tag=self.name, fill="white")
	def move(self):
		''' Moves the missle either up or down, checks impact for each frame. '''
		offset = 20

		if (self.UPMOVE):
			self.canvas.move(self.name, 0, -offset)
			self.posy -= offset
		else:
			self.canvas.move(self.name, 0, offset)
			self.posy += offset

		#Checks to see if it has encountered any case that causes death.
		self.check_death()
		if(self.alive):
			self.canvas.after(100,self.move)
	def check_death(self):
		'''Checks to see if the missle encountered any death along it's way. '''
		player = self.parent
		
		#Case for going out of bounds.
		if(self.posy < 20 or self.posy > W_HEIGHT-20):
			self.death()
			return;
		#Case for encountering player
		elif((self.posy <= player.posy+30) and (self.posy >= player.posy)
				and (self.posx <= player.posx+30) and (self.posx >= player.posx)):
			player.death(); #TODO: possibly replace with checkdeath
			return;
		#Case for encountering enemies, I might split this based on enemy types.
		#OR I might just check the GameScreen's characters list, kill all birds with one stone.
		"""for x in range (0, ENEMIES):
			enemy = self.canvas.find_withtag("enemy" + str(x))[0]
			if(self.posy <= enemy.posy+30 and self.posy >= enemy.posy
				and self.posx <= enemy.posx+30 and self.posx >= enemy.posx):
				enemy.death();
				return;
		"""

		return;
	def death(self):
		''' This kills the deadly exploding munitions round. Deletes from canvas, and form fired list.'''
		self.alive = False
		self.canvas.delete(self.canvas.find_withtag(self.name))
		self.remove_from_list();

	def remove_from_list(self):
		'''Do I really need a function for just this line? Maybe I can use this for more?'''
		self.parent.fired.remove(self)
