
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    def __init__(self):
        self.df3 = pd.read_csv("../data/data-raw/fars_data_03_sizeable.csv")
        self.df4 = pd.read_csv("../data/data-raw/fars_data_04.csv")
        
    def by_time(self):
    
        # Make two dfs. One for weekends. One for weekdays.
        noWeekend = self.df4[(self.df4["DAY_WEEKNAME"] != "Saturday") 
            & (self.df4["DAY_WEEKNAME"] != "Sunday")].copy()
        weekend = self.df4[(self.df4["DAY_WEEKNAME"] == "Saturday") 
            | (self.df4["DAY_WEEKNAME"] == "Sunday")].copy()
        
        
        hourMinute = []
        for minute, hour in zip(noWeekend["MINUTE"], noWeekend["HOUR"]):
            
            if minute <= 30:
                time = hour + 0.5
            else:
                time = hour + 1.0
            
            hourMinute.append(time)

        noWeekend["HOUR_MINUTE"] = hourMinute

        hourMinute = []
        for minute, hour in zip(weekend["MINUTE"], weekend["HOUR"]):
            
            if minute <= 30:
                time = hour + 0.5
            else:
                time = hour + 1.0
            
            hourMinute.append(time)

        weekend["HOUR_MINUTE"] = hourMinute


        labels = np.array(range(0, 24))
        labelVals = labels
        labels = [f"{val - 12} PM" if val > 12 else f"{val} AM" for val in labels]

        labels[0] = "Midnight"
        labels[12] = "Noon"
        
        
        fig, ax = plt.subplots()
        fig.set_facecolor('lightgray')

        plt.plot(noWeekend["HOUR_MINUTE"].value_counts().sort_index()/5, '-', label = "Monday-Friday")
        plt.plot(weekend["HOUR_MINUTE"].value_counts().sort_index()/2, '-', label = "Saturday-Sunday")

        labels = np.array(range(0, 24))
        labelVals = labels
        labels = [f"{val - 12} PM" if val > 12 else f"{val} AM" for val in labels]

        labels[0] = "Midnight"
        labels[12] = "Noon"

        ax.set_title("Average Number of Fatal Accidents in the US (2021) by Time of Day", fontsize = 12)
        ax.set_ylabel("Number of Fatal Accidents", fontsize = 12)
        ax.set_xlim(-1, 25)
        ax.xaxis.set_ticks(labelVals)
        ax.set_xticklabels(labels, rotation = 310, fontsize = 9)
        ax.legend(loc = 4)
        ax.grid(alpha = 0.2)
        plt.savefig("../plots/by_time.png")
        
    def by_weather(self):
        conditionList = []
        avgFatals = []
        errs = []
        for condition in set(self.df4.WEATHERNAME):
            
            conditionDF = self.df4[self.df4.WEATHERNAME == condition]
            avgFatal = conditionDF.FATALS.sum()/len(conditionDF)
            avgFatals.append(avgFatal)
            conditionList.append(condition)
            errs.append(np.std(conditionDF.FATALS)/np.sqrt(avgFatal))

        fig, ax = plt.subplots(figsize= (9,5))
        fig.set_facecolor("lightgrey")
        ax.bar(conditionList, avgFatals, yerr = errs)
        plt.xticks(rotation=290) 
        plt.ylabel("Average Fatalities", fontsize =13)
        plt.title("Average Fatalities by Weather Condition", fontsize = 14)
        plt.savefig("../plots/by_weather.png")
        
    def by_model_year(self):
        mask = (self.df3.MOD_YEAR < 2022) &  (self.df3.MOD_YEAR > 1980)

        years = []
        avgDeaths = []
        errs = []
        for year in set(self.df3.MOD_YEAR[mask]):
            years.append(year)
            
            subDF = self.df3[self.df3.MOD_YEAR == year]
            
            avgDeath = np.mean(subDF.DEATHS)
            avgDeaths.append(avgDeath)
            
            errs = np.std(subDF.DEATHS)/np.sqrt(len(subDF.DEATHS))
        
        
        fig, ax = plt.subplots()
        fig.set_facecolor("lightgrey")
        ax.errorbar(years, avgDeaths, yerr = errs, linestyle = "none", marker = ".")
        ax.grid(alpha = 0.2)
        ax.set_xlabel("Model Year", fontsize = 14)
        ax.set_ylabel("Average Death Rate")
        ax.set_title("Avg Deaths per Car Involved in a Fatal Crash by Model Year")
        plt.savefig("../plots/by_model_year.png")
        
        
if __name__ == "__main__":
    plotter = Plotter()
    plotter.by_time()
    #plotter.by_weather()
    #plotter.by_model_year()