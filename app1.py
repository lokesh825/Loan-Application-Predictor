#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import pickle
import pandas as pd
import streamlit as st 
from sklearn import preprocessing
from PIL import Image

pickle_in = open("model.pkl","rb")
predicter=pickle.load(pickle_in)

applicant_income_min,applicant_income_max,coapplicant_income_min ,coapplicant_income_max=150.0, 10000.0, 0.0, 8980.0
loan_amountmin,loan_amount_max,loan_amount_term_min,loan_amount_term_max =  9.0, 480.0, 12.0, 360.0


#@app.route('/')
def welcome():
    
    return "Welcome All"

#@app.route('/predict',methods=["Get"])
def predict_status(details):
    prediction=predicter.predict_proba(details)
    return prediction

def normalise(x,xmin,xmax):
    if x>xmax:
        xmax = x
        x=(x-xmin)/(xmax-xmin)
    elif x<xmin:
        xmin = x
        x=(x-xmin)/(xmax-xmin)
    else:
        x=(x-xmin)/(xmax-xmin)
    return x   


def main():
    
    st.title("Loan Predictor")
    html_temp = """
    <div style="background-color:#FF0000;padding:10px">
    <h2 style="color:Black;text-align:center;">Loan Predictor App By Lokesh Bhirud </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    Gender = st.radio("Select your Gender",('Male', 'Female'))
    Married = st.radio("Are you Married",('Yes', 'No'))
    Education = st.radio("Select your Education",('Graduate', 'Not Graduate'))
    Self_Employed = st.radio( "Are you Self Employed",('Yes', 'No'))
    ApplicantIncome = st.number_input(label='Enter your Monthly Salary in INR', min_value=None, max_value=None)
    ai=ApplicantIncome
    CoapplicantIncome = st.number_input(label='Enter Co-applicant Monthly Salary in INR', min_value=None, max_value=None,format='%f')
    ci=CoapplicantIncome
    LoanAmount = st.number_input(label='Enter LoanAmount Required in INR', min_value=None, max_value=None,format='%f')
    la=LoanAmount
    Loan_Amount_Term = st.number_input(label='Enter Loan Amount Term in Months', min_value=60, max_value=None,format='%f')
    lat=Loan_Amount_Term
    Credit_History =  st.radio("Select your Credit History: ",('Yes', 'No'))
    Rural =  st.radio("Enter your Region you lIve in ",('Rural', 'Urban'))
    
    if float((ai+ci)*(lat)) >=(1.2)*la:
        k=1
    else: 
        k=0    
    
    if Gender=='Male':
        Gender = 1
    else:
        Gender = 0    
    if Married=='Yes':
        Married = 1
    else:
        Married = 0 
    if Education=='Graduate':
        Education = 1
    else:
        Education = 0 
    if Self_Employed=='Yes':
        Self_Employed = 1
    else:
        Self_Employed = 0      
    if Rural=='Rural':
        Rural = 1
        Urban = 0
    else:
        Rural = 0
        Urban = 1  
    if Credit_History=='Yes':
        Credit_History = 1
    else:
        Credit_History = 0
    LoanAmount=int(LoanAmount/1000) 
    ApplicantIncome=normalise(ApplicantIncome,applicant_income_min,applicant_income_max)
    CoapplicantIncome=normalise(CoapplicantIncome,coapplicant_income_min ,coapplicant_income_max)
    LoanAmount=normalise(LoanAmount,loan_amountmin,loan_amount_max)
    Loan_Amount_Term=normalise(Loan_Amount_Term,loan_amount_term_min,loan_amount_term_max)
    Details=[[Gender, Married,Education,Self_Employed
                    ,ApplicantIncome,CoapplicantIncome,LoanAmount, Loan_Amount_Term,Credit_History
                    ,Rural,Urban]] 
    result=""    
    if st.button("Check"):
        result=predict_status(Details)
        if result[0,1]>(0.5):
            result=1
        else:
            result=0
      
        if  result ==1 and k==1:
            result= str('Approved')
        else:
            result= str('Rejected')
    st.success(result)
 

if __name__=='__main__':
    main()
    
    
    


# In[ ]:




