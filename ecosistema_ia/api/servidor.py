"""Small FastAPI server exposing SPS and dataset endpoints."""

from fastapi import FastAPI
from .endpoints import router as api_router

app = FastAPI(title="Mimir SPS API")
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "SPS API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
