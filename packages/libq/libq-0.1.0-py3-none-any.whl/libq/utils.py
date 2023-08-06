import asyncio
import numbers
from importlib import import_module
from typing import AsyncGenerator, Callable, Union

from nanoid import generate

from libq.errors import TimeoutFormatError


def generate_random(size=10):

    return generate(size=size)


def parse_timeout(timeout) -> Union[int, None]:
    """Transfer all kinds of timeout format to an integer representing seconds"""
    if not isinstance(timeout, numbers.Integral) and timeout is not None:
        try:
            timeout = int(timeout)
        except ValueError:
            digit, unit = timeout[:-1], (timeout[-1:]).lower()
            unit_second = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
            try:
                timeout = int(digit) * unit_second[unit]
            except (ValueError, KeyError):
                raise TimeoutFormatError('Timeout must be an integer or a string representing an integer, or '
                                         'a string with format: digits + unit, unit can be "d", "h", "m", "s", '
                                         'such as "1h", "23m".')

    return timeout


async def poll(step: float = 0.5) -> AsyncGenerator[float, None]:
    loop = asyncio.get_event_loop()
    start = loop.time()
    while True:
        before = loop.time()
        yield before - start
        after = loop.time()
        wait = max([0, step - after + before])
        await asyncio.sleep(wait)


def get_function(fullname) -> Callable:
    mod, name = fullname.rsplit(".", maxsplit=1)
    pkg = mod.split(".", maxsplit=1)[0]
    try:
        module = import_module(mod, pkg)
    except (ModuleNotFoundError, AttributeError):
        raise KeyError(fullname)
    return getattr(module, name)
