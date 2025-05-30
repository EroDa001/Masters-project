from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier

from experiments.config import RANDOM_SEED


def create_model(params):
    return CatBoostClassifier(
        iterations=int(params["iterations"]),
        depth=int(params["depth"]),
        learning_rate=params["learning_rate"],
        subsample=params["subsample"],
        rsm=params["colsample_bytree"],  # equivalent to colsample_bytree in CatBoost
        loss_function="Logloss",
        random_seed=RANDOM_SEED,
        verbose=0,  # suppress training output
        thread_count=-1,
    )


def default_params():
    return {
        "iterations": 100,
        "depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
    }


def param_space():
    return [
        {
            "name": "iterations",
            "type": "categorical",
            "categories": list(range(50, 301, 25)),
        },
        {"name": "depth", "type": "categorical", "categories": list(range(3, 13))},
        {"name": "learning_rate", "type": "continuous", "bounds": [0.01, 0.3]},
        {"name": "subsample", "type": "continuous", "bounds": [0.5, 1.0]},
        {"name": "colsample_bytree", "type": "continuous", "bounds": [0.5, 1.0]},
    ]


def evaluate(model, X_val, y_val):
    y_pred = model.predict(X_val)
    return accuracy_score(y_val, y_pred)
