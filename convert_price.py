import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('Final_data_rm.csv')

# Function to convert the price format to integers
def convert_price(price_str):
    if isinstance(price_str, str):
        # Check for values with "Thỏa thuận" and return None for those
        if price_str.strip() == "Thỏa thuận":
            return None
        
        # Use regular expression to extract numeric parts
        match = re.match(r'([\d,]+\s*[,]?\s*\d*)\s*(\w+)?', price_str)
        if match:
            numeric_part = match.group(1).replace(',','.').replace(' ', '')  # Remove spaces and replace comma by dot
            unit = match.group(2)
            
            # Define conversion factors for common units (you can add more)
            unit_factors = {
                'Triệu': 1e6,  # 1 million
                'Tỷ': 1e9,     # 1 billion
            }
            
            # Handle trailing zeros after the decimal point
            if '.' in numeric_part:
                numeric_part = numeric_part.rstrip('0').rstrip('.')  # Remove trailing zeros and the decimal point if it's all zeros

            # Convert the price to an integer value (removing the decimal part)
            if unit in unit_factors:
                return int(float(numeric_part) * unit_factors[unit])
            elif unit is None:
                return int(float(numeric_part))  # No unit specified
            else:
                return None  # Handle unknown units
        else:
            return None  # Handle invalid formats
    else:
        return price_str  # Keep non-string values as-is

# Apply the conversion function to the 'Price' column
df['Price'] = df['Price'].apply(convert_price)

# Save the updated DataFrame back to a CSV file
df.to_csv('updated_Final_data_rm.csv', index=False)
