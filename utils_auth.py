import hashlib
import pandas as pd
import os

USER_DATA_FILE = "users.csv"

def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    df = pd.read_csv(USER_DATA_FILE)
    hashed = make_hash(password)
    user_match = df[(df['username'] == username) & (df['password'] == hashed)]
    return not user_match.empty

def add_user(username, password):
    hashed = make_hash(password)
    new_data = pd.DataFrame([[username, hashed]], columns=["username", "password"])
    if os.path.exists(USER_DATA_FILE):
        new_data.to_csv(USER_DATA_FILE, mode='a', header=False, index=False)
    else:
        new_data.to_csv(USER_DATA_FILE, index=False)

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    df = pd.read_csv(USER_DATA_FILE)
    return username in df['username'].values
