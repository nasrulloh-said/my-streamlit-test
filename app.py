import streamlit as st

st.title("Hello Streamlit")
st.write("This my first website")
name = st.text_input("name")

if st.button("กดที่นี่"):
    st.success(f"สวัสดีกด {name}")
