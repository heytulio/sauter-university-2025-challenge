from fastapi import FastAPI
from src.routers import bucket
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.include_router(bucket.router)

@app.get("/")
def root():
    """
        Root endpoint to test API availability.

        Returns:
            dict: A simple welcome message.
    """
    return {"message": "Hello, World!"}