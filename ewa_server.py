from flask import Flask, Response, request, render_template, send_file
import ewa_sysapi_func, ewa_expapi_func, ewa_proapi_func, json

app = Flask("Email Web App Server")

# Error handling
def resource_not_found():
    error_message = {"Message" : "Resource not found."}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=404)

def bad_request(details="No details"):
    error_message = {"Message" : "Bad request.", "Details" : details}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=400)

def server_error(details="No details"):
    error_message = {"Message" : "Server error.", "Details" : details}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=500)

# Images
@app.route("/images/three-bars-icon.jpg")
@app.route("/web-app/images/three-bars-icon.jpg")
def load_bar_icon():
    filename = "images/three-bars-icon.jpg"
    return send_file(filename, mimetype='image/jpg')


# Web App
@app.route("/web-app/login")
def load_login_page():
    return render_template("login.html")

@app.route("/web-app/inbox")
def load_inbox_page():
    return render_template("inbox.html")

@app.route("/web-app/sent")
def load_sent_page():
    return render_template("sent.html")

@app.route("/web-app/drafts")
def load_drafts_page():
    return render_template("drafts.html")

@app.route("/web-app/inbox/<emailid>")
@app.route("/web-app/sent/<emailid>")
@app.route("/web-app/drafts/<emailid>")
def load_read_email(emailid):
    if request.args.get("edit") == "True":
        return render_template("writeemail.html")
    else:
        return render_template("reademail.html")

@app.route("/web-app/new_mail")
def write_email():
    return render_template("writeemail.html")

@app.route("/web-app/update-user")
def update_user_webapp():
    return render_template("updateuser.html")

# Sys API
# GET Requests
@app.route("/sys-api")
def hellosys():
    return "This is the ewa sysapi!"

@app.route("/sys-api/users")
def users():
    users=ewa_sysapi_func.get_user_list()
    if users == None:
        return resource_not_found()
    return Response(users, mimetype='application/json')

@app.route("/sys-api/users/<userid>")
def user_id(userid):
    try:
        int(userid)
    except Exception as e:
        #if userid cannot be parsed to int
        print(e)
        return bad_request("Userid must be int.")
    user=ewa_sysapi_func.get_user_by_id(userid)
    if user==None:
        #No user found
        return resource_not_found()
    return Response(user, mimetype='application/json')

@app.route("/sys-api/emails")
def emails():
    emails=ewa_sysapi_func.get_emails()
    if emails == None:
        return resource_not_found()
    return Response(emails, mimetype='application/json')

@app.route("/sys-api/emails/<emailid>")
def email_id(emailid):
    try:
        int(emailid)
    except Exception as e:
        #if emailid cannot be parsed to int
        print(e)
        return bad_request("Emailid must be int.")
    email=ewa_sysapi_func.get_email_by_id(emailid)
    if email==None:
        #No email found
        return resource_not_found()
    return Response(email, mimetype='application/json')

#POST Requests
@app.route("/sys-api/emails", methods=["POST"])
def create_email():
    email = request.json
    if type(email) == str:
        email = json.loads(email)
    if ewa_sysapi_func.create_email(email) == False:
        #NOTE: request.json is dict object
        return server_error()
    msg_json = json.dumps({"Message" : "Email created"})
    return Response(msg_json, mimetype='application/json', status=201) 

@app.route("/sys-api/users", methods=["POST"])
def create_user():
    if ewa_sysapi_func.create_user(request.json) == False:
        #NOTE: request.json is dict object
        return server_error()
    msg_json = json.dumps({"Message" : "User created"})
    return Response(msg_json, mimetype='application/json', status=201)

#PUT Requests
@app.route("/sys-api/emails/<emailid>", methods=["PUT"])
def update_email(emailid):
    email = request.json
    if type(email) == str:
        email = json.loads(email)
    try:
        int(emailid)
    except Exception as e:
        #if emailid cannot be parsed to int
        print(e)
        return bad_request("Emailid must be int.")
    if ewa_sysapi_func.update_email(email, emailid) == False:
        #NOTE: request.json is dict object
        return server_error()
    msg_json = json.dumps({"Message" : "Email updated"})
    return Response(msg_json, mimetype='application/json', status=200)

@app.route("/sys-api/users/<userid>", methods=["PUT"])
def update_user(userid):
    try:
        int(userid)
    except Exception as e:
        #if userid cannot be parsed to int
        print(e)
        return bad_request("Userid must be int.")
    user_details = request.json
    if type(user_details) == str:
        user_details = json.loads(user_details)
    if ewa_sysapi_func.update_user(user_details, userid) == False:
        #NOTE: request.json is dict object
        return server_error()
    msg_json = json.dumps({"Message" : "User updated"})
    return Response(msg_json, mimetype='application/json', status=200) 

#ProAPI
#GET Requests
@app.route("/pro-api/load_user")
def load_user_proapi():
    user_email = request.args.get('email')
    user_data = ewa_proapi_func.load_user(user_email)
    if user_data:
        return Response(user_data, mimetype='application/json', status=200)
    else:
        return resource_not_found()

@app.route("/pro-api/user/<userid>/emails")
def load_user_emails_proapi(userid):
    user_email_address = ewa_proapi_func.get_user_email_address(userid)
    user_emails = ewa_proapi_func.load_user_emails(userid, user_email_address)
    if user_emails:
        return Response(user_emails, mimetype='application/json', status=200)
    else:
        return resource_not_found()

@app.route("/pro-api/get_dashboard")
def get_dashboard():
    user_email = request.args.get('email')
    dashboard = ewa_proapi_func.get_dashboard(user_email)
    if dashboard:
        return Response(dashboard, mimetype='application/json', status=200)
    else:
        return resource_not_found()

