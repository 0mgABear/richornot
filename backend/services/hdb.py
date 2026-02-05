import requests

BASE_URL = "https://data.gov.sg/api/action/datastore_search"

DATASET_IDS = [
    "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",  # Jan-2017 onwards
    "d_ea9ed51da2787afaf8e51f827c304208",  # Jan 2015 - Dec 2016
    "d_2d5ff9ea31397b66239f245f57751537",  # Mar 2012 - Dec 2014
    "d_43f493c6c50d54243cc1eab0df142d6a",  # 2000 - Feb 2012
    "d_ebc5ab87086db484f88045b47411ebc5",  # 1990 - 1999
]


def _to_hdb_street(street: str) -> str:
    s = (street or "").upper().strip()
    s = " ".join(s.split())

    s = s.replace(" STREET ", " ST ")
    s = s.replace(" AVENUE ", " AVE ")
    s = s.replace(" ROAD ", " RD ")
    s = s.replace(" DRIVE ", " DR ")
    s = s.replace(" BOULEVARD ", " BLVD ")
    s = s.replace(" CENTRAL ", " CTRL ")
    s = s.replace(" CRESCENT ", " CRES ")
    s = s.replace(" CLOSE ", " CL ")
    s = s.replace(" PLACE ", " PL ")
    s = s.replace(" TERRACE ", " TER ")

    return s


def get_hdb_resale(block, street):
    street_hdb = _to_hdb_street(street)

    for dataset_id in DATASET_IDS:
        params = {
            "resource_id": dataset_id,
            "limit": 1,
            "sort": "month desc",
            "filters": f'{{"block":"{block}","street_name":"{street_hdb}"}}',
        }

        r = requests.get(BASE_URL, params=params, timeout=20)

        if r.status_code == 429:
            return None

        r.raise_for_status()
        data = r.json()
        records = (data.get("result") or {}).get("records") or []
        if not records:
            continue

        latest = records[0]
        return {
            "month": latest.get("month"),
            "town": latest.get("town"),
            "flat_type": latest.get("flat_type"),
            "street_name": latest.get("street_name"),
            "block": latest.get("block"),
            "resale_price": latest.get("resale_price"),
        }

    return None