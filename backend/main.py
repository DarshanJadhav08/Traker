from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from backend.database import Base, engine
from backend import models
Base.metadata.create_all(bind=engine)
exit()
from backend import models, schemas, database

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).all()
    total = sum(e.amount for e in expenses)
    return templates.TemplateResponse("index.html", {"request": request, "expenses": expenses, "total": total})

@app.post("/add_expense")
def add_expense(
    request: Request,
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    db: Session = Depends(database.get_db)
):
    new_expense = models.Expense(title=title, amount=amount, category=category, date=date.today())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return RedirectResponse("/", status_code=303)

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)