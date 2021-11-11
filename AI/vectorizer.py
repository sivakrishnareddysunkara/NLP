import os
import argparse
import configparser
import pandas as pd
import argparse 
import numpy as np
import config


def vectorize  (df1, indx_column, data_column,vocab_file,num_tokens,vec_len,min_vec_len):

    df = pd.read_csv(vocab_file).iloc[:num_tokens]
    tokens = df['token'].to_list()
    ids = [i for i in range (0, df.shape[0])]
    D = dict (zip (tokens, ids))
   
    indices = []
    count = 0 

    columns = ["dim_"+str(i) for i in range (0, vec_len)]
    df_out = pd.DataFrame(columns=columns)


    for index, row in df1.iterrows():
        text_data = str(row [data_column])
        tokens = text_data.split(" ")
        vec = [D[t] for t in tokens if t in D]
        if len (vec) > min_vec_len :
           if len (vec) < vec_len:
              diff = vec_len - len (vec)
              vec += [0 for i in  range (0, diff)]
           else:
              vec = vec[:vec_len]
             
           df_out.loc[count] = vec 
           indices.append (row[indx_column])
           print(count, row[indx_column], len (vec))
           count +=1

    df_out.index = indices 
    return df_out  
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rb_ml')
    parser.add_argument('-c', '--config', help='Config file path', required=True)
    parser.add_argument('-i', '--input-dir', help='Input dir', required=True)
    parser.add_argument('-o', '--output-dir', help='Column name', required=True)

    cfg_parser = configparser.ConfigParser()
    args = parser.parse_args()

    os.makedirs(args.output_dir,exist_ok=True)

    cfg_parser.read(args.config)
    cfg = config.Config(cfg_parser)

    df_cleaned_cv = pd.read_csv(args.input_dir + os.sep + "cv_cleaned.csv")
    df_cleaned_jd = pd.read_csv(args.input_dir + os.sep + "jd_cleaned.csv")

    df_vec_cv = vectorize  (df_cleaned_cv,'cnd_id','skills',cfg.vocab_file(),\
        cfg.num_input_tokens_cv(),cfg.len_input_vec_cv(),cfg.len_min_vec()) 
 
    df_vec_cv.to_csv(args.output_dir + os.sep + "cv_vec.csv")

    df_vec_jd = vectorize  (df_cleaned_jd,'job_id','requirements',cfg.vocab_file(),\
        cfg.num_input_tokens_jd(),cfg.len_input_vec_jd(),cfg.len_min_vec())

    df_vec_jd.to_csv(args.output_dir + os.sep + "jd_vec.csv")

