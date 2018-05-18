
import os
import shutil

WORK_DIR = 'issues_raw'

for item in os.listdir(WORK_DIR):
    print(os.sep.join([WORK_DIR, item]))
    folder_name = item.split('_')[0]
    os.makedirs(os.sep.join([WORK_DIR, folder_name]), exist_ok=True)
    shutil.move(os.sep.join([WORK_DIR, item]), os.sep.join([WORK_DIR, folder_name, item]))