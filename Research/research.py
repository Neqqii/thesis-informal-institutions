import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.offline as pyo
import plotly as ply
import plotly.tools as tls
import plotly.graph_objs as go
import cufflinks as cfl

os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Datasets')

# Импорт датасета (GDP growth)
aux_df1 = pd.read_csv('gdp_growth_90to19.csv')

aux_colnames1 = aux_df1.columns
print(aux_colnames1)

# Оставляем нужные столбцы
gdp_annual_growth = aux_df1[['Country Name', 'Country Code',
                             '1990 [YR1990]', '1991 [YR1991]', '1992 [YR1992]', '1993 [YR1993]',
                             '1994 [YR1994]', '1995 [YR1995]', '1996 [YR1996]', '1997 [YR1997]',
                             '1998 [YR1998]', '1999 [YR1999]', '2000 [YR2000]', '2001 [YR2001]',
                             '2002 [YR2002]', '2003 [YR2003]', '2004 [YR2004]', '2005 [YR2005]',
                             '2006 [YR2006]', '2007 [YR2007]', '2008 [YR2008]', '2009 [YR2009]',
                             '2010 [YR2010]', '2011 [YR2011]', '2012 [YR2012]', '2013 [YR2013]',
                             '2014 [YR2014]', '2015 [YR2015]', '2016 [YR2016]', '2017 [YR2017]',
                             '2018 [YR2018]', '2019 [YR2019]']]

print(gdp_annual_growth)

# Импорт датасета (population)
aux_df2 = pd.read_csv('population_90to19.csv')

aux_colnames2 = aux_df2.columns
print(aux_colnames2)

# Оставляем нужные столбцы
pops = aux_df2[['Country Code',
                '1990 [YR1990]']]

print(pops)

# Импорт датасета (emigration)
aux_df3 = pd.read_csv('tps00177.csv')

aux_colnames3 = aux_df3.columns
print(aux_colnames3)

# Оставляем нужные столбцы
emigration_total = aux_df3[['geo', '2017 ']]

print(emigration_total)

# Импорт датасета (immigration)
aux_df4 = pd.read_csv('tps00176.csv')

aux_colnames4 = aux_df4.columns
print(aux_colnames4)

# Оставляем нужные столбцы
immigration_total = aux_df4[['geo',
                             '2006 ', '2007 ', '2008 ', '2009 ',
                             '2010 ', '2011 ', '2012 ', '2013 ',
                             '2014 ', '2015 ',
                             '2016 ', '2017 ']]

print(immigration_total)

# Создаем словарь для кодов стран
ccodes_dict = {'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
               'CZ': 'Czechia', 'DE': 'Germany', 'DK': 'Denmark',  'EE': 'Estonia',
               'EL': 'Greece',  'ES': 'Spain',   'FI': 'Finland',  'FR': 'France',
               'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',  'IT': 'Italy',
               'LT': 'Lithuania', 'LV': 'Latvia', 'MT': 'Malta', 'NL': 'Netherlands',
               'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
               'SL': 'Slovenia', 'SK': 'Slovakia', 'UK': 'United Kingdom', 'LU': 'Luxembourg'}

# Визуализация
country_code = pops[0:27]['Country Code']
pops_17 = pops[0:27]['1990 [YR1990]']
pops_hist = go.Figure([go.Bar(x=country_code, y=pops_17)])
pops_hist.show()
