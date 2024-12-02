from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Enum, ForeignKey, Boolean, DECIMAL, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ENUM as PGEnum  # Use PostgreSQL ENUM type
from datetime import datetime

# Define the Base for declarative class definitions
Base = declarative_base()

# Define the Users table
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    phone = Column(String(15))
    role = Column(PGEnum('Admin', 'Customer', 'Service Provider', name='user_roles'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

# Define the Locations table
class Location(Base):
    __tablename__ = 'locations'
    
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    address = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(10))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))

# Define the Vehicles table
class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    vehicle_id = Column(Integer, primary_key=True)
    vehicle_type = Column(PGEnum('Car', 'Bike', name='vehicle_types'), nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    bike_specs = Column(Text)
    car_specs = Column(Text)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    daily_rate = Column(DECIMAL(10, 2), nullable=False)
    weekly_rate = Column(DECIMAL(10, 2), nullable=False)
    availability = Column(Boolean, default=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    location = relationship('Location', back_populates='vehicles')

Location.vehicles = relationship('Vehicle', order_by=Vehicle.vehicle_id, back_populates='location')

# Define the Bookings table
class Booking(Base):
    __tablename__ = 'bookings'
    
    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    status = Column(PGEnum('Pending', 'Confirmed', 'Cancelled', 'Completed', name='booking_status'), default='Pending')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    user = relationship('User', back_populates='bookings')
    vehicle = relationship('Vehicle', back_populates='bookings')

User.bookings = relationship('Booking', order_by=Booking.booking_id, back_populates='user')
Vehicle.bookings = relationship('Booking', order_by=Booking.booking_id, back_populates='vehicle')

# Define the Payments table
class Payment(Base):
    __tablename__ = 'payments'
    
    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(PGEnum('Pending', 'Completed', 'Refunded', name='payment_status'), default='Pending')
    payment_date = Column(TIMESTAMP, default=datetime.utcnow)
    payment_method = Column(PGEnum('Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', name='payment_methods'))
    
    booking = relationship('Booking', back_populates='payments')

Booking.payments = relationship('Payment', order_by=Payment.payment_id, back_populates='booking')

# Define the Reviews table
class Review(Base):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    review_date = Column(TIMESTAMP, default=datetime.utcnow)
    
    user = relationship('User', back_populates='reviews')
    vehicle = relationship('Vehicle', back_populates='reviews')

User.reviews = relationship('Review', order_by=Review.review_id, back_populates='user')
Vehicle.reviews = relationship('Review', order_by=Review.review_id, back_populates='vehicle')
