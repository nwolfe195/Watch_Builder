from tkinter import *
from tkinter.messagebox import showinfo
import pandas as pd
import random
import re
from random import randint


class Watch_Builder_GUI:
    def __init__(self, master):
        pd.set_option('display.max_colwidth', 1000)
        self.master = master
        self.master.geometry('600x600')
        self.master.title('Watch Builder')

        region_file = 'regions.csv'
        self.regions_df = pd.read_csv(region_file)
        self.description_text = StringVar()
        self.description_text.set('Select a region')
        self.cr_text = StringVar()
        self.foraging_text = StringVar()
        self.navigation_text = StringVar()
        self.encounter_chance_text = StringVar()
        self.region_variable = StringVar()

        encounter_file = 'encounters.csv'
        self.encounters_df = pd.read_csv(encounter_file)
        self.encounter_variable = StringVar()
        self.encounter_variable.set('10')

        rain_file = 'rain.csv'
        self.rain_df = pd.read_csv(rain_file)

        wind_file = 'wind.csv'
        self.wind_df = pd.read_csv(wind_file)

        self.encounter_text = StringVar()
        self.rain_text = StringVar()
        self.rain_text.set('Clear Skies')
        self.wind_text = StringVar()
        self.wind_text.set('No Wind')

        self.set_components()

    def set_components(self):
        regions = self.regions_df['Name'].tolist()
        OptionMenu(self.master, self.region_variable, *regions, command=self.select_region).grid(row=0, column=0)
        Label(textvariable=self.description_text, wraplength=600).grid(row=1, column=0, columnspan=6)
        Label(text='CR').grid(row=2, column=0)
        Label(textvariable=self.cr_text).grid(row=2, column=1)
        Label(text='Foraging DC').grid(row=2, column=2)
        Label(textvariable=self.foraging_text).grid(row=2, column=3)
        Label(text='Navigation DC',).grid(row=2, column=4)
        Label(textvariable=self.navigation_text).grid(row=2, column=5)

        Label(text='Encounter Chance').grid(row=3, column=0)
        encounter_modifiers = [-20, -10, 0, 10, 20, 30, 40, 50]
        OptionMenu(self.master, self.encounter_variable, *encounter_modifiers).grid(row=3, column=1)

        Button(text='Travel Watch', command=self.travel_watch).grid(row=4, column=0)
        Button(text='Activity Watch', command=self.activity_watch).grid(row=4, column=2)
        Button(text='Sleep Watch', command=self.sleep_watch).grid(row=4, column=4)

        Label(text='Encounter').grid(row=5, column=0)
        Label(textvariable=self.encounter_text).grid(row=5, column=1)
        Label(text='Rain').grid(row=6, column=0)
        Label(textvariable=self.rain_text).grid(row=6, column=1)
        Label(text='Wind').grid(row=7, column=0)
        Label(textvariable=self.wind_text).grid(row=7, column=1)

    def travel_watch(self):
        if self.description_text.get() == 'Select a region':
            showinfo('Error', 'Select a region first!')
            return
        self.all_watchs()

    def activity_watch(self):
        if self.description_text.get() == 'Select a region':
            showinfo('Error', 'Select a region first!')
            return
        self.all_watchs()

    def sleep_watch(self):
        if self.description_text.get() == 'Select a region':
            showinfo('Error', 'Select a region first!')
            return
        self.all_watchs()

    def all_watchs(self):
        self.encounter_check()
        self.weather_check()

    def weather_check(self):
        rain_weight = self.rain_df.loc[self.rain_df['Current Rain'] == self.rain_text.get()].values.flatten().tolist()[1:]
        rain_types = list(self.rain_df)[1:]
        new_rain = random.choices(rain_types, weights=rain_weight, k=1)[0]
        self.rain_text.set(new_rain)

        wind_weight = self.wind_df.loc[self.wind_df['Current Wind'] == self.wind_text.get()].values.flatten().tolist()[1:]
        wind_types = list(self.wind_df)[1:]
        new_wind = random.choices(wind_types, weights=wind_weight, k=1)[0]
        self.wind_text.set(new_wind)

    def encounter_check(self):
        encounter_chance = (int(self.encounter_chance_text.get()) + int(self.encounter_variable.get())) / 100
        roll = random.random()
        if roll < encounter_chance:
            encounters = self.encounters_df.loc[self.encounters_df['Region'] == self.region_variable.get()]
            encounter_name = encounters['Encounter'].tolist()
            encounter_weight = encounters['Chance'].tolist()
            encounter = random.choices(encounter_name, weights=encounter_weight, k=1)[0]
            self.encounter_text.set(self.roll_encounter(encounter))
        else:
            self.encounter_text.set('No encounter')

    def roll_encounter(self, encounter):
        regex = '\d+d\d+((\+|\-)\d+)?'
        split_encounter = encounter.split(', ')
        joined_encounter = []
        for split in split_encounter:
            roll = re.match(regex, split).group(0)
            rolled_role = self.roll_dice(roll)
            rolled_split = re.sub(regex, rolled_role, split)
            joined_encounter.append(rolled_split)
        joined_encounter_string = ', '.join(joined_encounter)
        return joined_encounter_string

    def roll_dice(self, roll):
        number_match = re.findall('\d+', roll)
        dice = int(number_match[0])
        sides = int(number_match[1])
        total = 0
        for x in range(dice):
            result = randint(1, sides)
            total += result
        if re.search('(\+|\-)', roll) is not None:
            mod = int(re.search('\d+$', roll).group(0))
            if re.search('(\+|\-)', roll).group(0) == '+':
                total += mod
            else:
                total -= mod
        if total < 1:
            return str(0)
        else:
            return str(total)

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
        encounter_chance = region_data['Chance'].to_string(index=False)
        self.encounter_chance_text.set(encounter_chance)


root = Tk()
watch_builder_gui = Watch_Builder_GUI(root)
root.mainloop()
