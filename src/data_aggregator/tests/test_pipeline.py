from dataclasses import asdict
from pprint import pprint

from data_aggregator.domain.models import ValidatedWeatherResponse
from data_aggregator.pipeline.pipeline import (
    Pipeline,
    PipelineConfig,
    PipelineStage,
    PipelineState,
)
from data_aggregator.sources.weather_source import WeatherSource

weather_source = WeatherSource()

pipeline = Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)

raw_resp = weather_source.fetch().parse()

pipeline_config = PipelineConfig(raw_resp, WeatherSource, ValidatedWeatherResponse)

output_state: PipelineState = pipeline.run(pipeline_config)

pprint(asdict(output_state))
