"""
Author: Prabal Pathak
"""
from threading import Thread
from typing import Dict
import time


def hello_world(first: str, work: str = "new", **kwargs: Dict) -> None:
    """
    This is a coroutine function
    """
    name = kwargs.get("name", "World")
    while True:
        print(f"Hello {first} {name} {work}")
        time.sleep(0.00001)
    return None


def other_func():
    """
    This is a coroutine function
    """
    while True:
        print("Other function")
        time.sleep(0.000001)


def other_func2():
    """
    This is a coroutine function
    """
    while True:
        print("Other function 2")
        time.sleep(0.000001)


def main():
    """
    This is a main function
    """
    first_thread = Thread(
        target=hello_world, args=("Prabal",), kwargs={"name": "Pathak"}
    )
    second_thread = Thread(target=other_func)
    third_thread = Thread(target=other_func2)
    first_thread.start()
    second_thread.start()
    third_thread.start()


if __name__ == "__main__":
    main()
