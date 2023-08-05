"""
Author: Prabal Pathak
"""
import asyncio


async def hello_world(first: str, work: str = "", **kwargs: dict):
    """
    This is a coroutine function
    """
    name = kwargs.get("name", "World")
    while True:
        print(f"Hello {name} {first} {work}")
        await asyncio.sleep(0.00001)


async def other_func():
    """
    This is a coroutine function
    """
    while True:
        print("Other function")
        await asyncio.sleep(0.000001)


async def other_func2():
    """
    This is a coroutine function
    """
    while True:
        print("Other function 2")
        await asyncio.sleep(0.000001)


def main():
    """
    This is a main function
    """
    loop = asyncio.get_event_loop()
    loop.create_task(hello_world("Prabal"))
    loop.create_task(other_func())
    loop.create_task(other_func2())
    loop.run_forever()


if __name__ == "__main__":
    main()
