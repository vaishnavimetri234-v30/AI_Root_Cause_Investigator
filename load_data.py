
import pandas as pd

# Load the machine dataset
df = pd.read_csv("data/raw/machine_data.csv")

# Display the complete dataset
print("MACHINE FAILURE DATASET")
print(df)

# Display first five rows
print("\nFIRST FIVE ROWS")
print(df.head())

# Display dataset information
print("\nDATASET INFORMATION")
df.info()

# Display rows and columns
print("\nDATASET SHAPE")
print(df.shape)
