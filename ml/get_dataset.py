import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_formatted_dataset():
    file_path = os.path.join(os.getcwd(), "csv_files", "dataset.csv")
    df = pd.read_csv(file_path)
    
    df = df.drop_duplicates()
    
    df_list = df.values.tolist()

    entries = []
    for entry in df_list:
        entry[2] = str(entry[2])
        row = (
            f"input: {entry[0]}\n"
            f"context: {entry[1]}\n"
            f"serious: {entry[2]}\n"
            f"length: {entry[3]}\n"
            f"output: {entry[4]}\n"
        )
        entries.append(row)
        
    return entries
        
if __name__ == "__main__":
    entries = get_formatted_dataset()[:10]
    
    for e in entries:
        print(e)
    