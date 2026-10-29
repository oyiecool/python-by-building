# test_weather.py
from unittest.mock import Mock

import pytest
import requests

import weather

FAKE = {"daily": {"time": ["2026-11-01", "2026-11-02", "2026-11-03"],
                  "precipitation_probability_max": [80, 20, None]}}


def fake_response(payload, status=200):
    resp = Mock()
    resp.json.return_value = payload
    resp.raise_for_status.side_effect = None if status == 200 else requests.HTTPError(f"{status}")
    return resp


def test_umbrella_days(monkeypatch):
    calls = []
    def fake_get(url, params, timeout):
        calls.append(params)
        return fake_response(FAKE)
    monkeypatch.setattr(weather.requests, "get", fake_get)   # no network needed
    assert weather.umbrella_days("baguio") == ["2026-11-01"]
    assert calls[0]["latitude"] == 16.41


def test_server_error_is_raised(monkeypatch):
    monkeypatch.setattr(weather.requests, "get", lambda *a, **k: fake_response({}, status=503))
    with pytest.raises(requests.HTTPError):
        weather.umbrella_days("manila")


def test_unknown_city():
    with pytest.raises(KeyError):
        weather.umbrella_days("atlantis")
