from tkinter import *
import numpy as np


class Trajectoire(object):
    CANVAS_SIZE = (300, 300)
    DRAW_METHOD = 0

    def __init__(self):
        self.root = Tk()

        self.Coordinates = np.array([[self.CANVAS_SIZE[0] // 2, self.CANVAS_SIZE[1] // 2]])
        self.c = Canvas(self.root, height=self.CANVAS_SIZE[0], width=self.CANVAS_SIZE[1], bg="white")

        self.c.bind("<Button-1>", func=self.draw)

        self.line_button = Button(self.root, text='line', command=lambda : self.change_method(nb=0))
        self.line_button.grid(row=0, column=0)

        self.arc_button = Button(self.root, text='rectangle', command=lambda : self.change_method(nb=1))
        self.arc_button.grid(row=0, column=1)

        self.coord_button = Button(self.root, text='cord', command=self.print_coord)
        self.coord_button.grid(row=0, column=2)

        self.c.grid(row=1, columnspan=3)
        self.root.mainloop()

    def draw(self, event):
        print("X = {0} et Y = {1}".format(event.x, event.y))
        self.draw_method(event)
        self.add_coord(event)

    def draw_method(self, event):
        if self.DRAW_METHOD == 0: # Create line
            self.c.create_line(self.Coordinates[-1][0], self.Coordinates[-1][1], event.x, event.y)
        elif self.DRAW_METHOD == 1 : # Create Rectangle
            x0, y0 = self.Coordinates[-1][0], self.Coordinates[-1][1]
            x1, y1 = event.x, event.y
            self.c.create_rectangle(x0,y0,x1,y1)

    def change_method(self, nb):
        if nb<2:
            self.DRAW_METHOD=nb

    # def method(self, i):
    #     switcher={
    #         0:'Ligne',
    #         1:'Rotation',
    #         2:'Arc',
    #         3:'Cercle',
    #         4:'Carré'
    #     }
    #     return switcher.get(i,"Invalid method")

    def add_coord(self, event):
        a = np.vstack((self.Coordinates, np.array([[event.x, event.y]])))
        self.Coordinates = a

    def print_coord(self):
        print(self.Coordinates)


if __name__ == '__main__':
    Trajectoire()
