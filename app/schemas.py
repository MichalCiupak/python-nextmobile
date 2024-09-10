from pydantic import BaseModel, Field

# Data models
class CarCreate(BaseModel):
    brand: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    production_year: int

class RatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)

class CarResult(BaseModel):
    id: int
    brand: str
    model: str
    production_year: int
    average_rating: float = None
