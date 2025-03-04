import streamlit as st

st.title("Agent Center")


home, info, data = st.tabs(["Home", "Info", "Data"])


with home:
    with open("schedule.txt", "r", encoding="utf-8") as file:
        schedule = file.readlines()
        

    for day in schedule[::-1]:
        date, time = day.split(": ")
        st.markdown(f"""{date}  
{time}""")




with info:
    with open("Akash_info.txt", "r", encoding='utf-8') as f:
        content = f.read()

    left, right = st.columns(2)
    with left:
        st.markdown(content)

    with right:
        st.text_area("New text", height=500)    

        st.button("Edit changes")


with data:
    pass
