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

class Character:
	name = "";
	posx = 0;
	posy = 0;
	sizey = 40
	sizex = 40
	mvmt_spd = 20
	canvas = None
	alive = True
	fired = []

	def __init__(self, n: str, x: int, y: int, c: tk.Canvas):
		self.posx = x
		self.posy = y
		self.name = n
		self.canvas = c

	def draw(self):
		self.canvas.create_rectangle(self.posx, self.posy,self.posx+30,self.posy+30, tag=self.name,fill="blue")
		return
	def move(self):
		if(not self.alive):
			self.death()
	def death(self):
		self.alive = False
		#freeze or something

	def set_pos(self, x, y):
		self.posx = x
		self.posy = y

	def check_death(self):
		return

class Player(Character):
	misslecount = 0
	key = ''

	#override draw with a picture
	#override death with screen flashes.
	def __init__(self):
		self.name = "player"
		self.posx = 20
		self.posy = W_HEIGHT - 50
	def __init__(self, n: str, x: int, y: int, c: tk.Canvas):
		Character.__init__(self,n,x,y,c)
		self.move()

	def move(self):
		self.check_death();
		if(self.alive):
			offset = W_WIDTH/50

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

	def fire_missle(self):
		if(len(self.fired) < 4):
			self.fired.append(Missle(self, len(self.fired)))
		else:
			self.canvas.create_rectangle(self.posx, self.posy, self.posx+30, self.posy+10, fill="red", tag="whiff")
			self.canvas.after(100, self.whiff_missle)
	def whiff_missle(self):
		#insert sound here
		self.canvas.delete("whiff") #might need to get the item
		return;
	#TODO: do
	def check_death(self):
		return

class Missle(Character):
	UPMOVE = None
	parent = None
	def __init__(self,parent, listnum):
		self.canvas = parent.canvas
		self.name = parent.name + "_mis" + str(parent.misslecount)
		self.posx = parent.posx + 15
		self.parent = parent;
		self.listnum = listnum

		if parent.name == "player":
			self.UPMOVE = True
			self.posy = parent.posy + 15
		else:
			self.UPMOVE = False
			self.posy = parent.posy - 35

		self.draw()
		self.move()
					
	def draw(self):
		self.canvas.create_rectangle(self.posx, self.posy, self.posx+10, self.posy+20, tag=self.name, fill="white")
	def move(self):
		offset = 20

		if (self.UPMOVE):
			self.canvas.move(self.name, 0, -offset)
			self.posy -= offset
		else:
			self.canvas.move(self.name, 0, offset)
			self.posy += offset

		self.check_death()
		if(self.alive):
			self.canvas.after(100,self.move)
	def check_death(self):
		player = self.parent

		if(self.posy < 0 or self.posy > W_HEIGHT):
			self.death()
			return;
		elif((self.posy <= player.posy+30) and (self.posy >= player.posy)
				and (self.posx <= player.posx+30) and (self.posx >= player.posx)):
			player.death(); #TODO: possibly replace with checkdeath
			return;
		#-=-=-=-=-=-=-
		"""for x in range (0, ENEMIES):
			enemy = self.canvas.find_withtag("enemy" + str(x))[0]
			if(self.posy <= enemy.posy+30 and self.posy >= enemy.posy
				and self.posx <= enemy.posx+30 and self.posx >= enemy.posx):
				enemy.death();
				return;
		"""

		return;
	def death(self):
		self.alive = False
		self.canvas.delete(self.canvas.find_withtag(self.name))
		self.remove_from_list();

	def remove_from_list(self):
		self.parent.fired.remove(self)