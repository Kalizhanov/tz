import logging

from fastapi import FastAPI

from api.balance import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI(title="KMF")
app.include_router(router=router)
