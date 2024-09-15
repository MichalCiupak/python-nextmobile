from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from typing import List

from .models import Car, CarRating
from .schemas import CarCreate, CarResult, RatingCreate
from .database import get_db

app = FastAPI()


# API endpoints
@app.post("/cars/")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    return {"message": "Car added"}


@app.post("/cars/{car_id}/rate")
def rate_car(car_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db_rating = CarRating(car_id=car_id, rating=rating.rating)
    db.add(db_rating)
    db.commit()
    return {"message": "Rating added"}


@app.get("/cars/top10", response_model=List[CarResult])
def get_top_10_cars(db: Session = Depends(get_db)):
    from sqlalchemy import func

    cars = (
        db.query(Car, func.avg(CarRating.rating).label("average_rating"))
        .join(Car.ratings)
        .group_by(Car.id)
        .order_by(func.avg(CarRating.rating).desc())
        .limit(10)
        .all()
    )

    return [
        CarResult(
            id=car.Car.id,
            brand=car.Car.brand,
            model=car.Car.model,
            production_year=car.Car.production_year,
            average_rating=car.average_rating,
        )
        for car in cars
    ]
