from src.utils.data_utils import (
    list_all_resource_parquet,
    download_files_ons,
    ingest_and_upload,
    build_folder_name,
    needs_ingestion
    )
from src.core.exceptions.handle_exceptions import DataPipelineError
from src.interfaces.bucket_adapter import IBucketAdapter
from src.core.decorators.logging import log_execution
from datetime import datetime,date
import logging
import os

logger = logging.getLogger(__name__)

class BucketService():
    def __init__(self, adapter: IBucketAdapter):
        self.adapter = adapter

    # @log_execution
    # def mount_pipeline(self, start_year: int = 2000, end_year: int = date.today().year):
    #     try:
    #         BASE_URL = os.getenv("BASEURL_ONS")
    #         BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
    #         PACKAGE_ID = os.getenv("PACKAGE_ID")
    #         BUCKET_PATH = os.getenv("BUCKET_PATH")

    #         if not BASE_URL or not BUCKET_NAME or not PACKAGE_ID:
    #             raise ValueError("Configuração de ambiente incompleta.")
            
    #         ingested_files = False
    #         start_time = datetime.now() 

    #         resources = list_all_resource_parquet(BASE_URL, PACKAGE_ID, start_year, end_year)

    #         resources_bucket = self.adapter.list_files()   
            
    #         today = date.today()

    #         for resource in resources:
    #             filename = f"{str(resource['name']).lower()}.parquet"
    #             folder_name = f"{BUCKET_PATH}/dt={today.year}-{today.month:02}-{today.day:02}/{filename}"

    #             must_ingest = (
    #                 folder_name not in resources_bucket or 
    #                 (start_year == end_year == today.year)
    #             )

    #             if must_ingest:
    #                 resources_ons = download_files_ons([resource])
    #                 for file in resources_ons:
    #                     file["file_obj"] = convert_parquet_columns_string(file["file_obj"])
    #                     self.adapter.upload_file(file, folder_name)
    #                     ingested_files = True

    #         end_time = datetime.now()
    #         runtime_seconds = (end_time - start_time).total_seconds()

    #         return {
    #             "status": "Pipeline executed successfully.",
    #             "ingested_files": ingested_files,
    #             "bucket": BUCKET_NAME,
    #             "runtime": str(runtime_seconds)
    #         }

    #     except DataPipelineError as e:
    #         return {    
    #             "status": "Pipeline falhou.",
    #             "error": str(e)
    #         }
    #     except Exception as e:
    #         return {
    #             "status": "Pipeline falhou.",
    #             "error": str(e)
    #         }

    @log_execution
    def mount_pipeline(self, start_year: int = 2000, end_year: int = date.today().year):
        try:
            BASE_URL = os.getenv("BASEURL_ONS")
            BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
            PACKAGE_ID = os.getenv("PACKAGE_ID")
            BUCKET_PATH = os.getenv("BUCKET_PATH")

            if not BASE_URL or not BUCKET_NAME or not PACKAGE_ID:
                raise ValueError("Configuração de ambiente incompleta.")
            
            ingested_files = False
            start_time = datetime.now() 

            resources = list_all_resource_parquet(BASE_URL, PACKAGE_ID, start_year, end_year)
            resources_bucket = self.adapter.list_files()   
            today = date.today()

            for resource in resources:
                folder_name = build_folder_name(BUCKET_PATH, resource['name'], today)

                if needs_ingestion(folder_name, resources_bucket, start_year, end_year):
                    resources_ons = download_files_ons([resource])
                    ingest_and_upload(self.adapter, resources_ons, folder_name)
                    ingested_files = True

            end_time = datetime.now()
            runtime_seconds = (end_time - start_time).total_seconds()

            return {
                "status": "Pipeline executed successfully.",
                "ingested_files": ingested_files,
                "bucket": BUCKET_NAME,
                "runtime": str(runtime_seconds)
            }

        except DataPipelineError as e:
            return {    
                "status": "Pipeline falhou.",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "Pipeline falhou.",
                "error": str(e)
            }