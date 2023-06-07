"""
Database
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config.settings import CurrentSettings

Base = declarative_base()


def get_engine(settings: CurrentSettings) -> Engine:
    """Database engine"""

    # Create engine
    engine = create_engine(f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}")

    return engine


def get_db(settings: CurrentSettings) -> Session:
    """Database session"""

    # Create engine
    engine = get_engine(settings)

    # Create session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        db = session_local()
        yield db
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]
