from sqlalchemy import Column, Date, Float
from .db import Base


class HS300Price(Base):
    __tablename__ = "hs300_prices"

    date = Column(Date, primary_key=True, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)