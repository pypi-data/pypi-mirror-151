import feature_engine.transformation as vt
import joblib
from feature_engine.encoding import OrdinalEncoder
from feature_engine.imputation import MeanMedianImputer
from feature_engine.outliers import Winsorizer
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline

# from regression_model.processing import features as pp
from sklearn.preprocessing import MinMaxScaler

# from feature_engine.encoding import OrdinalEncoder, RareLabelEncoder
# from feature_engine.imputation import (
#     AddMissingIndicator,
#     CategoricalImputer,
#     MeanMedianImputer,
# )
# from feature_engine.selection import DropFeatures
# from feature_engine.transformation import LogTransformer
# from feature_engine.wrappers import SklearnTransformerWrapper
# from sklearn.linear_model import Lasso
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import Binarizer, MinMaxScaler
#
from regression_model.config.core import config

# Loading best performing model devloped in the model development script
LASSO_RESULT = joblib.load(f"./../model/LASSO_model.sav")


sale_pipe = Pipeline(
    [
        # ===== IMPUTATION ===== with the mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        # ==== CATEGORICAL ENCODING ==== using the target mean
        (
            "categorical_encoding",
            OrdinalEncoder(
                encoding_method="ordered",
                variables=config.model_config.categorical_vars,
            ),
        ),
        # ==== VARIABLE TRANSFORMATION ====
        (
            "variable_transformation",
            vt.YeoJohnsonTransformer(variables=config.model_config.features),
        ),
        # ==== OUTLIER HANDLING ====
        (
            "winsorizer_capping",
            Winsorizer(
                capping_method="gaussian",
                tail="both",  # cap left, right or both tails
                fold=3,
                variables=config.model_config.features,
            ),
        ),
        # ==== FEATURE SCALING ====
        ("scaler", MinMaxScaler()),
        # ==== MODEL TRAINING ====
        ("Lasso", LASSO_RESULT),
    ]
)
