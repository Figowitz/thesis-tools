# -*- coding: utf-8 -*-
""" Tools for making calculations on VSM dataframes, specifically hysteresis curves """


import numpy as np
import re

import matplotlib.pyplot as plt
import vsmload


def area_between_curves(curve1, curve2, method='trapz'):
    """
    Calculates area between two curves with different x values.
    x1, y1 and x2,y2 should be lists of coordinates for each curve
    TODO: Add keyword for integration method for possible performance gains
    """
    x1, y1 = curve1
    x2, y2 = curve2
    if method == 'trapz':
        # Add most negative value to ensure integral stays positive for all points
        y1 = y1+abs(min(y1))
        y2 = y2+abs(min(y2))
        
        # Integrate each function separately
        y1_int = abs(np.trapz(y1, x=x1))
        y2_int = abs(np.trapz(y2, x=x2))
        
        # The area between curves is the absolute value of their difference
        area = abs(y1_int-y2_int)
    
    return area

def split_hyst_curve(x, y):
    """
    Splits hysteresis curve into a top and bottom part.
    x and y are pandas dataseries, i.e. what you get when using x = data['B']
    on a pandas dataframe.
    TODO: Support other datatypes (list, numpy array) (the idxmin() function only works with pandas)
    """
    idx_min = x.idxmin()
    
    x1 = x[0:idx_min+1]
    y1 = y[0:idx_min+1]
    
    x2 = x[idx_min:]
    y2 = y[idx_min:]
    
    idx1_max = x1.idxmax()
    idx2_max = x2.idxmax()

    if idx1_max > idx2_max:
        x1[0] = x2[-1]
        y1[0] = y2[-1]
    else:
        x2[-1] = x1[0]
        y2[-1] = y1[0]
        
    curve1 = (x1, y1)
    curve2 = (x2, y2)

    return curve1, curve2

def extract_columns(dataframe):
    """
    Recognises the columns of a dataset and returns each as individual columns
    """
    columns = dataframe.columns
    field = None
    moment = None
    temperature = None
    
    
    for column in columns:
        if re.search('\AField', column) or re.search('\AB(?!\w)\(?', column):
            # If column starts with "Field" or "B" possibly followed by parenthesis with units ( )
            field = dataframe[column]
            
        elif re.search('\AMoment', column) or re.search('\Am(?!\w)\(?', column):
            # If column starts with "Moment" or "m" possibly followed by parenthesis with units ( )
            moment = dataframe[column]
            
        elif re.search('\ATemp', column) or re.search('\AT(?!\w)\(?', column):
            temperature = dataframe[column]
            
    return field, moment, temperature
    
    
def hysteresis_area(dataframe):
    
    field, moment, _ = extract_columns(dataframe)
    curve1, curve2 = split_hyst_curve(field, moment)
    area = area_between_curves(curve1, curve2)
    
    return area

def temperature_average(dataframe):
    _, _, temperature = extract_columns(dataframe)
    
    temperature = temperature.mean()
    
    return temperature

#directory = '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/VSM/170509, Co-Al AX3, 17,5 mg, RT run (ProfileData)/'
#data = vsmload.load_directory(directory, index_vals='last')[0]
#print(data)
#field, moment, _ = extract_columns(data)
#c1, c2 = split_hyst_curve(field, moment)
#plt.plot(field, moment)
#plt.plot(c1[0], c1[1], 'k-')
#plt.plot(c2[0], c2[1], 'r-')
#plt.show()