import pyodbc, os, json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

server = os.getenv("server")
database = os.getenv("database")
username = os.getenv("db_admin_uname")
password = os.getenv("db_admin_pwd")
users_table = os.getenv("users_table")
emails_view = os.getenv("emails_view")
emails_table = os.getenv("emails_table")

conn_str = ('Driver={SQL Server};'
                        'Server=' + server + ';'
                        'Database=' + database + ';'
                        'UID=' + username + ';'
                        'PWD=' + password + ';'
                        'Trusted_Connection=no;')

def create_user_dict(row):
    return {
        "ID": row[0],
        "Email Address": row[1],
        "First Name": row[2],
        "Last Name": row[3],
        "Gender": row[4],
        "Password": row[5]
    }

def create_email_dict(row):
    return {
        "ID": row[0],
        "Subject": row[1],
        "Date Sent": int(row[2].timestamp()),
        "Message": row[3],
        "From Email": row[4],
        "From Name": row[5],
        "To Email": row[6],
        "To Name": row[7],
        "Draft": row[8]
    }

def collate_resource_dicts(data, dict_func):
    users_dict = {}
    index = 0
    for row in data:
        users_dict[index] = dict_func(data[index])
        index+=1
    return users_dict

def get_resource(table, dict_func, id=None):
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        if(id):
            cursor.execute("SELECT * FROM " + table + " WHERE ID = " + str(id))
            data = cursor.fetchall()
            return json.dumps(dict_func(data[0]))
        else:
            cursor.execute("SELECT * FROM " + table)
            data = cursor.fetchall()
            return json.dumps(collate_resource_dicts(data, dict_func))
    except:
        return None
    
def add_quotes_if_string(val):
    if(type(val) == str):
        val = val.replace("'", "''")
        val = "'" + val + "'"
    else:
        if type(val) == bool:
            val = int(val)
        val = str(val)
    return val

def stringify_user_data(user_dict):
    data = str(list(user_dict.values()))
    return data[1:len(data)-1]

def stringify_email_data(email_dict):
    email_dict['Date Sent'] = ms_to_datetime_str(email_dict['Date Sent'])
    vals = list(email_dict.values())
    email_str = ""
    for i in range(len(vals)):
        if i != 0:
            email_str += ", "
        if i == 1:
            email_str += "(convert(datetime,'" + vals[i] + "',13))"
        else:
            email_str += add_quotes_if_string(vals[i])
    return email_str

def ms_to_datetime_str(ms):
    #TODO FIX THIS!!! Gives the wrong date!
    date = dt.fromtimestamp(ms)
    date_string = date.strftime("%d %b %Y %H:%M:%S:") + str(int(date.strftime("%f"))//1000)
    return date_string


def stringify_user_data_update(user_dict):
    keys = list(user_dict.keys())
    user_string = ""
    for i in range(len(user_dict)):
        if i != 0:
            user_string += ", "
        user_string += "[" + keys[i] + "]" + " = " + add_quotes_if_string(user_dict[keys[i]])
    return user_string

def stringify_email_data_update(email_dict):
    keys = list(email_dict.keys())
    email_dict['Date Sent'] = ms_to_datetime_str(email_dict['Date Sent'])
    email_string = ""
    for i in range(1, len(email_dict)):
        if i != 1:
            email_string += ", "
        if keys[i] == "Date Sent":
            email_string += "[" + keys[i] + "]" + " = " + "(convert(datetime,'" + email_dict[keys[i]] + "',13))"
        else:
            email_string += "[" + keys[i] + "]" + " = " + add_quotes_if_string(email_dict[keys[i]])
    return email_string
            

def generate_statement(resource_dict, table, id):
    statement = ""
    if(table == users_table and not(id)):
        statement = "INSERT INTO " + table + " ([ID], [Email Address], [First Name], [Last Name], [Gender], [Password]) VALUES ((SELECT max([ID])+1 FROM " + table + "), " + stringify_user_data(resource_dict)+ ");"
    elif(table == users_table and id):
        statement = "UPDATE " + table + " SET " + stringify_user_data_update(resource_dict) + " WHERE ID = " + str(id)
    elif(table == emails_table and not(id)):
        statement = "INSERT INTO " + table + " ([Subject], [Date Sent], [Message], [From Email], [From Name], [To Email], [To Name], [Draft]) VALUES (" + stringify_email_data(resource_dict)+ ");"
    else: #update email (with id)
        statement = "UPDATE " + table + " SET " + stringify_email_data_update(resource_dict) + " WHERE ID = " + str(id)
    return statement

def set_resource(resource_dict, table, id=None):
    try:
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        statement = generate_statement(resource_dict, table, id)
        print(statement)
        cursor.execute(statement)
        cnxn.commit()
        return True
    except Exception as e:
        print(e)
        print("Error: could not add resource")
        return False



    
def get_users():
    return get_resource(users_table, create_user_dict)

def get_user_by_id(userid):
    return get_resource(users_table, create_user_dict, userid)

def get_emails():
    return get_resource(emails_view, create_email_dict)

def get_emails_by_id(emailid):
    return get_resource(emails_view, create_email_dict, emailid)

def add_user(user_dict):
    return set_resource(user_dict, users_table)

def update_user(user_dict, userid):
    return set_resource(user_dict, users_table, userid)

def add_email(email_dict):
    return set_resource(email_dict, emails_table)

def add_user(email_dict, emailid):
    return set_resource(email_dict, emails_table, emailid)


#print(get_resource("dbo.MyUser", create_user_dict))
#print(get_resource("dbo.EmailCollectionView", create_email_dict, 1))

myuser = {
    "Email Address": "lukevaughn@aol.com",
    "First Name": "Luke",
    "Last Name": "Vaughn",
    "Gender": "M",
    "Password": "pass6"
}

myuser2 = {
    "ID": 4,
    "Email Address": "lukevaughn@aol.com",
    "First Name": "Luke",
    "Last Name": "Vaughn",
    "Gender": "M",
    "Password": "pass60"
}

myemail = {
    "Subject": "RE: First Email",
    "Date Sent": 1675260840,
    "Message": "Hey sis! I've updated this email on 22/3/23",
    "From Email": "duanevaughn@hotmail.com",
    "From Name": "Duane Vaughn",
    "To Email": "marleevaughn@outlook.com",
    "To Name": "Marlee Vaughn",
    "Draft": False
}

myemail2 = {
    "ID" : 2,
    "Subject": "RE: First Email",
    "Date Sent": 1675260840,
    "Message": "Hey sis! I've updated AGAIN this email on 22/3/23",
    "From Email": "duanevaughn@hotmail.com",
    "From Name": "Duane Vaughn",
    "To Email": "marleevaughn@outlook.com",
    "To Name": "Marlee Vaughn",
    "Draft": False
}
