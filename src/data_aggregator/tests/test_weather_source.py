from data_aggregator.sources.weather_source import WeatherSource

ws = WeatherSource()
response = ws.fetch().parse()

print(response)