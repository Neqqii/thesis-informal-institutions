import pandas as pd
import numpy as np
import os
import plotly.offline as pyo
import plotly as ply
import plotly.tools as tls
import plotly.graph_objs as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Choose directory
os.chdir('C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research')

# Import dataset
eu_ei = pd.read_csv('.\\Datasets\\eu_consolide_ei.csv')

# Separating indicators from data
print(eu_ei.columns)
print(eu_ei.dtypes)
indicators = eu_ei.columns[2:]
aux_ind = eu_ei.loc[:, indicators].values

# Standardizing indicators values
ind = StandardScaler().fit_transform(aux_ind)
eu_indei = pd.DataFrame(data=ind, columns=indicators)
print(eu_indei)

# PCA projection (4D to 2D)
pca = PCA(n_components=2)
pComp = pca.fit_transform(ind)

eu_pCompei = pd.DataFrame(data=pComp, columns=['PC1', 'PC2'])
eu_PC2ei = pd.concat([eu_pCompei, eu_ei[['Country']]], axis=1)
print(eu_PC2ei)

# Visualise 2PC
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

eu_PCAei.show()

os.path.relpath(
    'C:\\Users\\Nvmind\\github\\thesis-informal-institutions\\Research\\Graphics', start=None)
eu_PCAei.write_image('.\\Graphics\\PCA_ei.png')
