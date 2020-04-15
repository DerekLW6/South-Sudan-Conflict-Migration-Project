# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 22:10:02 2020

@author: Joseph Littell
"""

# Required Libraries
import pandas as pd

#------------------#
#                  #
#  Base Dataframe  #
#                  #
#------------------#

# Read in the base dataframe.
baseDF = pd.read_csv('../20_intermediate/pop_fatalities.csv')

#-----------------#
#                 #
#  Hospital Data  #
#                 #
#-----------------#

# Read in the hospital data
hospitals = pd.read_excel('../00_source/health_facilities.xls')

# Subset the dataframe
hospitals_slice = hospitals[['STATE', 'COUNTY', 'HF_TYPE', "FUNCTIONAL Status"]]

# Subset for hospitals over clinics and other small medical facilities
hospitals_slice = hospitals_slice[hospitals_slice['HF_TYPE'] == 'PHCU']

# Subset for working hospitals
hospitals_slice = hospitals_slice[hospitals_slice['FUNCTIONAL Status'] == 'Functional']

# Count the number of working hospitals by county
hospitals_slice = hospitals_slice.groupby(['STATE', 'COUNTY'])['HF_TYPE'].count().rename("Hospitals").reset_index()

# Rename the columns for ease of merging
hospitals_slice.columns = ['State', 'County', 'Hospitals']

# Rename specific locations for merge
hospitals_slice = hospitals_slice.replace('Kajo-Keji', 'Kajo-keji')
hospitals_slice = hospitals_slice.replace('Lapon', 'Lafon')
hospitals_slice = hospitals_slice.replace('Bor', 'Bor South')
hospitals_slice = hospitals_slice.replace('Raja', 'Raga')

# Merge the dataset with the original data
baseDF = pd.merge(baseDF, hospitals_slice, on = ['County', 'State'], how = 'left')


#-----------------#
#                 #
#   Water  Data   #
#                 #
#-----------------#

# Read in the water yield data
water = pd.read_excel('../00_source/water.xlsx')

# Subset the data for yield by county by state
water_slice = water[['State', 'County', 'Estimated Yield']]

# Remove random piece of data
water_slice = water_slice[water_slice['Estimated Yield'] != '?']

# Fill NAs and ensure all values are floats
water_slice['Estimated Yield'] = water_slice['Estimated Yield'].fillna(0)
water_slice['Estimated Yield'] = water_slice['Estimated Yield'].astype('float')

# Sum the yield in a county and reset the index
water_slice = water_slice.groupby(['State', 'County']).sum()
water_slice.reset_index(inplace=True)

# Rename states so that they merge correctly
water_slice = water_slice.replace('CE', 'Central Equatoria')
water_slice = water_slice.replace('WE', 'Western Equatoria')
water_slice = water_slice.replace('EE', 'Eastern Equatoria')
water_slice = water_slice.replace('NBeG', 'Northern Bahr el Ghazal')
water_slice = water_slice.replace('WBeG', 'Western Bahr el Ghazal')

# Rename counties so that they merge correctly
water_slice = water_slice.replace('Kajo Keji', 'Kajo-keji')
water_slice = water_slice.replace('Atar', 'Kajo-keji')
water_slice = water_slice.replace('Bor', 'Bor South')
water_slice = water_slice.replace('Duken', 'Duk')
water_slice = water_slice.replace('Old Fangak', 'Fangak')
water_slice = water_slice.replace('Panyijar', 'Panyijiar')
water_slice = water_slice.replace('Mabaan', 'Maban')
water_slice = water_slice.replace('Nasir/Luakapiny', 'Luakpiny/Nasir')
water_slice = water_slice.replace('Raja', 'Raga')

# Merge the data
baseDF = pd.merge(baseDF, water_slice, on = ['State','County'], how = 'left')

#----------------#
#                #
#  Demographics  #
#                #
#----------------#

# Read in the demographics data
demographics = pd.read_excel('../00_source/demographics_2020.xlsx')

# Calculate the percent of the population that is children
demographics['Population_Percent_Child'] = demographics['Children <18yrs ']/demographics['2019 Baseline Population ']

# Calculate the percent of the population that is women
demographics['Population_Percent_Female'] = (demographics['No. female children under 5'] + demographics['No. female children aged 5 - 17 years'] + demographics['No. female adults aged 18 - 60'] + demographics['No. female adults aged over 60']) / demographics['2019 Baseline Population ']

# Subset the data for the required calculations
demographics_slice = demographics[['State', 'County', 'Population_Percent_Child', 'Population_Percent_Female']]

# Merge the data
baseDF = pd.merge(baseDF, demographics_slice, on = ['State','County'], how = 'left')

#-----------------#
#                 #
#  Poverty  Data  #
#                 #
#-----------------#

# Read in the data
poverty = pd.read_csv('../00_source/poverty.csv')

# Merge the data
baseDF = pd.merge(baseDF, poverty, on = ['County', 'State'], how = 'left')

#-----------------#
#                 #
#  Airport  Data  #
#                 #
#-----------------#

# Read in the airport data
airports = pd.read_csv('../00_source/Airports.csv')

# Subset the data and rename the columns
airports_slice = airports[['type', 'municipality']]
airports_slice.columns = ['Airport', 'County']

# remove the random row
airports_slice = airports_slice[airports_slice['Airport'] != '#loc +airport +type']

# Rename Municipalities for the County they are in for the merge
airports_slice = airports_slice.replace('Aweil', 'Aweil Centre')
airports_slice = airports_slice.replace('Bor', 'Bor South')
airports_slice = airports_slice.replace('Higleig', 'Renk')
airports_slice = airports_slice.replace('Bentu', 'Rubkona')
airports_slice = airports_slice.replace('Kago Kaju', 'Kajo-keji')
airports_slice = airports_slice.replace('Kapoeta', 'Kapoeta South')
airports_slice = airports_slice.replace('Marida', 'Maridi')
airports_slice = airports_slice.replace('Nimuli', 'Magwi')
airports_slice = airports_slice.replace('Pachella', 'Pochalla')
airports_slice = airports_slice.replace('Tong', 'Tonj South')
airports_slice = airports_slice.replace('Tumbura', 'Tambura')
airports_slice = airports_slice.replace('Yirol', 'Yirol West')
airports_slice = airports_slice.replace('Kibbish', 'Kapoeta East')
airports_slice = airports_slice.replace('Kokuro', 'Kapoeta South')
airports_slice = airports_slice.replace('Pibor Post', 'Pibor')
airports_slice = airports_slice.replace('Rumbek', 'Rumbek Centre')
                                 
# Merge the data
baseDF = pd.merge(baseDF, airports_slice, on = ['County'], how = 'left')       

# Fill any NAN with 0
baseDF = baseDF.fillna(0)     

# Save the dataframe to CSV
baseDF.to_csv('../20_intermediate/confounding_factors.csv')