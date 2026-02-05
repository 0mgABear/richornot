from services.classifier import classify_postal

OFFICE_JSON = {
    "found": 3,
    "results": [
        {
            "BUILDING": "CONSULATE OF SAINT VINCENT AND THE GRENADINES",
            "ADDRESS": "8 MARINA VIEW ... SINGAPORE 018960",
        },
        {
            "BUILDING": "CONSULATE OF THE REPUBLIC OF SLOVENIA",
            "ADDRESS": "8 MARINA VIEW ... SINGAPORE 018960",
        },
        {
            "BUILDING": "ASIA SQUARE TOWER 1",
            "ADDRESS": "8 MARINA VIEW ... SINGAPORE 018960",
        },
    ],
}

SCHOOL_JSON = {
    "found": 1,
    "results": [
        {
            "BUILDING": "UNITED WORLD COLLEGE OF SOUTH EAST ASIA (EAST CAMPUS)",
            "ADDRESS": "1 TAMPINES STREET 73 ... SINGAPORE 528704",
        }
    ],
}

CONDO_JSON = {
    "found": 1,
    "results": [
        {
            "BUILDING": "THE TAMPINES TRILLIANT",
            "ADDRESS": "11 TAMPINES CENTRAL 7 ... SINGAPORE 528769",
        }
    ],
}

HDB_JSON = {
    "found": 1,
    "results": [
        {
            "BUILDING": "NIL",
            "ADDRESS": "114 LENGKONG TIGA SINGAPORE 410114",
        }
    ],
}

NO_RESULTS_JSON = {"found": 0, "results": []}

def test_classifier_office_is_non_residential():
    assert classify_postal(OFFICE_JSON) == "NON_RESIDENTIAL"

def test_classifier_school_is_non_residential():
    assert classify_postal(SCHOOL_JSON) == "NON_RESIDENTIAL"

def test_classifier_condo_is_residential():
    assert classify_postal(CONDO_JSON) == "PRIVATE"

def test_classifier_hdb_is_residential():
    assert classify_postal(HDB_JSON) == "PUBLIC"

def test_classifier_no_results():
    assert classify_postal(NO_RESULTS_JSON) == "NOT_FOUND"