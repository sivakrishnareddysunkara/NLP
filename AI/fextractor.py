import os
import argparse  
import configparser
import txt_clean_utils as cln 
import nlp_utils as nlpu 
import config
import glob
from candidates import Candidates 
from io_utils import write_output 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='rbuddy_data')
    parser.add_argument('-c', '--config', help='Config file path', required=True)

    cfg_parser = configparser.ConfigParser()

    args = parser.parse_args()

    cfg_parser.read(args.config)
    cfg = config.Config(cfg_parser)

    os.makedirs (cfg.workspace_dir(),exist_ok=True)

    files = glob.glob(cfg.input_data_dir() + os.sep + '*')

    C = Candidates (cfg)

    count = 0 
    for f in files[:100]:
       with open (f,'r',encoding='cp1252') as fp:
          html = fp.read()
       text = cln.html2txt(html)
       text = cln.drop_long_string(text, 40)
       print(count, f)
       count +=1
       C.update (text)

    write_output(cfg,C) 



