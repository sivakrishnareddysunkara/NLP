import os
import re
import glob 
import argparse 
import pandas as pd
from text_utils import html2txt,get_emails,get_name 
from text_utils import drop_special_characters,get_experince



def jd_parser(input_dir):
    files = glob.glob (input_dir + os.sep + "jd*/*")

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
       count +=1
    return df 

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-dir',help='Input dir')
    parser.add_argument('-o','--output-file',help='Output file')
    args = parser.parse_args()
    
    df =  jd_parser(args.input_dir) 

    df.to_csv(args.output_file) 
