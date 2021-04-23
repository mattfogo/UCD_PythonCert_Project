#importing the required libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime

#import the datasets
GWh = pd.read_csv("Historic GWh by Fuel.csv")
GWh['Primary Energy'] = GWh['Primary Energy'].astype(int)
print(GWh)

#checking for Null values
print(GWh.isna().any())


#Dividing the data up into fuel types
Oil = GWh[GWh['Fuel Group']=='Oil']

Elec = GWh[GWh['Fuel Group']=='Electricity']

NatGas = GWh[GWh['Fuel Group']=='Natural Gas']

Waste = GWh[GWh['Fuel Group']=='Non-Renewable  Waste']

Coal = GWh[GWh['Fuel Group']=='Coal']

Peat = GWh[GWh['Fuel Group']=='Peat']

Renewables = GWh[GWh['Fuel Group']=='Renewables']

#merging the new datasets
Energy = Oil.merge(Elec, on = 'Year', how='left', suffixes=('_Oil', '_Elec'))

Energy= Energy.merge(NatGas, on='Year')
Energy = Energy.rename(columns={'Fuel Group':'Fuel Group_NatGas', 'Primary Energy':'Primary Energy_NatGas'})

Energy= Energy.merge(Waste, on='Year')
Energy = Energy.rename(columns={'Fuel Group':'Fuel Group_Waste', 'Primary Energy':'Primary Energy_Waste'})

Energy= Energy.merge(Coal, on='Year')
Energy = Energy.rename(columns={'Fuel Group':'Fuel Group_Coal', 'Primary Energy':'Primary Energy_Coal'})

Energy= Energy.merge(Peat, on='Year')
Energy = Energy.rename(columns={'Fuel Group':'Fuel Group_Peat', 'Primary Energy':'Primary Energy_Peat'})

Energy= Energy.merge(Renewables, on='Year')
Energy = Energy.rename(columns={'Fuel Group':'Fuel Group_Renewables', 'Primary Energy':'Primary Energy_Renewables'})
print(Energy.columns)


#graphing my results
Energy['Year'] = Energy['Year'].astype(int)
Years = Energy["Year"]
Fuel = Energy['Primary Energy_Renewables']

plt.scatter(Years, Energy['Primary Energy_Renewables'],color = 'green')
plt.scatter(Years, Energy['Primary Energy_Elec'],color = 'blue')
plt.scatter(Years, Energy['Primary Energy_Coal'],color = 'black')
plt.xlabel('Years')
plt.ylabel('GWh')
plt.title('Energy Generation in Ireland since 1990')
plt.show()

