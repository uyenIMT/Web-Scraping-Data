import pandas as pd

# Sample data
data_input = 'TinhHuyenXa2021.csv'
data_output = 'Dim_cities.csv'

# Read CSV file with the correct separator
df = pd.read_csv(data_input, sep=",")

# Print the DataFrame shape before drop
print("Shape before drop:", df.shape)

# Remove duplicate rows based on all columns
df.drop_duplicates(subset=None, inplace=True)

# Remove rows with ' ' in the 'Title' column and assign the result back to df
# df = df[df['ID'] != ' ']

# Print the DataFrame shape after drop
print("Shape after drop:", df.shape)

# Write the results to a different file
df.to_csv(data_output, index=False)

