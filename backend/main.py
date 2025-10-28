from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Home page - list all expenses
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).all()
    total = sum(exp.amount for exp in expenses)
    return templates.TemplateResponse("index.html", {"request": request, "expenses": expenses, "total": total})

# Add expense page
@app.get("/add", response_class=HTMLResponse)
def add_expense_page(request: Request):
    return templates.TemplateResponse("add_expense.html", {"request": request})

# Handle form submission
@app.post("/add")
def add_expense(
    request: Request,
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date_value: date = Form(...),
    db: Session = Depends(database.get_db)
):
    new_expense = models.Expense(title=title, amount=amount, category=category, date=date_value)
    db.add(new_expense)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
