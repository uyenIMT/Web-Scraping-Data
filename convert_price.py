import pandas as pd
import re

input = '.csv'
output = '.csv'
# Load the CSV file into a DataFrame
df = pd.read_csv(input)

# Function to convert the price format to integers
def convert_price(price_str):
    if isinstance(price_str, str):
        # Check for values with "Thỏa thuận" and return None for those
        if price_str.strip() == "Thỏa thuận":
            return "Thỏa thuận"
        
        # Use regular expression to extract numeric parts
        match = re.match(r'([\d,\s.]+\s*[,]?\s*\d*)\s*(\w+)?', price_str)
        print(match)
        if match:
            numeric_part = pd.to_numeric(match.group(1).replace(',','.').replace(' ', ''))  # Remove spaces and replace comma by dot
            print(numeric_part)
            unit = match.group(2)
            print(unit)
            
            # Define conversion factors for common units (you can add more)
            unit_factors = {
                'Triệu': 1e6,
                'Triệu -': 1e6,  # 1 million
                'Tỷ': 1e9, 
                'Tỷ -': 1e9    # 1 billion
            }
            
            # Convert the price 
            if unit in unit_factors:
                return (numeric_part) * unit_factors[unit]
            elif unit is None:
                return (numeric_part)  # No unit specified
            else:
                return None  # Handle unknown units
        else:
            return None  # Handle invalid formats
    else:
        return price_str  # Keep non-string values as-is

# Apply the conversion function to the 'Price' column
df['Price'] = df['Price'].apply(convert_price)

# Save the updated DataFrame back to a CSV file
df.to_csv(output, index=False)

