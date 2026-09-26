import asyncio
from time import perf_counter

from data_aggregator.sources.coin_source import AsyncCoinSource, CoinSource

# cs = CoinSource()

# print(cs.fetch("bitcoin").parse())
# start_time = perf_counter()
# response = cs.fetch().parse()
# end_time = perf_counter()
# print(repr(response))
# print(end_time - start_time)

async def test_async():
    cs = AsyncCoinSource()
    
    start_time = perf_counter()
    response = await cs.fetch("bitcoin")
    end_time = perf_counter()

    response = response.parse()
    print(repr(response))
    print(end_time - start_time)

asyncio.run(test_async())