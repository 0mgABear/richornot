from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from services.postal import postal_check
from services.onemap import get_onemap_data
from services.hdb import get_hdb_resale
from services.hdb_inventory import get_hdb_inventory_record


FRONTEND = os.getenv("FRONTEND", "")
origins = [o.strip() for o in FRONTEND.split(",") if o.strip()]
origins += ["http://localhost:3000", "http://127.0.0.1:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


_NON_RES_KWS = [
    "TOWER", "OFFICE", "MALL", "PLAZA", "CENTRE", "CENTER", "COMPLEX",
    "HOTEL", "HOSPITAL", "CLINIC", "SCHOOL", "COLLEGE", "UNIVERSITY",
    "MRT", "STATION", "INTERCHANGE", "DEPOT",
    "WAREHOUSE", "FACTORY", "INDUSTRIAL", "WORKSHOP",
    "TEMPLE", "CHURCH", "MOSQUE",
]


def _looks_non_residential(address: str | None) -> bool:
    if not address:
        return False
    a = address.upper()
    return any(k in a for k in _NON_RES_KWS)


def to_hdb_street(street: str) -> str:
    s = (street or "").upper().strip()
    words = s.split()

    STREET_ABBREVIATIONS = {
        "STREET": "ST",
        "ROAD": "RD",
        "AVENUE": "AVE",
        "DRIVE": "DR",
        "CRESCENT": "CRES",
        "CLOSE": "CL",
        "LANE": "LN",
        "PLACE": "PL",
        "TERRACE": "TER",
        "BOULEVARD": "BLVD",
        "CENTRAL": "CTRL",
    }

    words = [STREET_ABBREVIATIONS.get(w, w) for w in words]
    return " ".join(words)


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

    results = data.get("results") or []
    if not results:
        return {"postal": postal, "type": "NOT_FOUND", "address": None, "estimate": None}

    first = results[0]
    address = first.get("ADDRESS")
    block = first.get("BLK_NO")
    street = first.get("ROAD_NAME")

    if not block or not street:
        return {"postal": postal, "type": "UNKNOWN", "address": address, "estimate": None}

    street_hdb = to_hdb_street(street)

    kind = "UNKNOWN"
    estimate = None

    inv = get_hdb_inventory_record(block, street_hdb)
    if inv:
        if (inv.get("residential") or "").upper() == "Y":
            kind = "PUBLIC"
            estimate = get_hdb_resale(block, street_hdb)
            print(block)
            print(street_hdb)
            print(estimate)
        else:
            kind = "NON_RESIDENTIAL"
    else:
        if _looks_non_residential(address):
            kind = "NON_RESIDENTIAL"
        else:
            kind = "PRIVATE"

    return {
        "postal": postal,
        "type": kind,
        "address": address,
        "estimate": estimate,
    }