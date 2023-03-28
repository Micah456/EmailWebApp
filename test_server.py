import unittest, json, os, requests, ewa_sysapi_func2 as sysapi
from dotenv import load_dotenv
load_dotenv()
expapiBaseURL = os.getenv("expapi")
#Switch emails_table to test one before running tests!
emails_table = os.getenv("emails_table")



resource_not_found = {"Message": "Resource not found."}
test_user = {
    "ID": 11,
    "Email Address": "user@test.com",
    "First Name": "Test",
    "Last Name": "User",
    "Gender": "N",
    "Password": "testpass"
}

test2_user = {
    "Email Address": "user2@test.com",
    "First Name": "Test2",
    "Last Name": "User",
    "Gender": "N",
    "Password": "testpass"
}

test2_user_updated = {
    "ID" : 70,
    "Email Address": "user2@test.com",
    "First Name": "Test2",
    "Last Name": "User",
    "Gender": "F",
    "Password": "testpass"
}

test_user_emails = {
    "Inbox Emails": [],
    "Sent Emails": [],
    "Draft Emails": []
}

login_dict = {
    "email" : test_user["Email Address"],
    "password" : test_user["Password"]
}

fake_login_dict = {
    "email" : "not@anemail.com",
    "password" : "notapassword"
}

incorrect_login_dict = {
    "email" : test_user["Email Address"],
    "password" : "notpassword"
}

new_valid_draft_email = {
    "Subject": "Test Email 2",
    "Date Sent": 1675260840000,
    "Message": "Test Message 2",
    "From Email": "user2@test.com",
    "From Name": "Test2 User",
    "To Email": "{No Recipient Email}",
    "To Name": "{No Recipient Name}",
    "Draft": True
}

updated_valid_draft_email = {
    "ID" : 1,
    "Subject": "Test Email 2",
    "Date Sent": 1675260840000,
    "Message": "Test Message 2",
    "From Email": "user2@test.com",
    "From Name": "Test2 User",
    "To Email": "user@test.com",
    "To Name": "{No Recipient Name}",
    "Draft": False
}

updated_invalid_draft_email = {
    "ID" : 1,
    "Subject": "Test Email 2",
    "Date Sent": 1675260840000,
    "Message": "Test Message 2",
    "From Email": "user2@test.com",
    "From Name": "Test2 User",
    "To Email": "not@anemail.com",
    "To Name": "{No Recipient Name}",
    "Draft": False
}

