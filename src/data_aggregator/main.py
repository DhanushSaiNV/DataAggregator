from pprint import pprint

from data_aggregator.pipeline import PipelineStage
from data_aggregator.sources import CoinSource, CountriesSource, WeatherSource

from .data_aggregator import DataAggregator

sources = [CoinSource, CountriesSource, WeatherSource]
pipeline_stages = [PipelineStage.VALIDATE, PipelineStage.TRANSFORM]

da = DataAggregator(sources, pipeline_stages)

pprint(da._fetch())