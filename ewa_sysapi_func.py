import json
import pandas as pd

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
    emails_df = pd.read_excel("data/emailCollection.xlsx")
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

#print(get_user_list())

def hello_from_sys():
    print("Using sys-api")