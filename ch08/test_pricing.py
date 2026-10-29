import pytest
from pricing import discount

def test_basic_discount():
    assert discount(100, 20) == 80

def test_zero_and_full():
    assert discount(59.99, 0) == 59.99
    assert discount(59.99, 100) == 0

@pytest.mark.parametrize("price,pct,expected", [(200, 50, 100), (19.99, 10, 17.99)])
def test_many(price, pct, expected):
    assert discount(price, pct) == expected

def test_invalid_percent():
    with pytest.raises(ValueError):
        discount(100, 150)
