from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from .api.basket import router as basket_router
from .api.upload import router as upload_router
from .api.chat import router as chat_router
from .api.chart import router as chart_router

app = FastAPI(title="CSV Graph Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basket_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(chart_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
