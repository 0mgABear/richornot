import os
import requests
from datetime import date

_TOKEN = None
_TOKEN_DATE = None

TOKEN_URL = "https://eservice.ura.gov.sg/uraDataService/insertNewToken/v1"
TXN_URL = "https://eservice.ura.gov.sg/uraDataService/invokeUraDS/v1"


def _get_token():
    global _TOKEN, _TOKEN_DATE

    today = date.today()
    if _TOKEN and _TOKEN_DATE == today:
        return _TOKEN

    access_key = os.getenv("URA_API_KEY")
    if not access_key:
        raise RuntimeError("URA_API_KEY not set")

    r = requests.get(
        TOKEN_URL,
        headers={
            "AccessKey": access_key,
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
        timeout=15,
    )
    r.raise_for_status()

    ct = (r.headers.get("content-type") or "").lower()
    if "application/json" not in ct:
        raise RuntimeError(f"URA token returned non-JSON: {r.status_code} {r.text[:200]}")

    j = r.json()
    _TOKEN = j.get("Result")
    _TOKEN_DATE = today
    return _TOKEN


def get_private_by_street(street: str):
    access_key = os.getenv("URA_API_KEY")
    if not access_key:
        raise RuntimeError("URA_API_KEY not set")

    token = _get_token()

    r = requests.get(
        TXN_URL,
        params={"service": "PMI_Resi_Transaction", "batch": 1},
        headers={
            "AccessKey": access_key,
            "Token": token,
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
        timeout=30,
    )
    r.raise_for_status()

    ct = (r.headers.get("content-type") or "").lower()
    if "application/json" not in ct:
        raise RuntimeError(f"URA txn returned non-JSON: {r.status_code} {r.text[:200]}")

    payload = r.json()
    rows = payload.get("Result") or []
    s = (street or "").upper()

    matches = [x for x in rows if s in ((x.get("street") or "").upper())]
    if not matches:
        return None

    best = None
    best_date = ""
    for m in matches:
        txns = m.get("transaction") or []
        for t in txns:
            cd = t.get("contractDate") or ""
            if cd > best_date:
                best_date = cd
                best = {
                    "street": m.get("street"),
                    "project": m.get("project"),
                    "contractDate": cd,
                    "price": t.get("price"),
                    "area": t.get("area"),
                    "propertyType": t.get("propertyType"),
                    "tenure": t.get("tenure"),
                }

    return best