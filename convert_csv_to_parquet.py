import pandas as pd
import os

def convert_csv_to_parquet(csv_file, parquet_file):
    if os.path.exists(parquet_file):
        print(f"{parquet_file} already exists. Choose a different parquet file name, or delete the existing file.")
    else:
        #read csv file into pandas dataframe
        df = pd.read_csv(csv_file)
        
        #convert dataframe to parquet using a pandas method "to_parquet()" and the engine "pyarrow" (recommended over fastparquet)
        df.to_parquet(parquet_file, engine='pyarrow')


if __name__ == '__main__':
    #Example: convert xxxx.csv (file in the same folder as convert_csv_to_parquet.py) to output.parquet
    convert_csv_to_parquet('wages_japan.csv','wages_japan_parquet.parquet')