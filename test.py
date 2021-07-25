
from requests import get

import wget
# for num in range(1,8):
#     filename = 'vehicle.csv000{0}_part_00.gz'.format(num)
#     wget.download(test+filename,'/home/swati.singh/Data/carnext-data-engineering-assignment/test-data/{0}'.format(filename))


import subprocess
def run_cmd(args_list):
    """
    run linux commands
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err

import os
run_cmd(['hadoop', 'fs', '-put', '/home/swati.singh/Data/carnext-data-engineering-assignment/test-data/', '/user/swati.singh/carnext-data-engineering-assignment/'])
