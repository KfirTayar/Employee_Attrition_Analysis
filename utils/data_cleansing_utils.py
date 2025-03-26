import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Create a heatmap that represents the missing values in the DF
def plot_missing_heatmap(df, title="Missing Values Heatmap"):
    """
    Plots a heatmap showing missing values in a DataFrame.
    - White (lighter) areas indicate missing values.
    
    Parameters:
    - df: DataFrame with missing values.
    - title: Title for the plot.
    """
    plt.figure(figsize=(13, 6))
    sns.heatmap(df.isnull(), cmap='viridis', cbar=False, yticklabels=False)
    plt.title(title, fontsize=14)
    plt.show()

# Replace outlies with NaN values using IQR method
def replace_outliers_with_nan(df, threshold=1.5):
    df_clean = df.copy()
    
    for col in df_clean.columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        # Replace outliers with NaN
        df_clean[col] = df_clean[col].apply(lambda x: np.nan if x < lower_bound or x > upper_bound else x)

    return df_clean

# Fill missing values (outliers) using MICE method
def fill_missing_mice(df, max_iter=10, random_state=42):
    """
    Fills NaN values using the MICE (Iterative Imputer) method, setting 
    min_value and max_value dynamically for each feature.

    Parameters:
    - df: DataFrame with missing values.
    - max_iter: Number of imputation iterations.
    - random_state: Ensures reproducibility.

    Returns:
    - DataFrame with NaN values imputed.
    """
    # Get min and max for each column
    min_vals = df.min()
    max_vals = df.max()

    # Define the imputer with dynamic min/max values
    imputer = IterativeImputer(
        max_iter=max_iter, 
        random_state=random_state, 
        min_value=min_vals.values, 
        max_value=max_vals.values
    )
    
    # Apply the imputer
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    return df_imputed