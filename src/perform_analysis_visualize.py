import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

vehicle = pd.read_csv('..\data\data-clean\\accident_data_2021.csv')

##figure 1
state_death_toll = vehicle.groupby('STATENAME')['DEATHS'].sum().reset_index()

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
make_death_toll = vehicle.groupby('VPICMAKENAME')['DEATHS'].sum().reset_index()
top_make_death = make_death_toll.sort_values(['DEATHS'], ascending = False)[:10]
make_death_counts = plt.bar(
    x = top_make_death['VPICMAKENAME'],
    height = top_make_death['DEATHS'],
    width = 0.4
)
plt.xticks(rotation = 65)
plt.title('Top 10 Manufacturers by Death Counts')
plt.savefig('../plots/make_fatality_top_ten.png')


#Figure 3 used raw data here to demonstrate need for wxcluding salary based outliers
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


#Figure 4
ax = sns.displot(data = fatal_incident,
            x = 'COUNTYINCOME',
            kind = 'kde'
            )
ax.set_xlabels('Average County Income')
ax.set_ylabels('Proportion of Fatal Accidents')
ax.set(title='Density of Fatal Accidents by County Income')
plt.ticklabel_format(style='plain')
ax.savefig('../plots/fatality_income_density.png')

vehicle_data = pd.read_csv('..\data\data-clean\\accident_data_2021.csv')
clock_collision_values = ['1 Clock Point', '2 Clock Point','3 Clock Point', '4 Clock Point','5 Clock Point', '6 Clock Point',
                          '7 Clock Point', '8 Clock Point','9 Clock Point', '10 Clock Point','11 Clock Point', '12 Clock Point']
clock_mask = vehicle_data['IMPACT1NAME'].isin(clock_collision_values)
clock_collision_df = vehicle_data[clock_mask]
clock_collision_df.head()

categories = ['12 Clock Point',
              '1 Clock Point', 
              '2 Clock Point',
              '3 Clock Point', 
              '4 Clock Point',
              '5 Clock Point', 
              '6 Clock Point',
              '7 Clock Point', 
              '8 Clock Point',
              '9 Clock Point', 
              '10 Clock Point',
              '11 Clock Point', 
              '12 Clock Point'
]

vehicle_data['IMPACT1NAME'].value_counts()['1 Clock Point']

crach_point_list = [vehicle_data['IMPACT1NAME'].value_counts()['12 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['1 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['2 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['3 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['4 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['5 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['6 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['7 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['8 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['9 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['10 Clock Point'],
                 vehicle_data['IMPACT1NAME'].value_counts()['11 Clock Point']
]

hit_point = np.concatenate((crach_point_list, [crach_point_list[0]]))

label_place = np.linspace(start = 0, stop = (2*np.pi), num = 13)

plt.figure(figsize = (7,7))
plt.subplot(polar = True)
plt.plot(label_place, hit_point)
lines, labels = plt.thetagrids(np.degrees(label_place), labels = categories)
plt.title('Location of Primary Impact During Vehicle Collisions')
plt.legend(labels = ['Location of Impact'],
           loc = 'lower left')
plt.savefig('../plots/impact_point.png')


#Figure 5
vehicle_deformity_df = vehicle_data[vehicle_data['DEFORMEDNAME'].notna()]
vehicle_deformity_df = vehicle_deformity_df[vehicle_deformity_df['DEFORMEDNAME'] != 'Reported as Unknown']
vehicle_deformity_df = vehicle_deformity_df[vehicle_deformity_df['DEFORMEDNAME'] != 'Not Reported']
plt.figure()
plt.pie(vehicle_deformity_df['DEFORMEDNAME'].value_counts(),
    labels = vehicle_deformity_df['DEFORMEDNAME'].value_counts().index,
    autopct = '%.2f%%',
    textprops = {'color':'w','fontsize':12})
plt.legend(bbox_to_anchor=(1,0.5),
    loc="lower right",
    fontsize=14,
    bbox_transform=plt.gcf().transFigure)
plt.title('Vehicle Damage Present in Fatal Accidnets',
    fontsize = 16)
plt.savefig('../plots/vehicle_deformity.png')