from typing import List
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class WalletInfoRequest(BaseModel):
    address: str


class WalletInfoResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: Decimal


class WalletLog(WalletInfoResponse):
    timestamp: datetime


class WalletLogList(BaseModel):
    items: List[WalletLog]
