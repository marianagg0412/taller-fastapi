from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Query, status
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
        if calendar.price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio no puede ser negativo."
            )

        if calendar.minimum_nights < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La estancia mínima no puede ser menor que 1."
            )

        if calendar.maximum_nights < calendar.minimum_nights:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La estancia máxima no puede ser menor que la estancia mínima."
            )
        if calendar.available not in ["t", "f"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El valor de disponibilidad debe ser 't' o 'f'."
            )
        if calendar.listing_id < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de la lista no puede ser negativo."
            )

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
        # Return HTTP exception with status code and message
        raise e
    
    except Exception as e:
        # Handle any other exceptions and return a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error en el servidor: " + str(e)
        )


@app.get("/calendar/", response_model=list[Calendar])
def read_items(
   db: Session = Depends(get_db),
   page: int = Query(1, ge=1),  # Page number, starting from 1
   limit: int = Query(100, le=100, ge=1),  
   start_date: Optional[datetime] = None,  
   end_date: Optional[datetime] = None, 
   min_price: Optional[float] = None,  
   max_price: Optional[float] = None,  #Query(None) differs from None in that it will be present in the query string, but with no value
   available: Optional[str] = None,
):
   query = db.query(CalendarModel)

   if start_date:
       if end_date is not None and start_date > end_date:
           raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor que la fecha de fin")
       query = query.filter(CalendarModel.date >= start_date)
   if end_date:
       if start_date is not None and end_date < start_date:
           raise HTTPException(status_code=400, detail="La fecha de fin no puede ser menor que la fecha de inicio")
       query = query.filter(CalendarModel.date <= end_date)
   if min_price is not None:
       if min_price < 0:
           raise HTTPException(status_code=400, detail="El precio mínimo no puede ser negativo")
       query = query.filter(CalendarModel.price >= min_price)
   if max_price is not None:
       if max_price < 0:
           raise HTTPException(status_code=400, detail="El precio máximo no puede ser negativo")
       query = query.filter(CalendarModel.price <= max_price)
   if available:
       if available not in ["t", "f"]:
           raise HTTPException(status_code=400, detail="El valor de disponibilidad debe ser 't' o 'f'")
       query = query.filter(CalendarModel.available == available)
   # Calculate offset for pagination
   offset = (page - 1) * limit
   # Apply limit and offset for pagination
   items = query.offset(offset).limit(limit).all()
   if not items:
       raise HTTPException(status_code=404, detail="No hay registros en la base de datos")
   return items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
