# Блокнот исследования

---

## Содержание
- Анализ данных по экономическому развитию и миграции в странах Евросоюза
- Источники

## Анализ данных по экономическому развитию и миграции в странах Евросоюза

---
Код

```py
import pandas as pd
from pandas import DataFrame as df
import sys
import os

os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Datasets')
migr_reason = pd.read_csv('sdg_08_10.tsv', sep='\t')

print(migr_reason)

```

### Источники:
1. https://ec.europa.eu/eurostat/data/database
