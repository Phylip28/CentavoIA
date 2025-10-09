from fastapi import FastAPI
from controllers import analysis_controller

app = FastAPI(
    title="Centavo IA - Analysis Module",
    version="1.0"
)

app.include_router(analysis_controller.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Analysis Module Server is up and running."}