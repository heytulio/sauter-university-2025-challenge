from src.adapters.gcs_bucket_adapter import GCSBucketAdapter
from src.services.bucket import BucketService
import os

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

