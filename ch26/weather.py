import requests

CITIES = {"manila": (14.60, 120.98), "baguio": (16.41, 120.60)}


def forecast(lat: float, lon: float) -> dict:
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "auto"}, timeout=10)
    r.raise_for_status()
    return r.json()["daily"]


def umbrella_days(city: str) -> list[str]:
    d = forecast(*CITIES[city])
    return [day for day, p in zip(d["time"], d["precipitation_probability_max"]) if (p or 0) >= 60]
