import typing as t

import numpy as np
import pandas as pd

from regression_model import __version__ as _version
from regression_model.config.core import config
from regression_model.processing import features as pp
from regression_model.processing.data_manager import load_pipeline
from regression_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_sales_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    data = pp.date_variable_extractor(data, "date")
    validated_data, errors = validate_inputs(input_data=data)
    print("YOOOOO IM TESTING HERE")
    print(data.iloc[0], len(data))
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _sales_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [pred for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results
