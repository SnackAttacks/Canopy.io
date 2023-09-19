#!/bin/python
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk

#Wireshark button path routing
def wireshark():
   print("wireshark button is clicked")
   subprocess.Popen(["python3","wireshark_page.py"])
   window.destroy()
 
#Nmap button path routing
def nmap():
    print("nmap button is clicked")
    subprocess.Popen(["python3", "nmap_page.py"])
    window.destroy()

#Defining home_button action
def home_button():
    print("home button is clicked")
    subprocess.Popen(["python3", "home.py"])
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


#Defines window pop-up
window = Tk()
window.title('Canopy.io')
window.geometry("1239x664")

#Defines menu bar pop-up
canvas1 = tk.Canvas(window, width=1239, height=664, bg = "#FFFFFF")
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Home', command=home_button)
filemenu.add_command(label='Attack', command=attack_button)
filemenu.add_command(label='Reports', command=report_button)
menubar.add_cascade(label='Canopy.IO Menu', menu=filemenu)
window.config(menu=menubar)



#Canvas creation
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 664,
    width = 1239,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

#Links image to canvas and placement of image
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=r"scan_img.png")
image_1 = canvas.create_image(
    619.0,
    350.0,
    image=image_image_1
)

#Button image and location
button_image_1 = PhotoImage(file=r"wireshark_button_scan.png")
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= wireshark,
    relief="flat"
)

button_1.place(
    x=738.0,
    y=557.0,
    width=374.0,
    height=73.0
)


button_image_2 = PhotoImage(file=r"nmap_button_scan.png")
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=nmap,
    relief="flat"
)
button_2.place(
    x=120.0,
    y=557.0,
    width=374.0,
    height=73.0
)

#Runs the event of the window
window.resizable(False, False)
window.mainloop()
