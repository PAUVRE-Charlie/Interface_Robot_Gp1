import tkinter
import serial
import tkinter.scrolledtext as tkscrolledtext


root = tkinter.Tk()
root.wm_title("Serial v1.0 - Aziz S")
ser = None

def initser():
    global ser
    print("Initialise Serial Port")
    ser = serial.Serial()

def openser():
    if ser==None:
        print("No Serial Port initialised")
        return None
    if openser_button.cget("text") == "Open Serial":
        print("Opening Serial Port {0}".format(comPort.get()))
        ser.open()
        openser_button.config(text='Close Serial')
        # textbox.insert('1.0', "COM Port {} Opened\r\n".format(comPort.get()))
    elif openser_button.cget("text") == "Close Serial":
        print("Closing Serial Port {0}".format(comPort.get()))
        ser.close()
        openser_button.config(text='Open Serial')
        # textbox.insert('1.0',"COM Port {} Closed\r\n".format(comPort.get()))

def setPort():
    if ser==None:
        print("No Serial Port initialised")
        return None
    print("Set Serial Port to {0}".format(comPort.get()))
    ser.port = comPort.get()

def opentxt():
    return 0

# Set buttons
initSer = tkinter.Button(root, text = "Init", command = initser)
initSer.grid(row = 0)

comPort = tkinter.StringVar()
comPort.set("COM18")
defineCom = tkinter.Entry(root, textvariable=comPort)
defineCom.grid(row=1, column=0)

setSer = tkinter.Button(root, text = "set", command=setPort)
setSer.grid(row=1, column=1)

openser_button = tkinter.Button(root, text="Open Serial", command=openser)
openser_button.grid(row=1, column=2)

open_txt = tkinter.Button(root, text = "Open Text file", command=opentxt)
open_txt.grid(row=2, column =0, columnspan=3)

frame = tkinter.Frame(root, bg='cyan')
frame.grid(row=3, column=0, columnspan=3)
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=30, height=5) #width=characters, height=lines
textbox.grid(row=3, column=0, columnspan=3)


root.mainloop()