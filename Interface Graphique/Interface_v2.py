import matplotlib.pyplot as plt
import numpy as np
import math
import tkinter
import os
import matplotlib.patches as mpatches

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


class Interface():
    # VARIABLES
    FIGSIZE = (5, 4)
    DPI = 100
    DRAW_METHOD = 1
    AXIS = [-10, 10, -10, 10]
    GRID =True

    def __init__(self):
        ## Initialisation de Tkinter
        self.root = tkinter.Tk()
        self.root.wm_title("Interface Commande Robot")

        # Variables
        self.plt_draw = np.zeros((1, 2))  # Coordonnées interprété par matplotlib pour le tracé
        self.plt_draw[0] = np.array([0, 1])
        self.command = np.zeros((1, 3))
        self.command[0] = np.array([1, 0, 1])
        self.directions = np.array([[0, 1]])

        self.setup()
        self.drawing, = self.ax.plot(self.plt_draw[:, 0], self.plt_draw[:, 1])

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.on_key_press)

        self.set_buttons()

    def setup(self):
        """Mise en place de la Figure Matplotlib"""
        self.fig = Figure(figsize=self.FIGSIZE, dpi=self.DPI)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis(self.AXIS)

        self.set_grid()

        self.robot_im = plt.imread('robot.png')
        self.imgplot = self.ax.imshow(self.robot_im, origin=(0,1), extent=([-1, 1, 0, 2]))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

    def set_grid(self):
        if self.GRID:
            # Major ticks, minor ticks every
            major_ticks = np.arange(self.AXIS[0], self.AXIS[1], 1)
            # minor_ticks = np.arange(-10, 11, 0.5)

            self.ax.set_xticks(major_ticks)
            # self.ax.set_xticks(minor_ticks, minor=True)
            self.ax.set_yticks(major_ticks)
            # self.ax.set_yticks(minor_ticks, minor=True)

            # And a corresponding grid
            self.ax.grid(which='both', alpha=0.2)
            self.ax.set_axisbelow(True)

    def set_buttons(self):
        """Mise en place des boutons sur Tkinter"""

        # Create new window to add entries by hand
        self.window_button= tkinter.Button(self.root, text="Command Window", command=self.create_window)
        self.window_button.pack(side=tkinter.LEFT)

        self.update_methodbutton = tkinter.Button(master=self.root, text="Update",
                                                  command=self.change_method)
        self.update_methodbutton.pack(side=tkinter.LEFT)

        self.erase_methodbutton = tkinter.Button(master=self.root, text="Erase",
                                                  command=self.erase_plt)
        self.erase_methodbutton.pack(side=tkinter.LEFT)

        self.command_button = tkinter.Button(master=self.root, text="Command", command=self.print_command)
        self.command_button.pack(side=tkinter.LEFT)

        self.export_button = tkinter.Button(master=self.root, text="Export", command=self.command_txt)
        self.export_button.pack(side=tkinter.LEFT)

        self.quit_button = tkinter.Button(master=self.root, text="Quit", command=self._quit)
        self.quit_button.pack(side=tkinter.BOTTOM)

    def update_method(self):
        """Tempoiraire, c'est pour mettre à jour la méthode de tracé, ici 1 est la ligne droite"""
        self.DRAW_METHOD = 10
        print(self.DRAW_METHOD)

    def erase_plt(self):
        self.plt_draw = np.zeros((1, 2))  # Coordonnées interprété par matplotlib pour le tracé
        self.plt_draw[0] = np.array([0, 1])
        self.command = np.zeros((1, 3))
        self.command[0] = np.array([1, 0, 1])
        self.directions = np.array([[0, 1]])
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.ax.figure.canvas.draw()


    def change_method(self):
        if self.DRAW_METHOD < 3:
            self.DRAW_METHOD += 1
        else:
            self.DRAW_METHOD=1

    def on_key_press(self, event):
        """Gestion de l'évènement clic gauche et gestion du tracé"""
        print("you pressed ({0},{1})".format(event.xdata, event.ydata))
        key_press_handler(event, self.canvas, self.toolbar)
        if event.inaxes != self.ax.axes: return
        x, y = event.xdata, event.ydata
        if self.DRAW_METHOD == 1:  # Ligne droite
            self.draw_lineinter(x, y)
        if self.DRAW_METHOD == 2:  # CIR
            self.draw_CIR(10, self.plt_draw[-1][0], self.plt_draw[-1][1], x, y)
            self.command = np.vstack((self.command, np.array([2, x, y])))
        # Update Canvas
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.ax.figure.canvas.draw()

    def create_window(self):
        self.window = tkinter.Toplevel(self.root)
        self.set_windowbutton()


    def get_ang(self, v1, v2, dir=False, direction=(0, 1)):
        """Détermine l'angle de rotation avec considération possible de la direction précédante"""
        vect1, vect2 = v1, v2
        if dir:
            vect2 = vect2 - vect1
            vect1 = direction
        v1_unit = vect1 / np.linalg.norm(vect1)
        v2_unit = vect2 / np.linalg.norm(vect2)
        dot_product = np.dot(v1_unit, v2_unit)
        return np.arccos(dot_product)

    def ROT(self):
        return 0

    def LIN(self):
        return 0

    def CIR(self):
        print(self.plt_draw[-1][0], self.plt_draw[-1][1], self.xcirentry.get(), self.ycirentry.get())
        self.draw_CIR(float(self.rcirentry.get()), self.plt_draw[-1][0], self.plt_draw[-1][1], float(self.xcirentry.get()), float(self.ycirentry.get()))
        self.command = np.vstack((self.command, np.array([2, self.xcirentry.get(), self.ycirentry.get()])))

    def draw_lineinter(self, x,y):
        dv = x - self.plt_draw[-1][0], y - self.plt_draw[-1][1]
        angle = self.get_ang(self.plt_draw[-1], np.array([x, y]), dir=True,
                             direction=self.directions[-1])  # Détermination de l'angle de rotation (valeur absolue)
        self.directions = np.vstack(
            (self.directions, np.array(dv / np.linalg.norm(dv))))  # Mise à jour des directions deu robot
        # Ajout des coordonnées du click
        self.plt_draw = np.vstack((self.plt_draw, np.array([x, y])))
        if np.dot((self.directions[-1][0], 0),
                  (1, 0)) > 0:  # Essai pour déterminer le signe de l'angle mais infructueux
            angle = -angle
        # Ajout des commandes
        if angle != 0:  # Ajoute une commande de rotation s'il est non nul
            self.command = np.vstack((self.command, np.array([0, angle, 0])))  # Rotation
        # self.command = np.vstack((self.command, np.array([1,np.linalg.norm(dv), ]))) # Ligne Droite
        self.command = np.vstack((self.command, np.array([1, x, y])))

    def draw_CIR(self,rin,  xin, yin, xout, yout, ang=np.pi / 2):
        print(xin, yin, xout, yout)
        # r = np.abs(yin - rin)
        X = np.linspace(xin, xout, 1000)
        Y = yin-rin + np.sqrt(rin ** 2 - (X - xin) ** 2)
        for k in range(len(X)):
            if isinstance(X[k], float) and isinstance(Y[k], float):
                self.plt_draw = np.vstack((self.plt_draw, np.array([X[k], Y[k]])))
        self.plt_draw = np.vstack((self.plt_draw, np.array([xout, yout])))
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.ax.figure.canvas.draw()

    def print_command(self):
        """Imprime les commandes sur la console"""
        print(self.command)

    def command_txt(self):
        path = os.getcwd()
        text_data = open(path + "\\trajectoire.txt", "w")
        for instruct in self.command:
            txt = "{0};{1};{2}\n".format(int(instruct[0]), round(instruct[1],3), round(instruct[2], 3))
            text_data.write(txt)
        text_data.close()
        return 0

    def _quit(self):
        self.root.quit()  # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def set_windowbutton(self):
        col=0
        tkinter.Label(self.window, text ="CIR (r, x, y): ").grid(row=0, column=col)
        col+=1
        self.rcirentry = tkinter.Entry(self.window)
        self.rcirentry.grid(row=0, column = col)
        col+=1
        tkinter.Label(self.window, text =", ").grid(row=0, column=col)
        col+=1
        self.xcirentry = tkinter.Entry(self.window)
        self.xcirentry.grid(row=0, column = col)
        col+=1
        tkinter.Label(self.window, text =", ").grid(row=0, column=col)
        col+=1
        self.ycirentry = tkinter.Entry(self.window)
        self.ycirentry.grid(row=0, column=col)
        col+=1
        self.update_cirbutton = tkinter.Button(master=self.window, text="CIR", command=self.CIR)
        self.update_cirbutton.grid(row = 0, column = col)
        colcir = col
        col=0
        tkinter.Label(self.window, text ="ROT (theta): ").grid(row=1, column=col)
        col+=1
        self.thetaentry = tkinter.Entry(self.window)
        self.thetaentry.grid(row=1, column = col)
        col+=1
        self.update_rotbutton = tkinter.Button(master=self.window, text="ROT", command=self.ROT)
        self.update_rotbutton.grid(row = 1, column = colcir)
        col=0
        tkinter.Label(self.window, text ="LIN (d): ").grid(row=2, column=col)
        col+=1
        self.dentry = tkinter.Entry(self.window)
        self.dentry.grid(row=2, column = col)
        col+=1
        self.update_linbutton = tkinter.Button(master=self.window, text="LIN", command=self.LIN)
        self.update_linbutton.grid(row = 2, column = colcir)


Interface()
tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
