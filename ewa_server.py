from flask import Flask, Response
import ewa_sysapi_func, json

app = Flask("Email Web App Server")

def resource_not_found():
    error_message = {"Message" : "Resource not found."}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=404)

def bad_request(details="No details"):
    error_message = {"Message" : "Bad request.", "Details" : details}
    msg_json = json.dumps(error_message)
    return Response(msg_json, mimetype='application/json', status=400)

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

if __name__=="__main__":
    app.run(debug=True) 
    # When no port is specified, starts at default port 5000