import asyncio
import time


async def main():
    queue_1 = asyncio.Queue(maxsize=3)
    queue_2 = asyncio.Queue()

    start= time.perf_counter()
    await asyncio.gather(
        producer(queue_1),
        processor(queue_1, queue_2),
        processor(queue_1, queue_2),
        consumer(queue_2)
    )
    print(f"time took: {time.perf_counter() - start}")

async def producer(queue):
    print("Producer")
    for num in range(20):
        await asyncio.sleep(0.05)
        await queue.put(num)
        print(f"queue_1 size: {queue.qsize()}")


    await queue.put(None)
    await queue.put(None)


async def processor(queue_1, queue_2):
    print("Processor")
    while True:
        await asyncio.sleep(0.1)

        num = await queue_1.get()

        if num is None:
            await queue_2.put(num)
            break

        await queue_2.put(num**2)

async def consumer(queue):
    print("Consumer")
    none_count = 0
    while True:
        num = await queue.get()

        if num is None:
            none_count += 1

            if none_count < 2:
                continue

            break

        

        print(num)


if __name__ == "__main__":
    asyncio.run(main())

