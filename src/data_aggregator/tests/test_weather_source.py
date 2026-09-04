from data_aggregator.domain.exceptions import *
from data_aggregator.sources.weather_source import WeatherSource

ws = WeatherSource()

try:
    response = ws.fetch().parse()
    print(repr(response))

except ResponseValidationError as e:
    print(e)

