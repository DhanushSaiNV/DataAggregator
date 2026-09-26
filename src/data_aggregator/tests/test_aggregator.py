import asyncio
import time

from data_aggregator.data_aggregator import AsyncDataAggregator, DataAggregator
from data_aggregator.pipeline import PipelineStage
from data_aggregator.sources import *

sources = [WeatherSource, CountriesSource, CoinSource]
pipeline_stages = [PipelineStage.VALIDATE, PipelineStage.TRANSFORM]

da = DataAggregator(
    sources,
    pipeline_stages
)

ada = AsyncDataAggregator(
    [AsyncWeatherSource, AsyncCountriesSource, AsyncCoinSource],
    pipeline_stages
)

start = time.perf_counter()
da.run(display=False)
end = time.perf_counter()

print("Synchronous: ", end - start)


start = time.perf_counter()
asyncio.run(ada.run(display=False))
end = time.perf_counter()

print("Asynchronous: ", end - start)
