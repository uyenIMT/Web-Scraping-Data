import pandas as pd

input = '.csv'
output = '.csv'
# Load the addresses file into a DataFrame
addresses_df = pd.read_csv(input, encoding='UTF-8-SIG')
# print(addresses_df.head())

# Load the cities/districts file into a DataFrame
cities_districts_df = pd.read_csv('Cities.csv', encoding='UTF-8-SIG')

# Function to find city and district for each address
def find_city_district(location):
    location = str(location)  # Ensure location is a string
    for index, row in cities_districts_df.iterrows():
        if str(row["City"]) in location and str(row["District"]) in location:
            return row["City"], row["District"]
    return None, None

# Apply the function to the addresses DataFrame
addresses_df[["City", "District"]] = addresses_df["Location"].apply(find_city_district).apply(pd.Series)

# Save the new DataFrame to a CSV file
addresses_df.to_csv(output, index=False)
