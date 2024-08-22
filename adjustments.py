import pandas as pd
import yfinance as yf
import numpy as np

def get_tsmc_adjustments_df():

    TSMC_adjustments = [
    {
        "year":2019,
        "percentage":0.076,
    },
    {
        "year":2020,
        "percentage":0.077,
    },
    {
        "year":2021,
        "percentage":0.058
    },
    {
        "year":2022,
        "percentage":0.063,
    },
    {
        "year":2023,
        "percentage":0.11,
    }
]
    TSMC_adjustments_df = pd.DataFrame(TSMC_adjustments)
    TSMC_adjustments_df["year"] = pd.to_datetime(TSMC_adjustments_df["year"], format='%Y')
    TSMC_adjustments_df["year-quarter"] = TSMC_adjustments_df["year"].dt.to_period('Q')
    TSMC_adjustments_df = TSMC_adjustments_df.drop(columns=["year"])
    TSMC_adjustments_df = TSMC_adjustments_df.loc[TSMC_adjustments_df.index.repeat(4)].reset_index(drop=True)
    TSMC_adjustments_df["year-quarter"] = TSMC_adjustments_df["year-quarter"].add(TSMC_adjustments_df.groupby("year-quarter").cumcount())
    TSMC_adjustments_df.rename(columns={"percentage":"TSMC_Percentage"}, inplace=True)
    return TSMC_adjustments_df

def get_AMZN_adustments_df():

    amazon_adjustments = [
    {
        "year":2018,
        "AWS":9783,
        "Total":25068,
    },
    {
        "year":2019,
        "AWS":12058,
        "Total":30018,
    },
    {
        "year":2020,
        "AWS":16530,
        "Total":58976,
    },
    {
        "year":2021,
        "AWS":22047,
        "Total":72325,
    },
    {
        "year":2022,
        "AWS":27755,
        "Total":60836,
    },
    {
        "year":2023,
        "AWS":24843,
        "Total":48344,
    },
]

    amazon_adjustments_df = pd.DataFrame(amazon_adjustments)
    amazon_adjustments_df["Non_AWS_PPE"] = amazon_adjustments_df["Total"] - amazon_adjustments_df["AWS"]
    # transform year to year-quarter, duplicate the year-quarter for 4 quarters, divide absolute values by 4
    amazon_adjustments_df["year"] = pd.to_datetime(amazon_adjustments_df["year"], format='%Y')
    amazon_adjustments_df["year-quarter"] = amazon_adjustments_df["year"].dt.to_period('Q')
    amazon_adjustments_df = amazon_adjustments_df.drop(columns=["year"])
    amazon_adjustments_df = amazon_adjustments_df.loc[amazon_adjustments_df.index.repeat(4)].reset_index(drop=True)

    amazon_adjustments_df["year-quarter"] = amazon_adjustments_df["year-quarter"].add(amazon_adjustments_df.groupby("year-quarter").cumcount())

    amazon_adjustments_df["AWS"] = amazon_adjustments_df["AWS"] / 4
    amazon_adjustments_df["Total"] = amazon_adjustments_df["Total"] / 4
    amazon_adjustments_df["Non_AWS_PPE"] = amazon_adjustments_df["Total"] - amazon_adjustments_df["AWS"]
    amazon_adjustments_df.rename(columns={"Non_AWS_PPE":"AMZN-Non-AWS","Total":"AMZN_Total"}, inplace=True)
    return amazon_adjustments_df

def get_nvda_adjustments_df():
    

    percentages = [25.0, 27.3, 39.4, 40.2, 55.6, 78.0]
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    NVDA_datacenter_percentages = {
        "year": years,
        "percentage": percentages
    }
    NVDA_datacenter_percentages = pd.DataFrame(NVDA_datacenter_percentages).rename(columns={"year": "year-quarter"})
    NVDA_datacenter_percentages["year-quarter"] = pd.to_datetime(NVDA_datacenter_percentages["year-quarter"].astype(str)).dt.to_period('Q')
    # duplicate first 5 rows 4 times
    NVDA_datacenter_percentages = pd.concat([NVDA_datacenter_percentages]*4).sort_values(by="year-quarter")
    # cumulative  year-quarter
    NVDA_datacenter_percentages["year-quarter"] = NVDA_datacenter_percentages["year-quarter"].add(NVDA_datacenter_percentages.groupby("year-quarter").cumcount())
    # remove last 3 rows
    NVDA_datacenter_percentages = NVDA_datacenter_percentages.iloc[:-3]
    # add 2024Q2 with 84.4
    NVDA_datacenter_percentages = pd.concat([NVDA_datacenter_percentages,
                                            pd.DataFrame({"year-quarter": pd.Period("2024Q2"), "percentage": [84.4]})]).reset_index(drop=True)
    # shift all quarter by 1
    NVDA_datacenter_percentages["year-quarter"] = NVDA_datacenter_percentages["year-quarter"].shift(1)

    return NVDA_datacenter_percentages

def get_exchange_rate_df():

    exchange_rate = yf.Ticker("TWD=X").history(period="10y")["Close"]
    exchange_rate_df = pd.DataFrame(exchange_rate).reset_index()
    exchange_rate_df["year-quarter"] = exchange_rate_df["Date"].dt.to_period('Q')
    exchange_rate_df = exchange_rate_df.drop(columns=["Date"])
    exchange_rate_df = exchange_rate_df.groupby("year-quarter").median().reset_index()
    exchange_rate_df.rename(columns={"Close":"USD_to_TWD"}, inplace=True)
    return exchange_rate_df    