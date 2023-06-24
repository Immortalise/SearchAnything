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

    # bm25_results = filegpt.bm25_search(query)
    # exact_results = filegpt.exact_search(query)

    # return {"Semantic search results": semantic_results, "BM25 search results": bm25_results, "Exact search results": exact_results}  

  
def select_file_or_folder():  
    root = tk.Tk()  
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path  

 
st.sidebar.title("Memu")  

app_choice = st.sidebar.radio("Select Application", ["Anything", "Adding Files"])
  
if app_choice == "Anything":
    st.title("Anything")
    search_query = st.text_input("Type to search")
  
    columns = st.columns(2)  
    text_selected = columns[0].checkbox("Text", value=True)
    image_selected = columns[1].checkbox("Image")
    # audio_selected = columns[2].checkbox("Audio")
  
    if search_query:
        search_type = ""
        if text_selected:
            search_type = "text"
        if image_selected:
            search_type = "image"
        # if audio_selected:
        #     search_types.append("Audio")
        
        search_results = search_database(search_query, search_type)
        num_types = len(search_results.keys())
        cols = st.columns(num_types)

        if search_type == "text":
            for col, (results_type, results) in zip(cols, search_results.items()):
                col.write(results_type)
                for file_path, content, dist in results:
                    st.write(file_path, content, dist)
        
        elif search_type == "image":
            for col, (results_type, results) in zip(cols, search_results.items()):
                col.write(results_type)
                for file_path, dist in results:
                    st.write(file_path, dist)

  
elif app_choice == "Adding Files":
    st.title("Adding Files")
  
    if st.button("Select files"):
        selected_file = select_file_or_folder()
        st.write(f"{selected_file}")
