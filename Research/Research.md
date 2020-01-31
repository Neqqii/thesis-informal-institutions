# Блокнот исследования

---

## Содержание
- [Экономическое развитие и миграция](#Анализ-данных-по-экономическому-развитию-и-миграции-в-странах-Евросоюза)
- [Источники](#источники)

## Анализ данных по экономическому развитию и миграции в странах Евросоюза

---
Первая база данных (Ежегодные темпы роста ВВП 1990-2019 гг.) взята с сайта [Worldbank](https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.MKTP.KD.ZG&country=).

Приведем датафрейм в удобное для проведения дальнейшего анализа состояние:

Загружаем нужные библиотеки и создаем вспомогательную базу данных

```py
import pandas as pd
import os

os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Datasets')
aux_df1 = pd.read_csv('gdp_growth_90to19.csv')

```

Чистим данные, оставляем только нужное

```py
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

```

### Источники:
1. [Eurostat](https://ec.europa.eu/eurostat/data/database)
2. [Datahub](https://datahub.io/)
3. [Worldbank](https://data.worldbank.org/)
