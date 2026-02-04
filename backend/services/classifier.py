def classify_postal(data):
    results = data.get("results") or []
    found = data.get("found") or 0

    if found <= 0 or len(results) == 0:
        return "NOT_FOUND"

    NON_RES_KEYWORDS = [
        "SCHOOL", "COLLEGE", "UNIVERSITY", "INSTITUTE", "POLYTECHNIC",
        "CAMPUS", "ACADEMY", "KINDERGARTEN",
        "CONSULATE", "EMBASSY",
        "TOWER", "OFFICE", "BUILDING", "PLAZA", "MALL", "COMPLEX",
        "HOSPITAL", "CLINIC", "CHURCH", "TEMPLE", "MOSQUE", "MRT", "LRT"
    ]

    # If any result looks non-residential → NON_RESIDENTIAL
    for r in results:
        b = (r.get("BUILDING") or "").upper()
        a = (r.get("ADDRESS") or "").upper()
        for k in NON_RES_KEYWORDS:
            if k in b or k in a:
                return "NON_RESIDENTIAL"

    for r in results:
        building = (r.get("BUILDING") or "").strip().upper()
        if building == "NIL":
            return "PUBLIC"

    return "PRIVATE"