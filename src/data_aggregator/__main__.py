import argparse
import asyncio
import time

from data_aggregator.pipeline import PipelineStage
from data_aggregator.sources import *

from .data_aggregator import AsyncDataAggregator, DataAggregator

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--synchronous", action="store_true", help="Runs data aggregator in synchronous mode.")


args = parser.parse_args()


start_time = end_time = elapsed = None
pipeline_stages = [PipelineStage.VALIDATE, PipelineStage.TRANSFORM]

if not args.synchronous:
    sources = [AsyncWeatherSource, AsyncCountriesSource, AsyncCoinSource]

    data_agg = AsyncDataAggregator(sources, pipeline_stages)

    start_time = time.perf_counter()
    asyncio.run(data_agg.run())
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Response Time: {elapsed:.2f}sec")

else:
    sources = [WeatherSource, CountriesSource, CoinSource]

    data_agg = DataAggregator(sources, pipeline_stages)

    start_time = time.perf_counter()
    data_agg.run()
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Response Time: {elapsed:.2f}sec")
