from pydantic import BaseModel
from datetime import date
from pydantic import Field, field_validator


class YearRange(BaseModel):
    start_year: int = Field(..., ge=2000, le=date.today().year)
    end_year: int = Field(..., ge=2000, le=date.today().year)
    
    @field_validator('end_year')
    def end_year_must_be_after_start_year(cls, v, values):
        if 'start_year' in values.data and v < values.data['start_year']:
            raise ValueError('end_year must be equal or after start_year')
        return v