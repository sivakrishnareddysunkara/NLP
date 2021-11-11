
import fitz
import re
import spacy
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords 
import ConfigTesting as ct
import pandas as pd 


def extractDetails(text):
    EmpName= '' #initialising empty string in EmpName
    emailid= ''
    my_text=''
    check01=''
    phNum=''
    empNamePattern=re.compile(r'(([a-zA-Z]+((\ +\.)|(\.+\ )|\.|\ |)){1,4})')
    emailIdPattern=re.compile(r'(([a-zA-Z]{1})+[a-zA-Z0-9-_\.]+@+[a-zA-Z-\.]*\.(com|edu|net|in|COM|EDU|NET|IN))')
    phoneNumPattern=re.compile(r'(([(]?[+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d))')
    lineCount=0 
    for line in text.split('\n'):
        lineCount= lineCount+1
        if (EmpName is ""):
            if empNamePattern.search(line):
                check= empNamePattern.findall(line)
                TempEmpName= line.lower()
                TempEmpName= TempEmpName.replace(" ", "")
                if ("name" in TempEmpName and (len(check)== 1)):
                    continue
                elif ("curriculum" in TempEmpName or "ltd" in TempEmpName or "vitae" in TempEmpName or "resume" in TempEmpName or "confidential" in TempEmpName or "page" in TempEmpName or "profile" in TempEmpName):
                    continue
                elif "Name" in check[0][0] and check[1][0] != '':
                    EmpName= check[1][0]
                else:
                    EmpName= check[0][0]
            if(lineCount >= 15):
                EmpName= "Not Found"
        if (emailid is ""):
            if emailIdPattern.search(line):
                if "E-mail" in line:
                    my_text=line.split("E-mail",1)[1]
                else:
                    my_text= line
                
                check01= emailIdPattern.findall(my_text)
                if len(check01) >=1:
                    if len(check01[0][0]) >5:
                        emailid= check01[0][0]
                        
            if(lineCount >= 100):
                emailid= "Not Found"
        
        if (phNum is ""):
            if phoneNumPattern.search(line):
                check02= phoneNumPattern.findall(line)
                if len(check02) >1:
                    if len(check02[0][0]) <10:
                        phNum= check02[1][0]
                    else:
                        phNum= check02[0][0]
                elif len(check02) ==1:
                    if len(check02[0][0]) >= 10:
                        phNum= check02[0][0]
            if(lineCount >= 100):
                phNum= "Not Found"
        if(lineCount>= 100):
            break
    
    return EmpName, emailid, phNum

def ExtractEduSkills(text,sampleSkillsData):
    IsEducationFound=0
    edu = {}
    EDUCATION = [
            'BE', 'BS',
            'ME', 'MS',
            'BTECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', '10TH', '12TH', '10', '12'
        ]
    nlp= spacy.load('en_core_web_sm')
    word_Tokens= nltk.word_tokenize(text)
    stop_words= set(stopwords.words('english'))
    tokens_without_sw = [word for word in word_Tokens if not word in stop_words]
    nlp_text = nlp(text)
    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    for index, text01 in enumerate(nlp_text):
        for tex in text01.split():
            
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if ("edu" in tex.lower()):
                IsEducationFound=1
            if (IsEducationFound != 1):
                continue
            if tex.upper() in EDUCATION:
                if tex == "be" or tex == 'me':
                    continue
                if tex not in tokens_without_sw:
                    edu[tex] = tex
                else:
                    if "12" in tex or "10" in tex:
                        edu[tex] = tex
    skillset = []
    for token in tokens_without_sw:
        #if token.lower() in sampleSkillsData:
        if ((token.lower() in sampleSkillsData) and (token not in skillset)):
            skillset.append(token)
    return edu, skillset

def extractAllText(fileName,sampleSkillsData):
    page = 0
    text= ''
    doc = fitz.open(fileName)
    page_count = doc.pageCount
    while (page < page_count):
        p = doc.loadPage(page)
        page += 1
        text = text + p.getText()
    empName, emailID, phNum= extractDetails(text)
    
    Edu={}
    Edu, skillset= ExtractEduSkills(text,sampleSkillsData)
    #Edu={"a":"abc"}
    return empName, emailID, phNum, Edu, skillset
    
if __name__ == "__main__":
    #>>>>>>> sampleSkillsData WILL HAVE LIST OF SKILLS IN IT <<<<<<<
    skillsData = pd.read_csv(ct.skillFilePath)
    sampleSkillsData= list(skillsData.columns.values)
    #>>>>>>> * <<<<<<<
    empNameLst=[]
    emailIdLst=[]
    phNumLst=[]
    eduLst=[]
    skillsetLst=[]
    skillset=[]
    empName=''
    emailID=''
    phNum=''
    edu={}
    samplePdfPath=ct.samplePdfPath
    for file in os.listdir(samplePdfPath):
        if not(file.endswith(".pdf")):
            continue
        fileName= samplePdfPath+"\\"+file
        empName,emailID,phNum,edu,skillset= extractAllText(fileName,sampleSkillsData)
        empNameLst.append(empName)
        emailIdLst.append(emailID)
        phNumLst.append(phNum)
        eduLst.append(edu)
        skillsetLst.append(skillset)
    data = {'Name':empNameLst, 
        'Id':emailIdLst, 'PhNum':phNumLst, 'Edu':eduLst, 'Skills':skillsetLst} 
    df = pd.DataFrame(data) 
    print(df)
    