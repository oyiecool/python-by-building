# weather.py
import argparse
import requests

CITIES = {
    "manila": (14.60, 120.98), "cebu": (10.32, 123.89), "davao": (7.07, 125.61),
    "tarlac": (15.49, 120.59), "baguio": (16.41, 120.60),
}

def forecast(lat: float, lon: float) -> dict:
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
        "timezone": "auto",
    }, timeout=10)
    r.raise_for_status()
    return r.json()["daily"]

def report(city: str):
    d = forecast(*CITIES[city])
    print(f"\n7-day forecast for {city.title()}")
    print(f"{'Date':<12}{'Min':>6}{'Max':>6}{'Rain mm':>9}{'Chance':>8}")
    for day, lo, hi, rain, pop in zip(d["time"], d["temperature_2m_min"], d["temperature_2m_max"],
                                      d["precipitation_sum"], d["precipitation_probability_max"]):
        umbrella = "  umbrella" if (pop or 0) >= 60 else ""
        print(f"{day:<12}{lo:>6.1f}{hi:>6.1f}{rain:>9.1f}{pop:>7}%{umbrella}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("city", choices=CITIES)
    report(ap.parse_args().city)
