import os

class Config:
    def __init__(self, cfg_parser):
        self.cfg_parser = cfg_parser
        self.issue_key =  None
        self.logfile = None

    def input_dir(self):
        return self.cfg_parser.get('input', 'input_dir')

    def workspace_dir(self):
        work_dir = self.cfg_parser.get('input', 'workspace_dir')
        os.makedirs(work_dir, exist_ok=True)

    def output_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "output"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir
  
    def model_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "models"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def training_data_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "training_data"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def inference_data_dir(self):
        return self.cfg_parser.get('input', 'inference_data')



    def log_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "log"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir

    def vocab_file(self):
        return self.cfg_parser.get('input', 'vocab_file')

    def az_connection_string(self):
        return self.cfg_parser.get('azure', 'az_connection_string')

    def workspace_dir(self):
        work_dir = self.cfg_parser.get('input', 'workspace_dir')
        os.makedirs(work_dir, exist_ok=True)
        return work_dir

    def download_dir(self):
        tmp_dir =  self.workspace_dir() + os.sep + "download"
        os.makedirs(tmp_dir, exist_ok=True)
        return down_dir

    def az_connection_string(self):
        return self.cfg_parser.get('azure', 'az_connection_string')        

    def num_input_tokens_cv(self):
        return self.cfg_parser.getint('ml-mlp', 'num_input_tokens_cv')
  
    def num_input_tokens_jd(self):
        return self.cfg_parser.getint('ml-mlp', 'num_input_tokens_jd')
  
    def len_input_vec_cv(self):
        return self.cfg_parser.getint('ml-mlp', 'len_input_vec_cv')
  
    def len_input_vec_jd(self):
        return self.cfg_parser.getint('ml-mlp', 'len_input_vec_jd')
  
    def latent_dim(self):
        return self.cfg_parser.getint('ml-mlp', 'latent_dim')
  
    def num_output_labels(self):
        return self.cfg_parser.getint('ml-mlp', 'num_output_labels')

    def batch_size(self):
        return self.cfg_parser.getint('ml-mlp', 'batch_size')

    def nepochs(self):
        return self.cfg_parser.getint('ml-mlp', 'nepochs')

    def validation_split(self):
        return self.cfg_parser.getfloat('ml-mlp', 'validation_split')

    def len_min_vec(self):
        return self.cfg_parser.getint('ml-mlp', 'len_min_vec')

