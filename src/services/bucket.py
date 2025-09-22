from src.utils.data_utils import list_all_resource_parquet, download_files_ons
from src.core.exceptions.handle_exceptions import DataPipelineError
from src.interfaces.bucket_adapter import IBucketAdapter
from src.core.decorators.logging import log_execution
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class BucketService():
    """
        Manages operations on a cloud storage bucket by acting as a service layer.

        This class provides a high-level interface for interacting with a bucket,
        delegating the low-level tasks to a specific bucket adapter. It ensures 
        that the application's logic is decoupled from the underlying storage 
        technology
    """
    def __init__(self, adapter: IBucketAdapter):
        self.adapter = adapter

    @log_execution
    def mount_pipeline(self):
        try:
            BASE_URL = os.getenv("BASEURL_ONS")
            BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
            PACKAGE_ID = os.getenv("PACKAGE_ID")

            if not BASE_URL or not BUCKET_NAME or not PACKAGE_ID:
                raise ValueError("Configuração de ambiente incompleta.")
            
            ingested_files = False
            start_time = datetime.now() 

            resources = list_all_resource_parquet(BASE_URL, PACKAGE_ID)

            if not self.adapter.list_files(): 
                resources_ons = download_files_ons(resources)
                today = datetime.now()
                for file in resources_ons:
                    folder_name = f"RAW/ONS/PARQUET/{today.year}/{today.month:02}/{today.day:02}/{file['filename']}.parquet"
                    self.adapter.upload_file(file, target_path=folder_name)
                ingested_files = True

            end_time = datetime.now()
            runtime_seconds = (end_time - start_time).total_seconds()

            return {
                "status": "Pipeline executado com sucesso.",
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