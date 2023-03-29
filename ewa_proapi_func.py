import requests, json, ast, os, random, math
from datetime import datetime, date, timedelta

sysapiBaseURL = os.getenv("sysapi")

def validate(login_dict):
    #Convert to dict if str
    if type(login_dict) == str:
        login_dict = ast.literal_eval(login_dict)
        print("After converting to dict: ",type(login_dict))
    #Find user in database
    user_dict = json.loads(load_user(login_dict['email']))
    print("user_dict type: ", type(user_dict))
    #Check if user is valid
    if(user_dict):
        #If user is valid
        #Compare password with user password on db
        if(user_dict['Password'] == login_dict['password']):
            #If match, return true
            return True
    #User not found OR password doesn't match
    return False

def load_user(email):
    #Load all users
    print(sysapiBaseURL)
    resp = requests.get(sysapiBaseURL + "/users")
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

def load_user_emails(userid):
    user_email_address = get_user_email_address(userid)
    if(user_email_address == None):
        return None
    #Load all emails
    resp = requests.get(sysapiBaseURL + "/emails")
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
    url = sysapiBaseURL + "/users/" + str(userid)
    resp = requests.get(url)
    user_dict = resp.json()
    #Return address
    try:
        email_address = user_dict['Email Address']
    except:
        email_address = None
    finally:
        return email_address

def get_dashboard(email):
    user = load_user(email)
    print(user)
    try:
        user_dict = json.loads(user)
    except:
        return None
    userid = user_dict['ID']
    #Get email dict
    user_emails = load_user_emails(userid)
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
        resp = requests.post(sysapiBaseURL + "/emails", json=json.dumps(email_dict))
    else:
        #PUT
        url = sysapiBaseURL + "/emails/" + str(email_dict['ID'])
        resp = requests.put(url, json=json.dumps(email_dict))
    return resp.ok

def update_user(userid, user_details):
    #Send user to sys api
    print(type(user_details))
    url = sysapiBaseURL + "/users/" + str(userid)
    resp = requests.put(url, json=json.dumps(user_details))
    return resp.ok

    
def create_user(user_details):
    #Check user doesn't exist
    found_user = load_user(user_details['Email Address'])
    if not(found_user):
        print("user not found")
        #User doesn't exist - send user to sys api
        resp = requests.post( sysapiBaseURL + "/users", json=json.dumps(user_details))
        return resp.ok
    #User does exist
    print("user found!")
    return False 

def generate_token(email_address):
    #Create random token
    token = create_token()
    print("token: " + token)
    #Create expiry date for token
    mydate = datetime.today()
    mydate = mydate + timedelta(days=5)
    print("Five days from now" + str(mydate))
    #Convert date to ms
    expdate = int(mydate.timestamp())
    if expdate < 1000000000000:
        expdate *= 1000
    print(expdate)
    #Create dict with email, token, and date
    token_dict = {
        "Email Address" : email_address,
        "Token" : token,
        "Expiry Date" : expdate
    }
    #Send dict to 
    resp = requests.post(sysapiBaseURL + "/tokens", json=json.dumps(token_dict))
    #If okay, return token
    if resp.ok:
        return token_dict
    else:
        return None

def generate_char_frag(start, stop):
    char_frag = ""
    for i in range(start,stop):
        char_frag += chr(i)
    return char_frag
    
def generate_char_string():
    char_string = generate_char_frag(48,58)
    char_string += generate_char_frag(65,91)
    char_string += generate_char_frag(97,123)
    return char_string

def create_token():
    char_string = generate_char_string()
    print(len(char_string))
    token = ""
    for i in range(25):
        rand = math.floor(random.random() * 62)
        token += char_string[rand]
    return token
