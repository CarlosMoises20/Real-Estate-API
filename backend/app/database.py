from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.constants import *

db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/real_estate"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)