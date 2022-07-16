
from housing.component import data_validation, model_trainer
from housing.component import data_transformation
from housing.component.model_pusher import ModelPusher
from housing.config.configuration import Configuartion
from housing.logger import logging
from housing.exception import HousingException

from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact,\
    DataValidationArtifact, ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evaluation import ModelEvaluation
import os,sys

class Pipeline:
    def __init__(self,config:Configuartion = Configuartion())->None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(
                        data_ingestion_config=self.config.get_data_ingestion_config()
                        )

            return data_ingestion.initiate_data_ingestion()
        
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)\
    ->DataValidationArtifact:
        try:
            data_validation = DataValidation(
                            data_validation_config=self.config.get_data_validation_config(),
                            data_ingestion_artifact= data_ingestion_artifact)

    
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_data_transformation(self,
                                data_ingestion_artifact:DataIngestionArtifact,
                                data_validation_artifact:DataValidationArtifact
                                )->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                           data_ingestion_artifact=data_ingestion_artifact,
                           data_validation_artifact=data_validation_artifact)
            
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_trainer(self,
                        data_transformation_artifact:DataTransformationArtifact,
                        )->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                        model_trainer_config=self.config.get_model_trainer_config(),
                        data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer.initiate_model_trainer()        
        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_evaluation(self,data_ingestion_artifact:DataIngestionArtifact,
                            data_validation_artifact:DataValidationArtifact,
                            model_trainer_artifact:ModelTrainerArtifact
                            )->ModelEvaluationArtifact:
        try:
            model_eval =    ModelEvaluation(
                            model_evaluation_config= self.config.get_model_evaluation_config(),
                            data_ingestion_artifact= data_ingestion_artifact,
                            data_validation_artifact=data_validation_artifact,
                            model_trainer_artifact= model_trainer_artifact)
            return model_eval.initiate_model_evaluation()

        except Exception as e:
            raise HousingException(e,sys) from e

    def start_model_pusher(self,
                    model_eval_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.config.get_model_pusher_config(),
                model_evaluation_artifact=model_eval_artifact
                )
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise HousingException(e,sys) from e

    def run_pipeline(self):
        try:
            #data ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            #data validation
            data_validation_artifact= self.start_data_validation(
                                    data_ingestion_artifact=data_ingestion_artifact)

            #data transformation
            data_transformation_artifact=self.start_data_transformation(
                        data_ingestion_artifact=data_ingestion_artifact,
                        data_validation_artifact=data_validation_artifact)

            #model training
            model_trainer_artifact=self.start_model_trainer(
                        data_transformation_artifact=data_transformation_artifact)

        except Exception as e:
            raise HousingException(e,sys) from e