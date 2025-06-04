"""Small FastAPI server exposing SPS endpoints."""

from fastapi import FastAPI
from .endpoints import router as sps_router

app = FastAPI(title="Mimir SPS API")
app.include_router(sps_router)


@app.get("/")
def root():
    return {"message": "SPS API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
