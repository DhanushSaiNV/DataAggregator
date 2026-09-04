from data_aggregator.sources.countries_source import CountriesSource

cs = CountriesSource()

res = cs.fetch("?q=indi&pretty=1").parse()

print(res)