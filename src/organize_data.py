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

# data for modelling

data = pd.read_csv('..\data\data-clean\\accident_data_2021.csv', index_col = 0)
hit_runmap = {'No': 0, 'Yes':1}
data.HIT_RUNNAME = data.HIT_RUNNAME.map(hit_runmap)
#LICENSE REQ FOR VEHICLE
license_map = {3:0, 2:1, 0:1, 9:0, 6:0, 1:0, 8:0}
data.L_COMPL = data.L_COMPL.map(license_map)
# LICENSE VIOLATION = 1 \\ NO VIOLATION = 0
valid_map = {'Valid': 0, 
            'Not licensed': 1, 
            'Suspended': 1, 
            'Unknown License Status': 0, 
            'Expired': 1, 
            'Revoked': 1, 
            'No Driver Present/Unknown if Driver Present': 0, 
            'Canceled or denied': 1
}
data.L_STATUSNAME = data.L_STATUSNAME.map(valid_map)
data.OWNER = data.OWNER.replace(9,0)
data.NUMOCCS = data.NUMOCCS.replace(99, 0)
#Rollover = 1 else = 0
roll_map = {
    'No Rollover':0,
    'On Roadside':1,
    'On Roadway':1,
    'On Median/Separator':1,
    'Outside of Trafficway':1,
    'On Shoulder':1,
    'Unknown':0,
    'In Gore':1,
    'In Parking Lane/Zone':1
}
data.ROLINLOCNAME = data.ROLINLOCNAME.map(roll_map)
#Speeding = 1 else = 0
speed_map ={
    'No': 0,
    'Yes, Too Fast for Conditions':1,
    'Yes, Exceeded Speed Limit': 1,
    'Reported as Unknown': 0,
    'Yes, Specifics Unknown':1,
    'No Driver Present/Unknown if Driver Present': 0,
    'Yes, Racing':1
}
data.SPEEDRELNAME = data.SPEEDRELNAME.map(speed_map)
#TOWED = 1 ELSE = 0
tow_map = {
    'Towed Due to Disabling Damage' :1,
    'Not Towed': 0,
    'Towed, Unknown Reason': 1,
    'Towed But Not Due to Disabling Damage': 1,
    'Not Reported' : 0,
    'Reported as Unknown': 0
}
data.TOWEDNAME = data.TOWEDNAME.map(tow_map)
data = data.dropna(subset = ['TRAV_SP'])
data = data[data['TRAV_SP']<= 152]
#drinking = 1 else 0
drink_map = {
    'No':0,
    'Yes':1
}
data.DR_DRINKNAME = data.DR_DRINKNAME.map(drink_map)
damage_map = {
    'Disabling Damage' : 2,
    'Functional Damage' : 1,
    'Minor Damage' : 0,
    'Not Reported' : 0,
    'No Damage' : 0,
    'Reported as Unknown' : 0
}
data.DEFORMEDNAME = data.DEFORMEDNAME.map(damage_map)
vehicle_weight_map = {
    'Class 1: 6,000 lbs. or less (2,722 kg or less)' : 1,
    'Class 2: 6,001 - 10,000 lbs. (2,722 - 4,536 kg)' : 2,
    'Class 3: 10,001 - 14,000 lbs. (4,536 - 6,350 kg)' : 3,
    'Class 4: 14,001 - 16,000 lbs. (6,350 - 7,258 kg)' : 4,
    'Class 5: 16,001 - 19,500 lbs. (7,258 - 8,845 kg)' : 5,
    'Class 6: 19,501 - 26,000 lbs. (8,845 - 11,794 kg)' : 6,
    'Class 7: 26,001 - 33,000 lbs. (11,794 - 14,969 kg)' : 7,
    'Class 8: 33,001 lbs. and above (14,969 kg and above)' : 8,
    'Reported as Unknown' : 0,
    'Not Reported' : 0
}
data.GVWR_FROMNAME = data.GVWR_FROMNAME.map(vehicle_weight_map)
data.GVWR_TONAME = data.GVWR_TONAME.map(vehicle_weight_map)

data_noncat = data.drop(columns = ['DR_HGT',
                                  'DR_PRES', 
                                  'DR_PRESNAME', 
                                  'DR_WGT', 
                                  'FIRST_MO', 
                                  'FIRST_MONAME', 
                                  'FIRST_YR', 
                                  'FIRST_YRNAME', 
                                  'HARM_EVNAME', 
                                  'ICFINALBODYNAME', 
                                  'IMPACT1', 
                                  'IMPACT1NAME', 
                                  'IMPACT2', 
                                  'IMPACT2NAME', 
                                  'LAST_MO', 
                                  'LAST_MONAME', 
                                  'LAST_YR', 
                                  'L_ENDORS', 
                                  'L_COMPLNAME', 
                                  'L_ENDORSNAME', 
                                  'L_RESTRI', 
                                  'L_RESTRINAME', 
                                  'L_STATE', 
                                  'L_STATENAME', 
                                  'L_TYPENAME', 
                                  'MAN_COLLNAME', 
                                  'MINUTE', 
                                  'MINUTENAME', 
                                  'MODELNAME', 
                                  'MONTH', 
                                  'MONTHNAME', 
                                  'M_HARMNAME', 
                                  'OWNERNAME',
                                  'PCRASH4NAME', 
                                  'PCRASH5NAME', 
                                  'P_CRASH1NAME', 
                                  'P_CRASH2NAME', 
                                  'P_CRASH3NAME', 
                                  'REG_STAT', 
                                  'REG_STATNAME', 
                                  'STATE', 
                                  'STATENAME', 
                                  'ST_CASE', 
                                  'TOW_VEH', 
                                  'TOW_VEHNAME',
                                  'TRLR1GVWR', 
                                  'TRLR1GVWRNAME', 
                                  'VIN', 
                                  'VNUM_LAN', 
                                  'VNUM_LANNAME', 
                                  'VPAVETYPNAME', 
                                  'VPICMODELNAME', 
                                  'VPROFILENAME', 
                                  'VSURCONDNAME', 
                                  'VTCONT_FNAME', 
                                  'VTRAFCONNAME', 
                                  'VTRAFWAYNAME', 
                                  'V_CONFIGNAME']
)
data_noncat.to_csv('..\data\data-clean\modelling_data.csv')