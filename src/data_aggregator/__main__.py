from data_aggregator.pipeline import PipelineStage
from data_aggregator.sources import CoinSource, CountriesSource, WeatherSource

from .data_aggregator import DataAggregator

sources = [WeatherSource, CountriesSource, CoinSource]
pipeline_stages = [PipelineStage.VALIDATE, PipelineStage.TRANSFORM]

result = (
  DataAggregator(sources, pipeline_stages)
  .fetch()
  .transform()
  .display()
)
