# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:49:03 2020

@author: Joseph Littell
"""
# Required Libraries
import pandas as pd

#-------------------#
#                   #
#  Population Data  #
#                   #
#-------------------#

# Read in the population data
population = pd.read_excel('../00_source/population.xlsx')

# Check the data
population.head()

# Select the required columns for our time period
population_slice = population[['Admin_2','Admin_1','LS2011','LS2012','LS2013','LS2014','WP2015']]

# Rename the columns for ease of use
population_slice.columns = ['County', 'State','2011','2012', '2013', '2014', '2015']

# Remove the totals line from the dataset
population_slice = population_slice[population_slice['State'] != 'TOTALS:']

# Ensure the changes were made
population_slice.head()

# Change the orientation to be by county by year
population_melt = population_slice.melt(id_vars=['County', 'State'])
population_melt.columns = ['County', 'State', 'Year', 'Population']

# Determine the yearly population change as a percentage of total population
population_slice['pop_change_2011'] = (population_slice['2011'] - population_slice['2011']) / population_slice['2011']
population_slice['pop_change_2012'] = (population_slice['2012'] - population_slice['2011']) / population_slice['2012']
population_slice['pop_change_2013'] = (population_slice['2013'] - population_slice['2012']) / population_slice['2013']
population_slice['pop_change_2014'] = (population_slice['2014'] - population_slice['2013']) / population_slice['2014']
population_slice['pop_change_2015'] = (population_slice['2015'] - population_slice['2014']) / population_slice['2015']

# save the changes to a new dataframe
population_change = population_slice[['County', 'State','pop_change_2011','pop_change_2012',
                                      'pop_change_2013','pop_change_2014','pop_change_2015']]

# Change the orientation to be by county by year
population_change_melt = population_change.melt(id_vars=['County', 'State'])
population_change_melt.columns = ['County', 'State', 'Year', 'Pop_percent_change']

# Rename the 'Year' column to be proper
population_change_melt["Year"].replace({'pop_change_2011': 2011,
                                        'pop_change_2012': 2012,
                                        'pop_change_2013': 2013,
                                        'pop_change_2014': 2014,
                                        'pop_change_2015': 2015}, 
                                       inplace = True)

# ensure the 'Year' column is integers 
population_melt['Year'] = population_melt['Year'].astype('int64')

# Merge the two dataframes to be Population and Population Change by county by year
population_melt = pd.merge(population_melt, population_change_melt, on= ['County', 'State', 'Year'], how = 'outer')

# Ensure the changes were made
population_melt.head()

#-------------------#
#                   #
#   Conflict Data   #
#                   #
#-------------------#

# Read in the conflict data
conflict = pd.read_csv('../00_source/conflict_data.csv')

# Check the data
conflict.head()

# Select the required columns
conflict_sliced = conflict[['event_date', 'year', 'admin1', 'admin2', 'fatalities']]

# Sum the incidences by location and year
conflict_sliced = conflict_sliced.groupby(['admin1', 'admin2', 'year']).sum()

# Reset the index
conflict_sliced.reset_index(inplace=True)

# Rename the columns to fit Population's style for easier merge
conflict_sliced.columns = ['State','County', 'Year', 'Fatalities']

# Recheck the Data to ensure the transformations are complete
conflict_sliced.head()
conflict_sliced = conflict_sliced.replace("Kajo-Keji","Kajo-keji")
conflict_sliced = conflict_sliced.replace("Raja","Raga")
#------------------#
#                  #
#    Merge Data    #
#                  #
#------------------#

pop_fatalities = pd.merge(population_melt, conflict_sliced, on = ['County', 'State', 'Year'], how = "left")

# Since there are numerous locations that did not see violence every year, we are filling the nan values with zero
pop_fatalities['Fatalities'] = pop_fatalities['Fatalities'].fillna(0)

# Calculate Intensity
pop_fatalities["intensity"] = (pop_fatalities['Fatalities'] / pop_fatalities['Population']) * 10000

# Save the dataframe to a CSV file
pop_fatalities.to_csv('../20_intermediate/pop_fatalities.csv')
