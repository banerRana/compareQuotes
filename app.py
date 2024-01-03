
import os
os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
import sys
import numexpr as ne 

import streamlit as st
import PyPDF2
import pandas as pd
import tabula
from tabula import read_pdf

java_home = os.getenv('JAVA_HOME', '')
found_jni = False
if os.path.exists(java_home):
    platform_specific['include_dirs'] += [os.path.join(java_home, 'include')]

# Change the default recursion limit of 1000 to 30000
sys.setrecursionlimit(30000)
st.title('🎈 Compare Quotes')

def app():

    st.title('PDF Quotes Comparison')
    user_files = st.file_uploader('Upload PDFs', accept_multiple_files=True, type=['pdf'])
    
    # If some files are uploaded, we want to proceed
    if user_files:
        file_details = {"FileName": [], "Num of Pages": []}

        for file_info in user_files:
            pdf = PyPDF2.PdfReader(file_info)
            file_details["FileName"].append(file_info.name)
            file_details["Num of Pages"].append(len(pdf.pages))
            # multiple_tables option is enabled,
            # tabula-py uses not pd.read_csv(), but pd.DataFrame()
            df = tabula.read_pdf(file_info, 
                pages='all', 
                #stream=True, 
                #guess=False, 
                multiple_tables=True,
                java_options=["-Xmx256m"],
                silent=True)
            for this_df in df:
              st.dataframe(this_df)
            
            
        files_df = pd.DataFrame(file_details)
        st.dataframe(files_df)

    #Other code goes here.
    
    return

if __name__ == '__main__':
    app()
