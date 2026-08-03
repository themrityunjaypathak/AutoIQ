# Standard Libraries
from enum import Enum

# Third-Party Libraries
from pydantic import BaseModel, Field


# Input validation for fuel_type
class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    CNG = "CNG"


# Input validation for transmission
class Transmission(str, Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"


# Input validation for owner
class OwnerType(str, Enum):
    FIRST = "1st owner"
    SECOND = "2nd owner"
    THIRD = "3rd owner"
    OTHERS = "Others"


# Define Input Data Schema using Pydantic
class Input(BaseModel):
    brand: str = Field(..., description="Brand Name of your Car", examples=["MG"])
    model: str = Field(..., description="Model Name of your Car", examples=["HECTOR"])
    km_driven: int = Field(
        ..., ge=1000, le=200000, description="KM Driven of your Car", examples=[80000]
    )
    engine_capacity: int = Field(
        ...,
        ge=700,
        le=3000,
        description="Engine Capacity (in cc) of your Car",
        examples=[1498],
    )
    fuel_type: FuelType = Field(
        ..., description="Fuel Type of your Car", examples=["Petrol"]
    )
    transmission: Transmission = Field(
        ..., description="Transmission of your Car", examples=["Manual"]
    )
    year: int = Field(
        ...,
        ge=2010,
        le=2024,
        description="Manufacture Year of your Car",
        examples=[2022],
    )
    owner: OwnerType = Field(
        ..., description="Owner Type of your Car", examples=["1st owner"]
    )


# Response Schema for Root Endpoint
class RootResponse(BaseModel):
    message: str = Field(..., examples=["Pipeline is live"])


# Response Schema for Health Endpoint
class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    pipeline_loaded: bool = Field(..., examples=[True])
    model_frequency_loaded: bool = Field(..., examples=[True])
    lower_pipeline_loaded: bool = Field(..., examples=[True])
    upper_pipeline_loaded: bool = Field(..., examples=[True])


# Response Schema for Prediction Endpoint
class PredictResponse(BaseModel):
    output: str = Field(..., examples=["₹7,81,412 to ₹12,66,018"])
