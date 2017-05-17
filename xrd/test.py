#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xload
import xplot
import xtools

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
from scipy.optimize import curve_fit

dirs_9hr = {'raw':  '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-03-23_Co-Al_powder_700C_1pctO2/',
            '1pct': '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-03-23_Co-Al_powder_700C_1pctO2/',
            '0pct': '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-04-04_Co-Al_powder_700C_0pctO2/',
            '4pct': '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-03-24_Co-Al_powder_700C_4pctO2/',
            '20pct':'/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-04-06_Co-Al_powder_700C_20pctO2/'}

dirs_60hr = {'0pct': '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-04-07_Co-Al_powder_700C_40hr_He_annealing/',
             '1pct': '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-04-09_Co-Al_powder_700C_18hr_1pctO2/'}


#filenames = xload.match_files(directory, 
#                               I_range=[0,100],
#                               include_string='120m_scan')

patterns = dict()
plt.figure()

for key in dirs_9hr:
    directory = dirs_9hr[key]
    pattern = xload.load_patterns(directory, I_range=[10, 100], smoothing=3, include_string='120m_scan')
    print(key)
    patterns[key] = pattern


print(patterns['1pct'])

"""
#######################################################
# Plot many 30m scans
dir_40hr_anneal = '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/XRD XPert pro/2017-04-09_Co-Al_powder_700C_18hr_1pctO2/'

patterns_40hr = xload.load_patterns(dir_40hr_anneal, include_string='30m_scan')

cmap = cm.get_cmap('cool')

for i, pattern in enumerate(patterns_40hr):
    angle = pattern['Angle']
    intensity = pattern['Intensity']
    
    color = cmap(i/len(patterns_40hr))
    plt.plot(angle, intensity, color=color)

plt.show()
"""