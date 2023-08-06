from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from regression_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if var
        not in config.model_config.categorical_vars_with_na_frequent
        + config.model_config.categorical_vars_with_na_missing
        + config.model_config.numerical_vars_with_na
        and validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)
    # input_data.rename(columns=config.model_config.variables_to_rename, inplace=True)
    # input_data["MSSubClass"] = input_data["MSSubClass"].astype("O")
    # relevant_data = input_data[config.model_config.features].copy()
    # validated_data = drop_na_inputs(input_data=relevant_data)
    validated_data = input_data[config.model_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleSalesDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class SalesDataInputSchema(BaseModel):
    feature_1: Optional[float]
    feature_3: Optional[float]
    feature_4: Optional[float]
    feature_5: Optional[float]
    feature_6: Optional[float]
    feature_7: Optional[float]
    feature_8: Optional[float]
    feature_10: Optional[float]
    feature_15: Optional[float]
    feature_16: Optional[float]
    feature_18: Optional[float]
    feature_19: Optional[float]
    feature_23: Optional[float]
    feature_24: Optional[float]
    feature_26: Optional[float]
    feature_27: Optional[float]
    feature_30: Optional[float]
    feature_31: Optional[float]
    feature_32: Optional[float]
    feature_33: Optional[float]
    feature_34: Optional[float]
    feature_37: Optional[float]
    feature_38: Optional[float]
    feature_39: Optional[float]
    feature_40: Optional[float]
    feature_43: Optional[float]
    feature_44: Optional[float]
    feature_45: Optional[float]
    feature_46: Optional[float]
    feature_47: Optional[float]
    feature_49: Optional[float]
    feature_51: Optional[float]
    feature_52: Optional[float]
    feature_54: Optional[float]
    feature_56: Optional[float]
    feature_59: Optional[float]
    feature_60: Optional[float]
    feature_61: Optional[float]
    feature_63: Optional[float]
    feature_64: Optional[float]
    feature_66: Optional[float]
    feature_69: Optional[float]
    feature_70: Optional[float]
    feature_74: Optional[float]
    feature_76: Optional[float]
    feature_78: Optional[float]
    feature_81: Optional[float]
    feature_83: Optional[float]
    feature_84: Optional[float]
    feature_85: Optional[float]
    feature_86: Optional[float]
    feature_87: Optional[float]
    feature_88: Optional[float]
    feature_91: Optional[float]
    feature_92: Optional[float]
    feature_93: Optional[float]
    feature_94: Optional[float]
    feature_95: Optional[float]
    feature_96: Optional[float]
    feature_97: Optional[float]
    feature_98: Optional[float]
    feature_99: Optional[float]
    dt_day: Optional[str]
    dt_week: Optional[str]
    dt_quater: Optional[str]
    dt_dayofweek: Optional[str]
    dt_is_weekend: Optional[str]


class MultipleSalesDataInputs(BaseModel):
    inputs: List[SalesDataInputSchema]
