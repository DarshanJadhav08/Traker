from pydantic import BaseModel
from datetime import date

class ExpenseBase(BaseModel):
    date: date
    category: str
    amount: float
    description: str

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseShow(ExpenseBase):
    id: int
    class Config:
        orm_mode = True
from pydantic import BaseModel
from datetime import date

class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: str
    date: date

    class Config:
        from_attributes = True
