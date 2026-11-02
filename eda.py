
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("data/cleaned_machine_data.csv")

# Display dataset
print("MACHINE DATA")
print(df)

# Check failure count
print("\nFAILURE COUNT")
print(df["failure"].value_counts())

# 1. Temperature vs Failure
sns.boxplot(x="failure", y="temperature", data=df)
plt.title("Temperature vs Machine Failure")
plt.show()

# 2. Vibration vs Failure
sns.boxplot(x="failure", y="vibration", data=df)
plt.title("Vibration vs Machine Failure")
plt.show()

# 3. Pressure vs Failure
sns.boxplot(x="failure", y="pressure", data=df)
plt.title("Pressure vs Machine Failure")
plt.show()

# 4. Correlation Heatmap
sns.heatmap(df.select_dtypes(include="number").corr(),
            annot=True, cmap="coolwarm")

plt.title("Machine Data Correlation")
plt.show()
