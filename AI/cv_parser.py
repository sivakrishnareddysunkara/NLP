import os
import re
import glob 
import argparse 
import pandas as pd
from text_utils import html2txt,get_emails,get_name,get_education  
from text_utils import drop_special_characters,get_experince


def cv_parser(input_dir):

    files = glob.glob (input_dir + os.sep + "cv*/*")

    df = pd.DataFrame (columns=['cnd_id','name','email','exp','edu','skills'])
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
       print(count, name, email,edu,skills)
       
    return df 

if __name__ == "__main__":

    """
    Parse cv in html format and writes all the data in a csv file
    after extracting key features.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-dir',help='Input dir')
    parser.add_argument('-o','--output-file',help='Output file')
    args = parser.parse_args()

    df = cv_parser(args.input_dir)

    df.to_csv(args.output_file)
