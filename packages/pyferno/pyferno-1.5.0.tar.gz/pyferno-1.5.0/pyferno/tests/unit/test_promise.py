from typing import AsyncGenerator

import pytest
import asyncio
import random
from pyferno.promise import Promise
import math


async def dummy_fn(i: int = None):
    out = math.sqrt(i) * i
    return out


async def dummy_sleep(order: int):
    sleep = random.randint(0, 2)
    await asyncio.sleep(sleep)
    out = {"no": order, "sleep": sleep}
    return out


@pytest.fixture(name="list_of_tasks", scope="function")
def get_list_of_tasks():
    list_of_tasks = list()
    for i in range(0, 10):
        list_of_tasks.append(dummy_sleep(i))

    return list_of_tasks


@pytest.fixture(name="dict_of_tasks", scope="function")
def get_dict_of_tasks():
    dict_of_tasks = dict()
    for i in range(0, 1000):
        key = f"key_{i}"
        dict_of_tasks[key] = dummy_fn(i)

    return dict_of_tasks


@pytest.mark.asyncio
async def test_standard_description(list_of_tasks):
    out = await Promise.all(list_of_tasks, progress=True)
    assert isinstance(out, list)
    return out


@pytest.mark.asyncio
async def test_custom_description(list_of_tasks):
    out = await Promise.all(list_of_tasks, progress="A nice progressbar")
    assert isinstance(out, list)
    return out


@pytest.mark.asyncio
async def test_no_progress(list_of_tasks):
    assert isinstance(list_of_tasks, list)
    print("no progress bar")
    out = await Promise.all(list_of_tasks)
    assert isinstance(out, list)


@pytest.mark.asyncio
async def test_dict_of_tasks(dict_of_tasks):
    assert isinstance(dict_of_tasks, dict)
    out = await Promise.props(dict_of_tasks)
    assert isinstance(out, dict)


@pytest.mark.asyncio
async def test_generation(list_of_tasks):
    generator = Promise.generate(list_of_tasks, progress=False)
    assert isinstance(generator, AsyncGenerator)
    async for item in generator:
        assert item
