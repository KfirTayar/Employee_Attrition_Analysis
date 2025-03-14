import seaborn as sns
import matplotlib.pyplot as plt

# Create a heatmap that represents the missing values in the DF
def plot_missing_heatmap(df, title="Missing Values Heatmap"):
    """
    Plots a heatmap showing missing values in a DataFrame.
    - White (lighter) areas indicate missing values.
    
    Parameters:
    - df: DataFrame with missing values.
    - title: Title for the plot.
    """
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.isnull(), cmap='YlGnBu', cbar=False, yticklabels=False)
    plt.title(title, fontsize=14)
    plt.show()