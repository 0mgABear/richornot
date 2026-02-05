import requests

DATASET_ID = "d_17f5382f26140b1fdae0ba2ef6239d2f"
BASE_URL = "https://data.gov.sg/api/action/datastore_search"


def _norm_street(s: str) -> str:
    s = (s or "").upper().strip()
    s = " ".join(s.split())

    s = s.replace(" ROAD", " RD")
    s = s.replace(" STREET", " ST")
    s = s.replace(" AVENUE", " AVE")
    s = s.replace(" DRIVE", " DR")
    s = s.replace(" CRESCENT", " CRES")
    s = s.replace(" CENTRAL", " CTRL")
    s = s.replace(" PLACE", " PL")
    s = s.replace(" LANE", " LN")
    s = s.replace(" BOULEVARD", " BLVD")
    s = s.replace(" TERRACE", " TER")

    return s


def get_hdb_inventory_record(block: str, street: str):
    blk = (block or "").upper().strip()
    street_raw = (street or "").upper().strip()

    if not blk or not street_raw:
        return None

    street_candidates = []
    street_candidates.append(_norm_street(street_raw))
    street_candidates.append(_norm_street(street_raw).replace("RD", "ROAD"))
    street_candidates.append(_norm_street(street_raw).replace("ST", "STREET"))
    street_candidates = list(dict.fromkeys([s for s in street_candidates if s]))

    for st in street_candidates:
        params = {
            "resource_id": DATASET_ID,
            "limit": 1,
            "filters": f'{{"blk_no":"{blk}","street":"{st}"}}',
        }
        r = requests.get(BASE_URL, params=params, timeout=20)
        if r.status_code == 429:
          print("HDB inventory rate-limited (429)", flush=True)
          return None

        data = r.json()
        records = (data.get("result") or {}).get("records") or []
        if records:
            return records[0]

    return None