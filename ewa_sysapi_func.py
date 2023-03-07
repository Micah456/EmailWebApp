import json
import pandas as pd
import datetime as dt

def get_user_list():
    try:
        users_df = pd.read_csv("data/users.csv")
        users_df = users_df.transpose()
        users_json = users_df.to_json()
        return users_json
    except Exception as e:
        print(e)
        return None

def get_user_by_id(id):
    users_df = pd.read_csv("data/users.csv")
    print("--------------------")
    print(users_df)
    try:
        user_data_df = users_df.iloc[int(id)]
    except IndexError:
        print("Index out of bounds")
        return None
    print("--------------------")
    print(user_data_df)
    user_data_json = user_data_df.to_json()
    return user_data_json

def get_emails():
    try:
        emails_df = pd.read_excel("data/emailCollection.xlsx")
        emails_df = emails_df.transpose()
        emails_json = emails_df.to_json()
        return emails_json
    except Exception as e:
        print(e)
        return None

def get_email_by_id(id):
    emails_df = pd.read_excel("data/emailCollection.xlsx", sheet_name='Sheet1')
    print("--------------------")
    print(emails_df)
    try:
        email_data_df = emails_df.iloc[int(id)]
    except IndexError:
        print("Index out of bounds")
        return None
    print("--------------------")
    print(email_data_df)
    email_data_json = email_data_df.to_json()
    return email_data_json

def create_email(email_dict):
    print("ewa_sysapi_func.py: email_dict type: ", type(email_dict))
    try:
        print("ewa_sysapi_func.py: creating email\n------------------")
        emails_df = pd.read_excel("data/emailCollection.xlsx")
        print(emails_df)
        new_id = len(emails_df.index)
        print("New email's id: ", new_id)
        new_row = pd.DataFrame(email_dict, index=['0'])
        new_row['ID'] = new_id
        new_row['Date Sent'] = dt.datetime.fromtimestamp(new_row['Date Sent']/1000)
        print(new_row)
        new_emails_df = pd.concat([emails_df, new_row])
        new_emails_df = new_emails_df.set_index("ID")
        print(new_emails_df)
        new_emails_df.to_excel("data/emailCollection.xlsx")
        return True
    except Exception as e:
        print(e)
        return False

def create_user(user_dict):
    try:
        users_df = pd.read_csv("data/users.csv")
        print(users_df)
        new_id = len(users_df.index)
        print("New user's id: ", new_id)
        new_row = pd.DataFrame(user_dict, index=['0'])
        new_row['ID'] = new_id
        print(new_row)
        new_users_df = pd.concat([users_df, new_row])
        new_users_df = new_users_df.set_index("ID")
        print(new_users_df)
        new_users_df.to_csv("data/users.csv")
        return True
    except Exception as e:
        print(e)
        return False

def update_email(email_dict, emailid):
    try:
        row_id = int(emailid)
        #print(email_dict['ID'])
        if row_id != email_dict['ID']:
            print("URI parameter and email ID don't match")
            return False
        #print("ewa_sysapi_func.py: updating email\n------------------")
        emails_df = pd.read_excel("data/emailCollection.xlsx")
        #print(emails_df)
        replace_row = pd.DataFrame(email_dict, index=['0'])
        replace_row['Date Sent'] = dt.datetime.fromtimestamp(replace_row['Date Sent']/1000)
        #print(replace_row)
        num_col = len(emails_df.columns)
        for i in range(num_col):
            emails_df.iloc[row_id, i] = replace_row.iloc[0,i]
        emails_df = emails_df.set_index("ID")
        emails_df.to_excel("data/emailCollection.xlsx")
        #print(emails_df)
        return True
    except Exception as e:
        print(e)
        return False

def update_user(user_dict, userid):
    try:
        row_id = int(userid)
        print(row_id)
        if row_id != user_dict['ID']:
            print("URI parameter and user ID don't match")
            return False
        print("ewa_sysapi_func.py: updating user\n------------------")
        users_df = pd.read_csv("data/users.csv")
        print(users_df)
        replace_row = pd.DataFrame(user_dict, index=['0'])
        print(replace_row)
        num_col = len(users_df.columns)
        for i in range(num_col):
            users_df.iloc[row_id,i] = replace_row.iloc[0,i]
        users_df = users_df.set_index("ID")
        users_df.to_csv("data/users.csv")
        print(users_df)
        return True
    except Exception as e:
        print(e)
        return False

def hello_from_sys():
    print("Using sys-api")