import os  
import streamlit as st  
import tkinter as tk
from tkinter import filedialog


def search_database(query, search_types):  
    results = [  
        f"文本结果1：{query}",  
        f"文本结果2：{query}",  
        f"图片结果1：{query}",  
        f"音频结果1：{query}",  
    ]  
    return results  

  
def select_file_or_folder():  
    root = tk.Tk()  
    root.withdraw()  # 隐藏主窗口  
    file_path = filedialog.askopenfilename()  # 打开文件选择对话框  
    return file_path  


# 侧边栏标题  
st.sidebar.title("侧边栏")  
  
# 选择应用程序  
app_choice = st.sidebar.radio("选择应用程序", ["文件浏览器", "搜索应用程序"])  
  
if app_choice == "搜索应用程序":  
    st.title("搜索应用程序")  
    search_query = st.text_input("输入搜索关键词")  
  
    columns = st.columns(3)  
    text_selected = columns[0].checkbox("文本", value=True)  
    image_selected = columns[1].checkbox("图片")  
    audio_selected = columns[2].checkbox("音频")  
  
    if search_query:  
        search_types = []  
        if text_selected:  
            search_types.append("文本")  
        if image_selected:  
            search_types.append("图片")  
        if audio_selected:  
            search_types.append("音频")  
  
        search_results = search_database(search_query, search_types)  
        st.write("搜索结果：")  
        for i, result in enumerate(search_results):  
            with st.beta_expander(f"结果 {i + 1}"):  
                st.write(result)  
  
elif app_choice == "文件浏览器":  
    st.title("文件浏览器")  
  
    if st.button("选择文件"):  
        selected_file = select_file_or_folder()  
        st.write(f"您选择的文件是：{selected_file}")  
