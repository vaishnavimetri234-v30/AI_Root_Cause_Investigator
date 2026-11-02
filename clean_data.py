
import pandas as pd

# Load original dataset
df = pd.read_csv("data/raw/machine_data.csv")

print("ORIGINAL DATASET")
print(df)

# Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Check duplicate records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# Check data types
print("\nDATA TYPES")
print(df.dtypes)

# Remove duplicate records
df = df.drop_duplicates()

# Remove missing values
df = df.dropna()

# Save cleaned dataset
df.to_csv("data/cleaned_machine_data.csv", index=False)

print("\nCLEANED DATASET")
print(df)

print("\nData cleaning completed successfully!")
