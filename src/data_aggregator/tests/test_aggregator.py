from data_aggregator.sources.coin_source import CoinSource
from data_aggregator.sources.countries_source import CountriesSource
from data_aggregator.sources.weather_source import WeatherSource

ws = WeatherSource()
cs = CountriesSource()
coins = CoinSource()

with open("output.txt", "a", encoding="utf-8") as file:
    print("LOG:: [1/3] Fetching...")

    ws_output = ws.fetch().parse()

    print("LOG:: [2/3] Fetching...")

    cs_output = cs.fetch("?q=indi&pretty=1").parse()

    print("LOG:: [3/3] Fetching...")

    coins_output = coins.fetch("bitcoin").parse()

    print("LOG:: Logging outputs...")

    for output in (ws_output, cs_output, coins_output):
        file.write(output.model_dump_json())
        file.write("\n\n----\n\n")