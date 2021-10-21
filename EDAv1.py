# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 08:20:41 2021

@author: smaskara
"""

#%%
#Load all required packages

import streamlit as st
import pandas as pd
import numpy as np
import pandas_profiling
import openpyxl
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

#import SessionState
#%%
#Designing the main page
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="EDA Accelerator", page_icon="🔍", layout="wide")
hide_streamlit_style = """
            <style>
            footer {
	        visibility: hidden;
	            }
            footer:after {
	            content:'Developed by BI&A COE'; 
	            visibility: visible;
	            display: block;
	            position: relative;
	            #background-color: red;
	            padding: 5px;
	            top: 2px;
                    }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#Defining the function to read the uploaded data
@st.cache(allow_output_mutation=True, persist=True)
def reading_dataset():
    global dataset
    try:
        dataset = pd.read_excel(uploaded_file)
    except ValueError:
        dataset = pd.read_csv(uploaded_file)
    return dataset


#Designing the side bar
with st.sidebar.subheader('Connect your Data'):
    input_selector = st.sidebar.selectbox("Please choose your data source",["XLSX/CSV","SQL Server"])
    if input_selector == "XLSX/CSV":
        uploaded_file = st.sidebar.file_uploader("Please upload a file of type: xlsx, csv", type=["xlsx", "csv"])
    else:
        server = st.sidebar.text_input(label = "Enter Server")
        db = st.sidebar.text_input(label = "Enter Database")
        table = st.sidebar.text_input(label = "Enter Table")
        username = st.sidebar.text_input(label = "Enter Username")
        pwd = st.sidebar.text_input(label = "Enter Password",type = "password")
        


if uploaded_file is not None:
    dataset = reading_dataset()
    st.write("First 10 records")
    display_sample = st.dataframe(dataset.head(10))
    col_for_selection = dataset.columns
    #st.multiselect("Select columns for data profiling",col_for_selection)
    container = st.container()
    all = st.checkbox("Select all")
    if all:
        selected_options = container.multiselect("Select columns for data profiling",col_for_selection,list(col_for_selection))
    else:
        selected_options = container.multiselect("Select columns for Data Profiling",col_for_selection)

    st.write("Sample of data to be used for profiling")
    new_df = dataset[selected_options]    
    st.dataframe(new_df.head(10))
    if len(new_df.columns) > 0:
        dp_proceed = st.checkbox("Proceed with data profiling")
        if dp_proceed:
            report = ProfileReport(new_df, orange_mode=True,config_file="CustomConfig.yml")
            st_profile_report(report)
else:
    st.info("Please upload a file to continue")
    
        

        
    
    
    
    
    
    
    
    
    
    
    
    