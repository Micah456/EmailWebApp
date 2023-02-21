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

def load_user_emails():
    #TODO complete this: also complete on ewa_server.py - the route has not yet been declared
    pass