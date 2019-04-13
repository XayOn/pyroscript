from pathlib import Path
import sys

import pytest
from aioresponses import aioresponses


@pytest.fixture
def aiohttp_app():
    from pyroscript import get_app

    class FakeOptions(dict):
        """Fake options."""

        def option(self, option):
            return self.__getitem__(option)

    config_fixture = (
        Path(__file__).parent / 'fixtures' / 'config.ini').absolute()

    return get_app(
        FakeOptions({
            'debug': True,
            'host': '0.0.0.0',
            'port': '8080',
            'config': config_fixture
        }))
