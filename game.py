from tkinter import *
import sys
import random

class Board():
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.size = 600 // max(w,h)
        self.canvasDict = {} # Maps coordinate to drawing position
        self.tokens = {} # Key: (x,y) -> Val: Colour ; searching for surrounding pieces is constant time
        self.lastToken = None # (x, y, colour) ; Last position and colour stored

        for i in range(w):
            for j in range(h):
                self.tokens[(i,j)] = None

    def createToken(self, x, y, r, colour, width): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, fill=colour, width=width)

    def generateRandomTokens(self): # Random number of tokens in random positions
        colNum = random.randint(1, self.width)
        rowNum = random.randint(1, self.height)
        output = []
        seen = set()

        for _ in range(min(rowNum, colNum)):
                color = "black" if random.randint(0,1) else "white"
                row, col = random.randint(1, self.height) - 1, random.randint(1, self.width) - 1
                while (row, col) in seen:
                    row, col = random.randint(1, self.height) - 1, random.randint(1, self.width) - 1
                seen.add((row, col))
                output.append((row, col, color))

        return output

    def initTokens(self, tokens): # Consumes a list of tuples (pos, colour), size must be less than width x height
        for (y, x, colour) in tokens: # x,y denotes center coordinates
            self.tokens[(y,x)] = colour
            self.canvasDict[(y,x)] = self.createToken(self.size*(x + 0.5), self.size*(y + 0.5), 0.4 * self.size, colour, 2)

    def createBoard(self):
        for y in range(board.height):
            for x in range(board.width):
                x1 = x*self.size
                y1 = y*self.size
                x2 = x1 + self.size
                y2 = y1 + self.size
                canvas.create_rectangle((x1, y1, x2, y2), fill='white', width=2)


def onClick(event):
    # First need to check if piece exists on event click (needs to be in boundary as well - from testing, this doesn't need to be checked)
        # - If piece exists, then possibly needs to be computed

    # Map click coordinates to indices
        # - Find nearest center
    
    row, col = event.y // board.size, event.x // board.size
    if board.tokens[(row, col)]: # If there's a piece at the clicked position
        board.lastToken = (row, col, board.tokens[(row, col)])
    else:
        board.lastToken = None
    

def onRelease(event):
    row, col = event.y // board.size, event.x // board.size
    if board.lastToken and not board.tokens[(row, col)]: # If the last position exists and the hop space is free
        (old_x, old_y, old_col) = board.lastToken
        dist = (old_x - row)**2 + (old_y - col)**2
        if dist == 8 or dist == 4:
            hop_mid_x, hop_mid_y = (old_x + row) // 2, (old_y + col) // 2
            if not board.tokens[(hop_mid_x, hop_mid_y)]: # Nothing to hop over
                return
            mid_col = board.tokens[(hop_mid_x, hop_mid_y)]
            if old_col == "white":
                if mid_col == "white":
                    board.tokens[(hop_mid_x, hop_mid_y)] = "black"
                    board.tokens[(row, col)] = "black"
                else:
                    board.tokens[(hop_mid_x, hop_mid_y)] = "white"
                    board.tokens[(row, col)] = "black"
            else:
                if mid_col == "white":
                    board.tokens[(hop_mid_x, hop_mid_y)] = "black"
                    board.tokens[(row, col)] = "white"
                else:
                    board.tokens[(hop_mid_x, hop_mid_y)] = "white"
                    board.tokens[(row, col)] = "white"

            board.tokens[(old_x, old_y)] = None

            # Graphics manipulation

            # Moving
            canvas.move(board.canvasDict[(old_x, old_y)], board.size * (col - old_y), board.size * (row - old_x))
            board.canvasDict[(row, col)] = board.canvasDict[(old_x, old_y)]
            board.canvasDict[(old_x, old_y)] = None

            # Colour change
            canvas.itemconfig(board.canvasDict[(hop_mid_x, hop_mid_y)], fill=board.tokens[(hop_mid_x, hop_mid_y)])
            canvas.itemconfig(board.canvasDict[(row, col)], fill=board.tokens[(row, col)])


board = Board(10, 10)
root = Tk()

canvas = Canvas(root, width=600, height=600)
canvas.bind("<Button-1>", onClick)
canvas.bind("<ButtonRelease-1>", onRelease)
canvas.pack()


def close(event):
    #master.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing


board.createBoard()

# Trios 
#board.initTokens([(0,0, "white"), (1,1, "white"), (0,1, "white"), (3,3,"black"), (3,4,"black"), (4,4,"white")]) 

# Cluster
#board.initTokens([(1,1,"black"), (1,2,"black"), (1,3,"black"), (1,4,"black"), (0,1,"black")])

# Random
board.initTokens(board.generateRandomTokens())

root.bind('<Escape>', close)
root.mainloop()     
        
