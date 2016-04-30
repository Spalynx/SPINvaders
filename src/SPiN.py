#file	-	SPiN_entity.py
#pack	-	SPiNvaders
#ver	- 	0.0.1
#since 	-	4.16.16
#author	-	Spalynx

import tkinter as tk
import time
# GOOD EXAMPLE: http://stackoverflow.com/questions/24717440/tkinter-space-invaders-enemy-movement
# TKINTER LIBS: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
#               http://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.find_withtag-method
#               http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_text.html
#               http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/images.html#class-BitmapImage
W_HEIGHT = 480
W_WIDTH = 640

import SPiN_game as spinG

''' Review README.md and LICENSE.md before continuing.
	This program is simply a lame, library minimalistsic Space Invaders clone.
	I've always wanted to make a game, and it seemed like a good way to learn python again.
'''

root = tk.Tk()
root.title("SPInvaders v.0.2.0")
root.resizable(width = 1, height = 1)
root.geometry( '{}x{}'.format( W_WIDTH+10, W_HEIGHT+10) )
app = spinG.GameScreen(root)
root.bind('<Key>', app.on_key_press)

app.mainloop()
time.sleep(2)
