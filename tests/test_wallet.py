import pytest
from decimal import Decimal
from unittest.mock import patch

from sqlalchemy import select

from tron.models import Wallet


MOCK_WALLET_INFO = {
    "address": "testaddress",
    "balance": "100.5",
    "bandwidth": 500,
    "energy": 1000
}


@pytest.mark.asyncio
async def test_wallet_info_endpoint(test_db, test_client):
    with patch("routes.wallet.get_wallet_info", return_value=MOCK_WALLET_INFO):
        response = test_client.post(
            "/wallet_info",
            json={"address": "testaddress"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data == MOCK_WALLET_INFO

        result = await test_db.execute(
            select(Wallet).where(Wallet.address == "testaddress")
        )
        wallet = result.scalar_one_or_none()
        assert wallet is not None
        assert wallet.address == "testaddress"
        assert wallet.balance == Decimal("100.5")
        assert wallet.bandwidth == 500
        assert wallet.energy == 1000


@pytest.mark.asyncio
async def test_wallet_db_write(test_db):
    wallet = Wallet(
        address="testaddress",
        balance=Decimal("100.5"),
        bandwidth=500,
        energy=1000
    )

    test_db.add(wallet)
    await test_db.commit()

    result = await test_db.execute(
        select(Wallet).where(Wallet.address == "testaddress")
    )
    saved_wallet = result.scalar_one_or_none()

    assert saved_wallet is not None
    assert saved_wallet.address == "testaddress"
    assert saved_wallet.balance == Decimal("100.5")
    assert saved_wallet.bandwidth == 500
    assert saved_wallet.energy == 1000


@pytest.mark.asyncio
async def test_get_wallet_logs_endpoint(test_db, test_client):

    for i in range(15):
        wallet = Wallet(
            address=f"testaddress{i}",
            balance=Decimal(f"100.{i}"),
            bandwidth=500 + i,
            energy=1000 + i
        )
        test_db.add(wallet)
    await test_db.commit()

    response = test_client.get("/wallet_logs?limit=10&offset=0")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 10

    assert logs[0]["address"].startswith("testaddress")

    response = test_client.get("/wallet_logs?limit=10&offset=10")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) <= 5
