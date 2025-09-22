from requests.exceptions import RequestException, JSONDecodeError
from src.core.exceptions.handle_exceptions import ONSApiError
from src.core.decorators.logging import log_execution
from typing import List
import requests
import logging
import io

logger = logging.getLogger(__name__)

@log_execution
def download_files_ons(resources: List[dict]) -> List[dict]:
    """
        Downloads files from a list of ONS resources.

        Iterates through a list of resource dictionaries, downloads the file content 
        for each, and stores it in memory. It handles file downloading in chunks 
        to manage large files efficiently.

        Args:
            resources (List[dict]): A list of dictionaries, where each dictionary
                                    contains metadata about a file to be downloaded,
                                    including its 'url' and 'name'.

        Returns:
            List[dict]: A list of dictionaries, each containing the downloaded 
                        file content as a BytesIO object ('file_obj') and its 
                        original name ('filename').
    """
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
def list_all_resource_parquet(base_url: str, packageId: str) -> List[dict]:
    """
        Retrieves a list of all resources with a 'PARQUET' format from a ONS API package.

        This function queries a ONS API endpoint to get a package's metadata. It
        then filters the resources within that package to find and return only those 
        in the Parquet file format.

        Args:
            base_url (str): The base URL of the ONS API.
            packageId (str): The ID of the ONS package to query.

        Returns:
            List[dict]: A list of dictionaries, where each dictionary represents 
                        a Parquet resource and contains its 'id', 'name', and 'url'.
    """
    resources = []
    try:
        resp = requests.get(f"{base_url}/package_show", params={"id": packageId})
        resp.raise_for_status()
        data = resp.json()
        for resource in data['result']['resources']:
            if resource['format'].upper() == "PARQUET":
                resource_id = resource['id']
                resources_name = resource['name']
                resources_url = resource['url']
                resources.append({
                    "id": resource_id,
                    "name": resources_name,
                    "url": resources_url
                })
        return resources
    
    except RequestException as e:
        raise ONSApiError("Falha ao comunicar com a API do ONS para listar recursos.") from e
    
    except JSONDecodeError as e:
        raise ONSApiError("Resposta inválida (não-JSON) da API do ONS.") from e
        
    except KeyError as e:
        raise ONSApiError("Formato de resposta inesperado da API do ONS.") from e