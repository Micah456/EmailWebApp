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

def load_user(email):
    #Load all users
    resp = requests.get("http://127.0.0.1:5000/sys-api/users")
    user_dict = resp.json()
    #Filter users
    for i in range(len(user_dict)):
        found_user = user_dict[str(i)]
        found_email_address = found_user['Email Address']
        print(found_email_address)
        if found_email_address == email:
            return json.dumps(found_user)
    print("Email not found")
    return None

def load_user_emails(userid, user_email_address):
    #Load all emails
    resp = requests.get("http://127.0.0.1:5000/sys-api/emails")
    email_dict = resp.json()
    #Filter emails
    inbox_list = []
    sent_list = []
    drafs_list = []
    for i in range(len(email_dict)):
        found_email = email_dict[str(i)]
        if found_email['From Email'] == user_email_address:
            #sent email and drafts
            if found_email['Draft']:
                #Draft emails
                drafs_list.append(found_email)
            else:
                #Sent emails
                sent_list.append(found_email)
        elif found_email['To Email'] == user_email_address and not(found_email['Draft']):
            #inbox email
            inbox_list.append(found_email)
    #Return object containing all lists
    user_email_dict = {"Inbox Emails" : inbox_list,"Sent Emails" : sent_list, "Draft Emails" : drafs_list}
    user_emails = json.dumps(user_email_dict)
    return user_emails


def get_user_email_address(userid):
    #Load user
    url = "http://127.0.0.1:5000/sys-api/users/" + userid 
    resp = requests.get(url)
    user_dict = resp.json()
    #Return address
    return user_dict['Email Address']

def get_dashboard(email):
    user = load_user(email)
    print(user)
    user_dict = json.loads(user)
    userid = user_dict['ID']
    #Get email dict
    user_emails = load_user_emails(userid, email)
    user_emails_dict = json.loads(user_emails)
    #Return combined as json obj
    dashboard_dict = {"User Details" : user_dict, "User Emails" : user_emails_dict}
    return json.dumps(dashboard_dict)

def save_email(email_dict, methodType):
    #Check if email has recipient email
    print(email_dict)
    if not(email_dict["To Email"] == "{No Recipient Email}") or not(email_dict["Draft"]):
        #Validate toEmail and load recipient details
        try:
            recipient_dict = json.loads(load_user(email_dict["To Email"]))
        except:
            return None
        #Get and set recipient name
        recipient_name = recipient_dict["First Name"] + " " + recipient_dict["Last Name"]
        email_dict['To Name'] = recipient_name
    print(email_dict)
    #return json.dumps(email_dict)
    #Send email to sys api
    if methodType == "POST":
        resp = requests.post("http://127.0.0.1:5000/sys-api/emails", json=json.dumps(email_dict))
    else:
        #PUT
        url = "http://127.0.0.1:5000/sys-api/emails/" + str(email_dict['ID'])
        resp = requests.put(url, json=json.dumps(email_dict))
    if resp.ok:
        return True
    else:
        return False

def update_user(userid, user_details):
    #Send user to sys api
    print(type(user_details))
    url = "http://127.0.0.1:5000/sys-api/users/" + str(userid)
    resp = requests.put(url, json=json.dumps(user_details))
    if resp.ok:
        return True
    else:
        return False