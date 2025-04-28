from pydantic import BaseModel, Field, validator

class BMIInput(BaseModel):
    height: float = Field(..., gt=0, description="Height in meters")
    weight: float = Field(..., gt=0, description="Weight in kilograms")

class BMRInput(BaseModel):
    height: float = Field(..., gt=0, description="Height in centimeters")
    weight: float = Field(..., gt=0, description="Weight in kilograms")
    age: int = Field(..., gt=0, description="Age in years")
    gender: str = Field(..., description="Gender: 'male' or 'female'") # [cite: 29]

    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ('male', 'female'):
            raise ValueError("Gender must be 'male' or 'female'")
        return v.lower()