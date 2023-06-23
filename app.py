import os  
import streamlit as st  
import tkinter as tk
from tkinter import filedialog
from search import Anything

st.set_page_config(layout="wide")

@st.cache_resource()  
def create_filegpt_instance():  
    return Anything("sentence-transformers/all-mpnet-base-v2")


def search_database(query, search_types): 
    filegpt = create_filegpt_instance()
    semantic_results = filegpt.semantic_search(query)
    bm25_results = filegpt.bm25_search(query)
    exact_results = filegpt.exact_search(query)

    return {"Semantic search results": semantic_results, "BM25 search results": bm25_results, "Exact search results": exact_results}  

  
def select_file_or_folder():  
    root = tk.Tk()  
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path  

 
st.sidebar.title("Memu")  

app_choice = st.sidebar.radio("Select Application", ["SearchAnything", "Adding Files"])
  
if app_choice == "SearchAnything":
    st.title("SearchAnything")
    search_query = st.text_input("Type to search")
  
    columns = st.columns(3)  
    text_selected = columns[0].checkbox("Text", value=True)
    image_selected = columns[1].checkbox("Image")
    audio_selected = columns[2].checkbox("Audio")
  
    if search_query:
        search_types = []
        if text_selected:
            search_types.append("Text")
        if image_selected:
            search_types.append("Image")
        if audio_selected:
            search_types.append("Audio")
        
        search_results = search_database(search_query, search_types)
        num_types = len(search_results.keys())
        cols = st.columns(num_types)

        for col, (results_type, results) in zip(cols, search_results.items()):
            col.write(results_type)
            
            for file_path, file_info in results:
                expander = col.expander(f"{file_path} - Min distance: {file_info['min_distance']:.3f}")
        
                for content, distance, page in zip(file_info["content"], file_info["distance"], file_info["page"]):
                    expander.write(f"Page: {page}, Distance: {distance:.3f}")
                    expander.write(f"Content: {content}")

  
elif app_choice == "Adding Files":
    st.title("Adding Files")
  
    if st.button("Select files"):
        selected_file = select_file_or_folder()
        st.write(f"{selected_file}")
