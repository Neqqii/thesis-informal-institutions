# Блокнот исследования

---

## Содержание
* [Экономическое развитие и миграция](#Анализ-данных-по-экономическому-развитию-и-миграции-в-странах-Евросоюза)
  * [Импорт данных и базовая инфографика](#Импорт-данных-и-базовая-инфографика)
  * [Кластеризация](#Кластеризация)
* [Источники](#источники)

## Анализ данных по экономическому развитию и миграции в странах Евросоюза

---
### Импорт данных и базовая инфографика

Для начала настраиваем рабочую среду.
Загружаем нужные библиотеки и устанавливаем путь к директории, в которой будем работать:

```py
# Importing libraries
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go

# Change default directory
os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Datasets')

```

Первая база данных (ВВП 1990-2019 гг.) взята с сайта [Worldbank](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD?end=2018&start=2000).

Загружаем изначальный массив во вспомогательную таблицу.

```py
# Auxillary dataframe
aux_df5 = pd.read_csv('gdp_constant_prices.csv')

# Check headers
aux_colnames5 = aux_df5.columns

```

Приведем данные в удобный для дальнейшего использования формат:
```py
gdp = aux_df5[0:28][['Country Name',
                     '2017 [YR2017]']]
# Sort data
gdp = gdp.sort_values(by=['Country Name']).reset_index(drop=True)

```
Вторая база данных (Население стран) взята также с сайта взята с сайта [Worldbank](https://data.worldbank.org/indicator/SP.POP.TOTL).

Проделываем с ней аналогичные операции:
```py
# Import dataframe (population)
aux_df2 = pd.read_csv('population_90to19.csv')

# Check headers
aux_colnames2 = aux_df2.columns

# Clear & Sort
pops = aux_df2[0:28][['Country Name',
                      '2017 [YR2017]']]

pops = pops.sort_values(by=['Country Name']).reset_index(drop=True)

```

Теперь займемся данными по иммиграции и эмиграции в странах Евросоюза. Оба массива с данными взяты с сайта [Eurostat](https://ec.europa.eu/eurostat/data/database). Операции по импорту и обработке данных аналогичны тем, что применялись до этого. Различие состоит лишь в том, что необходимо заменить коды стран на их названия с целью дальнейшего объединения с другими датафреймами.

Для удобства замены создаем вспомогательный словарь ccodes_dict
```py
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

```

Как всегда:
```py
# Import dataset (emigration)
aux_df3 = pd.read_csv('tps00177.csv')

# Check headers
aux_colnames3 = aux_df3.columns
print(aux_colnames3)

# Clear & Sort
emigration_total = aux_df3[['geo', '2017']]

emigration_total['geo'] = emigration_total['geo'].map(ccodes_dict)

emigration_total = emigration_total.sort_values('geo').reset_index(drop=True)

print(emigration_total)

# Import dataset (immigration)
aux_df4 = pd.read_csv('tps00176.csv')

# Check Headers
aux_colnames4 = aux_df4.columns
print(aux_colnames4)

# Clear & Sort
immigration_total = aux_df4[['geo', '2017']]

immigration_total['geo'] = immigration_total['geo'].map(ccodes_dict)

immigration_total = immigration_total.sort_values('geo').reset_index(drop=True)

print(immigration_total)

```

Пришло время все консолидировать, создав единую таблицу:
```py
# Consolidate
eu_consolidate = {'Country': pops['Country Name'],
                  'GDP': gdp['2017 [YR2017]'],
                  'Population': pops['2017 [YR2017]'],
                  'Immigration': immigration_total['2017'],
                  'Emigration': emigration_total['2017']}
eu_df = pd.DataFrame(eu_consolidate)
eu_df.to_csv('eu_consolide_ei.csv')
print(eu_df)

```

Наконец-то можно визуализировать все это дело:
```py
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
        cmin=np.log10(eu_df['GDP'].min()),
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

```
Интерактивный график на сайте:

[Immigration vs Emigration](https://plot.ly/~Neqqi/1/)

Статичный график:

![Immigration vs Emigration](Graphics/ImmiEmi.png)

### Кластеризация

Для дальнейшего исследования необходимо разбить страны на кластеры, основываясь на некоторой подборке показателей...

```py
# Импортируеааа
import pandas as pd
import numpy as np
import os
import plotly.offline as pyo
import plotly as ply
import plotly.tools as tls
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

```


```py
# Choose directory
os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research')

# Import dataset
eu_ei = pd.read_csv('.\\Datasets\\eu_consolide_ei.csv')
```

```py
# Separating indicators from data
print(eu_ei.columns)
print(eu_ei.dtypes)
indicators = eu_ei.columns[2:]
aux_ind = eu_ei.loc[:, indicators].values

# Standardizing indicators values
ind = StandardScaler().fit_transform(aux_ind)
eu_indei = pd.DataFrame(data=ind, columns=indicators)
print(eu_indei)
```

```py
# PCA projection (4D to 2D)
pca = PCA(n_components=2)
pComp = pca.fit_transform(ind)

eu_pCompei = pd.DataFrame(data=pComp, columns=['PC1', 'PC2'])
eu_PC2ei = pd.concat([eu_pCompei, eu_ei[['Country']]], axis=1)
pca.explained_variance_ratio_
print(eu_PC2ei)
```

```py
# ТуПКа 2
hover_text = []

for index, row in eu_PC2ei.iterrows():
    hover_text.append(('Country: {country}<br>' +
                       'PC1: {pc1}<br>' +
                       'PC2: {pc2}<br>').format(country=row['Country'],
                                                pc1=row['PC1'],
                                                pc2=row['PC2'],))

eu_PCAei = go.Figure(data=[go.Scatter(
    x=eu_PC2ei['PC1'],
    y=eu_PC2ei['PC2'],
    text=hover_text,
    mode='markers',
    marker=dict(
        color='#1dec95',
        size=14,
        sizemode='area'
    )

)])

eu_PCAei.update_layout(
    title='<b>2 Component PCA projection</b>',
    xaxis=dict(
        title='<b>Principal Component 1</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=2,
    ),
    yaxis=dict(
        title='<b>Principal Component 2</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(255, 255, 255)',
)

# Шоу ТуПКа 2
eu_PCAei.show()

# Сохранить
os.path.relpath(
    'C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Graphics', start=None)
eu_PCAei.write_image('.\\Graphics\\PCA_ei.png')
```
Статичный график:

![2 Component PCA](Graphics/PCA_ei.png)

Теперь переходим к собственно кластеризации. Сначала используем алгоритм K-Means.
Первым делом определим оптимальное значение параметра k:
```py
inertia = []
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=1).fit(ind)
    inertia.append(np.sqrt(kmeans.inertia_))

opt_kmeans = go.Figure(data=[go.Scatter(
    x=[1, 2, 3, 4, 5, 6, 7, 8],
    y=inertia,
    mode='lines')],
    layout=dict(
    title='Best k-value',
    xaxis=dict(
        title='K-parameter',
        gridcolor='#EBF0F8'
    ),
    yaxis=dict(
        title='Criterium J(C)',
        gridcolor='#EBF0F8'
    ),
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(255, 255, 255)'
))
opt_kmeans.show()
opt_kmeans.write_image('.\\Graphics\\opt_kmeans.png')

```

![K-values](Graphics/opt_kmeans.png)

При рассмотрении графика, представленного выше, можно выделить две точки перелома: k=2, k=4. Попробуем построить модель для каждого значения параметра.
```py
# K-means (k=2)
kmeans = KMeans(n_clusters=2)
kmeans.fit(ind)
ind_k2means = kmeans.predict(ind)
print(ind_k2means)

# K-means (k=4)
kmeans = KMeans(n_clusters=4)
kmeans.fit(ind)
ind_k4means = kmeans.predict(ind)
print(ind_k4means)

```
Представим полученные варианты кластеризации стран:
```py
# Визаулайз (обожаю плотли)
# Инишиалайз суп в плов
ind_kmeans = make_subplots(rows=1, cols=2, subplot_titles=('K=2', 'K=4'))

# Добавляем traces (это кто/who?)
ind_kmeans.add_trace(go.Scatter(
    x=eu_PC2ei['PC1'],
    y=eu_PC2ei['PC2'],
    text=hover_text,
    mode='markers',
    marker=dict(
        color=ind_k2means,
        colorbar=dict(
            title='<b>Clusters</b>',
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4'],
            ticks='outside'
        ),
        colorscale=[[0.00, 'rgb(210, 29, 127)'], [0.25, 'rgb(210, 29, 127)'],
                    [0.25, 'rgb(33, 223, 155)'], [0.50, 'rgb(33, 223, 155)'],
                    [0.50, 'rgb(47, 37, 158)'], [0.75, 'rgb(47, 37, 158)'],
                    [0.75, 'rgb(150, 255, 0)'], [1.0, 'rgb(150, 255, 0)']],
        cmin=0,
        cmax=4,
        showscale=True,
        size=14,
        sizemode='area',
        line_width=0.4,
    ),
),
    row=1,
    col=1
)

ind_kmeans.add_trace(go.Scatter(
    x=eu_PC2ei['PC1'],
    y=eu_PC2ei['PC2'],
    text=hover_text,
    mode='markers',
    marker=dict(
        color=ind_k4means,
        colorbar=dict(
            title='<b>Clusters</b>',
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4'],
            ticks='outside'
        ),
        colorscale=[[0.00, 'rgb(210, 29, 127)'], [0.25, 'rgb(210, 29, 127)'],
                    [0.25, 'rgb(33, 223, 155)'], [0.50, 'rgb(33, 223, 155)'],
                    [0.50, 'rgb(47, 37, 158)'], [0.75, 'rgb(47, 37, 158)'],
                    [0.75, 'rgb(150, 255, 0)'], [1.0, 'rgb(150, 255, 0)']],
        showscale=True,
        cmin=0,
        cmax=4,
        size=14,
        sizemode='area',
        line_width=0.4
    ),
),
    row=1,
    col=2
)

# ХАкс
ind_kmeans.update_xaxes(
    patch=dict(
        title='<b>Principal component 1</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=1.4,
    ),
    row=1,
    col=1
)

ind_kmeans.update_xaxes(
    patch=dict(
        title='<b>Principal component 1</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=1.4,
    ),
    row=1,
    col=2
)

# УАкс
ind_kmeans.update_yaxes(
    patch=dict(
        title='<b>Principal component 2</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=1.4,
    ),
    row=1,
    col=1
)

ind_kmeans.update_yaxes(
    patch=dict(
        title='<b>Principal component 2</b>',
        gridcolor='#EBF0F8',
        type='linear',
        gridwidth=1.4,
    ),
    row=1,
    col=2
)

# Упд лаяют
ind_kmeans.update_layout(
    showlegend=False,
    title='K-Means clustering',
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(255, 255, 255)')

ind_kmeans.show()
ind_kmeans.write_image('.\\Graphics\\ind_kmeans.png')
```
Статичный вариант:

![Кластеры](Graphics/ind_kmeans.png)

Для большей наглядности представим это на карте Европы:
```py
eu_PC2ei['KMeans=2'] = ind_k2means
eu_PC2ei['KMeans=4'] = ind_k4means

eu_map = go.Figure(
    data=go.Choropleth(
        locations=eu_PC2ei['Country'],
        locationmode='country names',
        z=eu_PC2ei['KMeans=4'],
        hovertext=hover_text,
        colorscale=[[0.00, 'rgb(210, 29, 127)'], [0.25, 'rgb(210, 29, 127)'],
                    [0.25, 'rgb(33, 223, 155)'], [0.50, 'rgb(33, 223, 155)'],
                    [0.50, 'rgb(47, 37, 158)'], [0.75, 'rgb(47, 37, 158)'],
                    [0.75, 'rgb(150, 255, 0)'], [1.0, 'rgb(150, 255, 0)']],
        colorbar=dict(
            title='<b>Clusters</b>',
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4'],
            ticks='outside'
        ),
        zmin=0,
        zmax=4)
)

eu_map.update_layout(
    title_text='Clusters',
    geo_scope='europe',  # limite map scope
)

eu_map.show()
eu_map.write_image('.\\Graphics\\eu_map.png')
```

![Кластеры (Карта)](Graphics/eu_map.png)

### Источники:
1. [Eurostat](https://ec.europa.eu/eurostat/data/database)
2. [Datahub](https://datahub.io/)
3. [Worldbank](https://data.worldbank.org/)
