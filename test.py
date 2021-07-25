
from requests import get

import wget
# for num in range(1,8):
#     filename = 'vehicle.csv000{0}_part_00.gz'.format(num)
#     wget.download(test+filename,'/home/swati.singh/Data/carnext-data-engineering-assignment/test-data/{0}'.format(filename))



import os
run_cmd(['hadoop', 'fs', '-put', '/home/swati.singh/Data/carnext-data-engineering-assignment/test-data/', '/user/swati.singh/carnext-data-engineering-assignment/'])
