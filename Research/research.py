import pandas as pd
import numpy as np
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
gdp_annual_growth = aux_df1[0:28][['Country Name', 'Country Code',
                                   '1990 [YR1990]', '1991 [YR1991]', '1992 [YR1992]', '1993 [YR1993]',
                                   '1994 [YR1994]', '1995 [YR1995]', '1996 [YR1996]', '1997 [YR1997]',
                                   '1998 [YR1998]', '1999 [YR1999]', '2000 [YR2000]', '2001 [YR2001]',
                                   '2002 [YR2002]', '2003 [YR2003]', '2004 [YR2004]', '2005 [YR2005]',
                                   '2006 [YR2006]', '2007 [YR2007]', '2008 [YR2008]', '2009 [YR2009]',
                                   '2010 [YR2010]', '2011 [YR2011]', '2012 [YR2012]', '2013 [YR2013]',
                                   '2014 [YR2014]', '2015 [YR2015]', '2016 [YR2016]', '2017 [YR2017]',
                                   '2018 [YR2018]', '2019 [YR2019]']]

print(gdp_annual_growth)

# Импорт датасета (GDP)
aux_df5 = pd.read_csv('gdp_constant_prices.csv')

aux_colnames5 = aux_df5.columns
print(aux_colnames5)

# Приводим данные в нормальный вид
gdp = aux_df5[0:28][['Country Name',
                     '2017 [YR2017]']]

# Сортируем
gdp = gdp.sort_values(by=['Country Name']).reset_index(drop=True)

print(gdp)

# Импорт датасета (population)
aux_df2 = pd.read_csv('population_90to19.csv')

aux_colnames2 = aux_df2.columns
print(aux_colnames2)

# Приводим данные в нормальный вид
pops = aux_df2[0:28][['Country Name',
                      '2017 [YR2017]']]

# Сортируем
pops = pops.sort_values(by=['Country Name']).reset_index(drop=True)

print(pops)

# Создаем словарь для кодов стран
ccodes = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR',
          'HR', 'HU', 'IE',  'IT', 'LT', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE',
          'SL', 'SK', 'UK', 'LU']

ccodes_dict = {'AT': 'Austria', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CY': 'Cyprus',
               'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark',  'EE': 'Estonia',
               'EL': 'Greece',  'ES': 'Spain',   'FI': 'Finland',  'FR': 'France',
               'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland',  'IT': 'Italy',
               'LT': 'Lithuania', 'LV': 'Latvia', 'MT': 'Malta', 'NL': 'Netherlands',
               'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'SE': 'Sweden',
               'SI': 'Slovenia', 'SK': 'Slovak Republic', 'UK': 'United Kingdom', 'LU': 'Luxembourg'}

# Импорт датасета (emigration)
aux_df3 = pd.read_csv('tps00177.csv')

aux_colnames3 = aux_df3.columns
print(aux_colnames3)

# Приводим данные в нормальный вид
emigration_total = aux_df3[['geo', '2017']]

emigration_total['geo'] = emigration_total['geo'].map(ccodes_dict)

# Сортируем
emigration_total = emigration_total.sort_values('geo').reset_index(drop=True)

print(emigration_total)

# Импорт датасета (immigration)
aux_df4 = pd.read_csv('tps00176.csv')

aux_colnames4 = aux_df4.columns
print(aux_colnames4)

# Приводим данные в нормальный вид
immigration_total = aux_df4[['geo', '2017']]

immigration_total['geo'] = immigration_total['geo'].map(ccodes_dict)

# Сортируем
immigration_total = immigration_total.sort_values('geo').reset_index(drop=True)

print(immigration_total)

# Консолидация в один датасет
eu_consolidate = {'Country': pops['Country Name'],
                  'GDP': gdp['2017 [YR2017]'],
                  'Population': pops['2017 [YR2017]'],
                  'Immigration': immigration_total['2017'],
                  'Emigration': emigration_total['2017']}
eu_df = pd.DataFrame(eu_consolidate)
eu_df.to_csv('eu_consolide_ei.csv')
print(eu_df)

# Визуализация

# Гистограмма населения
country_name = eu_df['Country']
pops_17 = eu_df['Population']
pops_hist = go.Figure([go.Bar(x=country_name, y=pops_17)])
pops_hist.show()

# Биг плоу
hover_text = []
bubble_size = []

for index, row in eu_df.iterrows():
    hover_text.append(('Country: {country}<br>' +
                       'Population: {popul}<br>' +
                       'GDP: {gdp}<br>' +
                       'Immigration: {immi}<br>' +
                       'Emigration: {emi}').format(country=row['Country'],
                                                   popul=row['Population'],
                                                   gdp=row['GDP'],
                                                   immi=row['Immigration'],
                                                   emi=row['Emigration']))
    bubble_size.append(np.sqrt(row['Population']))

eu_scatter = go.Figure(data=[go.Scatter(
    x=eu_df['Immigration'],
    y=eu_df['Emigration'],
    text=hover_text,
    mode='markers',
    marker=dict(
        color=np.log10(eu_df['GDP']),
        colorscale='Viridis',
        colorbar=dict(title='<b>GDP, log</b>'),
        cmin=np.log10(12949237121.738998),
        cmax=np.log10(4278004030164.74),
        size=bubble_size,
        sizemin=4,
        sizemode='area',
        sizeref=4.*max(bubble_size)/(100**2),
        line_width=1,
        showscale=True
    )
)])

eu_scatter.update_layout(
    title='<b>Emigration v. Immigration, 2017</b>',
    xaxis=dict(
        title='<b>Immigration</b>',
        gridcolor='#EBF0F8',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='<b>Emigration</b>',
        gridcolor='#EBF0F8',
        type='log',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(255, 255, 255)',
)

os.path.relpath(
    'C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Graphics', start=None)
eu_scatter.show()
eu_scatter.write_image('..\\Graphics\\ImmiEmi.svg')
eu_scatter.write_image('..\\Graphics\\ImmiEmi.png')
