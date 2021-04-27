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
GWh['Year'] = GWh['Year'].astype(int)

#introducing the data
print(GWh.describe())

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

Energy ['Total Energy'] = Energy ['Primary Energy_Oil'] + Energy ['Primary Energy_Elec'] + Energy ['Primary Energy_NatGas']
+ Energy ['Primary Energy_Waste'] + Energy ['Primary Energy_Coal'] + Energy ['Primary Energy_Renewables']

#demonstartion of a while loop
x = Energy['Year'].min()
y = Energy['Year'].max()
z = x
while z<=y:
    z=z+1
    print('The current value of "z" is',z)

#import additional dataset
EUA = pd.read_csv("eua-price.csv")
EUA['Date']= pd.to_datetime(EUA['Date'])
EUA['Price'] = EUA['Price'].astype(int)

EUA['year']= EUA['Date'].dt.year
EUA['month']= EUA['Date'].dt.month
EUA['day']= EUA['Date'].dt.day

#averaging the price per year
print(EUA.groupby('year')['Price'].sum())
print(EUA.groupby('year')['Price'].count())

EUA['EUA_Avg']= EUA.groupby('year')['Price'].sum()/EUA.groupby('year')['Price'].count()
print(EUA['EUA_Avg'].head())

#graphing my results
Energy['Year'] = Energy['Year'].astype(int)
Years = Energy["Year"]
plt.scatter(Years, Energy['Total Energy'],color = 'Black', label= 'Total Energy')
plt.xlabel('Years')
plt.ylabel('GWh')
plt.title('Energy Generation in Ireland since 1990')
plt.legend()
plt.show()

#second graph
plt.scatter(Years, Energy['Primary Energy_Renewables'],color = 'green', label= 'Renewable Energy')
plt.scatter(Years, Energy['Primary Energy_NatGas'],color = 'red', label='Gas')
plt.scatter(Years, Energy['Primary Energy_Coal'],color = 'black', label = 'Coal')
plt.xlabel('Years')
plt.ylabel('GWh')
plt.title('Energy Generation in Ireland since 1990')
plt.legend()
plt.show()


