from app.schemas.trips import TripReq
from pydantic import ValidationError

import logging
logger = logging.getLogger(__name__)

def validate_trip_request(trip):
    try:
        user_trip = TripReq(**trip)
        return user_trip
     
    except ValidationError as e:
        logger.info(f"←  Validation Errror :{e}")