from main import to_hdb_street

def test_to_hdb_street_converts_end_word():
    assert to_hdb_street("Redhill Road") == "REDHILL RD"

def test_to_hdb_street_converts_middle_word():
    assert to_hdb_street("Tampines Street 24") == "TAMPINES ST 24"

def test_to_hdb_street_handles_extra_spaces():
    assert to_hdb_street("  Tampines   Street   24 ") == "TAMPINES ST 24"

def test_to_hdb_street_no_change():
    assert to_hdb_street("COVE DRIVE") == "COVE DR"