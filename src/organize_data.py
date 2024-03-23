import pandas as pd
import numpy as np


#FARS_DATA_03


vehicle_data = pd.read_csv('..\data\data-raw\\fars_data_03_sizeable.csv')
pd.set_option('display.max_columns', None)
vehicle_data.head()

#Removing unnecessary/duplicate data
vehicle_data = vehicle_data.drop(columns = vehicle_data.loc[:,'Unnamed: 0.1':'CDL_STATNAME'])
vehicle_data = vehicle_data.drop(columns = vehicle_data.loc[:,'MCARR_I1':'MCARR_IDNAME'])
vehicle_data = vehicle_data.drop(columns = vehicle_data.loc[:,'PEV_SUS1':'P_CRASH1'])
vehicle_data = vehicle_data.drop(columns = vehicle_data.loc[:,'MAKE':'MAK_MODNAME'])
vehicle_data = vehicle_data.drop(columns = [
                                            'DR_DRINK', 
                                              'DEFORMED',
                                              'Distractions',
                                              'FIRE_EXPNAME', 
                                              'EMER_USENAME', 
                                              'GVWR_TO',
                                              'GVWR_FROM',
                                              'HARM_EV', 
                                              'HOURNAME', 
                                              'ICFINALBODY',
                                              'ICFINALBODY',
                                              'J_KNIFE',
                                              'J_KNIFENAME',
                                              'L_STATUS',
                                              'L_TYPE',
                                              'MAN_COLL',
                                              'Maneuvers',
                                              'MODEL',
                                              'MOD_YEARNAME',
                                              'M_HARM',
                                              'PCRASH4',
                                              'PCRASH5',
                                              'P_CRASH2',
                                              'P_CRASH3',
                                              'ROLINLOC',
                                              'ROLLOVER',
                                              'ROLLOVERNAME',
                                              'SPEEDREL',
                                              'TRAV_SPNAME',
                                              'TOWED',
                                              'VPAVETYP',
                                              'VPICBODYCLASS',
                                              'VPICMAKE',
                                              'VPICMODEL',
                                              'VPROFILE',
                                              'VSURCOND',
                                              'VTCONT_F',
                                              'VTRAFCON',
                                              'VTRAFWAY',
                                              'V_CONFIG',
                                              'VSPD_LIMNAME'
                                              ])

#formatting data as needed
vehicle_data['DR_WGT'].astype(int)
vehicle_data.replace(999, np.nan, inplace = True)
vehicle_data['GVWR_FROMNAME'].replace('Reported as Unknown', np.nan, inplace = True)
vehicle_data['GVWR_FROMNAME'].replace('Not Reported', np.nan, inplace = True)

#reformat statenames to two letter codes for use in plotly
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

vehicle_data['STATENAME'] = vehicle_data['STATENAME'].map(lambda x: statename.get(x,x))
vehicle_data['L_STATENAME'] = vehicle_data['L_STATENAME'].map(lambda x: statename.get(x,x))

vehicle_data.to_csv('..\data\data-clean\\accident_data_2021.csv')


#FARS_DATA_04


accident_data = pd.read_csv('..\data\data-raw\\fars_data_04.csv')

#Adding BEA Economic information by county -- Avaerage income/capita/county
accident_data['COUNTYNAME'] = accident_data['COUNTYNAME'].str.split(" \(", regex = True).str[0].str.lower()
income_df = pd.read_csv('..\data\data-auxiliary\BEA_personal_per_capita_income.csv')
income_df = income_df.rename(columns = {'Table 1. Per Capita Personal Income, by County, 2020–2022':'county', 'Unnamed: 2': 'COUNTYINCOME'})
income_df['COUNTYNAME'] = income_df['county'].str.lower()

county_income_accident = accident_data.merge(income_df[['COUNTYNAME', 'COUNTYINCOME']], on = 'COUNTYNAME', how = 'left' )
county_income_accident['COUNTYINCOME']=county_income_accident['COUNTYINCOME'].str.replace(',','')
county_income_accident['COUNTYINCOME']=county_income_accident['COUNTYINCOME'].astype(float)
county_income_accident['FATALS']=county_income_accident['FATALS'].astype(int)

fatal_incident = county_income_accident.loc[(county_income_accident['FATALS']>=1)]

#Removing unnecessary/duplicate columns
fatal_incident = fatal_incident.drop(columns = fatal_incident.loc[:,'CF1':'CITY'])
fatal_incident = fatal_incident.drop(columns = fatal_incident.loc[:,'WEATHER1':'WEATHER2NAME'])

fatal_incident = fatal_incident.drop(columns = ['Unnamed: 0',
                               'COUNTY',
                               'DRUNK_DR', 
                               'FUNC_SYS',
                               'HARM_EV',
                               'LGT_COND',
                               'LATITUDENAME',
                               'LONGITUDNAME',
                               'MAN_COLL',
                               'MILEPT',
                               'MINUTENAME',
                               'MonthName',
                               'NHS',
                               'RAIL',
                               'RAILNAME',
                               'RD_OWNER',
                               'RELJCT1',
                               'RELJCT2',
                               'REL_ROAD',
                               'ROAD_FNC',
                               'ROAD_FNCNAME',
                               'ROUTE',
                               'RUR_URB',
                               'SCH_BUS',
                               'TYP_INT',
                               'WRK_ZONE'
])

#Removing outliers based on income

q1 = np.percentile(fatal_incident['COUNTYINCOME'].dropna(), 25)
q3 = np.percentile(fatal_incident['COUNTYINCOME'].dropna(), 75)
iqr = q3 - q1
outlier = iqr*1.5 + q3
fatal_incident = fatal_incident[fatal_incident['COUNTYINCOME'].notna()]
fatal_incident = fatal_incident[fatal_incident['COUNTYINCOME'] <= outlier]

fatal_incident.to_csv('..\data\data-clean\\fatal_incidents_by_county.csv')