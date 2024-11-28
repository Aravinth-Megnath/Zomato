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


def alter_table():
    try:
        # Fetch table names
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]

        # Select a table
        table_name = st.selectbox("Select a table to alter", table_list)

        # Alter options
        alter_action = st.selectbox("Choose an action", ["Add Column", "Modify Column", "Drop Column"])
        
        if alter_action == "Add Column":
            column_name = st.text_input("Enter the column name to add")
            column_type = st.text_input("Enter the column type (e.g., VARCHAR(255), INT)")
            if column_name and column_type:
                query = f"ALTER TABLE {table_name} ADD {column_name} {column_type}"
                cursor.execute(query)
                connection.commit()
                st.success(f"Column {column_name} added to {table_name} successfully")
        
        elif alter_action == "Modify Column":
            column_name = st.selectbox("Select the column to modify", get_columns(cursor, table_name))
            new_definition = st.text_input("Enter the new column definition (e.g., VARCHAR(255), NOT NULL)")
            if column_name and new_definition:
                query = f"ALTER TABLE {table_name} MODIFY {column_name} {new_definition}"
                cursor.execute(query)
                connection.commit()
                st.success(f"Column {column_name} modified in {table_name} successfully")
        
        elif alter_action == "Drop Column":
            column_name = st.selectbox("Select the column to drop", get_columns(cursor, table_name))
            if column_name:
                query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
                cursor.execute(query)
                connection.commit()
                st.success(f"Column {column_name} dropped from {table_name} successfully")
    except Exception as e:
        st.error(f"Error while altering table: {e}")

def get_columns(cursor, table_name):
    cursor.execute(f"DESCRIBE {table_name}")
    return [row[0] for row in cursor.fetchall()]



def create_table():
    table_name = st.selectbox("Select a table",full)
    column_definitions = st.text_area(
        "Enter column definitions (e.g., id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100))"
    )
    
    if st.button("Create Table"):
        if not table_name or not column_definitions:
            st.error("Table name and column definitions are required!")
            return
        
        create_table_query = f"CREATE TABLE {table_name} ({column_definitions});"
        try:
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()
            st.success(f"Table {table_name} created successfully!")
        except Exception as e:
            st.error(f"Error while creating table: {e}")



def read_table():
    table_name = st.selectbox("Select a table",full)
    read_table_query = f"select * from {table_name}"
    try:
        cursor = connection.cursor()
        cursor.execute(read_table_query)
        data = cursor.fetchall()
        df = pd.read_sql(read_table_query, connection)
        st.dataframe(df)
       
    except Exception as e:
        st.error(f"Error while reading table: {e}")

def update_table():
    try:
        # Step 1: Fetch all table names
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]

        # Step 2: Select a table
        table_name = st.selectbox("Select a table to update", table_list)

        # Step 3: Fetch column names for the selected table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]

        # Step 4: Select columns for the condition and update
        condition_column = st.selectbox("Select the column for the condition", columns)  # e.g., delivery_id
        condition_value = st.text_input(f"Enter the value for {condition_column}")  # e.g., specific delivery_id
        column_to_update = st.selectbox("Select the column to update", columns)  # e.g., delivery_status
        new_value = st.text_input(f"Enter the new value for {column_to_update}")  # e.g., Failed

        if condition_value and new_value:
            # Step 5: Construct and execute the update query
            update_query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition_column} = %s"
            cursor.execute(update_query, (new_value, condition_value))
            connection.commit()
            st.success(f"Updated {column_to_update} in {table_name} where {condition_column} = {condition_value}")
        else:
            st.warning("Please provide values for both the condition and the update.")
    except Exception as e:
        st.error(f"Error while updating table: {e}")

def delete_from_table():
    try:
        # Fetch table names
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]

        # Select a table
        table_name = st.selectbox("Select a table to delete from", table_list)

        # Delete options
        delete_action = st.selectbox("Choose an action", ["Delete Row(s)", "Drop Table"])
        
        if delete_action == "Delete Row(s)":
            condition_column = st.selectbox("Select the column for the condition", get_columns(cursor, table_name))
            condition_value = st.text_input(f"Enter the value for {condition_column}")
            if condition_column and condition_value:
                query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
                cursor.execute(query, (condition_value,))
                connection.commit()
                st.success(f"Rows with {condition_column} = {condition_value} deleted from {table_name}")
        
        elif delete_action == "Drop Table":
            confirm = st.checkbox(f"Are you sure you want to drop the table {table_name}?")
            if confirm:
                query = f"DROP TABLE {table_name}"
                cursor.execute(query)
                connection.commit()
                st.success(f"Table {table_name} dropped successfully")
    except Exception as e:
        st.error(f"Error while deleting: {e}")


st.sidebar.title("Zomato Data Analysis")
operations_type = st.sidebar.selectbox("Select an operation",['Create','Read','Update','Delete','Alter'])


if operations_type == 'Create':
    # creating a new table
    st.header("Create a new table")
    create_table()

elif operations_type == 'Read':
    # reading a table
   
    st.header("Read a table")
    
    read_table()

elif operations_type == 'Update':
    # updating a table
    st.header("Update a table")
    update_table()

elif operations_type == 'Delete':
    # deleting a table
    st.header("Delete a table")
    delete_from_table()

elif operations_type == 'Alter':
    # altering a table
    st.header("Alter a table")
    alter_table()