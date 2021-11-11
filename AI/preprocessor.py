import os
import argparse
import pandas as pd
from cv_parser import cv_parser
from jd_parser import jd_parser
from text_utils import drop_non_alpha,get_ignore_words

ignore_words = get_ignore_words ("config")

def trim_text (text_data):
    text_data = drop_non_alpha (str(text_data))
    tokens = str(text_data).split(" ")
    new_tokens = [t for t in tokens if t not in ignore_words and len(t) >2]
    return " ".join(new_tokens)


def get_parsed_data (args):
    df_cv = cv_parser(args.input_dir)
    df_jd = jd_parser(args.input_dir)
    return df_cv, df_jd 
 

def get_cleaned_data (df_cv, df_jd):
    df_cv['skills'] = df_cv['skills'].apply(trim_text)
    df_jd['requirements'] = df_jd['requirements'].apply(trim_text)
    return df_cv, df_jd 


def get_dict (df, column_name):
    text_data = df[column_name].to_list()
    text_data = " ".join(text_data)

    tokens = text_data.split(" ")
    D = {}
    for t in tokens:
       if t not in D:
          D[t] = 1
       else:
          D[t] +=1

    df = pd.DataFrame(columns=['tokens','freq'])
    df['tokens'] = [k for k in D.keys()]
    df['freq'] = [v for v in D.values()]
    df = df.sort_values(by='freq',ascending=False,ignore_index=True)
    df = df[df['freq'] > 5]
    return df


def get_common_dict (df1, df2):

    keys1 = df1['tokens'].to_list()
    keys2 = df2['tokens'].to_list()

    vocab  = [k for k in keys1 if k in keys2]

    df = pd.DataFrame(columns=['token'])
    df['token'] = vocab
    return df 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rb_ml')
    parser.add_argument('-i', '--input-dir', help='Input data dir', required=True)
    parser.add_argument('-o', '--output-dir', help='Output data dir', required=True)
    parser.add_argument('-v', '--vocab-dir', help='Vocabulary data dir', required=True)

    args = parser.parse_args()

    os.makedirs(args.output_dir,exist_ok=True)
    os.makedirs(args.vocab_dir,exist_ok=True)

    # parsed the html data 
    df_parsed_cv, df_parsed_jd = get_parsed_data (args)
    df_parsed_cv.to_csv(args.output_dir + os.sep + "cv_parsed.csv")
    df_parsed_jd.to_csv(args.output_dir + os.sep + "jd_parsed.csv")

    # cleaned the data 
    df_cleaned_cv, df_cleaned_jd = get_cleaned_data (df_parsed_cv, df_parsed_jd)
    df_cleaned_cv.to_csv(args.output_dir + os.sep + "cv_cleaned.csv")
    df_cleaned_jd.to_csv(args.output_dir + os.sep + "jd_cleaned.csv") 


    # get dictionaries 

    df_dict_cv = get_dict (df_cleaned_cv,'skills')
    df_dict_jd = get_dict (df_cleaned_jd,'requirements')
    df_dict_cm = get_common_dict (df_dict_cv,df_dict_jd)


    df_dict_cv.to_csv(args.vocab_dir + os.sep + "cv_vocab.csv")
    df_dict_jd.to_csv(args.vocab_dir + os.sep + "jd_vocab.csv")
    df_dict_cm.to_csv(args.vocab_dir + os.sep + "cm_vocab.csv")

