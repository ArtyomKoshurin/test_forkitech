import pytest

from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_wallet_info_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/wallet_info",
            json={"address": "TVjsr6BZqN2xYgv9fLh86q6gwwGfDmqhBW"}
        )
        data = response.json()

        assert response.status_code == 200
        assert "balance" in data


@pytest.mark.asyncio
async def test_get_logs():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/wallet_logs?limit=5&offset=0")
        data = response.json()

        assert response.status_code == 200
        assert "items" in data
