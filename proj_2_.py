# -*- coding: utf-8 -*-
"""proj 2 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OQc2yHZKKvbQLDMkcTm72fTqyJXdmlb7
"""

!pip install pandas matplotlib seaborn


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  datasets
death_data = pd.read_csv('death.csv')
incident_data = pd.read_csv('cancer_incident_rate.csv')
poverty_data = pd.read_csv('poverty_rate.csv', skiprows=4)

# column names to the poverty dataset
poverty_data.columns = ["state", "FIPS", "poverty_rate", "poverty_population", "rank"]

# Clean column names death data
death_data.rename(columns={
    "State": "state",
    "Age-Adjusted Death Rate([rate note]) - deaths per 100,000": "death_rate",
    "Average Annual Count": "annual_death_count"
}, inplace=True)

# Clean column names for incident data
incident_data.rename(columns={
    "State": "state",
    "Age-Adjusted Incidence Rate([rate note]) - cases per 100,000": "incidence_rate",
    "Average Annual Count": "annual_incident_count"
}, inplace=True)

# Standardize state and remove extra characters,
valid_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
    'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
    'West Virginia', 'Wisconsin', 'Wyoming', 'District Of Columbia'
]

# Standardize and filter valid states
for df in [incident_data, death_data, poverty_data]:
    df["state"] = df["state"].str.split("(").str[0].str.strip().str.title()
    df = df[df["state"].isin(valid_states)]

# Merge datasets
merged_data = pd.merge(incident_data, death_data, on="state", how="inner")
enhanced_data = pd.merge(merged_data, poverty_data, on="state", how="inner")

# Check if enhanced_data is empty
if not enhanced_data.empty:
    # Compute rankings
    enhanced_data["incidence_rank"] = enhanced_data["incidence_rate"].rank(ascending=False)
    enhanced_data["death_rank"] = enhanced_data["death_rate"].rank(ascending=False)
    enhanced_data["poverty_rank"] = enhanced_data["poverty_rate"].rank(ascending=False)

    # Compute overall  score
    enhanced_data["burden_score"] = enhanced_data["incidence_rank"] + enhanced_data["death_rank"] + enhanced_data["poverty_rank"]

    # Sort  burden score
    ranked_data = enhanced_data.sort_values("burden_score", ascending=True)

    # Save results
    ranked_data.to_csv("simplified_state_rankings.csv", index=False)

    # Visualization
    # Bar chart: Incidence rates

    plt.figure(figsize=(25, 25))
    sns.barplot(data=ranked_data, x="incidence_rate", y="state", color="blue")
    plt.title("Incidence Rates by State")
    plt.xlabel("Incidence Rate (per 100,000)")
    plt.ylabel("State")
    plt.subplots_adjust(bottom=0.15, top=0.9)
    plt.tight_layout()
    plt.savefig("simplified_incidence_chart.png")
    plt.show()

    #Bar chart: Poverty rates
    plt.figure(figsize=(15, 10))
    sns.barplot(data=ranked_data, x="poverty_rate", y="state", color="blue")
    plt.title("Poverty Rates by State")
    plt.xlabel("Poverty Rate (%)")
    plt.ylabel("State")
    plt.subplots_adjust(bottom=0.15, top=0.9)
    plt.tight_layout()
    plt.savefig("simplified_poverty_chart.png")
    plt.show()

    # Scatter plot: Poverty vs Mortality
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=ranked_data, x="poverty_rate", y="death_rate", hue="state", palette="coolwarm")
    plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.title("Poverty Rate vs Mortality Rate")
    plt.xlabel("Poverty Rate (%)")
    plt.ylabel("Mortality Rate (per 100,000)")
    plt.tight_layout()
    plt.savefig("scatter_legend_custom_position.png")
    plt.show()

    # Convert data for heat map
    # Convert columns to numeric
    ranked_data["poverty_rate"] = pd.to_numeric(ranked_data["poverty_rate"], errors="coerce")
    ranked_data["death_rate"] = pd.to_numeric(ranked_data["death_rate"], errors="coerce")
    ranked_data["incidence_rate"] = pd.to_numeric(ranked_data["incidence_rate"], errors="coerce")

    #Drop rows with NaN values
    ranked_data = ranked_data.dropna(subset=["poverty_rate", "death_rate", "incidence_rate"])
    # Compute correlation matrix
    correlation_matrix = ranked_data[["poverty_rate", "death_rate", "incidence_rate"]].corr()

    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap: Poverty, Mortality, and Incidence Rates")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    plt.show()




