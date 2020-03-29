#!/usr/bin/env python
# coding: utf-8

# # Covid19 Analysis for Nordic Countries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline


# In[2]:


df = pd.read_json('https://pomber.github.io/covid19/timeseries.json')[['Sweden','Denmark','Norway','Finland','Iceland']]


# In[3]:


n_rows = df.shape[0]
df['Sweden'][0]


# In[4]:


# extract dates
dates = []
for i in range(n_rows):
    dates.append(df['Sweden'][i]['date'])


# In[5]:


df['Date'] = dates
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')


# In[6]:


df.tail()


# In[7]:


df_deaths = pd.DataFrame(index=df.index)
for col in df.columns:
    df_deaths[col] = [c.get('deaths') for c in df[col]]


# In[8]:


# Start from March 10 before first deaths
df_deaths = df_deaths['2020-03-10':]
# Fix faulty Iceland data
df_deaths.loc['2020-03-15','Iceland'] = 0
df_deaths.loc['2020-03-20','Iceland'] = 1


# In[9]:


# population data from Wikipedia

df_pop = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)')[3]
df_pop = df_pop[['Country or area', 'Population(1 July 2019)']]

df_pop['Country or area'] = df_pop['Country or area'].str.replace('\[.*\]','')
df_pop = df_pop.pivot_table(columns='Country or area',values='Population(1 July 2019)')[df.columns]
df_pop = df_pop / 1000000


# In[10]:


df_pop['Sweden']


# In[11]:


df_deaths_per_mn = pd.DataFrame(index=df_deaths.index)
for col in df_deaths.columns:
    df_deaths_per_mn[col] = df_deaths[col] / df_pop[col].values


# In[12]:


df_deaths_per_mn


# # Trend from first death

# In[13]:


df_deaths_1 = df_deaths[df_deaths != 0]

# Remove all dates with zero deaths
df_deaths_1 = df_deaths_1.apply(lambda x: pd.Series(x.dropna().values))

# Add zero to first day
df_deaths_1 = pd.concat([pd.DataFrame(np.zeros((1,df_deaths_1.shape[1])),columns=df_deaths_1.columns), df_deaths_1], axis=0,ignore_index=True)


# In[14]:


# deaths per mn inhabitants since first death
df_deaths_per_mn_1 = pd.DataFrame(index=df_deaths_1.index)
for col in df_deaths.columns:
    df_deaths_per_mn_1[col] = df_deaths_1[col] / df_pop[col].values


# # Plots
# 
# ## Deaths over time

# In[15]:


import plotly.graph_objects as go
import pandas as pd
import plotly


fig = go.Figure()

for col in df_deaths:
    fig.add_trace(go.Scatter(x=df_deaths.index, y=df_deaths[col], name=col))

fig.update_layout(title_text='COVID19 Total Nordic Deaths, starting March 10 2020',hovermode = 'x',
                  xaxis_rangeslider_visible=True, annotations=[dict(x = 1, y = -.47, text = "Updated {}".format(str(df_deaths.tail().index[-1])[:10]), 
      showarrow = False, xref='paper', yref='paper', 
      xanchor='right', yanchor='auto', xshift=0, yshift=0, font=dict(color="red",size=12))])
plotly.offline.plot(fig, filename='deaths.html',auto_open=False)


# In[16]:


fig = go.Figure()

for col in df_deaths_per_mn:
    fig.add_trace(go.Scatter(x=df_deaths_per_mn.index, y=df_deaths_per_mn[col], name=col))

fig.update_layout(title_text='COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020',hovermode = 'x',
                  xaxis_rangeslider_visible=True,annotations=[dict(x = 1, y = -.47, text = "Updated {}".format(str(df_deaths.tail().index[-1])[:10]), 
      showarrow = False, xref='paper', yref='paper', 
      xanchor='right', yanchor='auto', xshift=0, yshift=0, font=dict(color="red",size=12))])
plotly.offline.plot(fig, filename='deaths_mn.html',auto_open=False)


# In[17]:


fig = go.Figure()

for col in df_deaths_1:
    fig.add_trace(go.Scatter(x=df_deaths_1.index, y=df_deaths_1[col], name=col))

fig.update_layout(template='plotly_white', title_text='COVID19 Total Nordic Deaths, daily data since first death',hovermode = 'x',
                  xaxis_rangeslider_visible=True,annotations=[dict(x = 1, y = -.47, text = "Updated {}".format(str(df_deaths.tail().index[-1])[:10]), 
      showarrow = False, xref='paper', yref='paper', 
      xanchor='right', yanchor='auto', xshift=0, yshift=0, font=dict(color="red",size=12))])
plotly.offline.plot(fig, filename='deaths_1.html',auto_open=False)


# In[18]:


fig = go.Figure()

for col in df_deaths_per_mn_1:
    fig.add_trace(go.Scatter(x=df_deaths_per_mn_1.index, y=df_deaths_per_mn_1[col], name=col))

fig.update_layout(template='plotly_white', title_text='COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death', hovermode = 'x',
                  xaxis_rangeslider_visible=True,annotations=[dict(x = 1, y = -.47, text = "Updated {}".format(str(df_deaths.tail().index[-1])[:10]), 
      showarrow = False, xref='paper', yref='paper', 
      xanchor='right', yanchor='auto', xshift=0, yshift=0, font=dict(color="red",size=12))])
plotly.offline.plot(fig, filename='deaths_mn_1.html',auto_open=False)


# In[ ]:




