import streamlit as st
import json
import os
import numpy as np
from docx import Document
import pdfplumber
import matplotlib.colors as mcolors
from operator import index
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import string
from dotenv import load_dotenv
import docx
from PIL import Image
from openai import OpenAI
import base64

# Load environment variables from a .env file
load_dotenv()

# Initialize session state
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0


def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(name, email, age, sex, password, json_file_path)
                if user:
                    session_state["logged_in"] = True
                    session_state["user_info"] = user
                    st.rerun()
            else:
                st.error("Passwords do not match. Please try again.")


def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                return user

        st.error("Invalid credentials. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None


def initialize_database(json_file_path="data.json"):
    try:
        if not os.path.exists(json_file_path):
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")


def create_account(name, email, age, sex, password, json_file_path="data.json"):
    try:
        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Check if email already exists
        for user in data["users"]:
            if user["email"] == email:
                st.error("An account with this email already exists. Please login.")
                return None

        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,
            "test_cases": [],
            "program": [],
        }
        data["users"].append(user_info)

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None


def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        user = check_login(username, password, json_file_path)
        if user is not None:
            st.rerun() # Rerun to reflect logged-in state immediately


def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
            return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None


def render_dashboard(user_info):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")
    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")


def extract_text(file) -> str:
    file_extension = os.path.splitext(file.name)[1].lower()

    text = ""
    if file_extension == ".pdf":
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_extension == ".docx":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_extension == ".txt":
        text = file.getvalue().decode("utf-8")
    else:
        st.warning(f"Unsupported file type: {file_extension}. Treating as a text file.")
        text = file.getvalue().decode("utf-8")
    return text


def get_unit_test_cases(program, language):
    """
    Generates unit test cases using OpenAI API.
    Returns the test cases on success, or an error message string on failure.
    """
    try:
        if not os.environ.get("OPENAI_API_KEY"):
            return "Error: OPENAI_API_KEY is not set. Please configure your .env file."

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        prompt = f"Given the following {language} program:\n{program}\nGenerate all possible unit test cases for this program. Make sure to cover all diverse scenarios. The test cases should be in the form of input and expected output."
        messages = [{"role": "system", "content": prompt}]
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating test cases: {e}"


def main(json_file_path="data.json"):
    st.sidebar.title("Unit Test Cases Generator")
    
    # Logout button
    if session_state.get("logged_in"):
        if st.sidebar.button("Logout"):
            for key in list(session_state.keys()):
                del session_state[key]
            st.rerun()

    page = st.sidebar.radio(
        "Go to",
        ("Signup/Login", "Dashboard", "Upload a program", "View Test Cases"),
        key="navigation",
    )

    if page == "Signup/Login" and not session_state.get("logged_in"):
        st.title("Signup/Login Page")
        login_or_signup = st.radio("Select an option", ("Login", "Signup"), key="login_signup")
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)
    
    elif page == "Dashboard":
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login or signup to view the dashboard.")

    elif page == "Upload a program":
        if session_state.get("logged_in"):
            st.title("Upload a Program to Generate Test Cases")
            uploaded_file = st.file_uploader("Choose a program file", type=['py', 'java', 'cpp', 'cs', 'js', 'txt'])
            language = st.selectbox(
                "Select the language of the program",
                ("Python", "Java", "C++", "C#", "Javascript"),
            )
            
            if st.button("Generate Test Cases"):
                if uploaded_file is not None and language:
                    with st.spinner("Analyzing program and generating test cases..."):
                        program = extract_text(uploaded_file)
                        st.subheader("Uploaded Program")
                        st.code(program, language=language.lower())
                        
                        unit_test_cases = get_unit_test_cases(program, language)

                        st.subheader("Generated Unit Test Cases")
                        if unit_test_cases.strip().startswith("Error:"):
                            st.error(unit_test_cases)
                        else:
                            st.code(unit_test_cases, language='bash')
                            # Save results to JSON using robust method
                            try:
                                with open(json_file_path, "r") as f:
                                    data = json.load(f)
                                
                                user_index = next((i for i, u in enumerate(data["users"]) if u["email"] == session_state["user_info"]["email"]), None)

                                if user_index is not None:
                                    # Ensure lists exist
                                    if "program" not in data["users"][user_index] or data["users"][user_index]["program"] is None:
                                        data["users"][user_index]["program"] = []
                                    if "test_cases" not in data["users"][user_index] or data["users"][user_index]["test_cases"] is None:
                                        data["users"][user_index]["test_cases"] = []
                                    
                                    data["users"][user_index]["program"].append(program)
                                    data["users"][user_index]["test_cases"].append(unit_test_cases)
                                    
                                    # Update session state with the latest info
                                    session_state["user_info"] = data["users"][user_index]

                                    with open(json_file_path, "w") as f:
                                        json.dump(data, f, indent=4)
                                    st.success("Program and test cases have been saved!")
                                else:
                                    st.error("Could not save results. User not found.")

                            except (FileNotFoundError, json.JSONDecodeError) as e:
                                st.error(f"Error saving data: {e}")
                else:
                    st.warning("Please upload a file and select a language.")
        else:
            st.warning("Please login or signup to upload a program.")

    elif page == "View Test Cases":
        if session_state.get("logged_in"):
            st.title("View Saved Programs and Test Cases")
            user_info = get_user_info(session_state["user_info"]["email"], json_file_path)
            
            if user_info and user_info.get("program"):
                programs = user_info["program"]
                test_cases = user_info["test_cases"]
                
                for i, (prog, tc) in enumerate(zip(programs, test_cases)):
                    with st.expander(f"Program {i + 1}"):
                        st.code(prog)
                        st.subheader("Associated Unit Test Cases")
                        st.code(tc, language='bash')
            else:
                st.info("No programs have been uploaded yet. Go to the 'Upload a program' page to get started.")
        else:
            st.warning("Please login or signup to view your saved test cases.")
    
    # Redirect if logged in and on the signup page
    if page == "Signup/Login" and session_state.get("logged_in"):
        st.info("You are already logged in. Please navigate using the sidebar.")
        render_dashboard(session_state["user_info"])


if __name__ == "__main__":
    initialize_database()
    main()