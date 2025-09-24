from src.interfaces.bq_adapter import ITableRepository
from typing import List, Dict, Optional 
from google.cloud import bigquery
from src.core.exceptions.handle_exceptions import BQAdapterError
from datetime import date

class BigQueryTableAdapter(ITableRepository):
    def __init__(self):
        self.client = bigquery.Client()

    def fetch_page(self, table: str, limit: int, offset: int, filter_date: Optional[date] = None) -> List[Dict]:
        query = f"SELECT * FROM `{table}`"
        count_query = f"SELECT COUNT(*) FROM `{table}`"

        if filter_date:
            query += " WHERE data_ear = @filter_date"
            count_query += " WHERE data_ear = @filter_date"

        query += f" LIMIT {limit} OFFSET {offset}"

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("filter_date", "DATE", filter_date)
            ] if filter_date else []
        )

        try:
            results = self.client.query(query, job_config=job_config).result()
            count_results = self.client.query(count_query, job_config=job_config).result()

            total_rows = [row[0] for row in count_results][0]

            return [dict(row.items()) for row in results], total_rows
        except Exception as e:
            raise RuntimeError(f"Erro ao consultar BigQuery: {e}")
        
        except Exception as e:
            raise RuntimeError(f"Adapter erro ao consultar BigQuery: {e}")