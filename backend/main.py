from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from backend import models, database

# ✅ Create all database tables
models.Base.metadata.create_all(bind=database.engine)

# ✅ Initialize app
app = FastAPI()

# ✅ Static and Templates setup
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


# ✅ Home route - show all expenses
@app.get("/")
def home(request: Request, db: Session = Depends(database.get_db)):
    expenses = db.query(models.Expense).all()
    total = sum(e.amount for e in expenses)
    return templates.TemplateResponse(
        "index.html", {"request": request, "expenses": expenses, "total": total}
    )


# ✅ Show Add Expense Form Page
@app.get("/add")
def show_add_form(request: Request):
    return templates.TemplateResponse("add_expense.html", {"request": request})


# ✅ Add Expense - Form Submission
@app.post("/add")
def add_expense(
    request: Request,
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date_value: str = Form(...),
    db: Session = Depends(database.get_db),
):
    # Convert date string to Python date
    expense_date = date.fromisoformat(date_value)

    new_expense = models.Expense(
        title=title, amount=amount, category=category, date=expense_date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return RedirectResponse("/", status_code=303)
