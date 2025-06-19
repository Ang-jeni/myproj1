import pandas as pd
import numpy as np

# define the file name and the data sheet
orig_data_file = r"climate_change_download_0.xls"
data_sheet = "Data"

# read the data from the excel file to a pandas DataFrame
data_orig = pd.read_excel(io=orig_data_file, sheet_name=data_sheet)

print("Shape of the original dataset:")
data_orig.shape

print("Available columns:")
data_orig.columns

print("Column data types:")
data_orig.dtypes

print("Overview of the first 5 rows:")
data_orig.head()

print("Descriptive statistics of the columns:")
data_orig.describe()

data_orig['Series name'].unique()
data_orig['Series code'].unique()
data_orig['SCALE'].unique()
data_orig['Decimals'].unique()

data_orig[data_orig['SCALE'] == 'Text']
data_orig[data_orig['Decimals'] == 'Text']

# assign the data to a new DataFrame, which will be modified
data_clean = data_orig

print("Original number of rows:")
print(data_clean.shape[0])

# remove rows characterized as "Text" in the SCALE column
data_clean = data_clean[data_clean['SCALE'] != 'Text']
print("Rows after removing 'Text' SCALE:")
print(data_clean.shape[0])

# remove rows characterized as "Text" in the Decimals column
data_clean = data_clean[data_clean['Decimals'] != 'Text']
print("Rows after removing 'Text' Decimals:")
print(data_clean.shape[0])

# convert the SCALE and Decimals columns to numeric
data_clean['SCALE'] = pd.to_numeric(data_clean['SCALE'])
data_clean['Decimals'] = pd.to_numeric(data_clean['Decimals'])

# assign all year values (column names) as a list
years = data_clean.columns[6:]

# reshape the data to have columns: Country name, Country code, Series name, Series code, Year, Value
data_tidy = pd.melt(
    frame=data_clean,
    id_vars=['Country name', 'Country code', 'Series name', 'Series code'],
    value_vars=years,
    var_name='Year',
    value_name='Value'
)

# drop NaN values
data_tidy = data_tidy.dropna(subset=['Value'])

# convert year and value columns to numeric
data_tidy['Year'] = pd.to_numeric(data_tidy['Year'], errors='coerce')
data_tidy['Value'] = pd.to_numeric(data_tidy['Value'], errors='coerce')

# reset index
data_tidy = data_tidy.reset_index(drop=True)

# preview cleaned data
print("Preview of the cleaned and reshaped data:")
print(data_tidy.head())

# export the cleaned dataset to a CSV file
data_tidy.to_csv("data_cleaned.csv", index=False)
print("Data exported to 'data_cleaned.csv'")
