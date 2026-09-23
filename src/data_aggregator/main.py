from pprint import pprint

from data_aggregator.pipeline import PipelineStage
from data_aggregator.sources import CoinSource, CountriesSource, WeatherSource

from .data_aggregator import DataAggregator

sources = [WeatherSource, CountriesSource, CoinSource]
pipeline_stages = [PipelineStage.VALIDATE, PipelineStage.TRANSFORM]

da = DataAggregator(sources, pipeline_stages)

da._fetch()
# pprint(da._fetch(), indent=4)
pprint(da   ._transform(), indent=4)