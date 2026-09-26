import asyncio
from time import perf_counter

from data_aggregator.domain.exceptions import *
from data_aggregator.sources.weather_source import AsyncWeatherSource, WeatherSource

# ws = WeatherSource()

# try:
#     start_time = perf_counter()
#     response = ws.fetch().parse()
#     end_time = perf_counter()
#     print(repr(response))
#     print(end_time - start_time)

# except ResponseValidationError as e:
#     print(e)

async def test_async():
    ws = AsyncWeatherSource()

    start_time = perf_counter()

    response = await ws.fetch()
    response = response.parse()

    end_time = perf_counter()
    print(repr(response))
    print(end_time - start_time)


asyncio.run(test_async())