from src.adapters.gcs_bucket_adapter import GCSBucketAdapter
from src.services.bucket import BucketService
from src.adapters.bq_bucket_adapter import BigQueryTableAdapter
from src.services.bigquery import ReservatorioService
from fastapi import HTTPException
import os
import dotenv

def get_bucket_service() -> BucketService:
    """
    Initializes and returns a BucketService instance for interacting with a Google Cloud Storage bucket.

    This function is a dependency injector that simplifies the process of 
    getting a properly configured service object for bucket operations.

    Returns:
        BucketService: An instance of BucketService ready for use.
    """
    adapter = GCSBucketAdapter(os.getenv("GCP_BUCKET_NAME"))
    return BucketService(adapter)



def get_bq_service() -> BucketService:

    PROJECT_ID = os.getenv("PROJECT_ID")
    GCP_DATASET_NAME = os.getenv("GCP_DATASET_NAME")
    GCP_TABLE_NAME = os.getenv("GCP_TABLE_NAME")

    # if not PROJECT_ID or not GCP_DATASET_NAME or not GCP_TABLE_NAME:
    #     raise HTTPException(
    #             status_code=400,
    #             detail="Configuração de ambiente incompleta Base URL, Project ID e Package ID."
    #         )    

    adapter = BigQueryTableAdapter()
    return ReservatorioService(adapter, table="{}.{}.{}".format(PROJECT_ID, GCP_DATASET_NAME, GCP_TABLE_NAME))
