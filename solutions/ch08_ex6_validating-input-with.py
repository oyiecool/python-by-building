def parse_age(text: str) -> int:
    try:
        age = int(text.strip())
    except ValueError:
        raise ValueError(f"age must be a whole number, got {text!r}") from None
    if age < 0:
        raise ValueError("age cannot be negative")
    if age > 150:
        raise ValueError("age above 150 is not realistic")
    return age

# test_age.py
import pytest
@pytest.mark.parametrize("bad", ["abc", "-1", "200", "", "4.5"])
def test_rejects(bad):
    with pytest.raises(ValueError):
        parse_age(bad)

def test_accepts():
    assert parse_age(" 42 ") == 42
