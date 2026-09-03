from data_aggregator.domain import ResponseModel
from data_aggregator.sources.weather_source import WeatherSource

weather_source = WeatherSource()

response = weather_source.fetch().parse()

print("Coordinates: " , response.coordinates)
print("Timezone: " , response.timezone_b)
print("Time: " , response.time)
print("Temperature: " , response.temperature_2m)
print("Humidity: " , response.relative_humidity_2m)
print("Is Day: " , response.is_day)
print("Is raining: " , response.rain)