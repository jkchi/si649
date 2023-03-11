#!/usr/bin/env python
# coding: utf-8

# # **SI649 W23 Altair Homework #4**
# ## Overview 
# 
# We'll focus on maps and cartrographic visualization. In this lab, you will practice:
# * Point Maps
# * Symbol Maps
# * Choropleth maps
# * Interactions with maps
# 
# 
# After building these charts, you will make a website with these charts using streamlit.
# 
# ### Lab Instructions
# 
# *   Save, rename, and submit the ipynb file (use your username in the name).
# *   Complete all the checkpoints, to create the required visualization at each cell.
# *   Run every cell (do Runtime -> Restart and run all to make sure you have a clean working version), print to pdf, submit the pdf file. 
# *   If you end up stuck, show us your work by including links (URLs) that you have searched for. You'll get partial credit for showing your work in progress.

# In[6]:


import pandas as pd
import altair as alt
from vega_datasets import data
import streamlit

alt.data_transformers.disable_max_rows()

df = pd.read_csv('https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/airports.csv')
url = "https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/small-airports.json"


# ## Visualization 1: Dot Density Map 

# ![vis1](https://pratik-mangtani.github.io/si649-hw/dot_density.png)
# **Description of the visualization:**
# 
# We want to visualize the density of small airports in the world. Each small airport is represented by a dot. 
# The visualization has two layers:
# * The base layer shows the outline of the world map. 
# * The point map shows different small airports. 
# * The tooltip shows the **name** of the airport. 
# 
# **Hint:**
# * How can we show continents on the map? Which object can be used from the json dataset ?
# * How can we show only small airports on the map?

# In[7]:


# TODO: Vis 1
countries = alt.Chart(alt.topo_feature(url, 'continent')).mark_geoshape(
    fill='#C0C0C0',stroke='#FFFFFF'
)

airport = alt.Chart(df).transform_filter(alt.datum.type =='small_airport').mark_circle(color='red').encode(
    longitude='longitude_deg:Q',
    latitude='latitude_deg:Q',
    size=alt.value(10),
    tooltip = 'name'
)

airportGraph = (countries+airport).properties(height = 600, width = 800, title = "Small airports in the world").configure_title(fontSize=24)


# ## Visualization 2: Propotional Symbol 

# ![vis2](https://pratik-mangtani.github.io/si649-hw/symbol_map.png)
# **Description of the visualization:**
# 
# The visualization shows faceted maps pointing the 20 most populous cities in the world by 2100. There are two layers in faceted charts:
# * The base layer shows the map of countries. 
# * The second layer shows size encoded points indicating the population of those countries.
# * Tooltip shows **city** name and **population**. 
# 
# **Hint:**
# * Which projection has been used in individual charts?
# * How to create a faceted chart with different years and 2 columns?

# ##### * The piazza answer was not direct
# ##### * This is the way to slove the identical layer issue
# > https://github.com/altair-viz/altair/issues/668

# In[8]:


countries_url = data.world_110m.url
source = 'https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/population_prediction.csv'


# In[9]:


df_popu = pd.read_csv(source)


# #### important website regarding setting title and legend
# > #### https://altair-viz.github.io/user_guide/configuration.html
# > #### https://altair-viz.github.io/user_guide/configuration.html#config-axis
# > #### https://altair-viz.github.io/user_guide/configuration.html#config-legend
# notice the tilte and lable control different thing

# In[20]:


# TODO: Vis 2
base = alt.Chart(alt.topo_feature(countries_url, 'countries')).mark_geoshape(
    fill='#C0C0C0', stroke='#FFFFFF', strokeWidth=0.1).project(
    type='naturalEarth1'
)

point =  alt.Chart().mark_circle(color = 'green',stroke = 'white',
    strokeWidth = 2,).encode(
    longitude='lon:Q',
    latitude='lat:Q',
    size=alt.Size('population:Q', scale=alt.Scale(range=[0, 1500]) ,title='Population (million)'),
    tooltip=['city:N','population:Q']
)

