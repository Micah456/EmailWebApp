import requests, json
def validate(login_dict):
    #validate login
    resp = requests.post("http://127.0.0.1:5000/pro-api/validate", json=json.dumps(login_dict))
    if(resp.ok):
        return True
    else:
        return False
    
def load_user(email):
    #currently working on this
    url = "http://127.0.0.1:5000/pro-api/load_user?email="
    url = url + email
    resp = requests.get(url)
    if(resp.ok):
        user = resp.json()
        return json.dumps(user)
    else:
        return None

def load_user_emails(userid):
    #TODO complete this
    url = "http://127.0.0.1:5000/pro-api/user/" + userid + "/emails"
    resp = requests.get(url)
    if(resp.ok):
        user_emails = resp.json()
        return json.dumps(user_emails)
    else:
        return None

def load_user_dashboard(email):
    url = "http://127.0.0.1:5000/pro-api/get_dashboard?email=" + email
    resp = requests.get(url)
    if resp.ok:
        dashboard_dict = resp.json()
        return json.dumps(dashboard_dict)
    else:
        return None

def save_new_email(email_dict):
    #print("ewa_expapi_func.py: type of email_dict", type(email_dict))
    #print("ewa_expapi_func.py: type of json.dumps(email_dict)", type(json.dumps(email_dict)))
    resp = requests.post("http://127.0.0.1:5000/pro-api/save_email", json=json.dumps(email_dict))
    if resp.ok:
        return True
    else:
        return None

def update_draft(email_dict):
    resp = requests.put("http://127.0.0.1:5000/pro-api/save_email", json=json.dumps(email_dict))
    if resp.ok:
        return True
    else:
        return None