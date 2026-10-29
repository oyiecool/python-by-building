import pytest

from passgen import entropy_bits, passphrase, password
from passgen.cli import main


def test_password_rules():
    for _ in range(200):
        pw = password(12)
        assert len(pw) == 12
        assert any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)


def test_too_short():
    with pytest.raises(ValueError):
        password(5)


def test_passphrase_words():
    assert len(passphrase(6).split("-")) == 6


def test_entropy():
    assert round(entropy_bits(2, 10)) == 10


def test_cli(capsys):
    assert main(["--count", "3", "--length", "20"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 4 and all(len(l) == 20 for l in lines[:3])
