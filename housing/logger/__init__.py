import logging
from datetime import datetime
import os

#Log directory name
LOG_DIR="housing_logs"

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
#Log filename
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

#Making Log directory
os.makedirs(LOG_DIR,exist_ok=True)

#Creating log file path
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME) 

#creating log file with level info
logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format="[%(asctime)s] - %(name)s- %(levelname)s-%(message)s",
level=logging.INFO
)