import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import pandas as pd


class Watch_Builder_GUI:
    def __init__(self, master):
        self.master = master
        master.title('Watch Builder')

        self.region_file = 'regions.txt'
        self.region_header = ['Name', 'Description', 'CR', 'Foraging', 'Navigation']

        self.tab_control = ttk.Notebook(root)
        self.tab_watches = ttk.Frame(self.tab_control)
        self.tab_tables = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_watches, text='Watch')
        self.tab_control.add(self.tab_tables, text='Tables')
        self.tab_control.pack(expand=1, fill='both')
        Label(self.tab_watches, text='This is where each watch will be calculated').grid(column=0, row=0, padx=30,
                                                                                         pady=30)
        Button(self.tab_watches, text='Clear Tables', command=self.Clear_Data).grid(column=0, row=1, padx=30, pady=30)

        self.Display_Regions()

    def Clear_Data(self):
        os.remove(self.region_file)

    def Display_Regions(self):
        Label(self.tab_tables, text='Regions')

        for i in range(len(self.region_header)):
            Label(self.tab_tables, text=self.region_header[i]).grid(row=1, column=i)

        if os.path.isfile(self.region_file):
            regions_df = pd.read_csv(self.region_file)
            rows = regions_df.shape[0]
            columns = regions_df.shape[1]
            for x in range(rows):
                for y in range(columns):
                    Label(self.tab_tables, text=regions_df.iloc[x, y]).grid(row=x + 2, column=y)
        else:
            rows = 1

        new_name = Entry(self.tab_tables)
        new_name.grid(row=rows + 3, column=0)
        new_description = Entry(self.tab_tables)
        new_description.grid(row=rows + 3, column=1)
        new_cr = Entry(self.tab_tables)
        new_cr.grid(row=rows + 3, column=2)
        new_foraging = Entry(self.tab_tables)
        new_foraging.grid(row=rows + 3, column=3)
        new_navigation = Entry(self.tab_tables)
        new_navigation.grid(row=rows + 3, column=4)
        Button(self.tab_tables, text='Add Region', command=lambda: self.Add_Region(new_name.get(), new_description.get(),
                                                                                   new_cr.get(), new_foraging.get(),
                                                                                   new_navigation.get())).grid(row=rows + 3, column=5)

    def Add_Region(self, name, description, cr, foraging, navigation):
        if os.path.isfile(self.region_file):
            regions_df = pd.read_csv(self.region_file)
        else:
            regions_df = pd.DataFrame(columns=self.region_header)

        new_region = {'Name': name, 'Description': description, 'CR': cr, 'Foraging': foraging,
                      'Navivation': navigation}
        regions_df = regions_df.append(new_region, ignore_index=True)

        regions_df.to_csv(self.region_file, index=False)


root = Tk()
watch_builder_gui = Watch_Builder_GUI(root)
root.mainloop()
