"""
Database configuration module.
- Establishes a connection to the SQLite database with the correct settings.
- Creates a session factory (`SessionLocal`) to manage database sessions.
- Defines a declarative base class (`Base`) for all ORM models to inherit from.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os 

"""
SQLite database URL
- "sqlite" → database type (tells SQLAlchemy which database backend to use)
- "./fantasy_data.db" → relative path to the database file
"""
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), 'fantasy_data.db'))}"

"""
Engine:
- Core interface to the database
- `check_same_thread=False` → allows multiple threads to use the same connection safely
"""
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


"""
Session factory:
- autocommit=False → changes must be explicitly committed
- autoflush=False → avoids automatic writes until commit
- bind=engine → links session to our engine
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""
Base class for ORM models:
- All table classes (e.g., Player, Team) will inherit from this
"""
Base = declarative_base()
