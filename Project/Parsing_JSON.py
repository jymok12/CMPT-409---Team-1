# %%
import pandas as pd
import os
import json
from datetime import datetime

# %%
df_data = pd.DataFrame()
for file in os.listdir('G:\CMPT 409\CMPT-409---Team-1\Project'):
    if file.endswith(".json"):
        print(file)
        df = pd.read_json(file)
        data = pd.json_normalize(df['data'])
        df_data = pd.concat([df_data, data])
        df_data = df_data.dropna(how='all')
df_data

# %%
df_data.to_csv('G:\CMPT 409\CMPT-409---Team-1\Project\combined_output.csv', index = False)



# %%
