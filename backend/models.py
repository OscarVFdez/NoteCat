from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True) # Primary key
    username = Column(String(50), unique=True, nullable=False, index=True) # Unique username for each user, cannot be null
    email = Column(String(255), unique=True, nullable=False, index=True) # Unique email for each user, cannot be null
    hashed_password = Column(String, nullable=False) # Hashed password for security, cannot be null

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"