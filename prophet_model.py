# prophet_model.py
from multiprocessing.context import _force_start_method
from operator import mod
import sys
from statsmodels.tsa.stattools import acovf
from statsmodels.tsa.stattools import acf
import prophet
from re import I
import numpy as np
import pandas as pd
from argparse import ArgumentError
from matplotlib import pyplot as plt
from datetime import datetime

# do mor research on bayesian modeling
# read prophet paper
def read_data(time="all"):
    if time == "all":
        df = pd.read_csv("data/LA_CO2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"]) 
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "jan":
        df = pd.read_csv("data/dataByMonth/jan_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "feb":
        df = pd.read_csv("data/dataByMonth/feb_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "mar":
        df = pd.read_csv("data/dataByMonth/mar_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "apr":
        df = pd.read_csv("data/dataByMonth/apr_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "may":
        df = pd.read_csv("data/dataByMonth/may_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "jun":
        df = pd.read_csv("data/dataByMonth/jun_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "jul":
        df = pd.read_csv("data/dataByMonth/jul_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "aug":
        df = pd.read_csv("data/dataByMonth/aug_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "sep":
        df = pd.read_csv("data/dataByMonth/sep_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "oct":
        df = pd.read_csv("data/dataByMonth/oct_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "nov":
        df = pd.read_csv("data/dataByMonth/nov_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    elif time == "dec":
        df = pd.read_csv("data/dataByMonth/dec_co2_weather.csv")
        df["ds"] = pd.DatetimeIndex(df["Time"])
        df.index = df["ds"]
        df = df.drop(columns = "Time")
    else:
        raise NotImplementedError('No dataset')

    return df


def is_covariance_stationary():

    df = read_data('all')

    # calculate autocovariance
    auto_cov = acovf(df["Temp (F)"])

    # calculate autocorelation
    auto_cor = acf(df["Temp (F)"])


    print(auto_cov)
    print(auto_cor)

    return


# def get_old_dti(time):

#     if time == "jan":

#         # get old days
#         jan = read_data(time="jan")
#         old_days = pd.DataFrame(jan['ds'])
#         # set columns
#         old_days.columns = ["ds"]

#     return old_days

# def get_future_dti(time):

#     if time == "feb":

#         # create date time index of hourly data for first week of February
#         future = pd.date_range(start='2/1/2018 00:53:00', end='2/7/2018 23:53:00', freq="H")
#         # change to dataframe
#         future = pd.DataFrame(future)
#         # set columns
#         future.columns = ["ds"]

#     return future

def get_future_df(month1, month2):

    old_days = pd.DataFrame(month1["ds"])
    old_days.columns = ["ds"]

    future = month2["ds"]
    future = future.iloc[:168]

    future = pd.DataFrame(future)


    return old_days.append(future)


def model_dew(predict):

    if predict == "feb":

        # read in january data
        jan = read_data(time="jan")
        jan["y"] = jan["Dew Point (F)"]
        jan = jan[["y", "ds"]]

        # read in February data
        feb = read_data(time="feb")
        feb["y"] = feb["Dew Point (F)"]
        feb = feb[["y", "ds"]]
        feb = feb.iloc[:168]

        #set up prophet model and fit
        model = prophet.Prophet(yearly_seasonality=False, daily_seasonality=True, weekly_seasonality=True)
        model.fit(jan)

        future = get_future_df(jan, feb)

        forecast = model.predict(future)

        fig = model.plot(forecast)
        fig.set_dpi(200)
        fig.set_size_inches(12, 12)
        plt.plot(feb['ds'], feb['y'], 'ro', markersize=2)
        plt.legend(['January data', 'prediction', 'confidence interval', 'February data' ], loc='best', fontsize=10)
        plt.xlabel(r'Time (hours)', fontsize=10)
        plt.ylabel(r'Dew Point ($\degree{}$ F)', fontsize=10)
        plt.title(f'1 week of February Dew Point forecast', fontsize=15)
        plt.show()


    else:
        raise NotImplementedError("{} is an invalid time for modeling dew point".format(predict))

    return

def model_temp(predict):

    if predict == "all": 
        df = read_data(time=predict)
        df["y"] = df["Temp (F)"]
        new = df[["y", "ds"]]
        model = prophet.Prophet()
        model.fit(new)
        future = model.make_future_dataframe(periods = 20)
        print(future.head(5))
        forecast = model.predict(future)
        fig1 = model.plot(forecast)
        plt.show()

    elif predict == "feb":
        # read in training data
        jan = read_data(time="jan")
        jan["y"] = jan["Temp (F)"]
        jan = jan[["y", "ds"]]

        # read in validation data
        feb = read_data(time='feb')
        feb["y"] = feb["Temp (F)"]
        feb = feb[["y", "ds"]]
        feb = feb.iloc[:168]

        # set up prophet model and fit
        model = prophet.Prophet(yearly_seasonality=True, daily_seasonality=True, weekly_seasonality=True)
        model.fit(jan)

        future = get_future_df(jan, feb)
        forecast = model.predict(future)

        # plot prediction
        fig = model.plot(forecast)
        fig.set_dpi(200)
        fig.set_size_inches(12, 12)
        plt.plot(feb['ds'], feb['y'], 'ro', markersize=2)
        plt.legend(['January data', 'prediction', 'confidence interval', 'February data' ], loc='best', fontsize=10)
        plt.xlabel(r'Time (hours)', fontsize=10)
        plt.ylabel(r'Temperature ($\degree{}$ F)', fontsize=10)
        plt.title(f'1 week of February temperature forecast', fontsize=15)
        plt.show()

    else:
        raise NotImplementedError("{} is an invalid time for modeling temperature.".format(predict))


    return

def model_humidity(predict):

    if predict =="feb":

        # read in january data
        jan = read_data(time="jan")
        jan["y"] = jan["Humidity (%)"]
        jan = jan[["y", "ds"]]

        # read in February data
        feb = read_data(time="feb")
        feb["y"] = feb["Humidity (%)"]
        feb = feb[["y", "ds"]]
        feb = feb.iloc[:168]

        #set up prophet model and fit
        model = prophet.Prophet(yearly_seasonality=False, daily_seasonality=True, weekly_seasonality=True)
        model.fit(jan)

        future = get_future_df(jan, feb)
        forecast = model.predict(future)

        fig = model.plot(forecast)
        fig.set_dpi(200)
        fig.set_size_inches(12, 12)
        plt.plot(feb['ds'], feb['y'], 'ro', markersize=2)
        plt.legend(['January data', 'prediction', 'confidence interval', 'February data' ], loc='best', fontsize=10)
        plt.xlabel(r'Time (hours)', fontsize=10)
        plt.ylabel(r'Humditiy (%))', fontsize=10)
        plt.title(f'1 week of February humidty forecast', fontsize=15)
        plt.show()

    else:
        raise NotImplementedError("{} is an invalid time for modeling humidity.".format(predict))

    return

def model_CO2(predict):

    if predict == "feb":
        # read in january data
        jan = read_data(time="jan")
        jan["y"] = jan["co2_ppm"]
        jan = jan[["y", "ds"]]

        # read in February data
        feb = read_data(time="feb")
        feb["y"] = feb["co2_ppm"]
        feb = feb[["y", "ds"]]

        # read in march data
        mar = read_data(time="mar")
        mar["y"] = mar["co2_ppm"]
        mar = mar[["y", "ds"]]

        # read in april data
        apr = read_data(time="apr")
        apr["y"] = apr["co2_ppm"]
        apr = apr[["y", "ds"]]

        # read in may data
        may = read_data(time="may")
        may["y"] = may["co2_ppm"]
        may = may[["y", "ds"]]

        # read in june data
        jun = read_data(time="jun")
        jun["y"] = jun["co2_ppm"]
        jun = jun[["y", "ds"]]

        jan_feb = jan.append(feb)
        jan_mar = jan_feb.append(mar)
        jan_apr = jan_mar.append(apr)
        jan_may = jan_apr.append(may)
        jan_jun = jan_may.append(jun)

        # read in jul
        jul = read_data(time="jul")
        jul["y"] = jul["co2_ppm"]
        jul = jul[["y", "ds"]]
        jul = jul.iloc[:168]

        #set up prophet model and fit
        model = prophet.Prophet(yearly_seasonality=True, daily_seasonality=True, weekly_seasonality=True)
        model.fit(jan_jun)

        future = get_future_df(jan_jun, jul)
        forecast = model.predict(future)

        fig = model.plot(forecast)
        fig.set_dpi(200)
        fig.set_size_inches(12, 12)
        plt.plot(jul['ds'], jul['y'], 'ro', markersize=2)
        plt.legend(['January data', 'prediction', 'confidence interval', 'February data' ], loc='best', fontsize=10)
        plt.xlabel(r'Time (hours)', fontsize=10)
        plt.ylabel(r'Humditiy (%))', fontsize=10)
        plt.title(f'1 week of February co2_ppm', fontsize=15)
        plt.show()


    else:
        raise NotImplementedError("{} is an invalid time for modeling co2_ppm.".format(predict))

    return




def main(key, time):


    if key == "temp":
        model_temp(time)

    else:
        ArgumentError("Incorrect model specification")

    return


if __name__ == "__main__":

    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        main(sys.argv[-2], sys.argv[-1])

    else:
        raise ArgumentError("Incorrect command line arguments")