import tkinter as tk
from tkinter import *
import os
import pandas as pd


class Watch_Builder_GUI:
    def __init__(self, master):
        pd.set_option('display.max_colwidth', 1000)
        self.master = master
        self.master.geometry('400x600')
        self.master.title('Watch Builder')

        region_file = 'regions.csv'
        self.regions_df = pd.read_csv(region_file)
        self.description_text = StringVar()
        self.description_text.set('Select a region')
        self.cr_text = StringVar()
        self.foraging_text = StringVar()
        self.navigation_text = StringVar()

        self.set_components()

    def set_components(self):
        regions = self.regions_df['Name'].tolist()
        region_variable = StringVar(self.master)
        OptionMenu(self.master, region_variable, *regions, command=self.select_region).grid(row=0, column=0)
        Label(textvariable=self.description_text, wraplength=400).grid(row=1, column=0, columnspan=6)
        Label(text='CR').grid(row=2, column=0)
        Label(textvariable=self.cr_text).grid(row=2, column=1)
        Label(text='Foraging DC').grid(row=2, column=2)
        Label(textvariable=self.foraging_text).grid(row=2, column=3)
        Label(text='Navigation DC').grid(row=2, column=4)
        Label(textvariable=self.navigation_text).grid(row=2, column=5)

    def select_region(self, selected):
        region_data = self.regions_df.loc[self.regions_df['Name'] == selected]
        description = region_data['Description'].to_string(index=False)
        self.description_text.set(description)
        cr = region_data['CR'].to_string(index=False)
        self.cr_text.set(cr)
        foraging = region_data['Foraging'].to_string(index=False)
        self.foraging_text.set(foraging)
        navigation = region_data['Navigation'].to_string(index=False)
        self.navigation_text.set(navigation)


root = Tk()
watch_builder_gui = Watch_Builder_GUI(root)
root.mainloop()
