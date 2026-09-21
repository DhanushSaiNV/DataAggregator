from dataclasses import asdict
from pprint import pprint

from data_aggregator.domain.models import ValidatedWeatherResponse
from data_aggregator.pipeline.pipeline import Pipeline, PipelineStage, PipelineState
from data_aggregator.sources.weather_source import WeatherSource

weather_source = WeatherSource()

pipeline = Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)

raw_resp = weather_source.fetch().parse()

output_state: PipelineState = pipeline.run(
    raw_resp,
    WeatherSource,
    ValidatedWeatherResponse
)

pprint(asdict(output_state))
