#!/bin/python
import tkinter
import subprocess
from tkinter import *

#Confirms button is clicked and runs the net_scan file in CLI
def home():
   print("start button is clicked")
   subprocess.Popen(["python3","home.py"])
   root.destroy()

root = tkinter.Tk()
root.title('Canopy.io')
root.geometry("1337x771")



canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 771,
    width = 1337,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=r"start_img.png")
image_1 = canvas.create_image(
    665.0,
    385.0,
    image=image_image_1
)

button_image_1 = PhotoImage(file=r"start_button.png")
button_1 = Button(root,
    image=button_image_1,
    #KGR tells button what to do when clicked - see def of home above
    command=home,
    relief="flat"
)

button_1.pack()
button_1.place(
    x=79.0,
    y=613.0,
    width=303.0,
    height=51.0
)

root.resizable(False, False)
root.mainloop()

