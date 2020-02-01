# Блокнот исследования

---

## Содержание
- [Экономическое развитие и миграция](#Анализ-данных-по-экономическому-развитию-и-миграции-в-странах-Евросоюза)
- [Источники](#источники)

## Анализ данных по экономическому развитию и миграции в странах Евросоюза

---
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
![Immigration vs Emigration](http://127.0.0.1:57172/)

![Immigration vs Emigration](C:\Users\Nvmind\github\thesis-informal-institutions\Research\Graphics\ImmieEmi)

### Источники:
1. [Eurostat](https://ec.europa.eu/eurostat/data/database)
2. [Datahub](https://datahub.io/)
3. [Worldbank](https://data.worldbank.org/)