popuMap = alt.layer(base,point).facet("year:N", data = df_popu,columns = 2).properties(title = "The 20 Most Populous Cities in the World by 2100").configure_title(fontSize=24
).configure_header(
    titleColor='black',
    titleFontSize=20,
    labelColor='black',
    labelFontSize=20
).configure_legend(titleFontSize = 15,labelFontSize = 15)



# ## Visualization 3: Hurricane Trajectories
# 
# 
# 

# ![vis3](https://pratik-mangtani.github.io/si649-hw/hurricane_trajectories.png)
# **Description of the visualization:**
# 
# Create a map that shows the paths (trajectories) of the 2017 hurricanes. Filter the data so that only 2017 hurricanes are shown. Remove Alaska and Hawaii from the map (Filter out ids 2 and 15).
# 
# **Hint:**
# * How will you filter out 2017 hurricanes?
# * Which object can be used to show state boundaries?

# #### important projection choice document
# > ##### https://vega.github.io/vega-lite/docs/projection.html#projection-types 
# > ##### https://github.com/d3/d3-geo#geoMercator

# In[11]:


states_url = data.us_10m.url
hurricane_data = pd.read_csv('https://raw.githubusercontent.com/pratik-mangtani/si649-hw/main/hurdat2.csv')
hurricane_data.sample(3)


# In[12]:


#TODO: Vis 3

states = alt.topo_feature(states_url, feature='states')

stateMap = alt.Chart(states).mark_geoshape(
        fill = 'white',
        stroke='black',
        strokeWidth=1
    ).transform_filter((alt.datum.id != 2) & (alt.datum.id != 15))

line = alt.Chart(hurricane_data).mark_line(color = 'blue',size = 1).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
).transform_filter(
    'year(datum.datetime) == 2017'
)

trTrace = alt.layer(stateMap,line).properties(height = 400, width = 600)



# ## Visualization 4: Choropleth Map
# 

# ![vis4](https://pratik-mangtani.github.io/si649-hw/choropleth.png)
# 
# **Interaction**
# 
# ![vis4](https://pratik-mangtani.github.io/si649-hw/choropleth-interaction.gif)
# 
# **Description of the visualization:**
# 
# The visualization has a choropleth map showing the population of different states and a sorted bar chart showing the top 15 states by population. These charts are connected using a click interaction. 
# 
# **Hint**
# 
# * Which object can be used to show states on the map?
# * Which transform can be used to add population data to the geographic data? How can we combine two datasets in Altair?
# 
# 

# In[13]:


state_map = data.us_10m.url
state_pop = data.population_engineers_hurricanes()[['state', 'id', 'population']]
state_pop.sample(5)


# In[27]:


# TODO: Vis 4 

click = alt.selection_multi(fields=['state'])

map = alt.Chart(alt.topo_feature(state_map, 'states')).mark_geoshape(
).project(
    type='albersUsa'
).transform_lookup(
    # notice the state need to extraced or the selection will not work
    lookup='id', from_=alt.LookupData(data=state_pop, key='id', fields = ['population', 'state'])
).encode(
    alt.Color('population:Q'),
    opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
).add_selection(click)

bars = alt.Chart(state_pop,
    title='Top 15 states by population').transform_window(
    sort=[alt.SortField('population', order='descending')],
    popu_rank = 'rank()').transform_filter(
    alt.datum.popu_rank < 16
    ).mark_bar().encode(
    x='population',
    color='population',
    opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
    y=alt.Y('state', sort='x')).add_selection(click)

choMap = (map | bars)


tab1,tab2,tab3,tab4 = streamlit.tabs(['q1','q2','q3','q4'])

with tab1:
    streamlit.altair_chart(airportGraph, theme = None)

with tab2:
    streamlit.altair_chart(popuMap, theme = None)

with tab3:
    streamlit.altair_chart(trTrace, theme = None)

with tab4:
    streamlit.altair_chart(choMap, theme = None)
# %%
