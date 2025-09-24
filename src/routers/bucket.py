from fastapi import APIRouter, Depends, Body
from src.core.factory.providers import get_bucket_service
from src.services.bucket import BucketService
from src.schemas.bucket import YearRange

router = APIRouter(
    prefix="/bucket",
    tags=["BUCKET"]
)

@router.post("/")
def mount_pipeline(
    bucket_service: BucketService = Depends(get_bucket_service),
    date: YearRange = Body(...),
    ):
    
    return bucket_service.mount_pipeline(
        start_year=date.start_year,
        end_year=date.end_year
    )   