import numpy as np
from config.core import config
from pipeline import sale_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split

from regression_model.processing import features as pp


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)
    data = pp.date_variable_extractor(data, "date")

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    y_train = y_train

    # fit model
    sale_pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=sale_pipe)


if __name__ == "__main__":
    run_training()
