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

# 10 sql queries for analysis
sql_queries = [
    "SELECT * FROM zomato_orders.customers WHERE average_rating > 4.5",
    "SELECT COUNT(*) FROM zomato_orders.customers WHERE preferred_cuisine = 'Indian'",
    "SELECT AVG(total_orders) FROM zomato_orders.customers",
    "SELECT avg(total_amount) FROM zomato_orders.orders WHERE payment_mode = 'Cash on Delivery'",
    "SELECT COUNT(*) FROM zomato_orders.customers WHERE signup_date BETWEEN '2022-01-01' AND '2022-12-31'",
    "Select avg(delivery_time) from zomato_orders.delivery where delivery_status = 'Delivered'",]
query_title = ["Customers with high rating","Number of Indian customers","Average number of orders","Average amount paid with cash on delivery","Number of customers signed up in 2022","Average delivery time"]
select_query = st.selectbox("Select a query",query_title)
if select_query == "Customers with high rating":
    cursor.execute(sql_queries[0])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[0], connection)
    st.dataframe(df)
elif select_query == "Number of Indian customers":
    cursor.execute(sql_queries[1])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[1], connection)
    st.dataframe(df)
elif select_query == "Average number of orders":
    cursor.execute(sql_queries[2])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[2], connection)
    st.dataframe(df)
elif select_query == "Average amount paid with cash on delivery":
    cursor.execute(sql_queries[3])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[3], connection)
    st.dataframe(df)
elif select_query == "Number of customers signed up in 2022":
    cursor.execute(sql_queries[4])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[4], connection)
    st.dataframe(df)
elif select_query == "Average delivery time":
    cursor.execute(sql_queries[5])
    data = cursor.fetchall()
    df = pd.read_sql(sql_queries[5], connection)
    st.dataframe(df)