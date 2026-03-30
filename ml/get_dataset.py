import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_formatted_dataset():
    file_path = os.path.join(os.getcwd(), "csv_files", "dataset.csv")
    df = pd.read_csv(file_path)
    df_list = df.values.tolist()

    entries = []
    for entry in df_list:
        entry[1] = str(entry[1])
        row = "input: " + entry[0] + "\nserious: " + entry[1] + "\nlength: " + entry[2] + "\noutput: " + entry[3]
        entries.append(row)
        
    return entries
        
if __name__ == "__main__":
    entries = get_formatted_dataset()
    
    print(entries)
    