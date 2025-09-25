from requests.exceptions import RequestException, JSONDecodeError
from src.core.exceptions.handle_exceptions import ONSApiError
from src.core.decorators.logging import log_execution
from src.interfaces.bucket_adapter import IBucketAdapter
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from typing import List
import pandas as pd
import requests
import logging
import io
import re

logger = logging.getLogger(__name__)

def download_files_ons(resources: List[dict]) -> List[dict]:
    download_files = []
    for resource in resources:
        try:
            file_url_download = resource['url']
            resp = requests.get(file_url_download, stream=True, timeout=30) 
            resp.raise_for_status()

            file_content = io.BytesIO()
            for chunk in resp.iter_content(chunk_size=8192):
                file_content.write(chunk)
            file_content.seek(0)

            download_files.append({
                "filename": resource['name'],
                "file_obj": file_content
            })

            logger.info(f"File downloaded: {resource['name']} .")
        except RequestException as e:
            raise ONSApiError(f"Não foi possível baixar o arquivo: {resource['name']}.") from e

    return download_files

@log_execution
def list_all_resource_parquet(
        base_url: str,
        packageId: str,
        start_year: int = 2000,
        end_year: int = date.today().year
    ) -> List[dict]:
    resources = []
    try:
        resp = requests.get(f"{base_url}/package_show", params={"id": packageId})
        resp.raise_for_status()
        data = resp.json()
        
        for resource in data['result']['resources']:
            if str(resource['format']).upper() == "PARQUET":   #TODO adicionar .env  
                match = re.search(r"(\d{4})", resource["name"])
                if match:
                    resource_year = int(match.group(1))
                    if start_year <= resource_year <= end_year:
                        resources.append({
                            "id": resource['id'],
                            "name": resource['name'],
                            "url": resource['url'],
                        })
        return resources
    
    except RequestException as e:
        raise ONSApiError("Falha ao comunicar com a API do ONS para listar recursos.") from e
    
    except JSONDecodeError as e:
        raise ONSApiError("Resposta inválida (não-JSON) da API do ONS.") from e
        
    except KeyError as e:
        raise ONSApiError("Formato de resposta inesperado da API do ONS.") from e

def convert_parquet_columns_string(file_obj: io.BytesIO) -> io.BytesIO:
    df = pd.read_parquet(file_obj)
    df = df.astype(str)
    file_out = io.BytesIO()
    df.to_parquet(file_out, index=False)
    file_out.seek(0)
    return file_out

def build_folder_name(bucket_path: str, filename: str, ingest_date: date = None) -> str:
    ingest_date = ingest_date or date.today()
    filename = str(filename).lower()
    return f"{bucket_path}/dt={ingest_date.year}-{ingest_date.month:02}-{ingest_date.day:02}/{filename}.parquet"

def needs_ingestion(folder_name: str, bucket_files: list, start_year: int, end_year: int) -> bool:
    today_year = date.today().year
    return folder_name not in bucket_files or (start_year == end_year == today_year)

def ingest_and_upload(adapter: IBucketAdapter, resources: list, folder_name: str):
    for resource in resources:
        resource["file_obj"] = convert_parquet_columns_string(resource["file_obj"])
        adapter.upload_file(resource, folder_name)

def schedule_ingestion(scheduler: BackgroundScheduler, service):
    today = date.today()
    scheduler.add_job(
        service.mount_pipeline,  
        trigger="cron",
        hour=0,
        minute=0,
        args=[today.year, today.year]
    )