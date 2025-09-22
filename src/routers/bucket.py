from fastapi import APIRouter, Depends
from src.core.factory.providers import get_bucket_service
from src.services.bucket import BucketService

router = APIRouter(
    prefix="/bucket",
    tags=["bucket"]
)

@router.post("/")
def mount_pipeline(bucket_service: BucketService = Depends(get_bucket_service)):
    return bucket_service.mount_pipeline()