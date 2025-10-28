from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))          # Expense title (must exist in DB)
    amount = Column(Float)
    category = Column(String(50))
    date = Column(Date)
