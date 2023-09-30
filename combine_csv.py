# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:56:11 2023

@author: hi
"""

import pandas as pd
import glob

input = '.csv'
output = '.csv'
# Get a list of all CSV files in the specified directory
file_paths = glob.glob(input)

# Load CSV files into DataFrames
data_frames = [pd.read_csv(file) for file in file_paths]

# Concatenate along columns (side by side)
combined_df = pd.concat(data_frames, axis=0, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv(output, index=False)
