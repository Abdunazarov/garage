from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Renter(Base):
    __tablename__ = 'renters'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    rentals = relationship("Rental", back_populates="renter")

class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)

    rentals = relationship("Rental", back_populates="car")

class Rental(Base):
    __tablename__ = 'rentals'
    
    id = Column(Integer, primary_key=True, index=True)
    renter_id = Column(Integer, ForeignKey('renters.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)
    issue_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    deposit = Column(Float, nullable=False)
    mileage = Column(Float)
    fuel_cost = Column(Float)
    other_expenses = Column(Float)
    
    renter = relationship("Renter", back_populates="rentals")
    car = relationship("Car", back_populates="rentals")
