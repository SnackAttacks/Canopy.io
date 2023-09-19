#!/bin/python
import tkinter as tk
from tkinter import *
import os
import contextlib
import sys
import io
from msf.lib.discovery import Discovery
from msf.lib.exploit import ExploitLoader, Revshell
from typing import List
import json 
from cmd import Cmd
import logging 
import socket 
import threading
import subprocess
    
#Redirect output into text box
class TextRedirector(io.StringIO):
    def __init__(self, widget):
        self.widget = widget
        super().__init__()

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)
        self.widget.update_idletasks()

    def flush(self):
        pass


class Application(tk.Tk):
    intro = '\n##### WELCOME TO MSFPY #####\n'
    valid_vars = sorted(('target', 'port', 'ports', 'revshell_ip', 'revshell_port'))
    discover_args = sorted(('print', 'show', 'get'))
    module_args = sorted(('list', 'describe', 'use'))
    
    
    def __init__(self, exploits=None, master=None):
        tk.Tk.__init__(self)
        self.title("Canopy.io")
        self.geometry("1239x664")
        self.all_vars = {}
        self.all_results = {}
        self.current_exploit_name = None
        self.current_exploit = {}
        self.exploits = exploits
        self.master = master 
        self.inp = None 
        self.revshell = Revshell()
        
        
         #Create a canvas widget
        self.canvas = Canvas(self, width=1239, height=664)
        self.canvas.pack()

        #Load the image file
        self.bg_image = PhotoImage(file=r"attacks_img.png")

        #Create a background image on the canvas
        self.canvas.place(x=-3,y=-3)
        self.canvas.create_image(650.0, 350.0, image=self.bg_image)
    
        #Scan button action
        def scan_button():
            print("scan button is clicked")
            subprocess.Popen(["python3", "scan.py"])
            self.destroy()
            
        #Defining report_button action
        def report_button():
            print("report button is clicked")
            subprocess.Popen(["python3", "reports_page.py"])
            self.destroy()

        #Defining the home_button action
        def home_button():
            print("home button is clicked")
            subprocess.Popen(["python3", "home.py"])
            self.destroy()

        #Menubar
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Home', command=home_button)
        filemenu.add_command(label='Scan', command=scan_button)
        filemenu.add_command(label='Reports', command=report_button)
        menubar.add_cascade(label='Canopy.IO Menu', menu=filemenu)
        self.config(menu=menubar)
        
        #Output text box
        self.output = tk.Text(self)
        self.output.place(x=775, y=200, width=300, height=300)
        
        #Scrollbar for the text box
        scrollbar = tk.Scrollbar(self, command=self.output.yview)
        scrollbar.place(x=1075, y=200, height=300)
        self.output.config(yscrollcommand=scrollbar.set)


        #Reverse shell interaction
        self.revshell_command = tk.Entry(self.master)
        self.revshell_command.place(x=150, y=285)
        send_button =tk.Button(self, text="Send",
        command=self.do_send_command)
        send_button.place(x=345, y=285)
                
        #Variable entry
        self.variable_name = tk.Entry()
        self.variable_name.place(x=150, y=315)
        self.variable_value = tk.Entry()
        self.variable_value.place(x=345, y=315)
        tk.Button(self, text="Set", command=self.do_set).place(x=540, y=317)
        tk.Button(self, text="Unset", command=self.do_unset).place(x=570, y=317)
        tk.Button(self, text="Discover", command=self.do_discover).place(x=615, y=317)

        #Module
        self.mod = tk.Entry()
        self.exp = tk.Entry()
        self.mod.place(x=150,y=345)
        self.exp.place(x=345, y=345)
        tk.Button(self, text="Module", command=self.do_module).place(x=540,y=347)

        #Exploit
        self.module = tk.Entry()
        self.exploit = tk.Entry()
        self.module.place(x=150,y=375)
        self.exploit.place(x=345, y=375)
        tk.Button(self, text="Exploit", command=self.do_exploit).place(x=540, y=377)

        
    @contextlib.contextmanager
    def redirect_output(self):
        #Save original stdout and stderr
        original_stdout, original_stderr = sys.stdout, sys.stderr

        try:
            #Redirect stdout and stderr to the text widget
            sys.stdout = sys.stderr = TextRedirector(self.output)
            yield
        finally:
            #Restore original stdout and stderr
            sys.stdout, sys.stderr = original_stdout, original_stderr

    def do_send_command(self):
        if hasattr(self, 'revshell') and isinstance(self.revshell, Revshell):
            command = self.revshell_command.get()
            if command:
                self.revshell.send_command(command)
                self.revshell_command.delete(0, tk.END)
                #Receive output from the remote shell
                output = self.revshell.recv_output()
                if output:
                    self.output.insert(tk.END, output + '\n')
            else:
                self.output.insert(tk.END, "No active reverse shell.\n")

    def do_submit_input(self):
        input_value = self.custom_input.get()
        if input_value:
            self.output.insert(tk.END, f"Submitted input: {input_value}\n")
            #Do something with the input_value here
            self.custom_input.delete(0, tk.END)
        else:
            self.output.insert(tk.END, "Empty input. Please enter a value.\n")
    
    def print_possible_modules(self):
        self.print_output('Possible Modules: {}'.format(self.module_args))
        return False

    def check_possible_mods(self, inp: str):
        """
        Sanitize input string, then check to make sure the input string is a valid variable name.
        :param inp: input string
        :return: sanitized input string on success, False otherwise
        """
        if not inp:
            return False
        self.inp = inp.strip().lower()
        if inp not in self.module_args:
            self.print_output('Error, {} is not set or is not a valid module argument.'.format(inp))
            return self.print_possible_modules()
        return inp
    
    def print_possible_vars(self):
        """
        Print out all valid variables that can be set.
        :return: None
        """
        self.print_output('Possible variables: {}'.format(self.valid_vars))
        return False

    def check_possible_vars(self, inp: str):
        """
        Sanitize input string, then check to make sure the input string is a valid variable name.
        :param inp: input string
        :return: sanitized input string on success, False otherwise
        """
        if not inp:
            return False
        inp = inp.strip().lower()
        if inp not in self.valid_vars:
            self.print_output('Error, {} is not set or is not a valid variable.'.format(inp))
            return self.print_possible_vars()
        return inp

    def get_completion(valid_options: List, text: str, line, begidx, endidx) -> List:
        """
        Build completion List based on given List of valid options.
        :param valid_options: List of valid options
        :param text: current input string
        :param line: line number
        :param begidx: beginning index
        :param endidx: ending index
        :return: List of possible completions
        """
        if not text:
            return valid_options
        return [v for v in valid_options if v.startswith(text)]

    def do_exit(self, inp):
        self.print_output('Bye!')
        return True

    def do_shell(self, inp):
        os.system(inp)

    def help_shell(self):
        self.print_output('Execute arbitrary shell commands')
        self.print_output('Usage:  shell <command>')

    def do_get(self, inp):
        if not inp:
            self.print_output(self.all_vars)
            return False
        inp = self.check_possible_vars(inp)
        if inp and inp in self.all_vars:
            self.print_output(self.all_vars[inp])

    def help_get(self):
        self.print_output('Get the value of a defined variable.')
        self.print_output('Usage:  get [variable_name]')

    def complete_get(self, text, line, begidx, endidx):
        return self.complete_set(text, line, begidx, endidx)
    
    def help_unset(self):
        self.print_output('Unset the value of a variable.')
        self.print_output('Usage:  unset [variable_name]')

    def complete_unset(self, text, line, begidx, endidx):
        return self.complete_set(text, line, begidx, endidx)

    def do_write_results(self, inp):
        if not inp:
            self.print_output('Error, you must specify a valid file path to write to.')
            return False
        inp = inp.strip()
        with open(inp, 'w') as of:
            json.dump(self.all_results, of, indent=2)
        self.print_output('Finished writing results to {}.'.format(inp))

    def help_write_results(self):
        self.print_output('Write results of discovery scan to a JSON file.')
        self.print_output('Usage:  write_results <output_file>')

    def do_set(self):
        if self.variable_name.get() == "":
            return self.print_possible_vars()
        if self.variable_name.get() == "":
            self.print_output('Error, you must specify a key and value.')
            return False
        variable_value = self.variable_value.get() 
        variable_name = self.variable_name.get()
        variable_name = self.check_possible_vars(variable_name)
        if variable_name:
            self.all_vars[variable_name] = variable_value
            self.output.insert(tk.END, f'Set {variable_name} to {variable_value}\n')

    def do_unset(self):
        self.inp = self.check_possible_vars.get()
        if self.inp:
            del self.all_vars[inp]

    def set_inp(self, inp):
        self.inp = inp

    def do_discover(self):
        if self.inp:
            inp = inp.strip().lower()
            if inp in self.discover_args:
                self.print_output(self.all_results['discover'][self.all_vars['target']])
            else:
                self.print_output('Error, invalid argument specified.')
            return False
        if 'target' not in self.all_vars:
            self.print_output('Error, no target defined. Set target first with "set target <target>".')
            return False
        discovery = Discovery()
        if 'ports' in self.all_vars:
            self.print_output('Starting discovery on host {} on ports {}.'.format(self.all_vars['target'], self.all_vars['ports']))
            port_results, os_results = discovery.do_discovery(self.all_vars['target'], ports=self.all_vars['ports'],
                                                              sudo=True)
        else:
            self.print_output('Starting discovery on host {} on all ports.'.format(self.all_vars['target']))
            port_results, os_results = discovery.do_discovery(self.all_vars['target'], sudo=True)
        self.all_results['discover'] = {self.all_vars['target']: (port_results, os_results)}
        self.output.insert(tk.END, f'{self.all_results}\n')

    def help_discover(self):
        self.print_output('Perform service discovery against target host.')

    def complete_discover(self, text, line, begidx, endidx):
        return MSFMenu.get_completion(self.discover_args, text, line, begidx, endidx)

    def do_exploit(self):
        if not self.current_exploit:
            self.print_output('Error, no exploit currently defined.')
            return False
        if 'target' not in self.all_vars:
            self.print_output('Error, no target currently defined.')
            return False
        if 'revshell_ip' not in self.all_vars:
            self.all_vars['revshell_ip'] = Revshell.DEFAULT_REVSHELL_IP
        if 'revshell_port' not in self.all_vars:
            self.all_vars['revshell_port'] = Revshell.DEFAULT_REVSHELL_PORT
        if 'port' not in self.all_vars:
            self.print_output('Error, no port currently defined.')
            return False

        revshell = self.current_exploit.exploit(self.all_vars['target'], int(self.all_vars['port']),
                                            self.all_vars['revshell_ip'], self.all_vars['revshell_port'])

        if revshell:
            self.revshell = revshell
            self.output.insert(tk.END, "Reverse shell established. Use the input field below to interact.\n")
        else:
            print('Error, exploit did not complete successfully.')

        

    def help_exploit(self):
        self.print_output('Attempt to execute selected exploit against target.')

    def do_check(self, inp):
        if not self.current_exploit:
            self.print_output('Error, no exploit currently defined.')
            return False
        if 'target' not in self.all_vars:
            self.print_output('Error, no target currently defined.')
            return False
        if 'port' in self.all_vars:
            self.current_exploit.check(self.all_vars['target'], self.all_vars['port'])
        else:
            self.current_exploit.check(self.all_vars['target'])

    def help_check(self):
        self.print_output('Check if target is vulnerable to selected exploit.')

    def do_module(self):
        module = self.mod.get()
        module = self.check_possible_mods(module)
        exploit = self.exp.get()
        self.print_output(f"{module}, {exploit}")
        if module == "":
            return self.check_possible_mods()
        if module not in self.module_args:
            self.print_output('Error, {} is not set or is not a valid module operation.'.format(self.module_args))
            self.print_output('Possible module operations: {}'.format(self.module_args))
            return False
        if module == 'use':
            if exploit in self.exploits:
                self.current_exploit = self.exploits[exploit]
                self.current_exploit_name = exploit
                self.prompt = '({}) msfpy> '.format(self.current_exploit_name)
            else:
                self.print_output(f"Error, exploit '{exploit}' not found.")
        elif module == 'describe':
            if self.current_exploit:
                self.current_exploit.describe()
        elif module == 'list':
            self.print_output('Available exploits: {}'.format(str(self.exploits.keys())))
            self.output.insert(tk.END, f'{module} set \n')


    def help_module(self):
        self.print_output('Look for and select available exploits.')
        self.print_output('Usage:  module <list|describe|use [module]>')

    def complete_module(self, text, line, begidx, endidx):
        return Application.get_completion(self.module_args, text, line, begidx, endidx)

    def print_output(self, text):
        self.output.insert(tk.END, f"{text}\n")
        self.output.see(tk.END)  # Autoscroll to the end of the output

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    print('\nLoading exploits...')
    exploits = ExploitLoader.load_exploits()
    app = Application(exploits=exploits)
    app.mainloop()
    

if __name__ == '__main__':
    main()
    revshell = Revshell()
    revshell.start()



