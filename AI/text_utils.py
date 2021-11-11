import re
import glob
import os
from bs4 import BeautifulSoup
import pandas as pd

def num_there(s):
    return any(i.isdigit() for i in s)

def get_name (text):
    return " ".join (text.split('\n')[0].split(" ")[:3])


def drop_special_characters(text):
    return re.sub('[^A-Za-z0-9\n]+', ' ', text)

def drop_non_alpha(text):
    return re.sub('[^A-Za-z]+', ' ', text)

def get_experince (text):
    lines = text.split("\n")
    for line in lines:
       if 'experience' in line:
         if 'year' in line :
            if num_there(line) : 
               parts = line.split(" ")
               for p in parts:
                   if num_there(p):
                      return p + " years"

def html2txt(html):
   soup = BeautifulSoup(html)
   text = soup.get_text()
   lines = text.split('\n')
   lines = [l for l in lines if l]
   text = "\n".join(lines)

   return text


def drop_long_string(text, str_size):
    tokens = text.split(" ")
    tokens = [t for t in tokens if len(t) < str_size]
    return " ".join(tokens)
 

def get_emails (text):
    text  = text.replace('|',' ')
    emails =  re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
    if len (emails) >= 1:
        email = emails[0]
    else:
        email = ""
    return email   

def get_urls (text):
    return  re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)

def get_education (text):
    text = drop_special_characters(text)
    lines = text.split("\n")
    edu = " "
    for line in lines:
       if 'Master of' in line or  'Bachelor of' in line or 'Diploma in' in line:
          edu +=" ".join(line.split(" ")[:7])
    return edu


def get_ignore_words(inp_dir):
    files = glob.glob (inp_dir + os.sep +"/*.txt")
    files += glob.glob (inp_dir + os.sep + "/*.csv")
    ignore_words = []
    for f in files:
       print("Parsing :",f)
       ext = f.split(".")[-1]
       if ext == 'csv':
          df = pd.read_csv(f)
          for c in df.columns[1:]:
             ignore_words += df[c].to_list()
          ignore_words = list (set (ignore_words))

       if ext == 'txt':
          with open (f,'r') as fp:
             data = fp.read().split("\n")[:-1]
             ignore_words += data

    ignore_words = list (set (ignore_words))
    return ignore_words

