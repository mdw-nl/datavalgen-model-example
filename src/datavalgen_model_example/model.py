from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator


# Example schema split into functional models so composed models can reuse the
# same pieces without repeating field definitions and make it easier to validate
# meaningful subsets of the full data model.
class IdentityAdminModel(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=25)
    site_code: Literal["SITE_A", "SITE_B", "SITE_C"]
    record_source: Literal["ehr", "registry", "manual"]


class DemographicsModel(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sex: Literal["F", "M", "X"]
    height_cm: float = Field(..., ge=50.0, le=250.0)
    weight_kg: float = Field(..., ge=2.0, le=300.0)


class EpisodeDatesModel(BaseModel):
    start_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))
    end_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))
    admission_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))
    discharge_date: date = Field(..., ge=date(1970, 1, 1), lt=date(2000, 1, 1))

    @model_validator(mode="after")
    def check_date_ranges(self):
        # Keep the two date pairs internally consistent.
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        if self.admission_date > self.discharge_date:
            raise ValueError("admission_date must be on or before discharge_date")
        return self


class ClinicalOutcomeModel(BaseModel):
    status: Literal["Yes", "No"] = Field(..., description="Boolean status")
    smoker: Literal["Yes", "No"]
    diagnosis_code: Literal["DX001", "DX002", "DX003", "DX004"]
    symptom_score: int = Field(..., ge=0, le=10)
    response_status: Literal["improved", "stable", "worsened"]
    mortality_30d: Literal["Yes", "No"]


class DemographicsClinicalOutcomeModel(
    DemographicsModel,
    ClinicalOutcomeModel,
):
    pass


class FullDataModel(
    IdentityAdminModel,
    DemographicsModel,
    EpisodeDatesModel,
    ClinicalOutcomeModel,
):
    # Full example schema assembled from the smaller functional groups above.
    pass
