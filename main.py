# importing the required libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# import the datasets
GWh = pd.read_csv("Historic GWh by Fuel.csv")
GWh['Primary Energy'] = GWh['Primary Energy'].astype(int)
GWh['Year'] = GWh['Year'].astype(int)

# introducing the data
print(GWh.describe())

# checking for Null values
print(GWh.isna().any())

# Dividing the data up into fuel types
Oil = GWh[GWh['Fuel Group'] == 'Oil']

Elec = GWh[GWh['Fuel Group'] == 'Electricity']

NatGas = GWh[GWh['Fuel Group'] == 'Natural Gas']

Waste = GWh[GWh['Fuel Group'] == 'Non-Renewable  Waste']

Coal = GWh[GWh['Fuel Group'] == 'Coal']

Peat = GWh[GWh['Fuel Group'] == 'Peat']

Renewables = GWh[GWh['Fuel Group'] == 'Renewables']

# merging the new datasets
Energy = Oil.merge(Elec, on='Year', how='left', suffixes=('_Oil', '_Elec'))

Energy = Energy.merge(NatGas, on='Year')
Energy = Energy.rename(columns={'Fuel Group': 'Fuel Group_NatGas', 'Primary Energy': 'Primary Energy_NatGas'})

Energy = Energy.merge(Waste, on='Year')
Energy = Energy.rename(columns={'Fuel Group': 'Fuel Group_Waste', 'Primary Energy': 'Primary Energy_Waste'})

Energy = Energy.merge(Coal, on='Year')
Energy = Energy.rename(columns={'Fuel Group': 'Fuel Group_Coal', 'Primary Energy': 'Primary Energy_Coal'})

Energy = Energy.merge(Peat, on='Year')
Energy = Energy.rename(columns={'Fuel Group': 'Fuel Group_Peat', 'Primary Energy': 'Primary Energy_Peat'})

Energy = Energy.merge(Renewables, on='Year')
Energy = Energy.rename(columns={'Fuel Group': 'Fuel Group_Renewables', 'Primary Energy': 'Primary Energy_Renewables'})
print(Energy.columns)

Energy['Total Energy'] = Energy['Primary Energy_Oil'] + Energy['Primary Energy_Elec'] + Energy['Primary Energy_NatGas']+ Energy['Primary Energy_Waste'] + Energy['Primary Energy_Coal'] + Energy['Primary Energy_Renewables'] + Energy[
    'Primary Energy_Peat']

# demonstartion of a while loop
x = Energy['Year'].min()
y = Energy['Year'].max()
z = x
while z <= y:
    z = z + 1
    print('The current value of "z" is', z)

# import additional datasets
EUA = pd.read_csv("eua-price.csv")
EUA['Date'] = pd.to_datetime(EUA['Date'])
EUA['Price'] = EUA['Price'].astype(int)

EUA['year'] = EUA['Date'].dt.year
EUA['month'] = EUA['Date'].dt.month
EUA['day'] = EUA['Date'].dt.day

GHG = pd.read_csv("All-GHG.csv")
GHG = GHG.rename(columns={'Irish greenhouse gas emissions (ktCO?)': 'Date', })
GHG['Date'] = GHG['Date'].astype(int)

print(GHG.columns)

# averaging the price per year
print(EUA.groupby('year')['Price'].mean())
EUA_Y_Av = EUA.groupby('year')['Price'].mean()

Energy_Y_Av_GHG = GHG.merge(EUA_Y_Av, left_on='Date', right_on='year', how='left', suffixes=['_EUA', '_GHG'])
Energy_Y_Av_GHG.fillna(0, inplace=True)

#replacing the ktCO2 values with tCO2 values
Energy_Y_Av_GHG['Agriculture (excluding energy related)']=Energy_Y_Av_GHG['Agriculture (excluding energy related)']*1000
Energy_Y_Av_GHG['Energy related Non-ETS']=Energy_Y_Av_GHG['Energy related Non-ETS']*1000
Energy_Y_Av_GHG['Other non-ETS']=Energy_Y_Av_GHG['Other non-ETS']*1000
Energy_Y_Av_GHG['ETS']=Energy_Y_Av_GHG['ETS']*1000

#cost of ireland's GHG emmissions
Energy_Y_Av_GHG['Cost'] = Energy_Y_Av_GHG['ETS']*Energy_Y_Av_GHG['Price']
print(Energy_Y_Av_GHG['Cost'])

# adding up the fossil fuel generation
Energy['Fossil Fuels'] = Energy['Primary Energy_Oil'] + Energy['Primary Energy_NatGas']+ Energy['Primary Energy_Waste'] + Energy['Primary Energy_Coal'] + Energy['Primary Energy_Peat']
print(Energy.columns)



# graphing my results
Energy['Year'] = Energy['Year'].astype(int)
Years = Energy["Year"]
sns.set_style("whitegrid")
tips = sns.load_dataset("tips")
plot1 = plt.figure(1)
sns.stripplot(x=Years, y=Energy['Total Energy'], data=tips, palette=['black'])
plt.xticks(fontsize=8,rotation=90)
plt.title('Energy Generation in Ireland since 1990')


# second graph
plot2 = plt.figure(2)
plt.scatter(Years, Energy['Primary Energy_Renewables'], color='green', label='Renewable Energy')
plt.scatter(Years, Energy['Primary Energy_Elec'], color='blue', label='Electricity')
plt.scatter(Years, Energy['Primary Energy_Coal'], color='black', label='Coal')
plt.xlabel('Years')
plt.ylabel('GWh')
plt.title('Energy Generation in Ireland since 1990')
plt.legend()


plot3 = plt.figure(3)
plt.scatter(Years, Energy['Primary Energy_Renewables'], color='green', label='Renewable Energy')
plt.scatter(Years, Energy['Primary Energy_NatGas'], color='red', label='Gas')
plt.scatter(Years, Energy['Primary Energy_Coal'], color='black', label='Coal')
plt.xlabel('Years')
plt.ylabel('GWh')
plt.title('Energy Generation in Ireland since 1990')
plt.legend()


# third graph
plot4 = plt.figure(4)
Date = Energy_Y_Av_GHG['Date']
CostM= Energy_Y_Av_GHG['Cost']/1000000
sns.barplot(Date, CostM, data=tips, palette=['black'])
plt.xticks(fontsize=8,rotation=90)
plt.xlabel('Years')
plt.ylabel('Cost in Million €/t')
plt.title('Cost of Generation in Ireland since 2005')
plt.show()