import streamlit as st
import pandas as pd
import os
import base64

def add_custom_css():
    background_url = "https://images.unsplash.com/photo-1507842217343-583bb7270b66"  # You can change this!
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{background_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}

        .stTextInput > div > div > input,
        .stSelectbox > div > div > div > div {{
            background-color: #1f1f1f !important;
            color: #FFD700 !important;
            border: 1px solid #FFD700 !important;
            border-radius: 8px !important;
            font-weight: bold;
        }}

        .stButton>button {{
            background-color: #FFD700 !important;
            color: #000000 !important;
            border: none;
            padding: 0.5em 1.5em;
            border-radius: 12px;
            font-weight: bold;
            box-shadow: 0 0 10px #FFD700;
        }}
        </style>
    """, unsafe_allow_html=True)


# File paths
USER_DATA_FILE = "users.csv"
BUS_ROUTE_FILE = "bus_routes.csv"

# Initialize user data CSV with headers
def init_user_data_file():
    if not os.path.exists(USER_DATA_FILE) or os.stat(USER_DATA_FILE).st_size == 0:
        with open(USER_DATA_FILE, 'w') as f:
            f.write("username,password\n")

# Check if user already exists
def user_exists(username):
    df = pd.read_csv(USER_DATA_FILE)
    return username in df['username'].values

# Register new user
def register_user(username, password):
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{password}\n")

# Verify login credentials
def verify_login(username, password):
    df = pd.read_csv(USER_DATA_FILE)
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty

# Show login form
def show_login_form():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if verify_login(username, password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")

# Show signup form
def show_signup_form():
    st.subheader("Sign Up")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')
    if st.button("Sign Up"):
        if user_exists(new_user):
            st.warning("User already exists. Please log in.")
        else:
            register_user(new_user, new_pass)
            st.success("Registration successful! You can now log in.")
            st.session_state.page = "login"
            st.rerun()

# Bus finder logic
def show_bus_finder():
    st.subheader("Find Buses Between Places")
    src = st.text_input("Enter Source")
    dest = st.text_input("Enter Destination")

    if os.path.exists(BUS_ROUTE_FILE):
        try:
            df = pd.read_csv(BUS_ROUTE_FILE)
            if src and dest:
                results = df[df['Stops'].str.contains(src, case=False) & df['Stops'].str.contains(dest, case=False)]
                if not results.empty:
                    st.write("Matching Routes:")
                    st.dataframe(results)
                else:
                    st.warning("No routes found between these places.")
        except Exception as e:
            st.error(f"Error reading bus route file: {e}")
    else:
        st.error("Bus route data file not found.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Main app
def main():

    add_custom_css()
    init_user_data_file()
    ...

    st.title("🚌 Tamil Nadu Bus Route Finder")
    
    init_user_data_file()
    ...


    init_user_data_file()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.sidebar.title("Welcome")
        page = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])
        st.session_state.page = page
        if page == "Login":
            show_login_form()
        elif page == "Sign Up":
            show_signup_form()
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        show_bus_finder()

if __name__ == "__main__":
    main()
