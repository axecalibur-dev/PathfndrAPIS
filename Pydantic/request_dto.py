from typing import Optional

from pydantic import BaseModel, field_validator
from datetime import datetime
import re


class FlightRequestDto(BaseModel):
    originCode: str
    destinationCode: str
    date: str
    no_cache: Optional[int] = 0

    @field_validator('originCode', 'destinationCode')
    def validate_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('Must be a string')
        if not re.match(r'^[A-Za-z]+$', v):
            raise ValueError(f'originCode and destinationCode must contain only alphabetical characters')
        return v

    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('date must be in the format YYYY-MM-DD')
        return v

    @field_validator('no_cache')
    def validate_cache_flag(cls, v):
        if v is not None:
            if v not in [0, 1]:
                raise ValueError('no_cache must be 0 or 1')
        return v