import httpx

@app.get("/weather/{city}")
async def weather(city: str):
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://api.open-meteo.com/v1/forecast",
                             params={"latitude": 14.6, "longitude": 121.0, "current": "temperature_2m"})
    return {"city": city, "temperature": r.json()["current"]["temperature_2m"]}
