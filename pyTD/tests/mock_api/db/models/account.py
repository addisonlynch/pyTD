# MIT License

# Copyright (c) 2018 Addison Lynch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime,
                        Float, Boolean)
from sqlalchemy.orm import relationship
from db.models.base import Base


class CurrentBalances(Base):
    __tablename__ = 'currentBalances'

    id = Column(Integer, primary_key=True)
    accruedInterest = Column(Float)
    availableFunds = Column(Float)
    availableFundsNonMarginableTrade = Column(Float)
    bondValue = Column(Float)
    buyingPower = Column(Float)
    buyingPowerNonMarginableTrade = Column(Float)
    cashBalance = Column(Float)
    cashReceipts = Column(Float)
    dayTradingBuyingPower = Column(Float)
    equity = Column(Float)
    equityPercentage = Column(Float)
    liquidationValue = Column(Float)
    longMarginValue = Column(Float)
    longMarketValue = Column(Float)
    longOptionMarketValue = Column(Float)
    maintenanceCall = Column(Float)
    maintenanceRequirement = Column(Float)
    marginBalance = Column(Float)
    moneyMarketFund = Column(Float)
    pendingDeposits = Column(Float)
    regTCall = Column(Float)
    savings = Column(Float)
    shortBalance = Column(Float)
    shortMarginValue = Column(Float)
    shortMarketValue = Column(Float)
    shortOptionMarketValue = Column(Float)
    sma = Column(Float)
    accountId = Column(Integer, ForeignKey('account.accountId'))
    account = relationship("Account", back_populates="currentBalances")


class InitialBalances(Base):
    __tablename__ = 'initialBalances'

    id = Column(Integer, primary_key=True)

    accountValue = Column(Float)
    accruedInterest = Column(Float)
    availableFundsNonMarginableTrade = Column(Float)
    bondValue = Column(Float)
    buyingPower = Column(Float)
    cashAvailableForTrading = Column(Float)
    cashBalance = Column(Float)
    cachREceipts = Column(Float)
    dayTradingBuyingPower = Column(Float)
    dayTradingBuyingPowerCall = Column(Float)
    dayTradingEquityCall = Column(Float)
    equity = Column(Float)
    equityPercentage = Column(Float)
    isInCall = Column(Boolean)
    liquidationValue = Column(Float)
    longMarginValue = Column(Float)
    longOptionMarketValue = Column(Float)
    longStockValue = Column(Float)
    maintenanceCall = Column(Float)
    maintenanceRequirement = Column(Float)
    margin = Column(Float)
    marginBalance = Column(Float)
    marginEquity = Column(Float)
    moneyMarketFund = Column(Float)
    mutualFundValue = Column(Float)
    pendingDeposits = Column(Float)
    regTCAll = Column(Float)
    shortBalance = Column(Float)
    shortMarginValue = Column(Float)
    shortOptionMarketValue = Column(Float)
    shortStockValue = Column(Float)
    totalCash = Column(Float)
    accountId = Column(Integer, ForeignKey('account.accountId'))
    account = relationship("Account", back_populates="initialBalances")


class ProjectedBalances(Base):
    __tablename__ = 'projectedBalances'

    id = Column(Integer, primary_key=True)

    availableFunds = Column(Float)
    buyingPower = Column(Float)
    dayTradingBuyingPower = Column(Float)
    dayTradingBuyingPowerCall = Column(Float)
    isInCall = Column(Boolean)
    maintenanceCall = Column(Float)
    regTCAll = Column(Float)
    stockBuyingPower = Column(Float)
    accountId = Column(Integer, ForeignKey('account.accountId'))
    account = relationship("Account", back_populates="projectedBalances")


class Account(Base):
    __tablename__ = 'account'

    accountId = Column(Integer, primary_key=True)
    isClosingOnlyRestricted = Column(Integer)
    isDayTrader = Column(Integer)
    roundTrips = Column(Integer)
    type = Column(String(10))
    last_updated = Column(DateTime)
    currentBalances = relationship(CurrentBalances, uselist=False,
                                   back_populates="account")
    initialBalances = relationship(InitialBalances, uselist=False,
                                   back_populates="account")
    projectedBalances = relationship(ProjectedBalances, uselist=False,
                                     back_populates="account")


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
