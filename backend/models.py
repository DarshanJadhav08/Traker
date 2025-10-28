from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    amount = Column(Float)
    category = Column(String(100))
    date = Column(Date)
