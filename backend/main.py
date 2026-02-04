from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from services.postal import postal_check
from services.onemap import get_onemap_data
from services.classifier import classify_postal

FRONTEND = os.getenv("FRONTEND", "")
origins = [o.strip() for o in FRONTEND.split(",") if o.strip()]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def root(postal: str):
    try:
        postal_check(postal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        data = get_onemap_data(postal)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach OneMap")

    kind = classify_postal(data)

    results = data.get("results") or []
    address = results[0].get("ADDRESS") if results else None

    return {"postal": postal, "type": kind, "address": address}