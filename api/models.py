# Standard Libraries
import pickle
import logging
from contextlib import asynccontextmanager

# Third-Party Libraries
from fastapi import FastAPI

# Local Modules
from api.config import settings

logger = logging.getLogger(__name__)


# Loading Pipeline, Model Frequency, and Range Pipelines
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipe = None
    app.state.model_freq = None
    app.state.lower_pipe = None
    app.state.upper_pipe = None

    try:
        with open(settings.PIPE_PATH, "rb") as f:
            app.state.pipe = pickle.load(f)
            logger.info("Pipeline loaded successfully")
        with open(settings.MODEL_FREQ_PATH, "rb") as f:
            app.state.model_freq = pickle.load(f)
            logger.info("Model frequency loaded successfully")
        with open(settings.LOWER_PIPE_PATH, "rb") as f:
            app.state.lower_pipe = pickle.load(f)
            logger.info("Lower bound pipeline loaded successfully")
        with open(settings.UPPER_PIPE_PATH, "rb") as f:
            app.state.upper_pipe = pickle.load(f)
            logger.info("Upper bound pipeline loaded successfully")
    except Exception:
        logger.exception("Model loading failed")

    yield
