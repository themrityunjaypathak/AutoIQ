# Standard Libraries
import logging

# Third-Party Libraries
import pandas as pd
from sigfig import round
from fastapi import FastAPI, Request, HTTPException
from babel.numbers import format_currency
from fastapi.middleware.cors import CORSMiddleware

# Rate Limiting Libraries
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler

# Local Modules
from api.config import settings
from api.models import lifespan
from api.schemas import Input, RootResponse, HealthResponse, PredictResponse

# Logging the Output
logging.basicConfig(level=logging.INFO, format="%(levelname)s:    %(message)s")
logger = logging.getLogger(__name__)

# Creating FastAPI App Instance
app = FastAPI(
    title="AutoIQ : Used Car Pricing System",
    description="Predicts a fair price range for used cars in (₹) using an XGBoost regression model.",
    version="1.0.0",
    lifespan=lifespan,
)

# Setting up Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS so frontend apps from different origins can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Root Endpoint
@app.get("/", tags=["General"], response_model=RootResponse)
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Pipeline is live"}


# Health Check Endpoint
@app.get("/health", tags=["Utility"], response_model=HealthResponse)
def health():
    logger.info("Health endpoint accessed")
    return {
        "status": "ok",
        "pipeline_loaded": app.state.pipe is not None,
        "model_frequency_loaded": app.state.model_freq is not None,
        "lower_pipeline_loaded": app.state.lower_pipe is not None,
        "upper_pipeline_loaded": app.state.upper_pipe is not None,
    }


# Prediction Endpoint
@app.post("/predict", tags=["Prediction"], response_model=PredictResponse)
@limiter.limit("5/minute")
async def predict(data: Input, request: Request):
    pipe = request.app.state.pipe
    model_freq = request.app.state.model_freq
    lower_pipe = request.app.state.lower_pipe
    upper_pipe = request.app.state.upper_pipe

    # Check if Models are Loaded
    if pipe is None:
        logger.error("Pipeline is not loaded")
        raise HTTPException(status_code=503, detail="Pipeline is not available")
    if model_freq is None:
        logger.error("Model frequency is not loaded")
        raise HTTPException(status_code=503, detail="Model frequency is not available")
    if lower_pipe is None or upper_pipe is None:
        logger.error("Range pipelines are not loaded")
        raise HTTPException(status_code=503, detail="Range pipelines are not available")

    try:
        input_data = pd.DataFrame(
            {
                "brand": [data.brand],
                "model_freq": [model_freq.get(data.model, 0)],
                "km_driven": [data.km_driven],
                "engine_capacity": [data.engine_capacity],
                "fuel_type": [data.fuel_type],
                "transmission": [data.transmission],
                "year": [data.year],
                "owner": [data.owner],
            }
        )
        logger.info("Input data prepared for prediction")

        lower_limit = max(round(lower_pipe.predict(input_data)[0]), 0)
        upper_limit = round(upper_pipe.predict(input_data)[0])
        if upper_limit < lower_limit:
            logger.warning(
                "Quantile crossing detected: upper prediction below lower, clamping"
            )
            upper_limit = lower_limit
        logger.info("Price range predicted successfully")

        format_lower = format_currency(lower_limit, "INR", locale="en_IN")
        format_upper = format_currency(upper_limit, "INR", locale="en_IN")

        result = f"{format_lower.split('.')[0]} to {format_upper.split('.')[0]}"
        logger.info("Prediction formatted successfully")
        return {"output": result}
    except Exception:
        logger.exception("Prediction failed due to an exception")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred during prediction"
        )
