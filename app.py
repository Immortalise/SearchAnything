import os  
import streamlit as st  
import tkinter as tk
from tkinter import filedialog
from anything import Anything

st.set_page_config(layout="wide")

@st.cache_resource()  
def create_instance():  
    return Anything()


def search_database(search_query, search_type): 
    anything = create_instance()
    semantic_results = anything.semantic_search(search_type, search_query)
    return {"Semantic search results": semantic_results}  

  
def select_file_or_folder():  
    root = tk.Tk()  
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path  


st.title("Anything")
search_query = st.text_input("Type to search")

option_selected = st.selectbox("Choose an option", ("Text", "Image"))

if search_query:
    search_type = option_selected.lower()
    
    search_results = search_database(search_query, search_type)
    num_types = len(search_results.keys())
    cols = st.columns(num_types)

    if search_type == "text":
        for col, (results_type, results) in zip(cols, search_results.items()):
            col.write(results_type)
            for file_path, content, dist in results:
                with col.expander("Path: {} Similarity: {:.2f}".format(file_path, dist)):
                    st.write(content)
    
    elif search_type == "image":
        for col, (results_type, results) in zip(cols, search_results.items()):
            col.write(results_type)
            for file_path, dist in results:
                st.image(file_path, caption="Path: {} Similarity: {:.2f}".format(file_path, dist))
