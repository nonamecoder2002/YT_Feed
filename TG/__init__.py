import logging

import os, shutil

if os.path.exists('./Temp'):
    shutil.rmtree('./Temp')
    os.mkdir('./Temp')

else:

    os.mkdir('./Temp')

logging.basicConfig(
    filename='./Temp/logs.txt',
    level=logging.INFO,
    filemode='w',
    format='%(levelname)s-->%(asctime)s:|%(name)s|: %(message)s'

)

logger = logging.getLogger(__name__)

