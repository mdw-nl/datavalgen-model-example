from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


# Example schema split into functional models so composed models can reuse the
# same pieces without repeating field definitions and make it easier to validate
# meaningful subsets of the full data model.
class IdentityAdminModel(BaseModel):
    id: Annotated[int, Field(gt=0, description="Positive record identifier.")]
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=25,
            description="Fictional person name or pseudonym.",
        ),
    ]
    site_code: Annotated[
        Literal["SITE_A", "SITE_B", "SITE_C"],
        Field(description="Fictional site identifier."),
    ]
    record_source: Annotated[
        Literal["ehr", "registry", "manual"],
        Field(description="Origin of the record within the fictional data flow."),
    ]


class DemographicsModel(BaseModel):
    age: Annotated[
        int,
        Field(ge=0, le=120, description="Age in completed years."),
    ]
    sex: Annotated[
        Literal["F", "M", "X"],
        Field(description="Administrative sex marker for the fictional subject."),
    ]
    height_cm: Annotated[
        float,
        Field(ge=50.0, le=250.0, description="Height in centimeters."),
    ]
    weight_kg: Annotated[
        float,
        Field(ge=2.0, le=300.0, description="Weight in kilograms."),
    ]


class EpisodeDatesModel(BaseModel):
    start_date: Annotated[
        date,
        Field(
            ge=date(1970, 1, 1),
            lt=date(2000, 1, 1),
            description="Start date of the fictional observation period.",
        ),
    ]
    end_date: Annotated[
        date,
        Field(
            ge=date(1970, 1, 1),
            lt=date(2000, 1, 1),
            description="End date of the fictional observation period.",
        ),
    ]
    admission_date: Annotated[
        date,
        Field(
            ge=date(1970, 1, 1),
            lt=date(2000, 1, 1),
            description="Admission date for the fictional episode of care.",
        ),
    ]
    discharge_date: Annotated[
        date,
        Field(
            ge=date(1970, 1, 1),
            lt=date(2000, 1, 1),
            description="Discharge date for the fictional episode of care.",
        ),
    ]

    @model_validator(mode="after")
    def check_date_ranges(self):
        # Keep the two date pairs internally consistent.
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        if self.admission_date > self.discharge_date:
            raise ValueError("admission_date must be on or before discharge_date")
        return self


class ClinicalOutcomeModel(BaseModel):
    status: Annotated[
        Literal["Yes", "No"],
        Field(description="General binary status flag for the fictional record."),
    ]
    smoker: Annotated[
        Literal["Yes", "No"],
        Field(description="Whether the fictional subject is marked as a smoker."),
    ]
    diagnosis_code: Annotated[
        Literal["DX001", "DX002", "DX003", "DX004"],
        Field(description="Fictional diagnosis code."),
    ]
    symptom_score: Annotated[
        int,
        Field(ge=0, le=10, description="Symptom severity score on a 0-10 scale."),
    ]
    response_status: Annotated[
        Literal["improved", "stable", "worsened"],
        Field(description="Clinical response category at follow-up."),
    ]
    mortality_30d: Annotated[
        Literal["Yes", "No"],
        Field(description="Whether death occurred within 30 days."),
    ]
    mortality_60d: Annotated[
        Literal["Yes", "No"],
        Field(description="Whether death occurred within 60 days."),
    ]
    mortality_90d: Annotated[
        Literal["Yes", "No"],
        Field(description="Whether death occurred within 90 days."),
    ]
    

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
