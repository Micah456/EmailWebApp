from flask import Flask, Response, request, render_template
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


# Web App
@app.route("/web-app/login")
def load_login_page():
    return render_template("login.html")

@app.route("/web-app/dashboard")
def load_dashboard_page():
    return render_template("dashboard.html")

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
    if ewa_sysapi_func.create_email(request.json) == False:
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
    try:
        int(emailid)
    except Exception as e:
        #if emailid cannot be parsed to int
        print(e)
        return bad_request("Emailid must be int.")
    if ewa_sysapi_func.update_email(request.json, emailid) == False:
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
    if ewa_sysapi_func.update_user(request.json, userid) == False:
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
    


#ExpAPI
#GET Requests
@app.route("/exp-api/user")
def load_user_expapi():
    user_email = request.args.get('email')
    user_data = ewa_expapi_func.load_user(user_email)
    if user_data:
        return user_data
    else:
        return resource_not_found()

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