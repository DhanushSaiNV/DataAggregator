import openmeteo_requests

openmeteo = openmeteo_requests.Client()

url = "https://api.open-meteo.com/v1/forecast"

params ={
	"latitude": 16.2997,
	"longitude": 80.4573,
	"daily": ["sunrise", "sunset"],
	"current": ["temperature_2m", "relative_humidity_2m", "is_day", "rain"],
	"timezone": "auto",
}

response = openmeteo.weather_api(url, params)[0]

print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")


current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_is_day = current.Variables(2).Value()
current_rain = current.Variables(3).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")
print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
print(f"Current is_day: {current_is_day}")
print(f"Current rain: {current_rain}")