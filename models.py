
from scipy.sparse import data
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import pandas as pd
import numpy as np
import pickle

MODELS = ['dtree', 'random_forest', 'svm', 'lgbm', 'xgboost']


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols = list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    # put it all together
    agg = pd.concat(cols, axis=1)
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)

    return agg.values


def get_training_model(X_train, y_train, model="dtree", svm_kernel="rbf", params=None, col_features=None):
    result = None

    if model == "dtree":
        result = DecisionTreeRegressor(
            max_depth=8)
        result.fit(X_train, y_train)
    elif model == "random_forest":
        result = RandomForestRegressor(
            n_estimators=10000, oob_score=True, max_depth=8)
        result.fit(X_train, y_train)
    elif model == "svm":
        result = svm.SVR(kernel="linear")
        #  {'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'}
        result.fit(X_train, y_train)
    elif model == "xgboost":
        result = XGBRegressor(
            objective='reg:squarederror', n_estimators=10000, max_depth=8)
        result.fit(X_train, y_train)
    elif model == "lgbm":
        result = LGBMRegressor(
            max_depth=8, n_estimators=10000, learning_rate=0.001)
        result.fit(X_train, y_train)
    return result


def main():
    aqi_sensor_hours = pd.read_csv("data/aqi_data_hours.csv")
    values = aqi_sensor_hours.values

    lag = 2

    supervise_values = series_to_supervised(values, n_in=lag, n_out=lag)
    n_obs = len(aqi_sensor_hours.columns) * lag
    num_test = int(len(aqi_sensor_hours) * 0.2) + 1

    train = supervise_values[:-num_test]

    test = supervise_values[-num_test:]

    X_train, y_train = train[:,
                             :n_obs], train[:, -1]

    X_test, y_test = test[:,
                          :n_obs], test[:, -1]
    y_actual = {}
    for i in range(len(y_test)):
        y_actual[i] = y_test[i]
    y_act_df = pd.DataFrame.from_dict(y_actual, orient="index").reset_index()

    y_act_df.to_csv("result/y_actual.csv", index=False)

    scores = {}
    for m in MODELS:
        m: str

        model_trained = get_training_model(X_train, y_train, m)

        file_name = "model/" + m + '.sav'
        pickle.dump(model_trained, open(file_name, 'wb'))

        pred_test = model_trained.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, pred_test))
        r_square = r2_score(y_test, pred_test)
        print(" *"*20, "MODEL: ", m, " *"*20)
        print("RMSE test: ", rmse)
        print("R-squared test: ", r_square)
        print("\n")
        scores[m] = {'rmse': rmse, 'r_square': r_square}
        y_pred = {}
        for i in range(len(pred_test)):
            y_pred[i] = pred_test[i]
        y_pred_df = pd.DataFrame.from_dict(
            y_pred, orient="index").reset_index()

        y_pred_df.to_csv(
            "result/y_pred_"+m+".csv", index=False)

    scores_df = pd.DataFrame.from_dict(scores, orient="index").reset_index()
    scores_df.columns = ["model", "rmse", "r_square"]
    scores_df.to_csv("result/score.csv", index=False)


if __name__ == '__main__':
    main()
