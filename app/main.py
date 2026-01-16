from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RC Fraud Detection API",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "running"}
