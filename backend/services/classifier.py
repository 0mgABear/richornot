def classify_postal(data: dict) -> str:
    results = data.get("results") or []
    found = int(data.get("found") or 0)

    if found <= 0 or len(results) == 0:
        return "NOT_FOUND"

    for r in results:
        if str(r.get("BUILDING") or "").strip().upper() == "NIL":
            return "RESIDENTIAL"

    NON_RES_KEYWORDS = [
        "SCHOOL", "COLLEGE", "UNIVERSITY", "INSTITUTE", "POLYTECHNIC",
        "CAMPUS", "ACADEMY", "KINDERGARTEN",
        "CONSULATE", "EMBASSY",
        "TOWER", "OFFICE", "BUILDING", "PLAZA", "MALL", "COMPLEX",
        "HOSPITAL", "CLINIC", "CHURCH", "TEMPLE", "MOSQUE",
    ]

    for r in results:
        b = str(r.get("BUILDING") or "").upper()
        a = str(r.get("ADDRESS") or "").upper()
        if any(k in b for k in NON_RES_KEYWORDS) or any(k in a for k in NON_RES_KEYWORDS):
            return "NON_RESIDENTIAL"

    if found == 1:
        b = str(results[0].get("BUILDING") or "").strip().upper()
        if b and b != "NIL":
            return "RESIDENTIAL"

    return "NON_RESIDENTIAL"