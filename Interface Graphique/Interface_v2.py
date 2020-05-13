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
import tkinter.scrolledtext as tkscrolledtext
from circlefrompt import circ


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

        self.setup()
        # Variables
        self.init_graph()

        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect("button_press_event", self.on_key_press)
        self.textbox = tkscrolledtext.ScrolledText(master=self.root, wrap='word', height=2)
        self.textbox.pack(side=tkinter.TOP, fill = 'x',  expand=1)
        self.set_buttons()

    def setup(self):
        """Mise en place de la Figure Matplotlib"""
        self.fig = Figure(figsize=self.FIGSIZE, dpi=self.DPI)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis(self.AXIS)

        self.set_grid()

        self.robot_im = plt.imread('robot.png')
        self.imgplot = self.ax.imshow(self.robot_im, origin=(0,0), extent=([-1, 1, -1, 1]))

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

        self.update_linmethodbutton = tkinter.Button(master=self.root, text="Line",
                                                  command=self.to_Line, relief= tkinter.SUNKEN)
        self.update_linmethodbutton.pack(side=tkinter.LEFT)

        self.update_cirmethodbutton = tkinter.Button(master=self.root, text="CIR",
                                                  command=self.to_CIR)
        self.update_cirmethodbutton.pack(side=tkinter.LEFT)

        self.erase_methodbutton = tkinter.Button(master=self.root, text="Erase",
                                                  command=self.erase_plt)
        self.erase_methodbutton.pack(side=tkinter.LEFT)

        self.command_button = tkinter.Button(master=self.root, text="Command", command=self.print_command)
        self.command_button.pack(side=tkinter.LEFT)

        self.export_button = tkinter.Button(master=self.root, text="Export", command=self.command_txt)
        self.export_button.pack(side=tkinter.LEFT)

        self.dir_button = tkinter.Button(master=self.root, text="dir", command=self.print_dir)
        self.dir_button.pack(side=tkinter.LEFT)

        self.dirtest_button = tkinter.Button(master=self.root, text="arrow dir", command=self.test_dir)
        self.dirtest_button.pack(side=tkinter.LEFT)

        self.quit_button = tkinter.Button(master=self.root, text="Quit", command=self._quit)
        self.quit_button.pack(side=tkinter.BOTTOM)

    def init_graph(self):
        self.plt_draw = np.zeros((1, 2))  # Coordonnées interprété par matplotlib pour le tracé
        # self.plt_draw[0] = np.array([0, 1])
        self.command = np.zeros((1, 3))
        # self.command[0] = np.array([1, 0, 1])
        self.directions = np.array([[0, 1]])
        self.drawing, = self.ax.plot(self.plt_draw[:, 0], self.plt_draw[:, 1])

    def print_dir(self):
        print(self.directions)

    def test_dir(self):
        xold, yold = self.plt_draw[-1]
        xdir, ydir = self.directions[-1]
        self.ax.arrow(xold, yold, xdir, ydir, width=0.5)
        self.ax.figure.canvas.draw()

    def to_CIR(self):
        self.update_cirmethodbutton.config(relief=tkinter.SUNKEN)
        self.update_linmethodbutton.configure(relief = tkinter.RAISED)
        self.DRAW_METHOD=2

    def erase_plt(self):
        self.ax.cla()
        self.init_graph()
        self.textbox.delete('1.0', tkinter.END)
        self.ax.axis(self.AXIS)
        self.set_grid()
        self.robot_im = plt.imread('robot.png')
        self.imgplot = self.ax.imshow(self.robot_im, origin=(0,1), extent=([-1, 1, -1, 1]))
        self.ax.figure.canvas.draw()

    def to_Line(self):
        self.update_linmethodbutton.config(relief=tkinter.SUNKEN)
        self.update_cirmethodbutton.configure(relief = tkinter.RAISED)
        self.DRAW_METHOD=1

    def on_key_press(self, event):
        """Gestion de l'évènement clic gauche et gestion du tracé"""
        print("you pressed ({0},{1})".format(event.xdata, event.ydata))
        key_press_handler(event, self.canvas, self.toolbar)
        if event.inaxes != self.ax.axes: return
        x, y = event.xdata, event.ydata
        if np.abs(x)>10 or np.abs(y)>10: return
        if self.DRAW_METHOD == 1:  # Ligne droite
            self.draw_lineinter(x, y)
        if self.DRAW_METHOD == 2:  # CIR
            self.draw_CIR2(x, y)
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
        # Update direction
        angrad = float(self.thetaentry.get())*np.pi*2/360
        xdir, ydir = self.directions[-1]
        new_dir = self.rotatenp(xdir, ydir, angrad)
        new_dir = np.array([round(new_dir[0],2), round(new_dir[1],2)])
        print(new_dir)
        self.directions = np.vstack(
            (self.directions, new_dir))
        # Add command
        self.add_command(0, angrad, 0)
        # Plot point to show rotation
        x, y = self.plt_draw[-1]
        self.ax.plot(x,y,'ro')
        self.ax.figure.canvas.draw()
        return 0

    def rotatenp(self, x, y, ang):
        """Use numpy to build a rotation matrix and take the dot product."""
        co, si = np.cos(ang), np.sin(ang)
        j = np.array([[co, si], [-si, co]])
        m = np.dot(j, [x, y])
        return float(m[0]), float(m[1])

    def LIN(self):
        d = float(self.dentry.get())
        xold, yold = self.plt_draw[-1]
        print(xold, yold)
        xdir, ydir = self.directions[-1]
        if xold==0:
            xout, yout = xold, yold +d
            if d>0:
                xout, yout = xold, yold +d
            else:
                xout, yout = xold, yold +d*ydir
                self.directions = np.vstack(
                    (self.directions, np.array([-self.directions[-1][0], -self.directions[-1][1]])))
        else:
            if d>0:
                xout = xold +d*xdir
                yout = yold +d*ydir
            else:
                xout = xold +d*xdir
                yout = yold +d*ydir
                self.directions = np.vstack(
                    (self.directions, np.array([-self.directions[-1][0], -self.directions[-1][1]])))
        self.plt_draw = np.vstack((self.plt_draw, np.array([xout, yout])))
        self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
        self.add_command(1, xout, yout)
        self.ax.figure.canvas.draw()
        return 0

    def CIR(self):
        print(self.plt_draw[-1][0], self.plt_draw[-1][1], self.xcirentry.get(), self.ycirentry.get())
        self.draw_CIR(float(self.xcirentry.get()), float(self.ycirentry.get()))
        # self.command = np.vstack((self.command, np.array([2, self.xcirentry.get(), self.ycirentry.get()])))
        self.add_command(2, self.xcirentry.get(), self.ycirentry.get())

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
        if np.abs(angle) > 0.001:  # Ajoute une commande de rotation s'il est non nul
            # self.command = np.vstack((self.command, np.array([0, angle, 0])))  # Rotation
            self.add_command(0, angle, 0)
        # self.command = np.vstack((self.command, np.array([1,np.linalg.norm(dv), ]))) # Ligne Droite
        # self.command = np.vstack((self.command, np.array([1, x, y])))
        self.add_command(1, x, y)


    def add_command(self, c, i1, i2):
        self.command = np.vstack((self.command, np.array([c, i1, i2])))
        command_dict = {0: 'ROT',1:'LIN', 2:'CIR' }
        c = command_dict[int(self.command[-1][0])]
        self.textbox.insert('1.0', "{0}({1},{2})\n".format(c, round(self.command[-1][1], 2), round(self.command[-1][2])), 2)

    def draw_CIR(self, xout, yout):
        xin, yin = self.plt_draw[-1][0], self.plt_draw[-1][1]
        print("(xin={0}, yin={1})".format(xin,yin))
        ang = self.get_ang(self.directions[-1], np.array([0, 1]), dir=True,
                          direction=self.directions[-1])
        print(ang)
        self.ax.plot([0,xin],[0,yin], color='g')
        self.ax.plot([0,xout],[0,yout], color='r')
        self.ax.plot([xin,xout],[yin,yout], color='b')
        dx, dy = xout-xin, yout-yin
        self.ax.plot([0,dx],[0,dy])
        xrel, yrel = self.rotatenp(dx, dy, -ang)
        # yrel,xrel = xrel,yrel
        self.ax.plot([0,xrel],[0,yrel], color='k')
        print(xrel, yrel)
        if(yrel==0 or xrel==0 or (yrel)<0):
            print("Configuration impossible pour CIR")
        else:
            # dx, dy = -dx,-dy
            theta_ini = self.get_ang((0,1),(0,1))
            Xcv = dy*np.sin(theta_ini)+dx*np.cos(theta_ini)
            Ycv = dy*np.cos(theta_ini)-dx*np.sin(theta_ini)
            sgn = (Xcv/np.abs(Xcv))
            R = sgn*(Xcv**2+Ycv**2)/(2*Xcv)
            X = np.linspace(0, xout, 100)
            Y = np.sqrt(R**2-np.power(X-sgn*R,2))
            dir_2 = self.directions[-1]
            dir_2 = dir_2 / np.linalg.norm(dir_2)
            theta = self.get_ang((0,1),dir_2)
            Xn, Yn, Vn = list(),list(), list()
            Vn2=np.zeros((1,2))
            Vn2[0] = np.array([xin,yin])
            for k in range (len(X)):
                xr, yr = self.rotatenp(X[k], Y[k],theta)
                Xn.append(xr)
                Yn.append(yr)
                Vn.append([xr+xin,yr+yin])
            for k in range (len(X)):
                xr, yr = self.rotatenp(X[k], Y[k],theta)
                Vn2=np.vstack((Vn,np.array([X[k],yr+Vn2[-1][-1]])))
            self.ax.plot(Vn2[:,0], Vn2[:,1])
            Xn, Yn = np.array(Xn)+xin, np.array(Yn)+yin
            # self.ax.plot(Xn, Yn)
            dv_dir = (X[-1]-X[-2], Y[-1]-Y[-2])
            dv_dir = dv_dir / np.linalg.norm(dv_dir)
            self.directions = np.vstack(
                (self.directions, dv_dir))  # Mise à jour des directions deu robot
            self.plt_draw = np.vstack((self.plt_draw, np.array(Vn)))
            self.drawing.set_data(self.plt_draw[:, 0], self.plt_draw[:, 1])
            self.ax.figure.canvas.draw()
            self.add_command(2, xout, yout)

    def draw_CIR2(self, xout, yout):
        xin, yin = self.plt_draw[-1][0], self.plt_draw[-1][1]
        if(yout==0 or xout==0):
            print("Configuration impossible pour CIR")
        else:
            dx, dy = xout-xin, yout-yin
            theta_ini = self.get_ang((0,1),(0,1))
            Xcv = dy*np.sin(theta_ini)+dx*np.cos(theta_ini)
            Ycv = dy*np.cos(theta_ini)-dx*np.sin(theta_ini)
            sgn = (Xcv/np.abs(Xcv))
            R = sgn*(Xcv**2+Ycv**2)/(2*Xcv)
            circle = plt.Circle((sgn*R,0), R, alpha=0.1)
            c1 = circles_from_p1p2r((xin,yin),(xout,yout),R)
            print(c1)
            c11, c12 =c1
            print((c11.x,c11.y), c11.r)
            circle1 = plt.Circle((c11.x,c11.y), c11.r, alpha=0.1)
            self.ax.add_artist(circle1)
            circle2 = plt.Circle((c12.x,c12.y), c12.r, alpha=0.1, color='g')
            self.ax.add_artist(circle2)
            self.ax.plot(xin, yin, 'ro', color='g')
        return 0

    def print_command(self):
        """Imprime les commandes sur la console"""
        print(self.command)
        print(self.plt_draw)
        xin, yin = self.plt_draw[-1][0], self.plt_draw[-1][1]
        # yin = self.plt_draw[:,-1][1]
        test = self.plt_draw[-1]
        print("(xin={0}, yin={1}), {2}".format(xin,yin, test))

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
        tkinter.Label(self.window, text ="CIR (x, y): ").grid(row=0, column=col)
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
        tkinter.Label(self.window, text ="ROT° (theta): ").grid(row=1, column=col)
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
