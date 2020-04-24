import matplotlib.pyplot as plt
import numpy as np
import math
import tkinter
import os

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

    def __init__(self):
        ## Initialisation de Tkinter
        self.root = tkinter.Tk()
        self.root.wm_title("Interface Commande Robot")

        # Variables
        self.plt_draw = np.zeros((1,2)) # Coordonnées interprété par matplotlib pour le tracé
        self.plt_draw[0] = np.array([0,1])
        self.command = np.zeros((1,2))
        self.command[0] = np.array([1,1])
        self.directions = np.array([[0,1]])

        self.setup()
        self.drawing, = self.ax.plot(self.plt_draw[:, 0], self.plt_draw[:, 1])

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.on_key_press)

        self.set_buttons()

    def setup(self):
        """Mise en place de la Figure Matplotlib"""
        self.fig = Figure(figsize=self.FIGSIZE, dpi=self.DPI)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()

    def set_buttons(self):
        """Mise en place des boutons sur Tkinter"""
        self.method_entry = tkinter.Entry(self.root)
        self.method_entry.pack(side=tkinter.TOP)

        self.update_methodbutton = tkinter.Button(master=self.root, text="Update", command=self.update_method)
        self.update_methodbutton.pack(side = tkinter.TOP)

        self.command_button = tkinter.Button(master=self.root, text="Command", command=self.print_command)
        self.command_button.pack(side = tkinter.TOP)

        self.export_button = tkinter.Button(master=self.root, text="Export", command=self.command_txt)
        self.export_button.pack(side = tkinter.TOP)

        self.quit_button = tkinter.Button(master=self.root, text="Quit", command=self._quit)
        self.quit_button.pack(side=tkinter.BOTTOM)

    def update_method(self):
        """Tempoiraire, c'est pour mettre à jour la méthode de tracé, ici 1 est la ligne droite"""
        self.DRAW_METHOD = self.method_entry.get()
        print(self.DRAW_METHOD)

    def on_key_press(self, event):
        """Gestion de l'évènement clic gauche et gestion du tracé"""
        print("you pressed ({0},{1})".format(event.xdata, event.ydata))
        key_press_handler(event, self.canvas, self.toolbar)

        if self.DRAW_METHOD==1: # Ligne droite
            x, y = event.xdata, event.ydata
            dv = x-self.plt_draw[-1][0] , y-self.plt_draw[-1][1]
            angle = self.get_ang(self.plt_draw[-1], np.array([x,y]), dir=True, direction=self.directions[-1]) # Détermination de l'angle de rotation (valeur absolue)
            self.directions = np.vstack((self.directions, np.array(dv / np.linalg.norm(dv)))) # Mise à jour des directions deu robot
            # Ajout des coordonnées du click
            self.plt_draw = np.vstack((self.plt_draw, np.array([x,y])))
            if np.dot((self.directions[-1][0],0), (1,0))>0: # Essai pour déterminer le signe de l'angle mais infructueux
                angle = -angle
            # Ajout des commandes
            if angle!=0: # Ajoute une commande de rotation s'il est non nul
                self.command = np.vstack((self.command, np.array([0,angle]))) # Rotation
            self.command = np.vstack((self.command, np.array([1,np.linalg.norm(dv)]))) # Ligne Droite


        # Update Canvas
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.ax.figure.canvas.draw()

    def get_ang(self, v1, v2, dir=False, direction=(0,1)):
        """Détermine l'angle de rotation avec considération possible de la direction précédante"""
        vect1, vect2 = v1, v2
        if dir :
            vect2 = vect2-vect1
            vect1=direction
        v1_unit = vect1 / np.linalg.norm(vect1)
        v2_unit = vect2 / np.linalg.norm(vect2)
        dot_product = np.dot(v1_unit, v2_unit)
        return np.arccos(dot_product)

    def print_command(self):
        """Imprime les commandes sur la console"""
        print(self.command)

    def command_txt(self):
        path = os.getcwd()
        text_data = open(path+"\\trajectoire.txt", "w")
        for instruct in self.command:
            txt = "{0} {1};".format(int(instruct[0]),instruct[1])
            text_data.write(txt)
        text_data.close()
        return 0

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate



Interface()
tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
