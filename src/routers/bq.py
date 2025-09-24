from fastapi import APIRouter, Depends
from src.core.factory.providers import get_bq_service
from src.services.bigquery import ReservatorioService
from datetime import date
from typing import Optional

router = APIRouter(
    prefix="/bq",
    tags=["BIGQUERY"]
)

@router.get("/")
def get_bq_service_data(
    bq_service: ReservatorioService = Depends(get_bq_service),
    page: int = 1, 
    page_size: int = 50,
    date: Optional[date] = None
):
    return bq_service.get_paginated(page=page, page_size=page_size, filter_date=date)