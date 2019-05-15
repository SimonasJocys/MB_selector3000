import numpy as np
import pandas as pd

import func as func
from sklearn.metrics import (
    auc,
    accuracy_score,
    confusion_matrix,
    mean_squared_error,
)
import xgboost as xgb
import pickle

Hela_data = pd.read_csv("Hela_data.csv")
mb_data = pd.read_csv("mb_data.csv")

# Ar čia tinkamas mb_data failas????
# Preprocess and combine =======================================================

# MB part
print(mb_data.shape)

mb_data = func.preprocess_strings(mb_data)
mb_data = func.drop_cols(mb_data)
mb_data = func.code_non_strings(mb_data)

mb_data["label"] = 1

print(mb_data.shape)

# Hela part
print(Hela_data.shape)

# Pasiimama tiek Hela baltymų kiek yra MB baltymų - ar to reikia?
# Hela_data = Hela_data.sample(mb_data.shape[0], random_state = 42)

Hela_data = func.preprocess_strings(Hela_data)
Hela_data = func.drop_cols(Hela_data)
Hela_data = func.code_non_strings(Hela_data)

Hela_data["label"] = 0

print(Hela_data.shape)

# Combine
data_train = pd.concat([mb_data, Hela_data], sort=False)
data_train = data_train[~data_train.index.duplicated(keep="first")]

print(data_train.shape)

df = data_train[data_train.T[data_train.dtypes != np.object].index]
print(df.shape)

X = df.loc[:, df.columns != "label"].values
y = df.label.values

# Model training ===============================================================

df = data_train[data_train.T[data_train.dtypes != np.object].index]
print(df.shape)

X = df.loc[:, df.columns != "label"].values
y = df.label.values

xgb_model = xgb.XGBClassifier(
    objective="binary:logistic", eta=0.01, scale_pos_weight=50, random_state=42
)

xgb_model.fit(X, y)

# Metrics ======================================================================
# Saving========================================================================

pickle.dump(xgb_model, open("model", "wb"))
