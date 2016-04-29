#ver 0.1.0
#since 4.16.16
#by Spalynx
import tkinter as tk
import time
# GOOD EXAMPLE: http://stackoverflow.com/questions/24717440/tkinter-space-invaders-enemy-movement
# TKINTER LIBS: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
#               http://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.find_withtag-method
#               http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_text.html
#               http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/images.html#class-BitmapImage
W_HEIGHT = 480
W_WIDTH = 640
SCORE = 0;
LIVES = 3;

class SPInvadersGui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)        
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        global canvas
        canvas = tk.Canvas(self, width= W_WIDTH, height = W_HEIGHT)
        canvas.pack()

        canvas.update()
        canvas.create_rectangle(10, W_HEIGHT-10, W_WIDTH-10, 10, 
               fill="black" , width=20, outline="grey", tag="background")

        self.drawPlayer()
        self.drawScore()
        self.drawLives()
        
        return;

    def on_key_press (self, event):
        c = canvas.coords("player")
        offset = W_WIDTH/50

        if event.keysym == "Left" and c[0] > 20:
            canvas.move("player", -offset, 0)
        elif event.keysym == 'Right' and c[2] < W_WIDTH-30:
            canvas.move("player", offset, 0)
        elif event.keysym == 'space':
            print("bang bang")
            self.scoreIterate(-1)

    def drawPlayer (self):
         canvas.create_rectangle(50, W_HEIGHT-50, 20, W_HEIGHT-20, fill="orange", tag = "player")

    #def drawEnemy (self):
    #def drawBarricade(self):
    def drawScore(self):
        canvas.create_text(100,10,tag = "score", 
            text = "[] your score", justify = tk.RIGHT, fill="red")
    def scoreIterate(self, i):
        global SCORE
        SCORE += i;
        canvas.itemconfigure(canvas.find_withtag("score"), 
            text="[" + str(SCORE) + "] your score") 
    def drawLives(self):
        canvas.create_text(W_WIDTH-100, 10, tag = "lives",
            text = "[] lives left", justify = tk.LEFT, fill="red")
    def livesIterate(self, i):
        global LIVES
        LIVES += i;
        canvas.itemconfigure(canvas.find_withtag("lives"),
            text="[" + str(LIVES) + "] your score")   

root = tk.Tk()
root.title("SPInvaders v.0.1.0")
root.resizable(width = 1, height = 1)
root.geometry( '{}x{}'.format( W_WIDTH+10, W_HEIGHT+10) )
app = SPInvadersGui(master = root)
root.bind('<Key>', app.on_key_press)

app.mainloop()
time.sleep(2)