class TestServer(unittest.TestCase):
    def contains(iterable, item):
        for i in range(len(iterable)):
            if iterable[i] == item:
                return True
        return False
    
    def test_load_user(self):
        resp = requests.get(expapiBaseURL + "/user?email=" + test_user["Email Address"])
        assert resp.json() == test_user
        resp = requests.get(expapiBaseURL + "/user?email=not@anemail.com")
        assert resp.status_code == 404
        assert resp.json() == resource_not_found

    def test_load_user_emails(self):
        #Existing user
        resp = requests.get(expapiBaseURL + "/user/" + str(test_user["ID"]) + "/emails")
        assert resp.json() == test_user_emails
        #Non existent user
        resp = requests.get(expapiBaseURL + "/user/1000/emails")
        assert resp.status_code == 404
        assert resp.json() == resource_not_found
        #Non int URI param
        resp = requests.get(expapiBaseURL + "/user/notanumber/emails")
        assert resp.status_code == 404
        assert resp.json() == resource_not_found

    def test_load_dashboard(self):
        #Existing user
        resp = requests.get(expapiBaseURL + "/load_dashboard?email=" + test_user["Email Address"])
        assert resp.json() == {"User Details" : test_user, "User Emails" : test_user_emails}
        #Non existent user
        resp = requests.get(expapiBaseURL + "/load_dashboard?email=not@anemail.com")
        assert resp.status_code == 404
        assert resp.json() == resource_not_found

    def test_logout(self):
        #Set initial cookies
        session = requests.Session()
        cookies_to_set = {"email" : test_user["Email Address"], "is_logged_in" : "True"}
        session.cookies.update(cookies_to_set)
        #Check initial cookies set successfully
        initial_session_cookies = session.cookies.get_dict()
        assert initial_session_cookies == cookies_to_set
        assert TestServer.contains(list(initial_session_cookies.keys()), 'email')
        assert TestServer.contains(list(initial_session_cookies.keys()), 'is_logged_in')
        #Check user is logged in
        assert initial_session_cookies['is_logged_in'] == "True"
        assert initial_session_cookies['email'] == test_user["Email Address"]
        #Log out
        resp = session.get(expapiBaseURL + "/logout")
        #Check message says logout successful
        assert resp.json() == {"Message" : "Logout successful"}
        #Check is_logged_out set to False
        final_cookies = resp.cookies.get_dict()
        assert final_cookies['is_logged_in'] == "False"
        #Check there is no 'email' cookie
        assert TestServer.contains(list(final_cookies.keys()), 'email') == False

    def test_login(self):
        #Existing user
        #Check there are no cookies
        session = requests.Session()
        assert session.cookies.get_dict() == {}
        #Check message
        resp = session.post("http://127.0.0.1:5000/exp-api/login", json=json.dumps(login_dict))
        assert resp.json() == {"Message" : "Login successful"}
        #Check email and is_logged_in cookies are present
        session_cookies = session.cookies.get_dict()
        assert TestServer.contains(list(session_cookies.keys()), 'email')
        assert TestServer.contains(list(session_cookies.keys()), 'is_logged_in')
        #Check cookies values are correct
        assert session_cookies['email'] == '"' + test_user["Email Address"] + '"'
        assert session_cookies['is_logged_in'] == "True"

        #Existing user but wrong password
        #Check there are no cookies
        session = requests.Session()
        assert session.cookies.get_dict() == {}
        #Check message and status code
        resp = session.post(expapiBaseURL + "/login", json=json.dumps(incorrect_login_dict))
        assert resp.json() == {"Message":"Login unsuccessful"}
        assert resp.status_code == 401
        #Check email and is_logged_in cookies are NOT present
        session_cookies = session.cookies.get_dict()
        assert session_cookies == {}

        #Non existent user
        #Check there are no cookies
        session = requests.Session()
        assert session.cookies.get_dict() == {}
        #Check message and status code
        resp = session.post(expapiBaseURL + "/login", json=json.dumps(fake_login_dict))
        assert resp.json() == {"Message":"Login unsuccessful"}
        assert resp.status_code == 401
        #Check email and is_logged_in cookies are NOT present
        session_cookies = session.cookies.get_dict()
        assert session_cookies == {}

    def test_save_email(self):
        #Checks you are accessing correct table
        assert emails_table == "dbo.TestEmailCollection"
        print("Correct emails_table selected")
        if emails_table == "dbo.TestEmailCollection":
            #Create Draft Email
            #Send post request
            resp = requests.post(expapiBaseURL + "/save_email", json=json.dumps(new_valid_draft_email))
            #Check successful response
            assert resp.ok
            #If successful
            if resp.ok:
                #Check email exists in db
                email_dict = sysapi.test_email_exists(new_valid_draft_email)
                assert email_dict != None
                print("Original email: ")
                print(email_dict)

                #Update Draft Email with invalid info
                #If email created successfully
                if email_dict:
                    #Get ID
                    id = email_dict['ID']
                    print(id)
                    #Update id of invalid email
                    updated_invalid_draft_email["ID"] = id
                    #Send put request
                    resp = requests.put(expapiBaseURL + "/save_email", json=json.dumps(updated_invalid_draft_email))
                    #Check resp not ok
                    assert not(resp.ok)
                    if not(resp.ok):
                        email_dict = sysapi.test_email_exists(new_valid_draft_email)
                        #Check original email still there
                        assert email_dict != None
                        print("Email hasn't changed: ")
                        print(email_dict)
                        #Check original email still original
                        assert email_dict['To Email'] == new_valid_draft_email["To Email"]
                    
                    #Update Draft Email with valid info
                    #Update id of invalid email
                    updated_valid_draft_email["ID"] = id
                    #Send put request
                    resp = requests.put(expapiBaseURL + "/save_email", json=json.dumps(updated_valid_draft_email))
                    #Check resp ok
                    assert resp.ok
                    if resp.ok:
                        email_dict = sysapi.test_email_exists(new_valid_draft_email)
                        #Check still exists
                        assert email_dict != None
                        #Check email updated
                        assert email_dict['To Email'] == updated_valid_draft_email["To Email"]
                        #Check email to name added
                        assert email_dict['To Name'] == "Test User"
                        print("Email HAS changed: ")
                        print(email_dict)
                    #Delete created email
                    sysapi.test_delete_email(new_valid_draft_email)
                    #Check email deleted
                    assert not(sysapi.test_email_exists(new_valid_draft_email))       
    def test_save_user(self):
        #Create User
        resp = requests.post(expapiBaseURL + "/create-user", json=json.dumps(test2_user))
        #Check User exists
        assert resp.ok
        if resp.ok:
            resp = requests.get(expapiBaseURL + "/user?email=" + test2_user["Email Address"])
            #Check resp.ok
            assert resp.ok
            user_dict = resp.json()
            assert user_dict != None
            if resp.ok:
                #Get ID of new user
                id = user_dict['ID']
                print("User id: ")
                print(id)
                #Create user with same email
                resp = requests.post(expapiBaseURL + "/create-user", json=json.dumps(test2_user))
                #Check new user was NOT created
                assert not(resp.ok)

                #Update user
                #Set id
                test2_user_updated["ID"] = id
                #Send put request
                resp = requests.put(expapiBaseURL + "/update-user/" + str(id), json=json.dumps(test2_user_updated))
                #Check resp.ok
                assert resp.ok
                #Check detail (gender) has changed
                resp = requests.get(expapiBaseURL + "/user?email=" + test2_user["Email Address"])
                user_dict = resp.json()
                if user_dict != None:
                    assert user_dict['Gender'] == test2_user_updated['Gender']
            #Delete user
            assert sysapi.test_delete_user(id)
            #Check user is deleted
            resp = requests.get(expapiBaseURL + "/user?email=" + test2_user["Email Address"])
            assert not(resp.ok)

# driver code
if __name__ == '__main__':
   
    unittest.main()