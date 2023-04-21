from flask import Flask, Response, request, render_template, send_file, redirect
import ewa_sysapi_func, ewa_expapi_func, ewa_proapi_func, ewa_sysapi_func2, json
from datetime import datetime as dt

port = 5000
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

# Resource getters and setters

def get_resource_response(resource):
    print(resource)
    if resource:
        return Response(resource, mimetype='application/json')
    return resource_not_found()

def set_resource_response(response, resourceType, create=True):
    if create:
        status_code=201
        action = "created"
    else:
        status_code=200
        action = "updated"
    if response:
        msg_json = json.dumps({"Message" : resourceType + " successfully " + action + "."})
        resp = Response(msg_json, mimetype='application/json', status=status_code)
    else:
        msg_json = json.dumps({"Message" : resourceType + " not " + action + "."})
        resp = Response(msg_json, mimetype='application/json', status=500)
    return resp

# Other functions
def authorise_user(cookies, template):
    token = cookies.get("Token")
    email = cookies.get("email")
    print("Token: " + str(token))
    print("Email: " + str(email))
    if ewa_expapi_func.isAuthorised(token, email):
        return render_template(template)
    else:
        return render_template("redirect.html", type="unauthorised")

def convert_resource_to_dict(resource):
    if type(resource) == str:
        resource = json.loads(resource)
    return resource  

def find_last_index(string, x):
    index = -1
    for i in range(0, len(string)):
        if string[i] == x:
            index = i
    return index

def get_view(base_url):
    viewIndex = find_last_index(base_url,'/') + 1
    view = str(base_url)[viewIndex:]
    print(view)
    return view

# Images
@app.route("/images/three-bars-icon.jpg")
@app.route("/web-app/images/three-bars-icon.jpg")
def load_bar_icon():
    filename = "images/three-bars-icon.jpg"
    return send_file(filename, mimetype='image/jpg')

# Web App
@app.route("/web-app/redirect/<type>")
def webapp_redirect(type):
    return render_template("redirect", type=type)

@app.route("/web-app/unauthorised")
def load_unauthorised():
    return render_template("unauthorised.html")

@app.route("/web-app/login")
def load_login():
    token = request.cookies.get("Token")
    email = request.cookies.get("email")
    if not(ewa_expapi_func.isAuthorised(token, email)):
        template = get_view(request.base_url) + ".html"
        return render_template(template)
    else:
        return render_template("redirect.html", type="inbox")

@app.route("/web-app/inbox")
@app.route("/web-app/sent")
@app.route("/web-app/drafts")
def load_page():
    template = get_view(request.base_url) + ".html"
    cookies = request.cookies
    return authorise_user(cookies, template)

@app.route("/web-app/inbox/<emailid>")
@app.route("/web-app/sent/<emailid>")
@app.route("/web-app/drafts/<emailid>")
def load_read_email(emailid):
    cookies = request.cookies
    if request.args.get("edit"):
        return authorise_user(cookies, "writeemail.html")
    else:
        return authorise_user(cookies, "reademail.html")

@app.route("/web-app/new_mail")
def write_email():
    cookies = request.cookies
    return authorise_user(cookies, "writeemail.html")

@app.route("/web-app/update-user")
def update_user_webapp():
    cookies = request.cookies
    return authorise_user(cookies, "updateuser.html")

@app.route("/web-app/new-user")
def new_user():
    return render_template("newuser.html")

# Sys API
# GET Requests
@app.route("/sys-api")
def hellosys():
    return "This is the ewa sysapi!"

@app.route("/sys-api/users")
def users():
    #return get_resource_response(ewa_sysapi_func.get_user_list()) 
    return get_resource_response(ewa_sysapi_func2.get_users())

@app.route("/old-sys-api/users")
def old_users():
    return get_resource_response(ewa_sysapi_func.get_user_list()) 

@app.route("/sys-api/users/<userid>")
def user_id(userid):
    #return get_resource_response(ewa_sysapi_func.get_user_by_id(userid))
    return get_resource_response(ewa_sysapi_func2.get_user_by_id(userid))
    

@app.route("/sys-api/emails")
def emails():
    return get_resource_response(ewa_sysapi_func2.get_emails())

@app.route("/old-sys-api/emails")
def old_emails():
    return get_resource_response(ewa_sysapi_func.get_emails())

@app.route("/sys-api/emails/<emailid>")
def email_id(emailid):
    return get_resource_response(ewa_sysapi_func2.get_emails_by_id(emailid))

@app.route("/sys-api/token/<token>")
def get_token_dict_by_token(token):
    return get_resource_response(ewa_sysapi_func2.get_token_dict_by_token(token))

#POST Requests
@app.route("/sys-api/emails", methods=["POST"])
def create_email():
    raw_resource = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_sysapi_func2.add_email(raw_resource), "Email", create=True)

@app.route("/sys-api/users", methods=["POST"])
def create_user():
    raw_resource = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_sysapi_func2.add_user(raw_resource), "User", create=True)

@app.route("/sys-api/tokens", methods=["POST"])
def add_token():
    print("Sys-api: adding token")
    raw_resource = convert_resource_to_dict(request.json)
    print("resource converted")
    return set_resource_response(ewa_sysapi_func2.add_token(raw_resource), "Token", create=True)

#PUT Requests
@app.route("/sys-api/emails/<emailid>", methods=["PUT"])
def update_email(emailid):
    raw_resource = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_sysapi_func2.update_email(raw_resource, emailid), "Email", create=False)

@app.route("/sys-api/users/<userid>", methods=["PUT"])
def update_user(userid):
    raw_resource = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_sysapi_func2.update_user(raw_resource, userid), "User", create=False)

