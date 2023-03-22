import requests, json

def load_resource(url):
    resp = requests.get(url)
    if(resp.ok):
        resource = resp.json()
        return json.dumps(resource)
    else:
        return None

def validate(login_dict):
    #validate login
    resp = requests.post("http://127.0.0.1:5000/pro-api/validate", json=json.dumps(login_dict))
    return resp.ok
    
def load_user(email):
    #currently working on this
    return load_resource("http://127.0.0.1:5000/pro-api/load_user?email=" + email)

def load_user_emails(userid):
    #TODO complete this
    return load_resource("http://127.0.0.1:5000/pro-api/user/" + userid + "/emails")

def load_user_dashboard(email):
    return load_resource("http://127.0.0.1:5000/pro-api/get_dashboard?email=" + email)

def save_new_email(email_dict):
    #print("ewa_expapi_func.py: type of email_dict", type(email_dict))
    #print("ewa_expapi_func.py: type of json.dumps(email_dict)", type(json.dumps(email_dict)))
    resp = requests.post("http://127.0.0.1:5000/pro-api/save_email", json=json.dumps(email_dict))
    return resp.ok

def update_draft(email_dict):
    resp = requests.put("http://127.0.0.1:5000/pro-api/save_email", json=json.dumps(email_dict))
    return resp.ok
    
def update_user(userid, user_details):
    url = "http://127.0.0.1:5000/pro-api/update-user/" + str(userid)
    resp = requests.put(url, json=json.dumps(user_details))
    return resp.ok

def create_user(user_details):
    resp = requests.post("http://127.0.0.1:5000/pro-api/create-user", json=json.dumps(user_details))
    return resp.ok