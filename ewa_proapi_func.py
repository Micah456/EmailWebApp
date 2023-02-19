import requests, json, ast
def validate(login_dict):
    if type(login_dict) == str:
        login_dict = ast.literal_eval(login_dict)
        print("After converting to dict: ",type(login_dict))
    #Find user in database
    #Load all users
    resp = requests.get("http://127.0.0.1:5000/sys-api/users")
    user_dicts = resp.json()
    print(user_dicts)
    user_email = ""
    user_dict = {}
    i = 0
    while(i < len(user_dicts)):
        valid_user = user_dicts[str(i)]
        print("Printing type of valid user and login dict")
        print(type(valid_user))
        print(type(login_dict))
        if valid_user.get('Email Address') == login_dict['email']:
            user_email = valid_user['Email Address']
            user_dict = valid_user
            break
        i = i+1
    if(user_email):
        #Email is valid
        #Compare password with user password on db
        if(user_dict['Password'] == login_dict['password']):
            #If match, return true
            return True
        else:
            return False
    else:
        #Email not valid
        return False