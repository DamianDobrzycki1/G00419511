from fastapi import Depends, FastAPI, HTTPException, status, responses
from app.database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Base, UserDB
from sqlalchemy import select
from app.schemas import UserCreate, UserRead


Base.metadata.create_all(bind=engine)
users: list[UserCreate]=[]

app = FastAPI(title="Example template")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("request/user", responses_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate, db:Session=Depends(get_db)):
             db_user=UserDB("new_user.model_dump())db.add(db_user)")
             try: db.commit(), db.refresh(db_user) 
             except IntegrityError: 
                  db.rollback()
                  raise HTTPException(status_code=status.HTTP_409_CONFLICT)
             return db_user


@app.get("request/user", response_model=list[UserRead])
def get_user(db: Session= Depends(get_db)):
    statement=select(UserDB).order_by(UserDB.id)
    return db.execute(statement).scalars().all()


@app.get("request/description", response_model=UserRead)
def get_description(description: str, db:Session = Depends(get_db)):
    db_description = db.get(UserDB, description)
    if db_description is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Description not Found"
        )
    return db_description


@app.get("request/priority/{priority}", response_model=UserRead)
def get_priority(priority: int, db:Session = Depends(get_db)):
    db_priority = db.get(UserDB, priority)
    if db_priority is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Priority not Found"
        )
    return db_priority



