from src.routers import bucket,bq
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import logging
import dotenv
import os

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(default_response_class=ORJSONResponse)

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
