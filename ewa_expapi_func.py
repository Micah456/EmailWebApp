import requests, json
def login(login_dict):
    #validate login
    resp = requests.post("http://127.0.0.1:5000/pro-api/validate", json=json.dumps(login_dict))
    if(resp.ok):
        return True
    else:
        return False
    