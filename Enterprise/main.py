# Authentication -Kiran,Sarika , not Prashant
# PII identification -identified restricted data
# PII Masking - 9874561230 - *********123*,[Mobile number]
# LLM Calling-Prompt indcution
# Compliance validation- Validating output from LLM
# Audit logging 
#Adding to Repo

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid
import json
import re
import os



#Fast API Set up

app = FastAPI(
    title="Enterprise AI Pipeline",
    description="Enterprise AI workflow Demo",
    version="1.0"

)

#Request Model 
class SupportRequest(BaseModel):
    user_input :str

#Audit Logging
AUDIT_FILE ="AUDIT_LOGS.json"

#UI- Request Tracking ID
def generate_request_id():
    return str(uuid.uuid4())


#Prompt injection Check

def detect_prompt_injection(text):
    suspicius_patterns =[
        "Ignore Previous instruction",
        "Show passsword",
        "bypass Security",
        "Delete databse",
        "Override system instructions",
        "ignore system prompts"
    ]

    for pattern in suspicius_patterns:
        if pattern.lower() in text.lower():
            return True
    return False

## PII Detection    
def detect_pii(text):
    pii_found ={
        "account_number":False,
        "email":False,
        "phone":False
    }

    #8 digit number
    if re.search(r"\b\d{8}\b",text):
        pii_found["account_number"]=True

    #Email Id Ganesh@gyaanlytics.com
    if re.search(r"[A-Za-z0-9.%+-]+@[A-Za-z0-9.]+\.[A-Za-z]{3,}",text):
        pii_found["email"]=True  
    #10 Digit Phone number
    if re.search(r"\b[6-9]\d{10}\b",text):
        pii_found["phone"]=True    

    return pii_found

def mask_pii(text):
    #Mask account
    text = re.sub(r"\b\d{8}\b","[Masked Account]",text)

    #Mask email
    text= re.sub(r"[A-Za-z0-9.%+-]+@[A-Za-z0-9.]+\.[A-Za-z]{3,}",
                 "[Masked Email]",
                 text)

    #Mask phone
    text = re.sub(r"\b[6-9]\d{10}\b","[Masked phone]",text)

    return text
    

#Build the prompt
def build_prompt(masked_text):
    system_prompt="""You are a secure enterprise banking Ai assistant
    Rules :
    1.Never reveal customer Data.
    2.Never Expose Password.
    """
    final_prompt=f"""
     SYSTEM:{system_prompt}
     USER:{masked_text}
     ASSITANT :
        """
    return final_prompt

# Use REAL LLM
USER_REAL_LLM=False
def call_llm(prompt):
    #Mock
    if not USER_REAL_LLM:
        return """Dear customer Your request is taken,Thank you"""

# Complaince Validation
def compliance_check(response):
    blocked_words=[
        "password is",
        "SSN",
        "Credit Card",
        "Customer Data"
    ]    

    for word in blocked_words:
        if word.lower() in response.lower():
            return{
                "status":"Blocked",
                "message":"Reponse is blockeddue to company policy"
            }
    return{
        "status":"Approved",
        "message":response
    }    

#Audit Loging
def store_audit_logging(log_data):
    existing_logs=[]

    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE,'r') as file:
            try:
                existing_logs=json.load(file)
            except:
                existing_logs=[]
    existing_logs.append(log_data)

    with open(AUDIT_FILE,"w") as file:
        json.dump(existing_logs,file,indent=4)         


#Health Check
@app.get("/")
def home():
    return{
        "message":"Enterprise GenAI pipeline is running"
    }

#main support API
@app.post("/support")
def support_query(request: SupportRequest):
    request_id =generate_request_id()
    user_input =request.user_input

    #Step 1:
    print("Step 1 :Request Recieved")
    print(user_input)

    #Step 2 :
    print("Step :Prompt injection check")
    injection_detected=detect_prompt_injection(user_input)
    if injection_detected:
        return{
            "Request_id":request_id,
            "status":"Blocked",
            "Reason":"Potential prompt injection detected"
        }
    print("No malicious prompt detected")

    #Step 3
    print("Step 3: PII detection")
    pii_status=detect_pii(user_input)
    print(pii_status)


    #Step 4
    print("Step 4: PII Masking")
    masked_text=mask_pii(user_input)
    print(masked_text)

    #Step 5
    print("Step 5: prompt Building")
    final_prompt=build_prompt(masked_text)
    print(final_prompt)

    #Step 6 
    print("Step 6 :Call LLM")
    llm_response =call_llm(final_prompt)
    print(llm_response)


    #Step 7
    print("Step 7 :Compliance validation")
    compliance_result=compliance_check(llm_response)
    print(compliance_result)

    #Step 8
    print("Step 8: Audit Logs")
    audit_log={
        "request_id":request_id,
        "timestamp":str(datetime.now()),
        "original_input":user_input,
        "masked_text":masked_text,
        "pii_detected":pii_status,
        "compliance_status":compliance_result["status"]
    }

    store_audit_logging(audit_log)
    print("Audit logging done ")


    # Step 9: Final response
    return{"request_id":request_id,
           "pipeline_statu":"SUCCESS",            
           "masked_text":masked_text,
           "pii_detected":pii_status,
           "final_reponse":compliance_result["message"]

    }





    