#POST Requests
@app.route("/pro-api/validate", methods=["POST"])
def validate():
    #print("In validate: type of login_dict: ", type(request.json))
    if ewa_proapi_func.validate(request.json):
        #Login validated
        msg_json = json.dumps({"Message":"Login validated"})
        return Response(msg_json, mimetype='application/json', status=200)
    else:
        #Login not validated
        msg_json = json.dumps({"Message":"Login not validated"})
        return Response(msg_json, mimetype='application/json', status=401)
    
@app.route("/pro-api/save_email", methods=["POST","PUT"])
def save_email_proapi():
    initial_email = request.json
    if type(initial_email) == str:
        initial_email = json.loads(initial_email)
    #print("PRO API: json.loads(initial_email) type: ", type(json.loads(initial_email)))
    #rint("PRO API: initial_email type: ", type(initial_email))
    success = ewa_proapi_func.save_email(initial_email, request.method)
    if success:
        msg_json = json.dumps({"Message":"Email created/updated successfully!"})
        resp = Response(msg_json, mimetype='application/json', status=200)
    else:
        msg_json = json.dumps({"Message":"Email not created/updated"})
        resp = Response(msg_json, mimetype='application/json', status=500)
    return resp

@app.route("/pro-api/update-user/<userid>", methods=["PUT"])
def update_user_proapi(userid):
    user_details = request.json
    if type(user_details) == str:
        user_details = json.loads(user_details)
    success = ewa_proapi_func.update_user(userid, user_details)
    if success:
        msg_json = json.dumps({"Message":"User updated successfully!"})
        resp = Response(msg_json, mimetype='application/json', status=200)
    else:
        msg_json = json.dumps({"Message":"User not updated"})
        resp = Response(msg_json, mimetype='application/json', status=500)
    return resp

#ExpAPI
#GET Requests
@app.route("/exp-api/user")
def load_user_expapi():
    user_email = request.args.get('email')
    user_data = ewa_expapi_func.load_user(user_email)
    if user_data:
        return Response(user_data, mimetype='application/json', status=200)
    else:
        return resource_not_found()

@app.route("/exp-api/user/<userid>/emails")
def load_user_emails_expapi(userid):
    #NOTE userid should be passed as int
    user_emails = ewa_expapi_func.load_user_emails(userid)
    if user_emails:
        return Response(user_emails, mimetype='application/json', status=200)
    else:
        return resource_not_found()

@app.route("/exp-api/load_dashboard")
def load_user_dashboard():
    user_email = request.args.get('email')
    dashboard_data = ewa_expapi_func.load_user_dashboard(user_email)
    if dashboard_data:
        return Response(dashboard_data, mimetype='application/json', status=200)
    else:
        return resource_not_found()

@app.route("/exp-api/logout")
def log_out():
    message = {"Message" : "Logout successful"}
    msg_json = json.dumps(message)
    resp = Response(msg_json, mimetype='application/json', status=200)
    resp.set_cookie("email",'',expires=0)
    resp.set_cookie("is_logged_in","False")
    return resp

#POST Requests
@app.route("/exp-api/login", methods=["POST"])
def login():
    login_dict = request.json
    print("Exp API: login_dict type: ", type(login_dict))
    if ewa_expapi_func.validate(login_dict):
        msg_json = json.dumps({"Message":"Login successful"})
        resp = Response(msg_json, mimetype='application/json', status=200)
        resp.set_cookie("email",login_dict['email'])
        resp.set_cookie("is_logged_in","True")
    else:
        msg_json = json.dumps({"Message":"Login unsuccessful"})
        resp = Response(msg_json, mimetype='application/json', status=401)
    return resp

@app.route("/exp-api/save_email", methods=["POST", "PUT"])
def save_email_expapi():
    initial_email = request.json
    print("EXP API: initial_email type: ", type(initial_email))
    if(request.method == "POST"):
        #New Email
        if ewa_expapi_func.save_new_email(initial_email):
            msg_json = json.dumps({"Message":"Email created and saved"})
            resp = Response(msg_json, mimetype='application/json', status=201)
        else:
            msg_json = json.dumps({"Message":"Email not created"})
            resp = Response(msg_json, mimetype='application/json', status=500)
    else:
        #Updating draft
        if ewa_expapi_func.update_draft(initial_email):
            msg_json = json.dumps({"Message":"Draft updated and saved"})
            resp = Response(msg_json, mimetype='application/json', status=200)
        else:
            msg_json = json.dumps({"Message":"Draft not updated"})
            resp = Response(msg_json, mimetype='application/json', status=500)
    return resp

@app.route("/exp-api/update-user/<userid>", methods=["PUT"])
def update_user_expapi(userid):
    user_details = request.json
    if ewa_expapi_func.update_user(userid, user_details):
        msg_json = json.dumps({"Message":"User successfully updated"})
        resp = Response(msg_json, mimetype='application/json', status=200)
    else:
        msg_json = json.dumps({"Message":"User not updated"})
        resp = Response(msg_json, mimetype='application/json', status=500)
    return resp

#TESTAPI

@app.route("/test-api/cookie")
def get_cookie():
    #Remember to pass in email
    email = request.args.get('email')
    msg_json = json.dumps({"Message":"Cookie set", "email":email})
    resp = Response(msg_json, mimetype='application/json', status=200)
    resp.set_cookie('email',email)
    return resp

if __name__=="__main__":
    app.run(debug=True) 
    # When no port is specified, starts at default port 5000