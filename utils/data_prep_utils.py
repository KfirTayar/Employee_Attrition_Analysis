import pandas as pd
import datetime
import os

# Trun all the Object features into Category
def turn_object_into_category(df):
    for col in df.select_dtypes(['object']):
        df[col] = df[col].astype('category')

    return df

# Display summary of category cols
def display_category_summary(df):
    cat_summary_df = pd.DataFrame({
        "Feature": df.select_dtypes(['category']).columns,
        "Unique Values": [df[col].nunique() for col in df.select_dtypes(['category'])],
        "Categories": [df[col].unique().tolist() for col in df.select_dtypes(['category'])],   
    })
    
    cat_summary_df.set_index('Feature', inplace=True)
    return cat_summary_df

# Drop selected features
def drop_selected_cols(df, cols: list):
    for col in cols:
        df = df.drop(columns=[col])
        
    return df

# Save file as a pickle file
def save_file_as_pickle(df, folder: str, file_name: str): 
    # Generate current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d")

    # Define the folder and filename
    folder = folder
    filename = f"../{folder}/{file_name}_{timestamp}.pkl"

    # Create the folder if it doesn't exist
    os.makedirs(os.path.join('..', folder), exist_ok=True)

    # Save DataFrame as a pickle file
    df.to_pickle(filename)

    print(f"File saved as: {filename}")