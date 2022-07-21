import sqlalchemy
import videostore.settings as settings
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(settings.DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
