import time
import configparser
import shutil
import os

# var from ini
config = configparser.ConfigParser()
config.read('config.ini')
SBL_DIR = config['execute_con']['SBL_DIR']
SBL_local_tmp = config['execute_con']['SBL_local_tmp']
WORK_DIR = config['execute_con']['WORK_DIR']

#CUST_LOT_ID = "F08BC"
#file_lot_id = "T1N3P002"
#SBL_start_string = SBL_DIR + "\\" + CUST_LOT_ID + "-" + file_lot_id + "-"

data_files = [x[2] for x in os.walk(WORK_DIR)]
for FileName in data_files[0]:
    stringlist = FileName.split("-")
    print(len(stringlist))