#ProAPI
#GET Requests
@app.route("/pro-api/load_user")
def load_user_proapi():
    user_email = request.args.get('email')
    return get_resource_response(ewa_proapi_func.load_user(user_email))

@app.route("/pro-api/user/<userid>/emails")
def load_user_emails_proapi(userid):
    return get_resource_response(ewa_proapi_func.load_user_emails(userid))

@app.route("/pro-api/get_dashboard")
def get_dashboard():
    user_email = request.args.get('email')
    return get_resource_response(ewa_proapi_func.get_dashboard(user_email))

@app.route("/pro-api/generate-token")
def generate_token_proapi():
    email_address = request.args.get('email')
    token_dict = ewa_proapi_func.generate_token(email_address)
    if token_dict:
        msg_json = json.dumps({"Message" : "Token generated successfully", "Token" : token_dict['Token'], "Expiry Date" : token_dict['Expiry Date']})
        return Response(msg_json, mimetype='application/json', status=200)
    else:
        msg_json = json.dumps({"Message" : "Token NOT generated"})
        return Response(msg_json, mimetype='application/json', status=400)

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
    
@app.route("/pro-api/authorise", methods=["POST"])
def authorise():
    authorisation_dict = convert_resource_to_dict(request.json)
    if ewa_proapi_func.is_authorised(authorisation_dict):
        msg_json = json.dumps({"Message" : "User is authorised"})
        return Response(msg_json, mimetype='application/json', status=202)
    else:
        msg_json = json.dumps({"Message" : "User is NOT authorised"})
        return Response(msg_json, mimetype='application/json', status=403)


@app.route("/pro-api/save_email", methods=["POST","PUT"])
def save_email_proapi():
    initial_email = convert_resource_to_dict(request.json)
    if request.method == "POST":
        return set_resource_response(ewa_proapi_func.save_email(initial_email, request.method), "Email", create=True)
    else:
        return set_resource_response(ewa_proapi_func.save_email(initial_email, request.method), "Email", create=False)


@app.route("/pro-api/update-user/<userid>", methods=["PUT"])
def update_user_proapi(userid):
    user_details = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_proapi_func.update_user(userid, user_details), "User", create=False)

@app.route("/pro-api/create-user", methods=["POST"])
def create_user_proapi():
    user_details = convert_resource_to_dict(request.json)
    return set_resource_response(ewa_proapi_func.create_user(user_details), "User", create=True)


#ExpAPI
#GET Requests
@app.route("/exp-api/user")
def load_user_expapi():
    user_email = request.args.get('email')
    return get_resource_response(ewa_expapi_func.load_user(user_email))

@app.route("/exp-api/user/<userid>/emails")
def load_user_emails_expapi(userid):
    #NOTE userid should be passed as int
    return get_resource_response(ewa_expapi_func.load_user_emails(userid))

@app.route("/exp-api/load_dashboard")
def load_user_dashboard():
    user_email = request.args.get('email')
    return get_resource_response(ewa_expapi_func.load_user_dashboard(user_email))

@app.route("/exp-api/logout")
def log_out():
    message = {"Message" : "Logout successful"}
    msg_json = json.dumps(message)
    resp = Response(msg_json, mimetype='application/json', status=200)
    resp.set_cookie("email",'',expires=0)
    resp.set_cookie("is_logged_in","False")
    resp.set_cookie("Token", '',expires=0)
    return resp

#POST Requests
@app.route("/exp-api/login", methods=["POST"])
def login():
    login_dict = request.json
    if type(login_dict) == str:
        login_dict = json.loads(login_dict)
    print("Exp API: login_dict type: ", type(login_dict))
    if ewa_expapi_func.validate(login_dict):
        msg_json = json.dumps({"Message":"Login successful"})
        resp = Response(msg_json, mimetype='application/json', status=200)
        token_dict = ewa_expapi_func.generate_token(login_dict['email'])
        token = token_dict['Token']
        expiry = dt.fromtimestamp(int(token_dict['Expiry Date'])/1000)
        print(expiry)
        if token:
            resp.set_cookie("email",login_dict['email'])
            #resp.set_cookie("is_logged_in","True")
            resp.set_cookie("Token", token, expires=expiry)
        else:
            msg_json = json.dumps({"Message":"Login unsuccessful", "Error" : "Could not generate token"})
            resp = Response(msg_json, mimetype='application/json', status=500)
    else:
        msg_json = json.dumps({"Message":"Login unsuccessful"})
        resp = Response(msg_json, mimetype='application/json', status=401)
    return resp

@app.route("/exp-api/save_email", methods=["POST", "PUT"])
def save_email_expapi():
    initial_email = request.json
    if type(initial_email) == str:
        initial_email = json.loads(initial_email)
    print("EXP API: initial_email type: ", type(initial_email))
    if(request.method == "POST"):
        #New Email
        return set_resource_response(ewa_expapi_func.save_new_email(initial_email), "Email", create=True)
    else:
        #Updating draft
        return set_resource_response(ewa_expapi_func.update_draft(initial_email), "Draft", create=False)


@app.route("/exp-api/update-user/<userid>", methods=["PUT"])
def update_user_expapi(userid):
    user_details = request.json
    if type(user_details) == str:
        user_details = json.loads(user_details)
    return set_resource_response(ewa_expapi_func.update_user(userid, user_details), "User", create=False)

@app.route("/exp-api/create-user", methods=["POST"])
def create_user_expapi():
    user_details = request.json
    if type(user_details) == str:
        user_details = json.loads(user_details)
    return set_resource_response(ewa_expapi_func.create_user(user_details), "User", create=True)
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
    app.run(debug=True, port=port) 
    # When no port is specified, starts at default port 5000