import logging
from datetime import datetime
import os
import pandas as pd

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
format="[%(asctime)s]-%(levelname)s-[%(lineno)s]-[%(filename)s]-[%(funcName)s]-%(message)s",
level=logging.INFO
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("-"))

    log_df =pd.DataFrame(data)
    columns=["Time_stamp","Log_level","Line_no","File_name","Function_name","Message"]
    log_df.columns=columns
    log_df["log_message"] = log_df['Time_stamp'].astype(str)+":$"+log_df["Message"]
    return log_df[["log_message"]]