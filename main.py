from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3
import regex as re
from prompt import get_date, eng_to_sql
import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(mail,question):
    model=genai.GenerativeModel('gemini-pro')
    response = model.generate_content([eng_to_sql(),question,mail])
    return response.text

## Fucntion To execute query from the database

def execute_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()

    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    # for row in rows:
    #     print(row)
    return rows



def check_availability(query):
    # print(prompt)
    # get_date()
    model=genai.GenerativeModel('gemini-pro')
    response = model.generate_content([get_date(),query])
    # get start_date and end_date based on prompt provided by user
    dates = response.text.split(",")
    sd,ed = dates[0], dates[1]
    
    # sql query to check number of bookings

    query = '''
    SELECT COUNT(*) AS available_beds
    FROM booking
    WHERE (start_date BETWEEN '{0}' AND '{1}' OR end_date BETWEEN '{0}' AND '{1}') OR (start_date <= '{0}' AND end_date >= '{1}');
    '''.format(sd,ed)
    print(query)
    return execute_sql_query(query,"guesthouse.db")


## Streamlit App

st.set_page_config(page_title="EC-Guest House Booking")
st.header("Guest House Booking using Gemini LLM")

mail = st.text_input("Mail ID: ", key = "mail")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:

    # convert User input to SQL
    response = get_gemini_response(mail,question)

    # sometimes the response query from Gemini can contain backtick(```), so try to eliminate from query
    if response.find("`") != -1:
        response = response.replace("`", "")
    print(response)

    # if required details are not provided, example: if bookingID is not mentioned to cancel the booking
    try:
        sql_query = response.split("--")[0]
        bookingID = response.split("--")[1]
    except:
        st.subheader("Please provide valid booking details")

    # checking if sql statemnt is insert or delete
        # if insert, check for availability of beds
            # if there is no availability return that there is no availability
            # else, update db based on start date and end date
        # if delete, delete the record based on bookingID
    
    if sql_query.find("INSERT") != -1:
        booked_beds = check_availability(sql_query)[0][0]
        
        # assuming only 2 beds are available
        if booked_beds < 2:
            sql_response = execute_sql_query(sql_query,"guesthouse.db")
            st.subheader("Booking Successful")
            st.subheader("your booking ID is {0}".format(bookingID))
        else:
            st.subheader("Booking UnSuccessful for dates specified, please try changing the dates")
    
    elif sql_query.find("DELETE") != -1:
        sql_response = execute_sql_query(sql_query,"guesthouse.db")
        st.subheader("Booking ID {0} is cancelled".format(bookingID))



