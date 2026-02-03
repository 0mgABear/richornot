import pytest
from services.postal import postal_check

def test_postal_check_valid():
    assert postal_check("410114") is True

def test_postal_check_wrong_length():
    with pytest.raises(ValueError):
        postal_check("12345")

def test_postal_check_non_digits():
    with pytest.raises(ValueError):
        postal_check("12A456")

def test_postal_check_spaces():
    with pytest.raises(ValueError):
        postal_check("410 14")