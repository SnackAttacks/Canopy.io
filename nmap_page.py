#!/bin/python
import csv
import nmap
import tkinter as tk
import datetime
import subprocess
import os
from tkinter import ttk
from datetime import datetime
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

#Defining report_button action
def report_button():
    print("report button is clicked")
    subprocess.Popen(["python3", "reports_page.py"])
    window.destroy()

#Defining the home_button action
def home_button():
    print("home button is clicked")
    subprocess.Popen(["python3", "home.py"])
    window.destroy()

#Redirect to nmap reporting page
def view_nmap_reports():
    print("nmap_results button is clicked")
    subprocess.Popen(["python3","nmap_results.py"])
    window.destroy()
   

#Create scan button
def run_nmap():
    nm = nmap.PortScanner()
    ip_addr = ip_entry.get()
    nm.scan(hosts=f"{ip_addr}", arguments=interface_combobox.get())
    nm.scaninfo()

    #Display results in a text box
    results_text = Text(window)
    results_text.place(x=565, y=220, width=400, height=300)
    results_text.insert(END, nm.all_hosts())
    
    #Set up the folder name and filename
    folder_name = "Nmap Results"
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f"nmap_results_{current_time}.csv"

    #Get the current working directory
    current_directory = os.getcwd()

    #Create the folder if it doesn't exist in current directory
    folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #Construct the full file path
    filepath = os.path.join(folder_path, filename)

    for host in nm.all_hosts():
        #Create "Saving..." banner
        banner_label = tk.Label(window, text="Generating Results...", bg="blue", fg="white", font=("Arial", 16))
        banner_label.place(x=0, y=0, relwidth=1)
        window.update()
        window.after(3000, banner_label.destroy)

        results_text.insert(END, "\n\n----------------------------------------------------\n")
        results_text.insert(END, f"Host : {host} ({nm[host].hostname()})\n")
        results_text.insert(END, f"State : {nm[host].state()}\n")
        for proto in nm[host].all_protocols():
            results_text.insert(END, "----------\n")
            results_text.insert(END, f"Protocol : {proto}\n")
            lport = nm[host][proto].keys()
            for port in lport:
                results_text.insert(END, f"port : {port}\tstate : {nm[host][proto][port]['state']}\n")

    #Write results to CSV file
    with open(filepath, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['IP Address', 'Host', 'State', 'Protocol', 'Port', 'Status'])
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    writer.writerow([host, nm[host].hostname(), nm[host].state(), proto, port, nm[host][proto][port]['state']])

    
    #Notify user that scan is complete and results are saved to a file
    results_text.insert(END, "\n\n----------------------------------------------------\n")
    results_text.insert(END, f"\nScan complete. Results saved to {filepath}.")

#Create window
window = tk.Tk()
window.title('Canopy.io')
window.geometry("1239x664")
window.configure(bg="#FFFFFF")

#Menu bar pop-up definitions
canvas1 = tk.Canvas(window, width=1239, height=664, bg = "#FFFFFF")
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Home', command=home_button)
filemenu.add_command(label='Scan', command=scan_button)
filemenu.add_command(label='Attack', command=attack_button)
filemenu.add_command(label='Reports', command=report_button)
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

#Background image creation
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=r"nmap_img.png")
image_1 = canvas.create_image(
    619.0,
    350.0,
    image=image_image_1
)



#Create IP address label
ip_label = Label(window, text="IP Address:")
ip_label.place(x=283, y=220)

#Create IP address entry
ip_var = tk.StringVar()
ip_entry = Entry(window, textvariable=ip_var)
ip_entry.place(x=283, y=245)

#Create port range label
port_range_label = Label(window, text="Port Range:")
port_range_label.place(x=283, y=280)

#Create port range entry
port_range_var = tk.StringVar()
port_range_entry = Entry(window, textvariable=port_range_var)
port_range_entry.place(x=283, y=305)

#Interface gui label
interface_label = tk.Label(window, text="Select Scan Type:")
interface_label.place(x=283, y=345)

#Interface drop-down menu
interface_combobox = ttk.Combobox(window, width=27, values=["-O", "-sS", "-sU", "-sn", "-sL", "-sV", "-sO"])
interface_combobox.place(x=283, y=370)

#Scan button creation and placement
scan_button = Button(window, text="Scan", command=run_nmap)
scan_button.place(x=283, y=400)

#Open new window button
new_window_button = tk.Button(window, text="View Past Results", command=view_nmap_reports)
new_window_button.place(x=357, y=400)


#Runs the event in the window
window.mainloop()
