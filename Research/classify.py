import pandas as pd
import numpy as np
import os
import plotly.offline as pyo
import plotly as ply
import plotly.tools as tls
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

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
pca.explained_variance_ratio_
print(eu_PC2ei)

# ТуПКа 2
hover_text = []

for index, row in eu_ei.iterrows():
    hover_text.append(('Country: {country}<br>' +
                       'Population: {popul}<br>' +
                       'GDP: {gdp}<br>' +
                       'Immigration: {immi}<br>' +
                       'Emigration: {emi}').format(country=row['Country'],
                                                   popul=row['Population'],
                                                   gdp=row['GDP'],
                                                   immi=row['Immigration'],
                                                   emi=row['Emigration']))

eu_PCAei = go.Figure(data=[go.Scatter(
    x=eu_PC2ei['PC1'],
    y=eu_PC2ei['PC2'],
    text=hover_text,
    mode='markers',
    marker=dict(
        color='#1dec95',
        size=10,
        sizemode='area',
        line_width=0.4
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

# Теперь надо надо кластеризовать

# Первый способ: KMeans

# Сначала выберем оптимальное число k
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

# А теперь на карте
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
    geo=dict(
        scope='europe',
    )
)

eu_map.show()
eu_map.write_image('.\\Graphics\\eu_map.png', scale=4)
