from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from tron.schema import WalletInfoRequest, WalletInfoResponse, WalletLogList
from tron.database import async_session
from tron.utils import get_wallet_info
from tron.models import Wallet


router = APIRouter()


async def get_session():
    async with async_session() as session:
        yield session


@router.post("/wallet_info", response_model=WalletInfoResponse)
async def wallet_info(
    request: WalletInfoRequest,
    session: AsyncSession = Depends(get_session)
):
    data = await get_wallet_info(request.address)
    wallet = Wallet(**data)
    session.add(wallet)
    await session.commit()

    return data


@router.get("/wallet_logs", response_model=WalletLogList)
async def get_wallet_logs(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Wallet).offset(offset).limit(limit))
    logs = result.scalars().all()

    return {"items": logs}
