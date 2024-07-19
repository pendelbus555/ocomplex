import openmeteo_requests
import requests
import requests_cache
import pandas as pd
from retry_requests import retry


def get_city_coordinates(city_name):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': city_name,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            location = results[0]
            return float(location['lat']), float(location['lon'])
    return None, None


def get_weather(latitude: float, longitude: float):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "pressure_msl"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "precipitation", "pressure_msl", "visibility"],
        "wind_speed_unit": "ms",
        "timezone": "auto",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    weather_data = {
        "coordinates": {"latitude": response.Latitude(), "longitude": response.Longitude()},
        "elevation": response.Elevation(),
        "timezone": response.Timezone(),
        "timezone_abbreviation": response.TimezoneAbbreviation(),
        "utc_offset_seconds": response.UtcOffsetSeconds(),
    }

    current = response.Current()
    weather_data["current"] = {
        "time": current.Time(),
        "temperature_2m": round(current.Variables(0).Value(), 1),
        "relative_humidity_2m": round(current.Variables(1).Value(), 1),
        "precipitation": round(current.Variables(2).Value(), 2),
        "pressure_msl": round(current.Variables(3).Value(), 1)
    }

    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["relative_humidity_2m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["precipitation_probability"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["precipitation"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_data["pressure_msl"] = hourly.Variables(4).ValuesAsNumpy()
    hourly_data["visibility"] = hourly.Variables(5).ValuesAsNumpy()

    hourly_display = []
    for i in range(len(hourly_data["date"])):
        time = hourly_data["date"][i].strftime("%I %p").lower()
        hour_data = {
            "time": time,
            "temperature_2m": round(hourly_data["temperature_2m"][i], 1),
            "relative_humidity_2m": round(hourly_data["relative_humidity_2m"][i], 1),
            "precipitation_probability": round(hourly_data["precipitation_probability"][i], 1),
            "precipitation": round(hourly_data["precipitation"][i], 1),
            "pressure_msl": round(hourly_data["pressure_msl"][i], 1),
            "visibility": round(hourly_data["visibility"][i], 1),
        }
        hourly_display.append(hour_data)

    hourly_display.sort(key=lambda x: (x["time"].endswith("am"), x["time"]))

    weather_data["hourly"] = hourly_display

    return weather_data
