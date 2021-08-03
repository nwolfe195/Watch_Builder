import tkinter as tk
from tkinter import *
from tkinter import ttk


class Watch_Builder_GUI:
    def __init__(self, master):
        self.master = master
        master.title('Watch Builder')

        self.tab_control = ttk.Notebook(root)
        self.tab_watches = ttk.Frame(self.tab_control)
        self.tab_tables = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_watches, text='Watch')
        self.tab_control.add(self.tab_tables, text='Tables')
        self.tab_control.pack(expand=1, fill='both')
        Label(self.tab_watches, text='This is where each watch will be calculated').grid(column=0, row=0, padx=30, pady=30)
        Label(self.tab_tables, text='This is where tables will be inputted and edited').grid(column=0, row=0, padx=30, pady=30)


root = Tk()
watch_builder_gui = Watch_Builder_GUI(root)
root.mainloop()
