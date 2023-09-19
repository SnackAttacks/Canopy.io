#!/bin/python
import subprocess
import tkinter as tk
import subprocess
from tkinter import *

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

#Defining the home_button action
def home_button():
    print("home button is clicked")
    subprocess.Popen(["python3", "home.py"])
    window.destroy()
    
#Defines wireshark reports button routes and closes window
def wireshark_reports():
    print("wireshark reports button is clicked")
    subprocess.Popen(["python3", "wireshark_results.py"])
    window.destroy()

#Defines nmap button routes and closes window
def nmap_reports():
    print("nmap reports button is clicked")
    subprocess.Popen(["python3", "nmap_results.py"])
    window.destroy()

#Window creation
window = Tk()
window.geometry("1239x664")
window.title('Canopy.io')
window.configure(bg = "#FFFFFF")

#Menu bar pop-up definitions
canvas1 = tk.Canvas(window, width=1239, height=664, bg = "#FFFFFF")
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Home', command=home_button)
filemenu.add_command(label='Scan', command=scan_button)
filemenu.add_command(label='Attack', command=attack_button)
menubar.add_cascade(label='Canopy.IO Menu', menu=filemenu)
window.config(menu=menubar)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 664,
    width = 1239,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=r"reports_img.png")
image_1 = canvas.create_image(
    660.0,
    350.0,
    image=image_image_1
)

#Image and button placement
button_image_1 = PhotoImage(file=r"nmap_rbutton.png")
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=nmap_reports,
    relief="flat"
)
button_1.place(
    x=225.0,
    y=430.0,
    width=233.21258544921875,
    height=67.77273559570312
)

button_image_2 = PhotoImage(file=r"wireshark_rbutton.png")
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=wireshark_reports,
    relief="flat"
)

button_2.place(
    x=875.0,
    y=430.0,
    width=229.0,
    height=70.0
)

#Runs the event in the window
window.resizable(False, False)
window.mainloop()
