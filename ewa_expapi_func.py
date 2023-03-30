import requests, json, os

proapiBaseURL = os.getenv("proapi")

def load_resource(url):
    resp = requests.get(url)
    if(resp.ok):
        resource = resp.json()
        return json.dumps(resource)
    else:
        return None

def validate(login_dict):
    #validate login
    resp = requests.post(proapiBaseURL + "/validate", json=json.dumps(login_dict))
    return resp.ok
    
def load_user(email):
    url = proapiBaseURL + "/load_user?email=" + email
    print(url)
    return load_resource(url)

def load_user_emails(userid):
    #TODO complete this
    return load_resource(proapiBaseURL + "/user/" + userid + "/emails")

def load_user_dashboard(email):
    return load_resource(proapiBaseURL + "/get_dashboard?email=" + email)

def save_new_email(email_dict):
    #print("ewa_expapi_func.py: type of email_dict", type(email_dict))
    #print("ewa_expapi_func.py: type of json.dumps(email_dict)", type(json.dumps(email_dict)))
    resp = requests.post(proapiBaseURL + "/save_email", json=json.dumps(email_dict))
    return resp.ok

def update_draft(email_dict):
    resp = requests.put(proapiBaseURL + "/save_email", json=json.dumps(email_dict))
    return resp.ok
    
def update_user(userid, user_details):
    url = proapiBaseURL + "/update-user/" + str(userid)
    resp = requests.put(url, json=json.dumps(user_details))
    return resp.ok

def create_user(user_details):
    resp = requests.post(proapiBaseURL + "/create-user", json=json.dumps(user_details))
    return resp.ok

def generate_token(email_address):
    resp = requests.get(proapiBaseURL + "/generate-token?email=" + email_address)
    if resp.ok:
        return resp.json()
    else:
        return None
    
def isAuthorised(token, email):
    authorisation_dict = {
        "Token" : token,
        "Email Address" : email
    }
    resp = requests.post(proapiBaseURL + "/authorise", json=json.dumps(authorisation_dict))
    return resp.ok