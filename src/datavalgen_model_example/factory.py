from datetime import date, timedelta
from typing import Literal

from datavalgen.factory import BaseDataModelFactory
from polyfactory.decorators import post_generated

from .model import FullDataModel


class DataModelFactory(BaseDataModelFactory):
    """Factory for generating example data model instances."""

    __model__ = FullDataModel

    @classmethod
    def sex(cls) -> Literal["F", "M", "X"]:
        # Weighted categorical sampling for the requested F/M/X mix.
        roll = cls.__random__.random()
        if roll < (45 / 95):
            return "F"
        if roll < (90 / 95):
            return "M"
        return "X"

    @post_generated
    @classmethod
    def height_cm(cls, sex: Literal["F", "M", "X"]) -> float:
        # Use sex-specific normal distributions, then clamp to plausible bounds.
        mean_height_cm = {
            "F": 165.0,
            "M": 178.0,
            "X": 171.5,
        }[sex]
        sd_height_cm = {
            "F": 6.5,
            "M": 7.0,
            "X": 6.75,
        }[sex]
        value = cls.__random__.gauss(mean_height_cm, sd_height_cm)
        return round(min(max(value, 140.0), 210.0), 1)

    @post_generated
    @classmethod
    def weight_kg(cls, height_cm: float, sex: Literal["F", "M", "X"]) -> float:
        # Correlate weight with height through a noisy BMI-like calculation.
        mean_bmi = {
            "F": 23.0,
            "M": 25.0,
            "X": 24.0,
        }[sex]
        bmi = cls.__random__.gauss(mean_bmi, 3.0)
        bmi = min(max(bmi, 17.0), 40.0)
        height_m = height_cm / 100.0
        weight_kg = bmi * (height_m**2)
        return round(min(max(weight_kg, 40.0), 180.0), 1)

    @post_generated
    @classmethod
    def discharge_date(cls, admission_date: date) -> date:
        # Keep admission/discharge dates internally consistent.
        return cls.__faker__.date_between_dates(
            date_start=admission_date,
            date_end=cls.get_field_constraint("discharge_date", "lt"),
        )

    @post_generated
    @classmethod
    def end_date(cls, start_date: date) -> date:
        # Start/end dates must be strictly ordered.
        return cls.__faker__.date_between_dates(
            date_start=start_date + timedelta(days=1),
            date_end=cls.get_field_constraint("end_date", "lt"),
        )

    @classmethod
    def mortality_30d(cls) -> Literal["Yes", "No"]:
        # Mortality is generated cumulatively so later windows cannot revert.
        return "Yes" if cls.__random__.random() < 0.05 else "No"

    @post_generated
    @classmethod
    def mortality_60d(cls, mortality_30d: Literal["Yes", "No"]) -> Literal["Yes", "No"]:
        if mortality_30d == "Yes":
            return "Yes"
        return "Yes" if cls.__random__.random() < 0.03 else "No"

    # NOTE: For more complex (higher quality) fake data generation, using
    # `@post_generated` or polyfactory is probably not the idea solution.
    # Complex: may rules about columns that depend on each other, etc.
    @post_generated
    @classmethod
    def mortality_90d(cls, mortality_60d: Literal["Yes", "No"]) -> Literal["Yes", "No"]:
        if mortality_60d == "Yes":
            return "Yes"
        return "Yes" if cls.__random__.random() < 0.02 else "No"
