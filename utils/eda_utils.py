import IPython.display as display
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