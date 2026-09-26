import asyncio
from time import perf_counter

from data_aggregator.sources.countries_source import (
    AsyncCountriesSource,
    CountriesSource,
)

# cs = CountriesSource()


# start_time = perf_counter()
# response = cs.fetch("?q=indi&pretty=1").parse()
# end_time = perf_counter()
# print(repr(response))
# print("Synchronous", end_time - start_time)


# Async
async def test_async():
    cs = AsyncCountriesSource()

    start_time = perf_counter()
    
    response = await cs.fetch("?q=indi&pretty=1")
    
    response = response.parse()
    
    end_time = perf_counter()
    print(repr(response))
    print("Asynchronous" , end_time - start_time)

asyncio.run(test_async())