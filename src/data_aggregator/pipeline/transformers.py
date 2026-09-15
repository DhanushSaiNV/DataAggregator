from data_aggregator.domain.models import (
    TransformedResponseModel,
    ValidatedCoinResponse,
    ValidatedCountriesResponse,
    ValidatedWeatherResponse,
)
from data_aggregator.sources.coin_source import CoinSource
from data_aggregator.sources.countries_source import CountriesSource
from data_aggregator.sources.weather_source import WeatherSource


def transform_countries(response: ValidatedCountriesResponse) -> TransformedResponseModel | ValidatedCountriesResponse:
    return response

def transform_coins(response: ValidatedCoinResponse) -> TransformedResponseModel | ValidatedCoinResponse:
    return response

def transform_weather(response: ValidatedWeatherResponse) -> TransformedResponseModel | ValidatedWeatherResponse:
    return response


TRANSFORMERS = {
    WeatherSource : transform_weather,
    CoinSource : transform_coins,
    CountriesSource : transform_countries
}