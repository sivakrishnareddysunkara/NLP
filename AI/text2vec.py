import argparse 
from text_stats import  get_tokens
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def padding (vec, size=100):

    l = len (vec)
    if l >= size:
       return vec[:size]
    else:
       pad = [0 for i in range  (0, size-l)]
       return np.array (vec + pad)
 
def text2vec (text, df, vec_len):
    keys = df['token'].to_list()
    D = dict (zip (keys, [int(i) for i in range (0, len(keys))]))
    tokens = get_tokens (text)
    vec=[]
    for t in tokens:
      if t in D:
        vec.append (D[t])
     
    return padding (vec,vec_len) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input file')
    parser.add_argument('-o','--output-file',help='Output file')
    parser.add_argument('-v','--vocab-file',help='Vocab  file')
    parser.add_argument('-c','--column-name',help='Column name')
    parser.add_argument('-x','--index-column',help='Index column name')
    parser.add_argument('-l','--vec-len',type=int,help='Vector length',default=100)

    args = parser.parse_args()

    df  = pd.read_csv(args.vocab_file)
    df1 = pd.read_csv(args.input_file)

    column_data = df1[args.column_name].to_list()
    cols = ['dim_'+str(i) for i in range(0,args.vec_len)]
    dF = pd.DataFrame(columns=cols)

    count = 0 
    for s in column_data:
       v = text2vec (s, df,args.vec_len)
       print(count, v)
       dF.loc[count]=v 
       count +=1
    dF.index = df1[args.index_column].to_list()

    dF.to_csv(args.output_file) 
 


