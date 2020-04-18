from tkinter import *
import numpy as np
import math

class Trajectoire(object):
    CANVAS_SIZE = (300, 300)
    DRAW_METHOD = 0

    def __init__(self):
        self.root = Tk()

        self.Coordinates = np.array([[None, self.CANVAS_SIZE[0] // 2, self.CANVAS_SIZE[1] // 2]])
        self.c = Canvas(self.root, height=self.CANVAS_SIZE[0], width=self.CANVAS_SIZE[1], bg="white")

        self.c.bind("<Button-1>", func=self.draw)

        self.line_button = Button(self.root, text='line', command=lambda: self.change_method(nb=0))
        self.line_button.grid(row=0, column=0)

        self.arc_button = Button(self.root, text='arc', command=lambda: self.change_method(nb=1))
        self.arc_button.grid(row=0, column=1)

        self.coord_button = Button(self.root, text='cord', command=self.print_coord)
        self.coord_button.grid(row=0, column=2)

        self.cons_button = Button(self.root, text='consigne', command=self.conv_cord)
        self.cons_button.grid(row=0, column=3)

        self.c.grid(row=1, columnspan=4)
        self.root.mainloop()

    def draw(self, event):
        print("X = {0} et Y = {1}".format(event.x, event.y))
        self.draw_method(event)
        self.add_coord(event)

    def draw_method(self, event):
        x0, y0 = self.Coordinates[-1][1], self.Coordinates[-1][2]
        x1, y1 = event.x, event.y
        if self.DRAW_METHOD == 0:  # Create line
            self.c.create_line(x0, y0, x1, y1)
        elif self.DRAW_METHOD == 1:  # Create Arc
            self._create_arc((x0, y0), (x1, y1))

    def _create_arc(self, p0, p1):
        # source stackoverflow : https://stackoverflow.com/questions/36958438/draw-an-arc-between-two-points-on-a-tkinter-canvas
        extend_x = (self._distance(p0,p1) -(p1[0]-p0[0]))/2 # extend x boundary
        extend_y = (self._distance(p0,p1) -(p1[1]-p0[1]))/2 # extend y boundary
        startAngle = math.atan2(p0[0] - p1[0], p0[1] - p1[1]) *180 / math.pi # calculate starting angle
        self.c.create_arc(p0[0]-extend_x, p0[1]-extend_y ,
                               p1[0]+extend_x, p1[1]+extend_y,
                               extent=180, start=90+startAngle, style=ARC)

    def _distance(self, p0, p1):
        # source stackoverflow : https://stackoverflow.com/questions/36958438/draw-an-arc-between-two-points-on-a-tkinter-canvas
        '''calculate distance between 2 points'''
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def change_method(self, nb):
        if nb < 2:
            self.DRAW_METHOD = nb

    def add_coord(self, event):
        a = np.vstack((self.Coordinates, np.array([[self.DRAW_METHOD, event.x, event.y]])))
        self.Coordinates = a

    def conv_cord(self):
        data = []
        for i in range(len(self.Coordinates)):
            d, x, y = self.Coordinates[i]
            x_clas, y_clas = x, self.CANVAS_SIZE[1]-y
            data.append([d, (x_clas, y_clas)])
        print(data)

    def print_coord(self):
        print(self.Coordinates)






if __name__ == '__main__':
    Trajectoire()
