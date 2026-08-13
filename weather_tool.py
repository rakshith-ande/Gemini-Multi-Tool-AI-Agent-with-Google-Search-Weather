import requests
from langchain.tools import tool


# Open-Meteo endpoint for Hyderabad
WEATHER_API_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


@tool
def get_weather() -> str:
    """
    Get the current and upcoming hourly weather information
    for Hyderabad, India.

    Returns temperature, humidity, rain, precipitation probability,
    apparent temperature, dew point, visibility, and wind speed.
    """

    params = {
        "latitude": 17.384,
        "longitude": 78.4564,

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "rain,"
            "precipitation,"
            "precipitation_probability,"
            "apparent_temperature,"
            "dew_point_2m,"
            "showers,"
            "visibility,"
            "wind_speed_10m"
        ),

        "timezone": "Asia/Kolkata",

        # Get today's and tomorrow's forecast
        "forecast_days": 2
    }

    try:
        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        hourly = data["hourly"]

        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        humidity = hourly["relative_humidity_2m"]
        rain = hourly["rain"]
        precipitation = hourly["precipitation"]
        precipitation_probability = hourly["precipitation_probability"]
        apparent_temperature = hourly["apparent_temperature"]
        dew_point = hourly["dew_point_2m"]
        showers = hourly["showers"]
        visibility = hourly["visibility"]
        wind_speed = hourly["wind_speed_10m"]

        # Return the first 24 hours
        weather_data = []

        for i in range(min(24, len(times))):

            weather_data.append(
                f"""
Time: {times[i]}
Temperature: {temperatures[i]} °C
Feels Like: {apparent_temperature[i]} °C
Humidity: {humidity[i]} %
Rain: {rain[i]} mm
Precipitation: {precipitation[i]} mm
Precipitation Probability: {precipitation_probability[i]} %
Showers: {showers[i]} mm
Dew Point: {dew_point[i]} °C
Visibility: {visibility[i]} meters
Wind Speed: {wind_speed[i]} km/h
"""
            )

        return "\n".join(weather_data)

    except requests.exceptions.RequestException as e:

        return f"Weather API request failed: {str(e)}"

    except KeyError as e:

        return f"Unexpected response from weather API. Missing field: {str(e)}"

    except Exception as e:

        return f"Unexpected error while fetching weather: {str(e)}"