from typing import Literal
from pydantic import BaseModel, model_validator
from pydantic import Field
from datetime import date


class DataModel(BaseModel):
    # some example 'id', must be greater than 0
    id: int = Field(..., gt=0)

    # some example 'name', must be a string
    name: str = Field(..., min_length=1, max_length=25)

    # some example 'status', must be either "Yes" or "No"
    status: Literal["Yes", "No"] = Field(..., description="Boolean status")

    # we expect an average between 30 and 40, but doesn't belong to pydantic validation
    age: int = Field(..., ge=0, le=120)

    # example with dates
    start_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))
    end_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))

    # make sure start_date is before end_date
    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self
