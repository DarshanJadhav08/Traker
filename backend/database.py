from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:darshan08@localhost/expense_db"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:oGuPa3RBkQciy1Cd6mzH5ltYlL1s109r@dpg-d40amff5r7bs73aanrlg-a:5432/expense_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
