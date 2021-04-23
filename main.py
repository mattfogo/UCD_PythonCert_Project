#importing the required libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime

#import the datasets
GWh = pd.read_csv("Historic GWh by Fuel.csv")
GWh.set_index("Year").sort_index()
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
Energy = Oil.merge(Elec, on = 'Year', suffixes=('_Oil','_Elec'))\
            .merge(NatGas, on = 'Year', suffixes=('_Oil','_NatGas'))\
                .merge(Waste, on = 'Year', suffixes=('_Oil','_Waste'))\
                    .merge(Coal, on = 'Year', suffixes=('_Oil','_Coal'))\
                        .merge(Peat, on = 'Year', suffixes=('_Oil','_Peat'))\
                            .merge(Renewables, on = 'Year', suffixes=('_Oil','_Renew'))
print(Energy.columns)