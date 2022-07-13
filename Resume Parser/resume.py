from flask import request, redirect, Flask, render_template

import os

import docx
import pandas as pd
import spacy
import csv

import pickle
import io
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

#from package import lr1

#x=[]

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage




def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            yield text
            converter.close()
            fake_file_handle.close()



def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
nlp = spacy.load('en_core_web_sm')


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    return(tokens)
def matchjad(t,jad):
  for word in t:
    if word!="":
      word=word.lower()
      if word in jad.keys():
        jad[word]=1
def matchba(t,ba):
  for word in t:
    if word!="":
      word=word.lower()
      if word in ba.keys():
        ba[word]=1
def matchpm(t,pm):
  for word in t:
    if word!="":
      word=word.lower()
      if word in pm.keys():
        pm[word]=1
'''
def extract_education(resume_text):
    nlp = spacy.load('en_core_web_sm')
    STOPWORDS = set(stopwords.words('english'))
    EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII',
        ]
    ED2=['bachelorofengineering','bachelor','bachelors','masters','master','masterofengineering']
    nlp_text = nlp(resume_text)
    #nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    edu = {}
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text 
            if tex.lower() in ED2 and tex not in STOPWORDS:
                edu[tex] = text 
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return len(education)
'''
def extract_education(t):
    EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'bachelorofengineering','bachelor','bachelors','masters','master','masterofengineering']
    c=0
    for j in t:
        for i in EDUCATION:
            if(i==j):
                EDUCATION.remove(i)
                c=c+1
    return c
from spacy.matcher import Matcher
def wet(x):
  we=0
  dic={"microsoft":0,"google":0,"apple":0,"nasa":0,"walmart":0,"amazon":0,"sony":0,"baidu":0,"ibm":0,"lenevo":0,"hp":0,"amd":0,"nvidea":0,
        "sun":0,"cisco":0,"xerox":0,"dell":0,"yahoo":0,"oracle":0,"fujitsu":0,"adobe":0,"lenevo":0,"paypal":0,"goldmn sachs":0,"barclays":0,"verizon":0,
        "mckinsey":0,"comcast":0,"deloitte":0,"alibaba":0,"ey":0}
  d2=["worked at","work history","intern"]
  for i in x:
    if i in dic.keys():
      if(dic[i]==0):
        dic[i]==1
        we=we+1
        print(dic[i],i)
  if(we==0):    
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
# Add match ID "HelloWorld" with no callback and one pattern
    p1 = [{"LOWER": "work"},  {"LOWER": "history"}]
    p2=[{"LOWER": "work"},  {"LOWER": "expirience"}]
    p3=[{"LOWER":"intern"}]
    matcher.add("WorkHistory", [p1])
    matcher.add("WorkExpirience", [p2])
    matcher.add("WorkExpirience", [p3])
    doc = nlp(x)
    matches = matcher(doc)
    x=0
    for match_id, start, end in matches:
      if(x<1):
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        x=x+1
    we=x
  return we

def rea(utt):
    t=extract_skills(utt)
    edk=extract_education(t)
    wke=wet(utt)
    row_list=[["java","jsp","servlets","ejb","spring","soap","rest","html","css","javascript","jquery","xml","json","oops","oop","ajax",
            "tomcat""apache","jdk","jdbc","sql","oracle","xslt","struts","hibernate","dhtml","edk","wke"]]
    jad={"java":0,"jsp":0,"servlets":0,"ejb":0,"spring":0,"soap":0,"rest":0,"html":0,"css":0,"javascript":0,"jquery":0,"xml":0,"json":0,"oops":0,"oop":0,"ajax":0,
            "tomcat":0,"apache":0,"jdk":0,"jdbc":0,"sql":0,"oracle":0,"xslt":0,"struts":0,"hibernate":0,"dhtml":0,"edk":edk,"wke":wke}
    t=extract_skills(utt)
    matchjad(t,jad)
    l=[]
    for y in jad:
        l.append(jad[y])
    row_list.append(l)
    os.remove('test6.csv')
    with open('test6.csv', 'w', newline='') as file:            
        writer = csv.writer(file)
        writer.writerows(row_list)
            #f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    lr=pickle.load(open('m1.py', 'rb')) 
    fi='test6.csv'
    fi=pd.read_csv(fi)
    x=((lr.predict(fi.iloc[:,:])).tolist())
    return x

