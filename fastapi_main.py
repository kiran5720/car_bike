from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models import Base, User, Location, Vehicle, Booking, Payment, Review  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt


DATABASE_URL = "postgresql://postgres:admin@localhost:5432/car_bike"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(plain_text_pass):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_pass.encode('utf-8'),salt)
    return hashed_password

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str]
    role: str

class LocationCreate(BaseModel):
    location_name: str
    address: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]

class VehicleCreate(BaseModel):
    vehicle_type: str
    make: str
    model: str
    year: int
    bike_specs: Optional[str]
    car_specs: Optional[str]
    hourly_rate: float
    daily_rate: float
    weekly_rate: float
    availability: Optional[bool] = True
    location_id: int

class BookingCreate(BaseModel):
    user_id: int
    vehicle_id: int
    start_date: datetime
    end_date: datetime
    total_cost: float
    status: str

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_status: str
    payment_method: str

class ReviewCreate(BaseModel):
    user_id: int
    vehicle_id: int
    rating: int
    comment: Optional[str]



@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(**user.dict(exclude={'password'}),
                   password = hashed_password, 
                   created_at=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/locations/", response_model=LocationCreate)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.post("/vehicles/", response_model=VehicleCreate)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**vehicle.dict(), created_at=datetime.utcnow())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.post("/bookings/", response_model=BookingCreate)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(**booking.dict(), created_at=datetime.utcnow())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.post("/payments/", response_model=PaymentCreate)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict(), payment_date=datetime.utcnow())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@app.post("/reviews/", response_model=ReviewCreate)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict(), review_date=datetime.utcnow())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
