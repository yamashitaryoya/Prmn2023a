import streamlit as st
import pandas as pd
from data import Database


class Reminder:
    
    def __init__(self):
        
        st.set_page_config(
            page_title="Reminder",
            #layout="wide"
        )
    
        self.db = Database()
        self.choice = None
        self.menus = ["View","Create","Edit","Delete"]
        self.run_menu()
        
    def run_menu(self):
        st.title("Reminder")
        
        self.choice = st.radio("Menu", self.menus, horizontal=True)
        self.run_app(self.choice)
            
    def run_app(self, menu):
        if menu == "View":
            self.view_task()
    
        if menu == "Create":
            self.create_task()
            
        if menu == "Edit":
            self.edit_task()
            
        if menu == "Delete":
            self.delete_task()
            
    def view_task(self):
        st.header("All Task")
        data = self.db.read_db()
        data = pd.DataFrame(data,columns=["Task","Status","Date","Priority"])
        st.table(data.style)
        
        tab1, tab2, tab3 = st.tabs(["Status", "Date", "Priority"])
            
        with tab1:
            status = ["Todo","Doing","Done"]
            cols = st.columns(3)
            for i, statu in enumerate(status):
                data = self.db.get_task_status(statu)
                with cols[i]:
                    st.write(statu)
                    data = pd.DataFrame(data,columns=["Task","Status","Date","Priority"])
                    st.table(data[["Task","Date","Priority"]])
            
        with tab3:
            priorities = ["low", "medium", "high"]
            cols = st.columns(3)
            for i, priority in enumerate(priorities):
                data = self.db.get_task_priority(priority)
                with cols[i]:
                    st.write(priority)
                    data = pd.DataFrame(data,columns=["Task","Status","Date","Priority"])
                    st.table(data[["Task","Status","Date"]])
                    
        with tab2:
            data = self.db.get_task_date()
            data = pd.DataFrame(data,columns=["Task","Status","Date","Priority"])
            st.table(data[["Task","Status","Date", "Priority"]])
            
            
    def create_task(self):
        st.header("New Task")
        col1, col2 = st.columns(2)
                
        with col1:
            task = st.text_area("Task Name")
            task_due_date = st.date_input("Due Date")
                    
        with col2:
            task_status = st.select_slider("Status",["Todo","Doing","Done"])
            task_priority = st.select_slider("Priority", ["low", "medium", "high"])
    
                
        if st.button("Add"):
            task_list = [i[0] for i in self.db.view_task_names()]
            if task not in task_list:
                self.db.add_db(task, task_status, task_due_date, task_priority)
                st.success("Added! : {} ".format(task),icon="✅")
                self.reset()
            
            else:
                st.error("「{}」 have already been entered!     Please change Task Name!".format(task),icon="❗")
                
            
    def reset(self):
        self.task = ""
        self.task_due_date = None
        self.task_status = "Todo"
        self.task_priority = "low"
        
            
    def edit_task(self):
        st.header("Edit Task")   
        task_list = [i[0] for i in self.db.view_task_names()]
        selected_task = st.selectbox("Select",task_list)
        task_result = self.db.get_task(selected_task)
            
        if task_result:
            do = task_result[0][0]
            status =  task_result[0][1]
            date = task_result[0][2]
            priority = task_result[0][3]
                
            col1,col2 = st.columns(2)
                
            with col1:
                new_task = st.text_area("Task Name",do)
                new_date = st.date_input("Date[{}]".format(date))
                    
            with col2:
                new_status = st.select_slider("Status", ["Todo","Doing","Done"], status)
                new_priority = st.select_slider("Priority", ["low", "medium", "high"], priority)
                    
            if st.button("Update Task"):
                task_list = [i[0] for i in self.db.view_task_names()]
                    
                if do != new_task and new_task in task_list:
                        st.error("「{}」 have already been entered!     Please change Task Name!".format(new_task),icon="❗")
                    
                else: 
                    if new_status == "Done":
                        st.balloons()
                    self.db.edit_task_db(new_task, new_status, new_date, new_priority, do, status, date, priority)
                    st.success("Updated : {} To {}".format(do,new_task), icon="✅")
                
                        
    def delete_task(self):      
        st.header("Delete Task")        
        task_list = [i[0] for i in self.db.view_task_names()]
        delete_task = st.selectbox("Select",task_list)
        delete_check = st.checkbox("Delete.")
        
        if delete_check:
            st.warning("Do you really want to delete it ?",icon="⚠️")
            if st.button("Yes!!"):
                self.db.delete_db(delete_task)
                st.success("Deleted!! : {}".format(delete_task), icon="✅")
            