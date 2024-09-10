import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api import app
from app.database import get_db, Base
from app.models import Car

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Mock db session
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_car_ok(setup_database):
    response = client.post(
        "/cars/", json={"brand": "Toyota", "model": "Corolla", "production_year": 2022}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Car added"}


def test_create_car_long_name_error(setup_database):
    response = client.post(
        "/cars/",
        json={"brand": "Toyota" * 10, "model": "Corolla", "production_year": 2022},
    )

    assert response.status_code == 422


def test_rate_car_ok(setup_database):
    client.post(
        "/cars/", json={"brand": "Honda", "model": "Civic", "production_year": 2021}
    )
    car_id = setup_database.query(Car).filter(Car.brand == "Honda").first().id
    response = client.post(f"/cars/{car_id}/rate", json={"rating": 5})

    assert response.status_code == 200
    assert response.json() == {"message": "Rating added"}


def test_rate_car_invalid_rating(setup_database):
    client.post(
        "/cars/", json={"brand": "Honda", "model": "Civic", "production_year": 2021}
    )
    car_id = setup_database.query(Car).filter(Car.brand == "Honda").first().id
    response = client.post(f"/cars/{car_id}/rate", json={"rating": 6})

    assert response.status_code == 422


def test_rate_car_invalid_car_id(setup_database):
    client.post(
        "/cars/", json={"brand": "Honda", "model": "Civic", "production_year": 2021}
    )
    response = client.post(f"/cars/{0}/rate", json={"rating": 4})

    assert response.json() == {"detail": "Car not found"}
    assert response.status_code == 404


def test_get_top_10_cars_fewer_in_db(setup_database):
    client.post(
        "/cars/", json={"brand": "Ford", "model": "Focus", "production_year": 2020}
    )
    client.post(
        "/cars/", json={"brand": "Honda", "model": "Civic", "production_year": 2020}
    )

    client.post(f"/cars/1/rate", json={"rating": 4})
    client.post(f"/cars/2/rate", json={"rating": 3})
    client.post(f"/cars/2/rate", json={"rating": 2})
    response = client.get("/cars/top10")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["brand"] == "Ford"
    assert response.json()[0]["average_rating"] == 4.0
    assert response.json()[1]["brand"] == "Honda"
    assert response.json()[1]["average_rating"] == 2.5


def test_get_top_10_cars(setup_database):
    client.post(
        "/cars/", json={"brand": "Ford", "model": "Focus", "production_year": 2020}
    )
    client.post(
        "/cars/", json={"brand": "Honda", "model": "Civic", "production_year": 2020}
    )
    client.post(
        "/cars/", json={"brand": "Toyota", "model": "Corolla", "production_year": 2021}
    )
    client.post(
        "/cars/", json={"brand": "Ford", "model": "Focus", "production_year": 2019}
    )
    client.post(
        "/cars/",
        json={"brand": "Chevrolet", "model": "Malibu", "production_year": 2022},
    )
    client.post(
        "/cars/", json={"brand": "Nissan", "model": "Altima", "production_year": 2020}
    )
    client.post(
        "/cars/", json={"brand": "BMW", "model": "3 Series", "production_year": 2018}
    )
    client.post(
        "/cars/",
        json={"brand": "Mercedes", "model": "C-Class", "production_year": 2021},
    )
    client.post(
        "/cars/", json={"brand": "Audi", "model": "A4", "production_year": 2019}
    )
    client.post(
        "/cars/",
        json={"brand": "Volkswagen", "model": "Passat", "production_year": 2020},
    )
    client.post(
        "/cars/", json={"brand": "Hyundai", "model": "Elantra", "production_year": 2022}
    )

    client.post(f"/cars/1/rate", json={"rating": 4})
    client.post(f"/cars/2/rate", json={"rating": 3})
    client.post(f"/cars/3/rate", json={"rating": 2})
    client.post(f"/cars/4/rate", json={"rating": 2})
    client.post(f"/cars/5/rate", json={"rating": 2})
    client.post(f"/cars/6/rate", json={"rating": 2})
    client.post(f"/cars/7/rate", json={"rating": 2})
    client.post(f"/cars/8/rate", json={"rating": 2})
    client.post(f"/cars/9/rate", json={"rating": 2})
    client.post(f"/cars/10/rate", json={"rating": 2})
    client.post(f"/cars/11/rate", json={"rating": 2})
    response = client.get("/cars/top10")

    assert response.status_code == 200
    assert len(response.json()) == 10
