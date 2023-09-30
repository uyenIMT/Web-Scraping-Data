import pandas as pd

# Sample data
data_input = '.csv'
data_output = '.csv'

# Read CSV file with the correct separator
df = pd.read_csv(data_input, sep=",")

# Print the DataFrame shape before drop
print("Shape before drop:", df.shape)

# Remove duplicate rows based on all columns
df.drop_duplicates(subset = 'ID', inplace=True)
df.dropna(subset = 'ID')

df['Parking slot'] = pd.to_numeric(df['Parking slot'].str.replace(' (Chỗ)', ''), errors='coerce')
df['Area'] = pd.to_numeric(df['Area'].str.replace(' M²', ''), errors='coerce')
df['Floor'] = pd.to_numeric(df['Floor'].str.replace(' (Tầng)', ''), errors='coerce')
df['Road width'] = pd.to_numeric(df['Road width'].str.replace(' (m)', ''), errors='coerce')
df['Front width'] = pd.to_numeric(df['Front width'].str.replace(' (m)', ''), errors='coerce')
df['Email'] = df['Email'].astype(object)

# df=df[~((df['Price'] == 'Thỏa thuận'))]

# # Convert the 'Price' column to numeric, ignoring "Thỏa thuận"
# df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# df=df[~((df['Category'] == 'Sale') & (df['Price'] > 1000000000000))]
# df=df[~((df['Category'] == 'Sale') & (df['Price'] < 700000000))]
# df=df[~((df['Category'] == 'Rent') & (df['Price'] > 500000000))]

# Print the DataFrame shape after drop
print("Shape after drop:", df.shape)
print(df.info())

# Write the results to a different file
df.to_csv(data_output, index=False)

