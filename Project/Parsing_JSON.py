# %%
import pandas as pd
import os
import json
from datetime import datetime

# %%
dict_from_csv = pd.read_csv('G:\CMPT 409\CMPT-409---Team-1\Project\high_diamond_ranked_10min.csv', header = None, index_col = 0, squeeze = True).to_dict()

with open('dict.json','w') as fp:
    json.dump(dict_from_csv, fp)
dict_from_csv


