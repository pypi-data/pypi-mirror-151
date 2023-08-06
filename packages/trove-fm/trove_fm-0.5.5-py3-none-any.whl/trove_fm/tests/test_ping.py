
from fastapi import FastAPI
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_ping(app: FastAPI, client: AsyncClient) -> None:
    res = await client.get(app.url_path_for("ping:pong"))
    assert res.json() == {"ping": "pong!"}
