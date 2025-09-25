from apscheduler.schedulers.background import BackgroundScheduler
from src.utils.data_utils import schedule_ingestion
from src.adapters.gcs_bucket_adapter import GCSBucketAdapter
from fastapi.responses import ORJSONResponse
from src.routers import bucket,bq
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.services.bucket import BucketService
import logging
import dotenv
import os

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    adapter = GCSBucketAdapter(os.getenv("GCP_BUCKET_NAME"))
    service = BucketService(adapter)
    schedule_ingestion(scheduler=scheduler,service=service)
    scheduler.start()
    logging.info("Scheduler iniciado com job de ingestão de dados todos os dias as 00:00.")

    yield  

    scheduler.shutdown()
    logging.info("Scheduler parado.")


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)


app.include_router(bucket.router)
app.include_router(bq.router)


@app.get("/")
def root():
    """
        Root endpoint to test API availability.

        Returns:
            dict: A simple welcome message.
    """
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
