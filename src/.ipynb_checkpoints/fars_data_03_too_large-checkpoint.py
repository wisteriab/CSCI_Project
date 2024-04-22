import pandas as pd
df = pd.read_csv('..\data\data-raw\\fars_data_03.csv')
df = df.drop(columns=['ACC_TYPE', 
           'ADS_ENG', 
           'ADS_ENGName', 
           'ADS_LEV', 
           'ADS_LEVName', 
           'ADS_PRES', 
           'ADS_PRESName', 
           'CASEYEAR',
           'DR_SF1',
           'DR_SF1NAME',
           'DR_SF2',
           'DR_SF2NAME',
           'DR_SF3',
           'DR_SF3NAME',
           'DR_SF4',
           'DR_SF4NAME',
           'DR_WGTNAME',
           'DR_ZIPNAME',
           'Damages',
           'DrImpairs',
           'DrierRFs',
           'EMER_USE',
           'FIRE_EXP',
           'Factors',
           'GVWR',
           'GVWRNAME',
           'HAZ_CNO',
           'HAZ_CNONAME',
           'HAZ_ID',
           'HAZ_IDNAME',
           'HAZ_INV',
           'HAZ_INVNAME',
           'HAZ_PLAC',
           'HAZ_PLACNAME',
           'HAZ_REL',
           'HAZ_RELNAME',
           'HIT_RUN',
           'NCSABODY_TYP',
           'NCSABODY_TYPNAME',
           'NCSAMAKE',
           'NCSAMAKENAME',
           'NCSAMODEL',
           'NCSAMODELNAME',
           'NUMOCCSNAME',
           'PREV_SUS',
           'PREV_SUSNAME',
           'Persons',
           'SPEC_USE',
           'SPEC_USENAME',
           'VehicleSFs',
           'VinDecodes',
           'VinDeriveds',
           'Violations',
            'Vsoes',
            'Visions'
           ]
)
df = df.drop(columns = df.loc[:,'TRLR1VIN':'VEvents'].columns)
df = df.drop(columns = df.loc[:,'VINNAME':'VIN_9'].columns)
df.to_csv("..\data\data-raw\\fars_data_03_sizeable.csv")
