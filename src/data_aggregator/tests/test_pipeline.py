from data_aggregator.domain.models import RawWeatherResponse, ValidatedWeatherResponse
from data_aggregator.pipeline.pipeline import Pipeline, PipelineStage
from data_aggregator.sources.coin_source import CoinSource
from data_aggregator.sources.countries_source import CountriesSource
from data_aggregator.sources.weather_source import WeatherSource

p = Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)

ws = WeatherSource()

raw_resp = ws.fetch().parse()

print(p.run(response=raw_resp, source=WeatherSource, validation_model=ValidatedWeatherResponse))