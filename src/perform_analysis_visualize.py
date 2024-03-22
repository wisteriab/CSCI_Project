import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

vehicle = pd.read_csv('..\data\data-raw\\fars_data_03.csv')

##figure 1
state_death_toll = vehicle.groupby('STATENAME')['DEATHS'].sum().reset_index()

statename = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
}

state_death_toll['STATENAME'] = state_death_toll['STATENAME'].map(lambda x: statename.get(x,x))

fig = go.Figure(data = go.Choropleth(
    locations = state_death_toll['STATENAME'],
    z = state_death_toll['DEATHS'],
    locationmode='USA-states',
    colorscale = 'Oranges',
    colorbar_title = "Death Count"
))
fig.update_layout(
    geo_scope = 'usa',
    title_text = "2021 Death Count by State"
)
fig.write_image('../plots/us_fatality_map.png')

#figure 2
make_death_toll = vehicle.groupby('MAKENAME')['DEATHS'].sum().reset_index()
top_make_death = make_death_toll.sort_values(['DEATHS'], ascending = False)[:10]
make_death_counts = plt.bar(
    x = top_make_death['MAKENAME'],
    height = top_make_death['DEATHS'],
    width = 0.4
)
plt.xticks(rotation = 65)
plt.title('Top 10 Manufacturers by Death Counts')
plt.savefig('../plots/make_fatality_top_ten.png')


accident_df = pd.read_csv('..\data\data-raw\\fars_data_04.csv')
accident_df['COUNTYNAME'] = accident_df['COUNTYNAME'].str.split(" \(", regex = True).str[0].str.lower()
income_df = pd.read_csv('..\data\data-auxiliary\BEA_personal_per_capita_income.csv')
income_df = income_df.rename(columns = {'Table 1. Per Capita Personal Income, by County, 2020–2022':'county', 'Unnamed: 2': 'COUNTYINCOME'})
income_df['COUNTYNAME'] = income_df['county'].str.lower()

county_income_accident = accident_df.merge(income_df[['COUNTYNAME', 'COUNTYINCOME']], on = 'COUNTYNAME', how = 'left' )
county_income_accident['COUNTYINCOME']=county_income_accident['COUNTYINCOME'].str.replace(',','')
county_income_accident['COUNTYINCOME']=county_income_accident['COUNTYINCOME'].astype(float)
county_income_accident['FATALS']=county_income_accident['FATALS'].astype(int)

fatal_incident = county_income_accident.loc[(county_income_accident['FATALS']>=1)]

ax = sns.displot(data = fatal_incident,
            x = 'COUNTYINCOME',
            kind = 'kde'
            )
ax.set_xlabels('Average County Income')
ax.set_ylabels('Proportion of Fatal Accidents')
ax.set(title='Density of Fatal Accidents by County Income')
plt.ticklabel_format(style='plain')
ax.savefig('../plots/fatality_income_density.png')