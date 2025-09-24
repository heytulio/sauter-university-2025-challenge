from abc import ABC, abstractmethod
from typing import Optional
from datetime import date

class ITableRepository(ABC):
    
    @abstractmethod
    def fetch_page(self, table: str, limit: int, offset: int,filter_date: Optional[date] = None) -> list[dict]:
        pass

    def run_transformations(self):
        pass