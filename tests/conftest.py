import pytest
from typing import AsyncGenerator

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
