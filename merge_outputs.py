import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

csv_files = [file for file in os.listdir(dir_path) if '.csv' in file and ".~lock." not in file]
print(csv_files)

for csv in csv_files:
    df = pd.read_csv(csv)
    print(df.to_string())
