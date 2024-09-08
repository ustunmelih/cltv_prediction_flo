#importing libraries
import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from sklearn.preprocessing import MinMaxScaler
import numpy as np


# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# load the data
df_ = pd.read_csv("Case\\cltv_prediction\\flo_data_20k.csv")
df = df_.copy()
df.head()


# Replace the outliers with the threshold values.
def outlier_thresholds(dataframe, column):
    quartile_1 = dataframe[column].quantile(0.01)
    quartile_3 = dataframe[column].quantile(0.99)
    iqr_range = quartile_3 - quartile_1
    up_limit = quartile_3 + 1.5 * iqr_range
    low_limit = quartile_1 - 1.5 * iqr_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit, 0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit, 0)


threshold_columns = ["order_num_total_ever_online", "order_num_total_ever_offline",
                     "customer_value_total_ever_offline", "customer_value_total_ever_online"]

for col in threshold_columns:
    replace_with_thresholds(df, col)


# Create the "order_num_total" and "customer_value_total" variables by summing the online and offline values.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]


date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

df["last_order_date"].max()
last_date = dt.datetime(2021, 6, 1)

cltv_df = pd.DataFrame()
cltv_df["customer_id"] = df["master_id"]
cltv_df["recency_cltv_weekly"] = (df["last_order_date"] - df["first_order_date"]).dt.days / 7
cltv_df["T_weekly"] = (last_date - df["first_order_date"]).dt.days / 7
cltv_df["frequency"] = df["order_num_total"]
cltv_df["monetary_cltv_avg"] = df["customer_value_total"] / df["order_num_total"]


cltv_df.head()


# Create the BG/NBD model
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_df['frequency'],
        cltv_df['recency_cltv_weekly'],
        cltv_df['T_weekly'])


# Estimate the expected purchases from customers in 3 months and add to the CLTV DataFrame as exp_sales_3_month.
cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3,
                                           cltv_df['frequency'],
                                           cltv_df['recency_cltv_weekly'],
                                           cltv_df['T_weekly'])


# Estimate the expected purchases from customers in 6 months and add to the CLTV DataFrame as exp_sales_6_month.
cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6,
                                           cltv_df['frequency'],
                                           cltv_df['recency_cltv_weekly'],
                                           cltv_df['T_weekly'])


# We examine the 10 people who will make the most purchase in the 3rd and 6th month.
cltv_df.groupby('customer_id').agg({'exp_sales_3_month': 'sum',
                                    'exp_sales_6_month': 'sum'}).sort_values(by='exp_sales_6_month',
                                                                             ascending=False).head(10)
                                    

# Fit the gamma-gamma model. Estimates the average value of customers and add to CLTV DataFrame as exp_average_value.
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])
cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                       cltv_df['monetary_cltv_avg'])
cltv_df.head()


# Calculate 6-month CLTV and add dataframe with the name 'cltv'.
cltv_df['cltv'] = ggf.customer_lifetime_value(bgf,
                                              cltv_df['frequency'],
                                              cltv_df['recency_cltv_weekly'],
                                              cltv_df['T_weekly'],
                                              cltv_df['monetary_cltv_avg'],
                                              time=6,
                                              freq="W",
                                              discount_rate=0.01)


# Observe 20 people at the highest value of CLTV.
cltv_df.sort_values("cltv", ascending=False).head(20)


# Create a segment for the CLTV values in the data set. Assign with the name CLTV_segment.
cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])
cltv_df.head()
