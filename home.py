#!/bin/python
import subprocess
import tkinter as tk
from tkinter import *


#Defines a scan method which when the scan button is clicked opens the scan page
def scan():
   print("scan button is clicked")
   subprocess.Popen(["python3","scan.py"])
   window.destroy()

#Defines an attack method which when the attack button is clicked opens the attack page
def attack():
    print("attack button is clicked")
    subprocess.Popen(["python3", "msfpygui.py"])
    window.destroy()

#Defines an report method which when the report button is clicked opens the report page
def report():
    print("report button is clicked")
    subprocess.Popen(["python3", "reports_page.py"])
    window.destroy()

#Defining scan_button action
def scan_button():
    print("scan button is clicked")
    subprocess.Popen(["python3", "scan.py"])
    window.destroy()

#Defining attack_button action
def attack_button():
    print("attack button is clicked")
    subprocess.Popen(["python3", "msfpygui.py"])
    window.destroy()

#Defining report_button action
def report_button():
    print("report button is clicked")
    subprocess.Popen(["python3", "reports_page.py"])
    window.destroy()
    
    
#Defines window pop-up and names it
window = Tk()
window.title('Canopy.io')
window.geometry("1239x664")
window.configure(bg = "#FFFFFF")

#Menu bar pop-up definitions
canvas1 = tk.Canvas(window, width=1239, height=664, bg = "#FFFFFF")
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Scan', command=scan_button)
filemenu.add_command(label='Attack', command=attack_button)
filemenu.add_command(label='Reports', command=report_button)
menubar.add_cascade(label='Canopy.IO Menu', menu=filemenu)
window.config(menu=menubar)


#Dfines Canvas for background image placement
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 664,
    width = 1239,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

#Links image to canvas
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=r"home_img.png")
image_1 = canvas.create_image(
    619.0,
    332.0,
    image=image_image_1
)

#Scan button image link and placement
button_image_1 = PhotoImage(file=r"scan_button.png")
button_1 = Button(window,
    image=button_image_1,
    borderwidth=4,
    highlightthickness=0,
    command=scan,
    relief="flat"
)

button_1.place(
    x=75.0,
    y=410.0,
    width=230.06349182128906,
    height=63.95452880859375
)

#Attacks button image link and placement
button_image_2 = PhotoImage(file=r"attacks_button.png")
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=attack,
    relief="flat"
)
button_2.place(
    x=502.0,
    y=410.0,
    width=230.0634765625,
    height=63.95452880859375
)

#Reports button image link and placement
button_image_3 = PhotoImage(file=r"reports_button.png")
button_3 = Button(window,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=report,
    relief="flat"
)

button_3.place(
    x=930.9365234375,
    y=412.0454406738281,
    width=230.0634765625,
    height=63.95452880859375
)

#Tells Python to run the event loop
window.resizable(False, False)
window.mainloop()
