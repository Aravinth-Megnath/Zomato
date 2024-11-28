import streamlit as st
import pandas as pd

class CRUDOperations:
    def __init__(self, db_manager):
        self.db = db_manager

    def create_table(self):
        table_name = st.text_input("Enter the table name")
        column_definitions = st.text_area(
            "Enter column definitions (e.g., id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100))"
        )
        if st.button("Create Table"):
            if not table_name or not column_definitions:
                st.error("Table name and column definitions are required!")
                return

            query = f"CREATE TABLE {table_name} ({column_definitions});"
            try:
                self.db.execute_query(query)
                st.success(f"Table {table_name} created successfully!")
            except Exception as e:
                st.error(str(e))

    def read_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_tables())
        if table_name:
            query = f"SELECT * FROM {table_name}"
            try:
                data = pd.read_sql(query, self.db.connection)
                st.dataframe(data)
            except Exception as e:
                st.error(str(e))

    def update_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_tables())
        if table_name:
            columns = self.db.fetch_columns(table_name)
            column_to_update = st.selectbox("Select the column to update", columns)
            new_value = st.text_input(f"Enter the new value for {column_to_update}")
            condition_column = st.selectbox("Select the condition column", columns)
            condition_value = st.text_input(f"Enter the condition value for {condition_column}")

            if new_value and condition_value:
                query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition_column} = %s"
                try:
                    self.db.execute_query(query, (new_value, condition_value))
                    st.success("Update successful!")
                except Exception as e:
                    st.error(str(e))

    def delete_from_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_tables())
        if table_name:
            delete_action = st.selectbox("Choose an action", ["Delete Row(s)", "Drop Table"])
            if delete_action == "Delete Row(s)":
                condition_column = st.selectbox("Select the condition column", self.db.fetch_columns(table_name))
                condition_value = st.text_input(f"Enter the condition value for {condition_column}")
                if condition_value:
                    query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
                    try:
                        self.db.execute_query(query, (condition_value,))
                        st.success("Row(s) deleted successfully!")
                    except Exception as e:
                        st.error(str(e))
            elif delete_action == "Drop Table":
                if st.checkbox(f"Confirm drop table {table_name}"):
                    query = f"DROP TABLE {table_name}"
                    try:
                        self.db.execute_query(query)
                        st.success(f"Table {table_name} dropped successfully!")
                    except Exception as e:
                        st.error(str(e))

    def alter_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_tables())
        if table_name:
            alter_action = st.selectbox("Choose an action", ["Add Column", "Modify Column", "Drop Column"])
            if alter_action == "Add Column":
                column_name = st.text_input("Enter the column name to add")
                column_type = st.text_input("Enter the column type (e.g., VARCHAR(255), INT)")
                if column_name and column_type:
                    query = f"ALTER TABLE {table_name} ADD {column_name} {column_type}"
                    try:
                        self.db.execute_query(query)
                        st.success(f"Column {column_name} added successfully!")
                    except Exception as e:
                        st.error(str(e))
            elif alter_action == "Modify Column":
                column_name = st.selectbox("Select the column to modify", self.db.fetch_columns(table_name))
                new_definition = st.text_input("Enter the new column definition")
                if column_name and new_definition:
                    query = f"ALTER TABLE {table_name} MODIFY {column_name} {new_definition}"
                    try:
                        self.db.execute_query(query)
                        st.success(f"Column {column_name} modified successfully!")
                    except Exception as e:
                        st.error(str(e))
            elif alter_action == "Drop Column":
                column_name = st.selectbox("Select the column to drop", self.db.fetch_columns(table_name))
                if column_name:
                    query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
                    try:
                        self.db.execute_query(query)
                        st.success(f"Column {column_name} dropped successfully!")
                    except Exception as e:
                        st.error(str(e))
