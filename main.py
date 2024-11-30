from class_database import DatabaseManager
from class_crud import CRUDOperations
import streamlit as st

# Initialize DatabaseManager
db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="Ta9ta6me@27",
    database="zomato_orders"
)

# Initialize CRUDOperations
crud_ops = CRUDOperations(db_manager)

# Streamlit UI
st.sidebar.title("Zomato Data Analysis")
operation = st.sidebar.selectbox("Select Operation", ["Create", "Read", "Update","Insert", "Delete", "Alter"])

if operation == "Create":
    crud_ops.create_table()
elif operation == "Read":
    crud_ops.read_table()
elif operation == "Insert":
    crud_ops.insert_data()
elif operation == "Update":
    crud_ops.update_table()
elif operation == "Delete":
    crud_ops.delete_from_table()
elif operation == "Alter":
    crud_ops.alter_table()
