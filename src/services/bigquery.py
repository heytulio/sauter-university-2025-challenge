from src.interfaces.bq_adapter import ITableRepository
from typing import List, Dict, Optional
from datetime import date
from src.core.exceptions.handle_exceptions import BQServiceError, BQAdapterError

class ReservatorioService:
    def __init__(self, repository: ITableRepository, table: str):
        self.repository = repository
        self.table = table

    def get_paginated(self, page: int, page_size: int = 50, filter_date: Optional[date] = None) -> List[Dict]:
        try:
            offset = (page - 1) * page_size
            date_to_filter = filter_date.isoformat() if filter_date else None
        
            results, total_rows = self.repository.fetch_page(self.table, page_size, offset, date_to_filter)
        
            total_pages = (total_rows + page_size - 1) // page_size

            return {
                "results": results,
                "total_pages": total_pages,
                "total_rows": total_rows,
                "current_page": page,
                "page_size": page_size,
            }
        
        except BQAdapterError as e:
            raise BQServiceError(f"Erro no adaptador BigQuery: {e}") from e
        except Exception as e:
            raise BQServiceError(f"Erro ao consultar BigQuery: {e}")
        