else:
    print("No valid data available after cleaning and merging. Check source datasets.")

import matplotlib.pyplot as plt
import seaborn as sns

# Sort by incidence and mortality rates
ranked_data = ranked_data.sort_values("incidence_rate", ascending=False)

# Plot  bar chart
plt.figure(figsize=(14, 10))
x = range(len(ranked_data))  # Position for each state
bar_width = 0.4

# Incidence rates
plt.bar(x, ranked_data["incidence_rate"], width=bar_width, label="Incidence Rate", color="skyblue")

# Mortality rates
plt.bar([pos + bar_width for pos in x], ranked_data["death_rate"], width=bar_width, label="Mortality Rate", color="salmon")


plt.xticks([pos + bar_width / 2 for pos in x], ranked_data["state"], rotation=90)

plt.title("State Rankings: Incidence Rate vs Mortality Rate", fontsize=16)
plt.xlabel("State", fontsize=12)
plt.ylabel("Rates (per 100,000)", fontsize=12)
plt.legend()
plt.tight_layout()

plt.savefig("state_rankings_incidence_vs_mortality.png")
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Sort by incidence and mortality rates
ranked_data = ranked_data.sort_values("death_rate", ascending=False)

# Plot the grouped bar chart
plt.figure(figsize=(14, 10))
x = range(len(ranked_data))  # Position for each state
bar_width = 0.4


# Mortality rates
plt.bar([pos + bar_width for pos in x], ranked_data["death_rate"], width=bar_width, label="Mortality Rate", color="salmon")


plt.xticks([pos + bar_width / 2 for pos in x], ranked_data["state"], rotation=90)


plt.title(" Mortality Rate", fontsize=16)
plt.xlabel("State", fontsize=12)
plt.ylabel("Rates (per 100,000)", fontsize=12)
plt.legend()
plt.tight_layout()


plt.savefig('mortality.png')
plt.show()

import pandas as pd

# Ensure columns are numeric
ranked_data["poverty_rate"] = pd.to_numeric(ranked_data["poverty_rate"], errors="coerce")
ranked_data["incidence_rate"] = pd.to_numeric(ranked_data["incidence_rate"], errors="coerce")
ranked_data["death_rate"] = pd.to_numeric(ranked_data["death_rate"], errors="coerce")

# Drop rows with missing data in any of the relevant columns
ranked_data = ranked_data.dropna(subset=["poverty_rate", "incidence_rate", "death_rate"])

#  rankings
ranked_data["poverty_rank"] = ranked_data["poverty_rate"].rank(ascending=False).astype(int)
ranked_data["incidence_rank"] = ranked_data["incidence_rate"].rank(ascending=False).astype(int)
ranked_data["mortality_rank"] = ranked_data["death_rate"].rank(ascending=False).astype(int)

# relevant columns
rankings = ranked_data[[
    "state", "poverty_rate", "poverty_rank",
    "incidence_rate", "incidence_rank",
    "death_rate", "mortality_rank"
]]

# Sort by burden
rankings = rankings.sort_values(by=["poverty_rank", "incidence_rank", "mortality_rank"])

#  CSV
rankings.to_csv("state_rankings_poverty_incidence_mortality.csv", index=False)

# Display rankings
print(rankings)

import statsmodels.api as sm

# Prepare  data for regression analysis

ranked_data["poverty_rate"] = pd.to_numeric(ranked_data["poverty_rate"], errors="coerce")
ranked_data["incidence_rate"] = pd.to_numeric(ranked_data["incidence_rate"], errors="coerce")
ranked_data["death_rate"] = pd.to_numeric(ranked_data["death_rate"], errors="coerce")

# Drop rows with missing values
regression_data = ranked_data.dropna(subset=["poverty_rate", "incidence_rate", "death_rate"])

#  independent (X) and dependent (y) variables
X = regression_data[["poverty_rate", "incidence_rate"]]
X = sm.add_constant(X)
y = regression_data["death_rate"]

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the regression summary
print(model.summary())