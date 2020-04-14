from tkinter import *
import numpy as np


class Trajectoire(object):
    CANVAS_SIZE = (300, 300)

    def __init__(self):
        self.root = Tk()

        self.Coordinates = np.array([[self.CANVAS_SIZE[0] // 2, self.CANVAS_SIZE[1] // 2]])
        self.c = Canvas(self.root, height=self.CANVAS_SIZE[0], width=self.CANVAS_SIZE[1], bg="white")

        self.c.bind("<Button-1>", func=self.draw_line)

        self.coord_button = Button(self.root, text='cord', command=self.print_coord)
        self.coord_button.grid(row=0, column=1)

        self.c.grid(row=1, columnspan=2)
        self.root.mainloop()

    def draw_line(self, event):
        print("X = {0} et Y = {1}".format(event.x, event.y))
        self.c.create_line(self.Coordinates[-1][0], self.Coordinates[-1][1], event.x, event.y)
        self.add_coord(event)

    def add_coord(self, event):
        a = np.vstack((self.Coordinates, np.array([[event.x, event.y]])))
        self.Coordinates = a

    def print_coord(self):
        print(self.Coordinates)


if __name__ == '__main__':
    Trajectoire()
