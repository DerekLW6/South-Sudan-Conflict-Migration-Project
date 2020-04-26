# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:29:50 2020

@author: Joseph Littell
"""

# Libraries Required
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols
from linearmodels import PanelOLS

# Read in Data
conflict = pd.read_csv('./../20_intermediate/confounding_factors.csv')
del conflict['Unnamed: 0']
del conflict['Unnamed: 0.1']

# Create indicator variables for Difference in Difference
conflict["PostConflict"] = conflict['Year'].apply(lambda x : 1 if x >= 2014 else 0)
conflict['Treated'] = conflict['intensity'].apply(lambda x : 1 if x > 1 else 0)

# Conduct base Difference in Difference
BaseModel = smf.ols("Pop_percent_change ~ Treated * PostConflict ", data = conflict).fit()
print(BaseModel.summary())

# Difference in Difference with Confounding Factors
CFModel = smf.ols("Pop_percent_change ~ Treated * PostConflict + Hospitals + Population_Percent_Child + Population_Percent_Female + Poverty_Rate + Airport", data = conflict).fit()
print(CFModel.summary())

# Difference in Difference by County
CountyModel = smf.ols("Pop_percent_change ~ C(County) + Treated * PostConflict", data = conflict).fit()
print(CountyModel.summary())

# Panel OLS 
conflict = conflict.set_index(['County','Year'])
PanelModel = PanelOLS.from_formula('Pop_percent_change ~ Treated * PostConflict + EntityEffects', data = conflict,
                           drop_absorbed=True)
PanelModel.fit(cov_type = 'clustered', cluster_entity = True)
