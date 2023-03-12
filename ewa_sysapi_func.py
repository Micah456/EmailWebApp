import json
import pandas as pd
import datetime as dt

emailFile = "data/emailCollection.xlsx"
userFile = "data/users.csv"

def get_resource(read_func, filename):
    try:
        resource_df = read_func(filename)
        resource_df = resource_df.transpose()
        resource_json = resource_df.to_json()
        return resource_json
    except Exception as e:
        print(e)
        return None
    
def get_resource_by_id(read_func, filename, id):
    resource_df = read_func(filename)
    print("--------------------")
    print(resource_df)
    try:
        resource_data = resource_df.iloc[int(id)]
    except IndexError:
        print("Index out of bounds")
        return None
    print("--------------------")
    print(resource_data)
    resource_data_json = resource_data.to_json()
    return resource_data_json

def create_resource(read_func, filename, resource_dict, isEmail):
    try:
        print("ewa_sysapi_func.py: creating new email/user\n---------------------")
        resources_df = read_func(filename)
        print(resources_df)
        new_id = len(resources_df.index)
        print("New resource's id: ", new_id)
        new_row = pd.DataFrame(resource_dict, index=['0'])
        new_row['ID'] = new_id
        if isEmail:
            new_row['Date Sent'] = dt.datetime.fromtimestamp(new_row['Date Sent']/1000)
        print(new_row)
        new_resources_df = pd.concat([resources_df, new_row])
        new_resources_df = new_resources_df.set_index("ID")
        print(new_resources_df)
        if(isEmail):
            new_resources_df.to_excel(filename)
        else:
            new_resources_df.to_csv(filename)
        return True
    except Exception as e:
        print(e)
        return False

def update_resource(read_func, filename, resource_dict, isEmail, id):
    try:
        row_id = int(id)
        if row_id != resource_dict['ID']:
            print("URI parameter and ID don't match")
            return False
        resources_df = read_func(filename)
        replace_row = pd.DataFrame(resource_dict, index=['0'])
        if isEmail:
            replace_row['Date Sent'] = dt.datetime.fromtimestamp(replace_row['Date Sent']/1000)
        num_col = len(resources_df.columns)
        for i in range(num_col):
            resources_df.iloc[row_id, i] = replace_row.iloc[0,i]
        resources_df = resources_df.set_index("ID")
        if isEmail:
            resources_df.to_excel(filename)
        else:
            resources_df.to_csv(filename)
        return True
    except Exception as e:
        print(e)
        return False

def get_user_list():
    return get_resource(pd.read_csv, userFile)

def get_user_by_id(id):
    return get_resource_by_id(pd.read_csv, userFile, id)

def get_emails():
    return get_resource(pd.read_excel, emailFile)

def get_email_by_id(id):
    return get_resource_by_id(pd.read_excel, emailFile, id)

def create_email(email_dict):
    return create_resource(pd.read_excel, emailFile, email_dict, True)

def create_user(user_dict):
    return create_resource(pd.read_csv, userFile, user_dict, False)

def update_email(email_dict, emailid):
    return update_resource(pd.read_excel, emailFile, email_dict, True, emailid)
    
def update_user(user_dict, userid):
    return update_resource(pd.read_csv, userFile, user_dict, False, userid)

def hello_from_sys():
    print("Using sys-api")