from src.interfaces.bucket_adapter import IBucketAdapter
from google.cloud.exceptions import GoogleCloudError
from src.core.exceptions.handle_exceptions import GCSAdapterError
from google.cloud import storage
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)

class GCSBucketAdapter(IBucketAdapter):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, file_obj: Path, target_path: str = None):
        try:
            target_path = target_path or file_obj["filename"]
            blob = self.bucket.blob(target_path)

            file_obj["file_obj"].seek(0)
            blob.upload_from_file(
                file_obj["file_obj"],
                rewind=True,
                content_type="application/octet-stream"
            )
        except GoogleCloudError as e:
            logger.error(f"Erro no GCS ao tentar fazer upload para '{target_path}': {e}")
            raise GCSAdapterError(f"Falha no upload para o bucket GCS.") from e

    def list_files(self) -> List[str]:
        try:
            blobs = self.bucket.list_blobs()
            return [blob.name for blob in blobs]
        except GoogleCloudError as e:
            logger.error(f"Erro no GCS ao listar arquivos do bucket '{self.bucket_name}': {e}")
            raise GCSAdapterError("Falha ao listar arquivos do bucket GCS.") from e