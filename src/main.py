from fastapi import FastAPI
from src.routers import bucket
import logging
import dotenv
import os

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
