import pandas as pd
import datetime
import numpy as np
from pandas.core.frame import DataFrame
import plotly.express as px
import aqi
import datetime

base_dir = "data/"
sensor_dir = "sensor_data_in_"
traffic_dir = "hours_traffic_camera_"
# result_base = "result/"


def read_file_csv(file_name: str):
    return pd.read_csv(base_dir + file_name + ".csv")


def save_file_csv(df: DataFrame, base: str, file_name: str):
    df.to_csv(base + file_name + ".csv", index=False)


def get_statistic_sensor_data(df: DataFrame):
    result = df.describe().reset_index()

    cols = ["values"]
    for i in range(1, len(result.columns)):
        cols.append(result.columns[i])

    result.columns = cols
    return result


def processing_traffic_data(df: DataFrame) -> DataFrame:
    result = df.copy()
    result.columns = ['date', 'cameraIp', 'values']

    result['time'] = np.NaN
    for i in range(len(result)):
        result.loc[i, 'time'] = df.loc[i, 'time'].split(" ")[1]
        result.loc[i, 'date'] = df.loc[i, 'time'].split(" ")[0]

    return result


def get_statistic_traffic_data(df: DataFrame) -> DataFrame:
    result = df.copy().groupby(['time']).describe()

    result.columns = [' '.join(str(i).split(" ")[0]
                               for i in col) for col in result.columns]
    result.reset_index(inplace=True)

    cols = [result.columns[0]]
    for i in range(1, len(result.columns)):
        cols.append(result.columns[i].split(" ")[1])

    result.columns = cols

    result['sum'] = df.copy().groupby(['time']).sum().loc[:].values

    return result


def clean_sensor_data(df: DataFrame) -> DataFrame:
    result = df.copy()
    result = result.drop(['UTC', 'Type', 'LocalTime'], axis=1)
    return result


def add_aqi_sensor(df: DataFrame) -> DataFrame:
    result = df.copy()
    result['aqi'] = np.NaN
    for i in range(len(result)):
        pm25 = result.loc[i, 'PS_PM2P5_AVG_24hr']
        myaqi = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pm25), algo=aqi.ALGO_EPA)
        result.loc[i, 'aqi'] = int(myaqi)
    return result


def add_new_feature(df: DataFrame, match_col: str, new_col: str, feature_df: DataFrame, col_feature: str, col_type="DateTime"):
    temp = df.copy()

    if col_type == "DateTime":
        for i in range(len(temp)):
            temp_date = datetime.datetime.strptime(
                temp.loc[i, match_col], "%Y-%m-%dT%H:%M:%S.000Z")
            temp.loc[i, match_col] = temp_date.strftime("%Y-%m-%d %H:%M:%S")
    temp_feature = feature_df[[match_col, col_feature]].copy()
    temp_feature.columns = [match_col, new_col]
    result = temp.merge(temp_feature, left_on=match_col,
                        right_on=match_col)
    return result


def processing_data_for_train():
    sensor_data_in_hours = read_file_csv(sensor_dir + "hours")

    clean_sensor_hours = clean_sensor_data(sensor_data_in_hours)

    # read traffic
    traffic_data = read_file_csv("hours_traffic_camera")
    # read tree density
    tree_data = read_file_csv("tree_density_data")
    ndvi = tree_data.loc[:, 'NDVI'].values
    evi = tree_data.loc[:, "EVI"].values
    if len(ndvi == 1):
        temp_ndvi = [ndvi[0] for i in range(len(clean_sensor_hours) - 1)]
        ndvi = np.concatenate((ndvi, temp_ndvi))
    if len(evi == 1):
        temp_evi = [evi[0] for i in range(len(clean_sensor_hours)-1)]
        evi = np.concatenate((evi, temp_evi))

    clean_sensor_hours['ndvi'] = ndvi
    clean_sensor_hours['evi'] = evi

    # add new features

    clean_sensor_hours = add_new_feature(
        clean_sensor_hours, 'Datetime', "traffic", traffic_data, "value")

    hours = [datetime.datetime.strptime(
        clean_sensor_hours.loc[i, 'Datetime'], "%Y-%m-%d %H:%M:%S").hour for i in range(len(clean_sensor_hours))]

    clean_sensor_hours['hours'] = hours
    clean_sensor_hours = clean_sensor_hours.drop(['Datetime'], axis=1)
    aqi_sensor_hours = add_aqi_sensor(clean_sensor_hours)

    save_file_csv(aqi_sensor_hours, "data/", "aqi_data_hours")


processing_data_for_train()


# def processing_data_for_real_app():
#     sensor_data_in_hours = read_file_csv(sensor_dir + "hours")

#     clean_sensor_hours = clean_sensor_data(sensor_data_in_hours)

#     # read traffic
#     traffic_data = read_file_csv("hours_traffic_camera")
#     # read tree density
#     tree_data = read_file_csv("tree_density_data")
#     ndvi = tree_data.loc[:, 'NDVI'].values
#     evi = tree_data.loc[:, "EVI"].values
#     if len(ndvi == 1):
#         temp_ndvi = [ndvi[0] for i in range(len(clean_sensor_hours) - 1)]
#         ndvi = np.concatenate((ndvi, temp_ndvi))
#     if len(evi == 1):
#         temp_evi = [evi[0] for i in range(len(clean_sensor_hours)-1)]
#         evi = np.concatenate((evi, temp_evi))

#     clean_sensor_hours['ndvi'] = ndvi
#     clean_sensor_hours['evi'] = evi

#     # add new features

#     clean_sensor_hours = add_new_feature(
#         clean_sensor_hours, 'Datetime', "traffic", traffic_data, "value")
#     hours = [datetime.datetime.strptime(
#         clean_sensor_hours.loc[i, 'Datetime'], "%Y-%m-%d %H:%M:%S").hour for i in range(len(clean_sensor_hours))]
#     clean_sensor_hours['hours'] = hours
#     clean_sensor_hours = clean_sensor_hours.drop(['Datetime'], axis=1)
#     aqi_sensor_hours = add_aqi_sensor(clean_sensor_hours)

#     save_file_csv(aqi_sensor_hours[-6:], "data/",
#                   "data_processed")


# processing_data_for_real_app()
