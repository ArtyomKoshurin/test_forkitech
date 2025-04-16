from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func

from tron.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    balance = Column(Numeric(precision=18, scale=6))
    bandwidth = Column(Integer)
    energy = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
