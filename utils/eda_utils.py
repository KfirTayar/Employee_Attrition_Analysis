import IPython.display as display
from scipy.stats import chi2_contingency
import pandas as pd
import datetime
import os

# Create a folder for data protocol and save the data protocol file in there
def data_protocol(processed_df, folder, df_name):
    # Select all the numeric features in the DF
    numerical_processed_df = processed_df.select_dtypes(include=['number'])
    
    print("Creating ", df_name,"_datatype\n", df_name,"_Max\n", 
          df_name,"_Min\n", df_name,"_Missing_Values\n", 
          "and ", df_name,"_Unique", " files...\n", sep='')

    # Define the folder and filename
    folder = f"{folder}/data_protocol"
    filename = f"../{folder}/{df_name}"

    # Create the folder if it doesn't exist
    os.makedirs(os.path.join('..', folder), exist_ok=True)
    
    # Type of values 
    numerical_processed_df.dtypes.to_excel(f"{filename}_datatype.xlsx",
                 sheet_name='data_type')
    # Maximum values 
    numerical_processed_df.max().to_excel(f"{filename}_Max.xlsx",
                 sheet_name='max')
    # Minimum values
    numerical_processed_df.min().to_excel(f"{filename}_Min.xlsx",
                 sheet_name='min')
    # Missing values
    numerical_processed_df.isnull().sum(axis=0).to_excel(f"{filename}_Missing_Values.xlsx",
                 sheet_name='NA')
    # Exporting results to the protocol
    numerical_processed_df.nunique().to_excel(f"{filename}_Unique.xlsx",
                 sheet_name='unique')

    print(f"Data Protocol process is done!")
    print(f"Saved path: {folder}")

# Display the png images from the AutoVis report
def display_png_plots(path, target_feature):
    # Path to the subfolder where AutoViz saves plots
    plots_path = os.path.join(f"{path}", target_feature)
    
    # List all PNG files in the directory
    if os.path.exists(plots_path):
        image_files = [f for f in os.listdir(plots_path) if f.endswith(".png")]
    
        # Display each image
        for image in image_files:
            img_path = os.path.join(plots_path, image)
            display.display(display.Image(filename=img_path))
    else:
        print(f"Directory {plots_path} does not exist!")

# Create a Skewness data frame of the continuous features
def skewness_report(processed_df: pd.DataFrame, continuous_features: list):
    # Calculate skewness for the selected features
    skewness_df = pd.DataFrame(processed_df[continuous_features].skew(), columns=['skewness'])
    # Sort the skewness values in descending order
    skewness_df = skewness_df.sort_values(by='skewness', ascending=False)
    
    # Apply styles directly
    return skewness_df.style.apply(
        lambda x: ['background-color: mediumspringgreen' if val > 1 else
                   'background-color: hotpink' if val < -1 else '' for val in x],
        subset=['skewness']
    )

# Perform a Chi-Square test for the categorical features
# Calculate only the cells in the bottom triangle to prevent duplicate cells.
def chi_square_matrix(df, categorical_features, alpha=0.05):
    """
    Compute the Chi-Square test between all pairs of categorical features 
    and return a styled dataframe with Chi-Square and P-value results.

    - Green: Significant (p < alpha)
    - Light red: Not significant (p >= alpha)
    - Light gray: Upper triangle
    - diagonal: Feature names
    """
    n = len(categorical_features)
    results = pd.DataFrame(index=categorical_features, columns=categorical_features, dtype=object)

    for i, col1 in enumerate(categorical_features):
        for j, col2 in enumerate(categorical_features):
            if i < j:  # Upper triangle
                results.loc[col1, col2] = " "  # Placeholder for styling
            elif i == j:  # Diagonal
                results.loc[col1, col2] = f"{col1}"
            else:  # Bottom triangle (Chi-Square test)
                contingency_table = pd.crosstab(df[col1], df[col2])
                chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
                results.loc[col1, col2] = f"χ²={chi2_stat:.2f}, p={p_value:.4f}"

    # Styling function
    def highlight_significance(val):
        if isinstance(val, str):
            if val.startswith("**"):  # Bold diagonal (feature names)
                return "font-weight: bold; text-align: center;"
            elif "p=" in val:  # Chi-Square results
                p_value = float(val.split("p=")[-1])  # Extract p-value
                return "background-color: lightgreen" if p_value < alpha else "background-color: lightcoral"
            elif val == " ":  # Upper triangle (blur)
                return "background-color: lightgray; color: lightgray"
        return ""

    return results.style.applymap(highlight_significance)