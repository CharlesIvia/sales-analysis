import os
from matplotlib.pyplot import axis
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.arrays.integer import coerce_to_array

print("Done")

# READ DATA

df = pd.read_csv("all_data.csv")
print(df.head())
print(df.shape)

# CLEANING UP THE DATA

# The first step in this is figuring out what we need to clean.
# I have found in practice, that you find things you need to clean as you perform your operations and get errors.
# Based on the error, you decide how you should go about cleaning the data


# Drops rows of NaN

nan_df = df[df.isna().any(axis=1)]
print(nan_df.head())

df = df.dropna(how="all")
# print(df.head())


# Get rid of text in order date column
df = df[df["Order Date"].str[0:2] != "Or"]

# Make columns correct type

df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")

print(df.head())

# Augment data with additional columns

df["Month"] = df["Order Date"].str[0:2]
df["Month"] = df["Month"].astype("int32")
print(df.head())

# Add month column (alternative but slower method)

# df["Sales Month"] = pd.to_datetime(df["Order Date"]).dt.month
# print(df.head())

# Add city column


def get_city(address):
    return address.split(",")[1].strip(" ")


def get_state(addres):
    return addres.split(",")[2].split(" ")[1]


df["City"] = df["Purchase Address"].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
print(df.head())

# DATA EXPLORATION

fig1, ax1 = plt.subplots()

# What is the best month for sales? How much was earned that month?

df["Sales"] = df["Quantity Ordered"].astype("int") * df["Price Each"].astype("float")

print(df.head())


sales = df.groupby(["Month"]).sum()
print(sales)
months = range(1, 13)

ax1.bar(months, sales["Sales"])
ax1.set_title("Sales per Month")
ax1.set_xticks(months)
ax1.set_ylabel("Sales in USD ($)")
ax1.set_xlabel("Month number")

plt.show()
