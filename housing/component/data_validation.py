

from housing.exception import HousingException
from housing.logger import logging
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import json
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard.tabs import DataDriftTab
from evidently.dashboard import Dashboard
from housing.util.util import read_yaml_file
from housing.constant import DATASET_SCHEMA_COLUMNS_KEY, DOMAIN_VALUE_KEY,OCEAN_PROXIMITY_KEY
from collections import Counter

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}\n\n")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e 

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path) 

            is_available =  is_test_file_exist and is_train_file_exist
            logging.info(f"Is train and test file exists?->{is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file:{training_file} or Testing file: {testing_file}" \
                            "is not present"
                raise Exception(message)    
            
            return is_available

        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status=False
            # validate training and testing dataset using schema file
            train_df,test_df=self.get_train_and_test_df() 
            #1. checking number of columns in training dataset 
            chk1 = self.check_length_column(train_df)              
            logging.info(f"Number of columns in training dataset match with the schema:{chk1}")
           
            chk2 = self.check_length_column(test_df)
            logging.info(f"Number of columns in testing dataset match with the schema:{chk2}")
           
                       
           
            #2. Check the value of ocean proximity 
            # acceptable values     <1H OCEAN
            # INLAND
            # ISLAND
            # NEAR BAY
            # NEAR OCEAN
            #training dataset
            chk3= self.check_ocean_proximity_values(train_df)
            logging.info(f"Ocean proximity values in training dataset match with the schema:{chk3}")

            chk4= self.check_ocean_proximity_values(train_df)
            logging.info(f"Ocean proximity values in testing dataset match with the schema:{chk4}")

            #3. Check column names in training dataset
            chk5= self.check_column_names(train_df)
            logging.info(f"all columns in training dataset are correct: {chk5}")

            chk6= self.check_column_names(test_df)
            
            logging.info(f"all columns in testing dataset are correct: {chk6}")
            

            if (chk1 and chk2 and chk3 and chk4 and chk5 and chk6) is False:
                validation_status =False
                raise Exception(f"data is not valid")

            else:
                validation_status =True
              
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def check_ocean_proximity_values(self,df:pd.DataFrame)->bool:
        try:
            schema = read_yaml_file(self.data_validation_config.schema_file_path)
            ocean_proximity_values_df = list(Counter(df[OCEAN_PROXIMITY_KEY]).keys())
            logging.info(f"values of ocean df :[{ocean_proximity_values_df}]")
            ocean_proximity_values_schema = schema[DOMAIN_VALUE_KEY][OCEAN_PROXIMITY_KEY]
            logging.info(f"values of ocean schema :[{ocean_proximity_values_schema}]")
            validation_status = all(val in ocean_proximity_values_df for val in ocean_proximity_values_schema)
            
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e


    def check_length_column(self,df:pd.DataFrame)->bool:
        try:
            schema = read_yaml_file(self.data_validation_config.schema_file_path)
            if len(df.columns)==len(schema[DATASET_SCHEMA_COLUMNS_KEY].keys()):
                validation_status = True
            else:
                validation_status=False
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e

    def check_column_names(self,df:pd.DataFrame)->bool:
        try:
            schema = read_yaml_file(self.data_validation_config.schema_file_path)
            columns_names = list(df.columns)
            
            for col in columns_names:
                if col not in list(schema[DATASET_SCHEMA_COLUMNS_KEY].keys()):
                    logging.info(f"{col} not in the dataset")
                    validation_status=False
                    break
                else:
                    validation_status = True         
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)
            

            report_page_file_path = self.data_validation_config.report_page_file_path

            report_page_dir = os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df=self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path

            report_dir = os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)    

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            return report    

        except Exception as e:
            raise HousingException(e,sys) from e
    
    
    
    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact=DataValidationArtifact(
                                    schema_file_path=self.data_validation_config.schema_file_path,
                                    report_file_path=self.data_validation_config.report_file_path,
                                    report_page_file_path=self.data_validation_config.report_page_file_path,
                                    is_validated=True,
                                    message="Data Validation performed successfully")
            logging.info(f"Data validation artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e 

    def __del__(self):
        logging.info(f"{'='*20}Data Validation log completed.{'='*20}\n\n")        