#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Often used tools and functions for handling XRD data, e.g. curve fitting, averaging multiple patterns etc"""

import numpy as np
from scipy.optimize import curve_fit


def gaussian(x, *p):
    A, mu, sigma, B = p
    
    return A*np.exp(-(x-mu)**2 / (2*sigma**2)) + B


"""
# Try fitting a gaussian
patterns = xload.load_patterns(dir_1pct, smoothing=3)

angle = np.array(patterns[0]['Angle'])
intensity = np.array(patterns[0]['Intensity'])

FWHM = 0.5
sigma = FWHM/(2*np.sqrt(np.log(4)))
p0 = [1000 , 65, sigma, 1600]

# Only fit relevant part of angles
x1, x2 = 63, 67
condition = (angle>x1) & (angle<x2)

# Curve fit
popt, pcov = curve_fit(xtools.gaussian, angle[condition], intensity[condition], 
                       p0=p0)

# Plot data and fit
plt.plot(angle, intensity)
plt.plot(angle[condition], xtools.gaussian(angle[condition], *popt))
#plt.plot(angle, xtools.gaussian(angle, *p0))
plt.show()

"""

"""
angle = np.array(patterns[0]['Angle'])
intensity = np.array(patterns[0]['Intensity'])

indexes = peakutils.indexes(intensity, thres=0.5, min_dist=30)  # Find index of peaks
indexes = peakutils.interpolate(angle, intensity, ind=indexes)   # Improve with interpolation


"""