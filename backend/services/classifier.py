# services/classifier.py

_NON_RES_KWS = [
    "TOWER", "OFFICE", "MALL", "PLAZA", "CENTRE", "CENTER", "COMPLEX",
    "HOTEL", "HOSPITAL", "CLINIC", "SCHOOL", "COLLEGE", "UNIVERSITY",
    "MRT", "STATION", "INTERCHANGE", "DEPOT",
    "WAREHOUSE", "FACTORY", "INDUSTRIAL", "WORKSHOP",
    "TEMPLE", "CHURCH", "MOSQUE", "CONSULATE",
]

def classify_postal(data: dict) -> str:
    results = data.get("results") or []
    if not results:
        return "NOT_FOUND"

    first = results[0] or {}
    building = (first.get("BUILDING") or "").upper().strip()
    address = (first.get("ADDRESS") or "").upper().strip()

    hay = f"{building} {address}"
    if any(k in hay for k in _NON_RES_KWS):
        return "NON_RESIDENTIAL"

    if building and building != "NIL":
        return "PRIVATE"

    if building == "NIL":
        return "PUBLIC"

    return "PRIVATE"