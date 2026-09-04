from data_aggregator.sources.coin_source import CoinSource

cs = CoinSource()

print(cs.fetch("bitcoin").parse())