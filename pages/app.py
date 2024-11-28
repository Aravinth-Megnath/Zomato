import streamlit as st 
import pandas as pd 
import pymysql
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Ta9ta6me@27",
    database="zomato_orders"
)
cursor = connection.cursor()
cursor.execute("show tables")
tables = cursor.fetchall()

tables_list = list(tables)
full = [table[0] for table in tables_list]

st.title("Zomato Data Analysis")
st.sidebar.title("Zomato Data Analysis")

table = st.selectbox("Select a table",full)
if table == 'orders':
    df = pd.read_sql("select * from orders",connection)
    st.dataframe(df)
elif table == 'restaurants':
    df = pd.read_sql("select * from restaurants",connection)
    st.dataframe(df)
elif table == 'customers':
    df = pd.read_sql("select * from customers",connection)
    st.dataframe(df)
elif table == 'delivery':
    df = pd.read_sql("select * from delivery",connection)
    st.dataframe(df)
