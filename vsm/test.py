
import vsmload
import vsmcalc
import matplotlib.pyplot as plt

from scipy import interpolate
 
directory = '/home/nikolaj/Dropbox/DTU/12. semester/Speciale/data/VSM/170509, Co-Al AX3, 17,5 mg, RT run (ProfileData)/'


alldata = vsmload.load_directory(directory, index_vals='all')

#print(alldata)

for data in alldata:
    area = vsmcalc.hysteresis_area(data)
    print(area)


