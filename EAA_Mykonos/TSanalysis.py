import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
# Initial File paths and make print globally outputs to results.txt"
file_path = "./data/data_sample.txt"
result_path = "./results/results.txt"
sys.stdout = open(result_path, 'w')


def myplot(x, y, title, ylabel, fig):
    plt.figure(fig)
    plt.subplot(211)
    plt.plot(x, y)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid()
    plt.savefig("./results/plots/{}_{}.png".format(title, ylabel))


print "Timeseries Analysis of Meteorological Station Mukonos(meteo.gr)\n"
print "Raw Dataset is provided from Kostas Lagouvardos <lagouvar@meteo.noa.gr>\n"
print "TS_analysis_Mykonos.py was originally written by Anastasiadis Stavros,<anastasiadis.st00@gmail.com>\n"

print "Copyright (C) 2013 - 2014 University of the Aegean\n"

print """TS_analysis.py script is free script:
you can redistribute it and/or modify it under the
terms of the GNU General Public License,
as published by the Free Software Foundation;
either version 3 of the License, or (at your option) any later version."""

print """This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the licenses for more details. http://www.gnu.org/licenses/."""
print "----------------"

# Reading dataset & add missing value .nan & change type .asfloat()
df = pd.read_csv(file_path, header=True,
                 names=["date", "time", "temp", "rain"],
                 parse_dates=[[0, 1]], index_col=[0], sep=r"\s+")

df[df.temp == "---"] = np.nan
df[df.rain == "---"] = np.nan
df[['temp', 'rain']] = df[['temp', 'rain']].astype(float)

print "Primary  Raw dataset Information"
ms_temp = len(df.index) - df.temp.count()
ms_rain = len(df.index) - df.rain.count()
print "-------------"
df[df == np.nan].to_csv("./results/MissingValuesLog.txt", sep='\t', encoding='utf-8')
print "Dataset Time Period: {} to {} ".format(df.index[0], df.index[-1])
print "-------------"
print """Number of Missing Values: Temp:{}/{} -  Rain:{}/{} ,
         check your  ./MissingValuesLog.csv
         for more date details\n""".format(ms_temp, len(df.index), ms_rain, len(df.index))
print "Missing Values of raw dataset"
data = df.resample('10min', how='sum')
empty = data.apply(lambda col: pd.isnull(col))
missing = empty[empty == True]
missing.describe()
mdata = missing.groupby([lambda x: x.year]).agg('count')
print mdata
print "-------------"
print "Descriptive statistics:{} {}".format("\n", df.describe())
print "\nLast  Rainfall Record {} with Amount {}\n".format(df.index[df.rain > 0][-1], df.rain[df.rain > 0][-1])
print "-------------"
print "Monthly TS Analysis"
month_df = {'temp': df.temp.resample('M', how="mean"), 'rain': df.rain.resample('M', how='sum')}
month_df = pd.DataFrame(month_df)
print "Descriptive statistics:{} {}".format("\n", month_df.describe())
print "----------------"
print "Annual TS Analysis"
annual_df = {'temp': df.temp.resample('A', how="mean"), 'rain': df.rain.resample('A', how='sum')}
annual_df = pd.DataFrame(annual_df)
print "Descriptive statistics:{} {}".format("\n", annual_df.describe())
print "----------------"

# Plots raw and monthy with storage at my file
myplot(df.index, df.rain, "Raw", "Rainfall (mm)", 1)
myplot(df.index, df.temp, "Raw", "Temperature (oC)", 2)
# Plots raw and monthy with storage at my file
myplot(month_df.index, month_df.rain, "Monthly", "Rainfall (mm)", 3)
myplot(month_df.index, month_df.temp, "Monthly", "Temperature (oC)", 4)
myplot(annual_df.index, annual_df.rain, "Annual", "Rainfall (mm)", 5)
myplot(annual_df.index, annual_df.temp, "Annual", "Temperature (oC)", 6)


print "----------------"
print "Potential Evapotranspiration Monthly Calculations"
temps = df.temp.resample('H', how=['max', 'min', 'mean'])
temps['emax'] = temps['max'].apply(lambda x: 0.6108 * math.exp(17.27 * x) / (x + 273))
temps['emin'] = temps['min'].apply(lambda x: 0.6108 * math.exp(17.27 * x) / (x + 273))
temps['es'] = (temps['emax'] + temps['emin']) / 2
temps['ea'] = temps['mean'].apply(lambda x: 0.6108 * math.exp(17.27 * x) / (x + 273))
temps['PET'] = 4.5 * (1 + (temps['mean'] / 25) * (temps['mean'] / 25)) * (1 - temps['ea'] / temps['es'])
pet = temps.PET
pet[pet < 0] = 0
print "Descriptive statistics (Monthly):{} {}".format("\n", pet.resample("M", how="mean").describe())
print "----------------"
print "Descriptive statistics (Annual):{} {}".format("\n", pet.resample("A", how="mean").describe())
print "----------------"
myplot(pet.resample("M", how="mean").index, pet.resample("M", how="mean"), "Monthly", "PET (mm)", 7)
myplot(pet.resample("A", how="mean").index, pet.resample("A", how="mean"), "Annual", "PET (mm)", 8)


print "Rain Events"
print "----------------"
df['date'] = df.index
##################

threshold = 0
df = df[df.rain > threshold]
timespam = 2
diff = df.date - df.date.shift(1)
df['event_id'] = (diff > np.timedelta64(timespam, "h")).astype(int).cumsum()
start = [row for row in df.date.groupby(df.event_id).min()]
finish = [row for row in df.date.groupby(df.event_id).max()]
mean = [row for row in df.rain.groupby(df.event_id).mean()]
sum = [row for row in df.rain.groupby(df.event_id).sum()]
min = [row for row in df.rain.groupby(df.event_id).min()]
max = [row for row in df.rain.groupby(df.event_id).max()]
event_id = [row for row in df.event_id.groupby(df.event_id).max()]
d = {'start': start, 'finish': finish, 'mean': mean, 'min': min, 'max': max, 'sum': sum}
df1 = pd.DataFrame(d)
df1['duration'] = df1.finish - df1.start
df1_sort = df1.sort(['sum'], ascending=False)
print df1_sort.head(10)
