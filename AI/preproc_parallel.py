import argparse 
from parallel_process import parallel_process 
import os
import re
import glob
import argparse
import pandas as pd
from text_utils import html2txt,get_emails,get_name,get_education
from text_utils import drop_special_characters,get_experince
from preprocessor import  get_cleaned_data, get_dict, get_common_dict,trim_text 
from logutil import get_logger 


def cv_parser(w, cfg, files, return_dict):

    df = pd.DataFrame (columns=['cnd_id','name','email','exp','education','skills'])
    count = 0
    for f in files:
       with open (f,"r",encoding='cp1252') as fp:
          data = fp.read()
       text = html2txt (data)
       email = get_emails (text)
       exp = get_experince (text.lower())

       cndid = os.path.basename (f).split('.')[0]
       text = drop_special_characters(text)
       skills = text.lower().split('skills')
       name  = get_name (text)
       edu = get_education (text)

       if len (skills) > 1:
          skills = skills[1]
       else:
          skills = ""

       data = [cndid, name, email,exp,edu,skills]
       df.loc[count] = data
       count +=1
       print(count, f)

    return_dict[w] = df


def jd_parser(w, cfg, files, return_dict):

    df = pd.DataFrame (columns=['job_id','exp','requirements','responsibilities'])
    count = 0
    for f in files:
       with open (f,"r",encoding='cp1252') as fp:
          data = fp.read()
       text = html2txt (data).lower()
       exp = get_experince (text)
       jobid = os.path.basename (f).split('.')[0]

       requirements = text

       responsibilities = ""

       if 'requirements' in text:
           requirements  = text.split('requirements')[1]
       if 'responsibilities' in text:
           responsibilities = text.split('responsibilities')[1]

       data = [jobid,exp,requirements,responsibilities]
       df.loc[count] = data
       print(count, f)
       count +=1
    return_dict[w] = df


def cleaned_data_cv (w, cfg, df, return_dict):
    df['skills'] = df['skills'].apply(trim_text) 
    return_dict[w] = df 
 
def cleaned_data_jd (w, cfg, df, return_dict):
    df['requirements'] = df['requirements'].apply(trim_text)
    return_dict[w] = df 

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rb_ml')
    parser.add_argument('-i', '--input-dir', help='Input data dir', required=True)
    parser.add_argument('-o', '--output-dir', help='Output data dir', required=True)
    parser.add_argument('-v', '--vocab-dir', help='Vocabulary data dir')
    parser.add_argument('-n', '--num-processes',type=int,default=8,help='Num processes')

    args = parser.parse_args()

    os.makedirs(args.output_dir,exist_ok=True)

    args.logger = get_logger('parse_log','log','parse.log', log_level='DEBUG', log_to_console=True)

    all_files_cv = glob.glob (args.input_dir + os.sep + "cv*/*")
    df_parsed_cv = parallel_process(args, cv_parser, all_files_cv)
    args.logger.info("CV parsed:" +str(df_parsed_cv.shape))
    df_parsed_cv.to_csv (args.output_dir + os.sep + "cv_parsed.csv")


    all_files_jd = glob.glob (args.input_dir + os.sep + "jd*/*")
    df_parsed_jd = parallel_process(args, jd_parser, all_files_jd)
    args.logger.info("JD parsed:" +str(df_parsed_jd.shape))
    df_parsed_jd.to_csv (args.output_dir + os.sep + "jd_parsed.csv")

    df_cleaned_cv = parallel_process(args, cleaned_data_cv, df_parsed_cv)
    args.logger.info("CV cleaned:" + str(df_cleaned_cv.columns))

    df_cleaned_jd = parallel_process(args, cleaned_data_jd, df_parsed_jd)
    args.logger.info("JD cleaned:" + str(df_cleaned_jd.columns))

    df_cleaned_cv.to_csv(args.output_dir + os.sep + "cv_cleaned.csv")
    df_cleaned_jd.to_csv(args.output_dir + os.sep + "jd_cleaned.csv")

    if args.vocab_dir:
        os.makedirs(args.vocab_dir,exist_ok=True)
        # get dictionaries 
        args.logger.info("Building dictionries")
        df_dict_cv = get_dict (df_cleaned_cv,'skills')
        df_dict_jd = get_dict (df_cleaned_jd,'requirements')
        df_dict_cm = get_common_dict (df_dict_cv,df_dict_jd)

        df_dict_cv.to_csv(args.vocab_dir + os.sep + "cv_vocab.csv")
        df_dict_jd.to_csv(args.vocab_dir + os.sep + "jd_vocab.csv")
        df_dict_cm.to_csv(args.vocab_dir + os.sep + "cm_vocab.csv")
    args.logger.info("Everything done")