def reb(utt):
    t=extract_skills(utt)
    edk=extract_education(t)
    wke=wet(utt)
    row_list=[["access","sql","visio","jira","red mine","word","excel","snagit","rally","sharepoint","ms office suite","oracle","tdp","erwin","edk","wke"]]
    ba={"access":0,"sql":0,"visio":0,"jira":0,"red mine":0,"word":0,"excel":0,"snagit":0,"rally":0,"sharepoint":0,"office suite":0,"oracle":0,"tdp":0,"erwin":0,"edk":edk,"wke":wke}
    t=extract_skills(utt)
    matchba(t,ba)
    l=[]
    for y in ba:
        l.append(ba[y])
    row_list.append(l)
    os.remove('test6.csv')
    with open('test6.csv', 'w', newline='') as file:            
        writer = csv.writer(file)
        writer.writerows(row_list)
    #f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    lr=pickle.load(open('m2.py', 'rb')) 
    fi='test6.csv'
    fi=pd.read_csv(fi)
    x=((lr.predict(fi.iloc[:,:])).tolist())
    return x

def rec(utt):
    t=extract_skills(utt)
    edk=extract_education(t)
    wke=wet(utt)
    row_list=[["risk","agile","scrum","sql","oracle","edk","wke"]]
    pm={"risk":0,"agile":0,"scrum":0,"sql":0,"oracle":0,"edk":edk,"wke":wke}
    t=extract_skills(utt)
    matchba(t,pm)
    l=[]
    for y in pm:
        l.append(pm[y])
    row_list.append(l)
    os.remove('test6.csv')
    with open('test6.csv', 'w', newline='') as file:            
        writer = csv.writer(file)
        writer.writerows(row_list)
    #f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
    lr=pickle.load(open('m3.py', 'rb')) 
    fi='test6.csv'
    fi=pd.read_csv(fi)
    x=((lr.predict(fi.iloc[:,:])).tolist())
    return x
    
app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = "C:\\Resume\\"
@app.route("/upload_file",methods=["GET","POST"])


def upload_file():
    x=[]
    r=[]
    if request.method=='POST' : 
        os.remove("result2.txt")
        res=open("result2.txt",'a')
        for f in request.files.getlist('file_name'):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
            a='C:\\Resume\\'
            b=f.filename
            if b[-1]=='x':
                ut=getText(a+b)
            else :
                text=" "
                tl=[]
                for page in extract_text_from_pdf(a+b):
                    text += ' ' + page
                text = text.replace("\\n", "")
                text=' '.join(text.split())
                ut=text
            #t=extract_skills(ut)
            #edk=extract_education(t)
            #edk=1
            #wke=wet(ut)
            #wke=0
            if(request.form.get('roles')=='jd'):
                x=rea(ut)
                arr=b
                
                if(x[0]):
                    
                    arr+=" Selected"
                else :
                    arr+=" Not Selected"
                    y=reb(ut)
                    z=rec(ut)
                    if(y[0] or z[0]):
                        arr+=" The recommened role is "

                        if(y[0]):
                            arr+="Business Analyst"
                        if(z[0]):
                           # res.write("\t")
                            
                            arr+=" Project Manager"
                       # res.write(" ]")
                r.append(arr)



                    


                   
                
            elif(request.form.get('roles')=='ba'):
                x=reb(ut)
                arr=b
                if(x[0]):
                    
                    arr+=" Selected"
                else :
                    arr+=" Not Selected"
                    y=rea(ut)
                    z=rec(ut)
                    if(y[0] or z[0]):
                        arr+=" The recommended role is "
                        if(y[0]):
                            arr+="Java Developer"
                        if(z[0]):
                            #res.write("\t")
                            arr+=" Project Manager"
                        #res.write(" ]")
                r.append(arr)
                        
            elif(request.form.get('roles')=='pm'):
                x=rec(ut)
                arr=b
                
                if(x[0]):
                    arr+=" Selected"
                else :
                    arr+=" Not Selected"
                    y=rea(ut)
                    z=reb(ut)
                    if(y[0] or z[0]):
                        arr+=" The recommended role is "
                        if(y[0]):
                            arr+="Java Developer"
                        if(z[0]):
                            #res.write("\t")
                            arr+=" Business Analyst"
                        #res.write(" ]")
                r.append(arr)
            #res.write("\n")
            os.remove('C:\\Resume\\'+b)

            
        #return render_template("upload_image.html",msg=x)

    return render_template("upload_image.html",msg=r)

#res.close()
if __name__=='__main__' : 
    app.run(debug=True)
