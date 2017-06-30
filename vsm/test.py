
import vsmload
import vsmcalc
import matplotlib.pyplot as plt

from scipy import interpolate
 
#directory = '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/VSM/170509, Co-Al AX3, 17,5 mg, RT run (ProfileData)/'
directory = '/home/nikolaj/Dropbox/Inducat - Mads/VSM data/170614, Co-Al AX7 (60h), 61,55 mg, T-run1-5 (ProfileData)/'




alldata = vsmload.load_directory(directory, index_vals=(24,39), sample_mass_mg = 61.55)

for data in alldata:
    area = vsmcalc.hysteresis_area(data)
    temp = vsmcalc.temperature_average(data)
    print(area, temp)


'''
for i in range(2,50):
    data = vsmload.load_directory(directory, index_vals=i)[0]
    #print(data)
    area = vsmcalc.hysteresis_area(data)
    temp = vsmcalc.temperature_average(data)
    print(area, temp)
'''