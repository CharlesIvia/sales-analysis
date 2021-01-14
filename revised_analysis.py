import os
from typing import Counter
from matplotlib.pyplot import axis
from numpy.core.fromnumeric import product
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.arrays.integer import coerce_to_array
from itertools import combinations
from collections import Counter

print("Importation done")

# Read data

df = pd.read_csv("all_data.csv")
print(df.head())
print(df.shape)

# cLean data

print(df.isna())
print(df.isna().any(axis=1))
df = df.dropna(how="all")
print(df.isna())
print(df)

# Make columns the correct data type

df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")

print(df.head())

# Get rid of text in order date column
df = df[df["Order Date"].str[0:2] != "Or"]

# Add month column

# Slow
# df["Sales Month"] = pd.to_datetime(df["Order Date"]).dt.month

# Faster

df["Month"] = df["Order Date"].str[0:2]
df["Month"] = df["Month"].astype("int32")

print(df.head())

# Add city column


def get_city(address):
    return address.split(",")[1].strip(" ")


def get_state(address):
    return address.split(",")[2].split(" ")[1]


df["City"] = df["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

print(df.head())


# Data exploration

# fig, ax = plt.subplots(1, 4, figsize=(14, 5))

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

# WANT: Determine the best month for sales

# Create a sales column first - quantity_ordered * Price

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
fig1.tight_layout()

# WANT: Determine which city sold the most products

highest_selling_city = df.groupby(["City"]).sum()
print(highest_selling_city)

cities = [city for city, cty in df.groupby(["City"])]
print(cities)

ax2.bar(cities, highest_selling_city["Sales"])
ax2.set_title("Sales Per City")
ax2.set_ylabel("Sales in USD ($)")
ax2.set_xlabel("Month number")
ax2.set_xticks(cities)
ax2.set_xticklabels(cities, rotation=90)
fig2.tight_layout()

# WANT: To determine the optimal advertisement time to maximize likelihood of customers buying product

# Add hour and minute column

# Slow
# df["Hour"] = pd.to_datetime(df["Order Date"]).dt.hour
# df["Minute"] = pd.to_datetime(df["Order Date"]).dt.minute

# Faster


def get_hour(date):
    return date.split(" ")[1].split(":")[0]


df["Time"] = df["Order Date"].apply(lambda x: f"{get_hour(x)}")

df["Count"] = 1

print(df.head(50))

order_hour = [pair for pair, dt in df.groupby(["Time"])]
y_axis = df.groupby(["Time"]).count()["Count"]
print(order_hour)
print(y_axis)

ax3.plot(order_hour, y_axis)
ax3.set_title("Unique Orders Per Each Hour")
ax3.set_xlabel("Hours in a day")
ax3.set_ylabel("Unique Orders")
ax3.grid()
fig3.tight_layout()

## From this analysis,I would recommend advertisements to be run slightly before 11am or 7pm
