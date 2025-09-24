from src.adapters.gcs_bucket_adapter import GCSBucketAdapter
from src.services.bucket import BucketService
from src.adapters.bq_bucket_adapter import BigQueryTableAdapter
from src.services.bigquery import ReservatorioService
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
    dotenv.load_dotenv()
    
    adapter = BigQueryTableAdapter()
    return ReservatorioService(adapter, table="sauter-university-desafio.ons_dataset.dados_ons_transformado") #TODO adicionar ao .env