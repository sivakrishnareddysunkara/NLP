import os
import re
import pandas as pd
import numpy as np

def get_commits_info(w, cfg, commits, return_dict):

    df = pd.DataFrame (columns=['cnd_id','name','email','exp','skills'])

    return_dict[w] = df


