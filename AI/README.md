# Recuiter Buddy AI/ML Backend 


## Summary 
 
  - The purpose of this module is to match the candidates for a given job description on the basis of machine learning.
  In the first step a set of job descriptions & candidate profiles are downloaded from Azure blob storage [which were 
  downloaded from Bullhorn] and then pre-processed for downstream machine learning task.

  - All the packages needed are specified in the install.txt 

  - The basis idea is as follows:
    
    * Get a lits of resume and featureize those (extract lingustic & numerical)

    * Do the same for Job description for 

    * Find a common space for resume and JDs

    * Develop a matching and ranking procedure which may involve ML, NLP and other techniques.

  
## Installation  

   - Install [anaconda3](https://www.anaconda.com/products/individual) 

   - Create vitual env 

      conda create --name rbml_env  python=3.7 --no-default-packages 

   - Switch to virtul env

       conda activate rbml_env

   -  Install required packages 
 
       pip install -r requirements.txt  --ignore-installed

   - Change to 'srv' and launch the ml engine 

      cd srv

      python app.py 

   - Test the server by visiting the following URL  
   [http://127.0.0.1:5000/api/v1.0](http://127.0.0.1:5000/api/v1.0)

## API Calls
   - Get all jobs 
   [http://127.0.0.1:5000/api/v1.0/jobs](http://127.0.0.1:5000/api/v1.0/jobs)
   - Get all candidates 
   [http://127.0.0.1:5000/api/v1.0/candidates](http://127.0.0.1:5000/api/v1.0/candidates)
   - Find matching candidates 
   [http://127.0.0.1:5000/api/v1.0/get_candidates/?job_id=Job_288220](http://127.0.0.1:5000/api/v1.0/get_candidates/?job_id=Job_288220)
   - Find matching score  
   [http://127.0.0.1:5000/api/v1.0/get_match_score/?job_id=Job_288332&cnd_id=Candidate_16061920](http://127.0.0.1:5000/api/v1.0/get_match_score/?job_id=Job_288332&cnd_id=Candidate_16061920)
   - Similar candidates  
   [http://127.0.0.1:5000/api/v1.0/similar_candidates/?cnd_id=Candidate_16057614](http://127.0.0.1:5000/api/v1.0/similar_candidates/?cnd_id=Candidate_16057614)
   - Similar jobs 
   [http://127.0.0.1:5000/api/v1.0/similar_jobs/?job_id=Job_287923](http://127.0.0.1:5000/api/v1.0/similar_jobs/?job_id=Job_287923) 
   - Show data    
   * [http://127.0.0.1:5000/api/v1.0/show/?job_id=Job_288109](http://127.0.0.1:5000/api/v1.0/show/?job_id=Job_288109)
   * [http://127.0.0.1:5000/api/v1.0/show/?cnd_id=Candidate_16060890](http://127.0.0.1:5000/api/v1.0/show/?cnd_id=Candidate_16060890)





