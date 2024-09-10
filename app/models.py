from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Database models
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(length=50), index=True)
    model = Column(String(length=50), index=True)
    production_year = Column(Integer)

    ratings = relationship("CarRating", back_populates="car")

class CarRating(Base):
    __tablename__ = "car_ratings"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    rating = Column(Integer)

    car = relationship("Car", back_populates="ratings")