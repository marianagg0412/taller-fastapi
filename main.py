from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()
# Configuración de la base de datos
DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo SQLAlchemy (para la base de datos)
class CalendarModel(Base):
    __tablename__ = "calendar"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    available = Column(String, index=True)
    price = Column(Float)
    minimum_nights = Column(Integer)
    maximum_nights = Column(Integer)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Modelo Pydantic (para validación)
class Calendar(BaseModel):
    listing_id: int
    date: datetime
    available: str
    price: float
    minimum_nights: int
    maximum_nights: int

    class Config:
        orm_mode = True  # Esto permite que Pydantic trabaje con modelos de SQLAlchemy

# Operación POST para crear un nuevo calendario
@app.post("/calendar/")
def create_item(calendar: Calendar, db: Session = Depends(get_db)):

    try:

        count_before = db.query(CalendarModel).count()

        db_calendar = CalendarModel(
            listing_id=calendar.listing_id,
            date=calendar.date,
            available=calendar.available,
            price=calendar.price,
            minimum_nights=calendar.minimum_nights,
            maximum_nights=calendar.maximum_nights
        )
        db.add(db_calendar)
        db.commit()
        db.refresh(db_calendar)

        count_after = db.query(CalendarModel).count()

        return {
            "message": "Registro agregado exitosamente",
            "new_item": db_calendar,
            "count_before": count_before,
            "count_after": count_after,
            "records_added": count_after - count_before,
            "calendar": db_calendar
        }
    except HTTPException as e:
        return {"error": str(e),
                "code": e.status_code}


@app.get("/calendar/", response_model=list[Calendar])
def read_items(db: Session = Depends(get_db)):
    items = db.query(CalendarModel).all()
    return items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
