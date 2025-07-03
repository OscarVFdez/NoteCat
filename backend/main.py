from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)  # Create database tables

app = FastAPI(title= "NoteCat API") # Initialize FastAPI app with title

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password hashing context

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register", response_model=schemas.UserOut)

def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get("/")
def read_root():
    return {"message": "Welcome to NoteCat API!"}