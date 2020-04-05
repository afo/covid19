#!/usr/bin/env python
# coding: utf-8

# # Covid19 Analysis for Nordic Countries

# In[48]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline


# In[49]:


df = pd.read_json('https://pomber.github.io/covid19/timeseries.json')[['Sweden','Denmark','Norway','Finland','Iceland']]


# In[50]:


n_rows = df.shape[0]
df['Sweden'][0]


# In[51]:


# extract dates
dates = []
for i in range(n_rows):
    dates.append(df['Sweden'][i]['date'])


# In[52]:


df['Date'] = dates
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')


# In[53]:


df.tail()


# In[54]:


df_deaths = pd.DataFrame(index=df.index)
for col in df.columns:
    df_deaths[col] = [c.get('deaths') for c in df[col]]


# In[55]:


# Start from March 10 before first deaths
df_deaths = df_deaths['2020-03-10':]
# Fix faulty Iceland data
df_deaths.loc['2020-03-15','Iceland'] = 0
df_deaths.loc['2020-03-20','Iceland'] = 1


# In[56]:


# population data from Wikipedia

df_pop = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)')[3]
df_pop = df_pop[['Country or area', 'Population(1 July 2019)']]

df_pop['Country or area'] = df_pop['Country or area'].str.replace('\[.*\]','')
df_pop = df_pop.pivot_table(columns='Country or area',values='Population(1 July 2019)')[df.columns]
df_pop = df_pop / 1000000


# In[57]:


df_pop['Sweden']


# In[58]:


df_deaths_per_mn = pd.DataFrame(index=df_deaths.index)
for col in df_deaths.columns:
    df_deaths_per_mn[col] = df_deaths[col] / df_pop[col].values


# In[59]:


df_deaths_per_mn


# # Trend from first death

# In[60]:


df_deaths_1 = df_deaths[df_deaths != 0]

# Remove all dates with zero deaths
df_deaths_1 = df_deaths_1.apply(lambda x: pd.Series(x.dropna().values))

# Add zero to first day
df_deaths_1 = pd.concat([pd.DataFrame(np.zeros((1,df_deaths_1.shape[1])),columns=df_deaths_1.columns), df_deaths_1], axis=0,ignore_index=True)


# In[61]:


# deaths per mn inhabitants since first death
df_deaths_per_mn_1 = pd.DataFrame(index=df_deaths_1.index)
for col in df_deaths.columns:
    df_deaths_per_mn_1[col] = df_deaths_1[col] / df_pop[col].values


# # Plots
# 
# ## Deaths over time

# In[69]:


from datetime import datetime, timedelta

import plotly.graph_objects as go
import plotly

end_date = df_deaths.tail().index[-1] + timedelta(days=1)
date = str(end_date)[:10] + ' 03:00 CET'

def plot_graph(data, title, x_title, y_title, file_name, date, template='seaborn',end_date=end_date):
    fig = go.Figure()

    for col in data:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], name=col))

    fig.update_layout(template=template, title_text=title,
                  xaxis_title=x_title, xaxis=dict(tickmode='linear'), xaxis_range=[data.index[0], end_date],
                  yaxis_title=y_title,
                  hovermode = 'x',
                  xaxis_rangeslider_visible=True, annotations=[dict(x = 1, y = 0, text = "Updated {}".format(date), 
      showarrow = False, xref='paper', yref='paper', 
      xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red",size=8.5))])
    plotly.offline.plot(fig, filename=file_name,auto_open=False)
    
plot_graph(df_deaths, 'COVID19 Total Nordic Deaths, starting March 10 2020', "Date", "Deaths", 'deaths.html', date)
plot_graph(df_deaths_per_mn, 'COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020', "Date", "Deaths per Mn inhabitants", 'deaths_mn.html',date)
plot_graph(df_deaths_1, 'COVID19 Total Nordic Deaths, daily data since first death', "Days since first Death", "Deaths", 'deaths_1.html', date, template='plotly_white', end_date =df_deaths_1.index[-1]+1)
plot_graph(df_deaths_per_mn_1, 'COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death', "Days since first Death", "Deaths per Mn inhabitants", 'deaths_mn_1.html', date, template='plotly_white', end_date =df_deaths_1.index[-1]+1)


# In[ ]:




