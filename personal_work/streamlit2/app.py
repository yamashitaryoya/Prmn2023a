import streamlit as st
from data import Database
import pandas as pd

class Reminder:
    
    def __init__(self):
        self.db = Database()
        st.title("Reminder")
        self.menu = ["View","Create","Edit","Delete"]
        self.choice = st.sidebar.radio("Menu",self.menu)
        self.run_menu()

    def run_menu(self):
        if self.choice == "Create":
            self.create_task()
                    
        elif self.choice == "View":
            self.view_task()   
                
        elif self.choice == "Edit":
            self.edit_task()
            
        elif self.choice == "Delete":
            self.delete_task()
             
        else:
            st.subheader("About")    
            
    def create_task(self):
        st.subheader("Add Task")
        col1, col2 = st.columns(2)
                
        with col1:
            task = st.text_area("Task To Do")
                    
        with col2:
            task_status = st.selectbox("Status",["Todo","Doing","Done"])
            task_due_date = st.date_input("Due Date")
                
        if st.button("Add"):
            self.db.add_db(task, task_status, task_due_date)
            st.success("Added : {} ".format(task))
        
    def view_task(self):
        st.subheader("View All Task")
        data = self.db.read_db()
        data = pd.DataFrame(data,columns=["Task","Status","Date"])
        st.dataframe(data)
            
        with st.expander("View Status"):
            task_data = data["Status"].value_counts().to_frame()
            task_data = task_data.reset_index()
            st.dataframe(task_data)
        
    def edit_task(self):
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            data = self.db.read_db()
            data = pd.DataFrame(data,columns=["Task","Status","Date"])
            st.dataframe(data)
            
        task_list = [i[0] for i in self.db.view_task_names()]
        selected_task = st.selectbox("Task",task_list)
        task_result = self.db.get_task(selected_task)
            
        if task_result:
            do = task_result[0][0]
            status =  task_result[0][1]
            date = task_result[0][2]
                
            col1,col2 = st.columns(2)
                
            with col1:
                new_task = st.text_area("Task To Do",do)
                    
            with col2:
                new_status = st.selectbox(status,["ToDo","Doing","Done"])
                new_date = st.date_input(date)
                    
            if st.button("Update Task"):
                self.db.edit_task_db(new_task,new_status,new_date,do,status,date)
                st.success("Updated : {} To {}".format(do,new_task))
                    
            with st.expander("View Updated Data"):
                data = self.db.read_db()
                data = pd.DataFrame(data,columns=["Task","Status","Date"])
                st.dataframe(data)
                    
    def delete_task(self):               
        st.subheader("Delete Items")
        with st.expander("View Data"):
            data = self.db.read_db()
            data = pd.DataFrame(data,columns=["Task","Status","Date"])
            st.dataframe(data)
                
        task_list = [i[0] for i in self.db.view_task_names()]
        delete_task = st.selectbox("Select Task",task_list)
            
        if st.button("Delete"):
            self.db.delete_db(delete_task)
            st.warning("Deleted : {}".format(delete_task))
                
        with st.expander("View Updated Data"):
                data = self.db.read_db()
                data = pd.DataFrame(data,columns=["Task","Status","Date"])
                st.dataframe(data)