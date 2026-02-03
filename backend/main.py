from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.postal import postal_check
from services.onemap import get_onemap_data
from services.classifier import classify_postal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root(postal):
    try:
        postal_check(postal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    try:
        data = get_onemap_data(postal)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach OneMap")

    if not data:
        raise HTTPException(status_code=502, detail="No response from OneMap")

    try:
        kind = classify_postal(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to classify postal")

    return {"postal": postal, "type": kind}