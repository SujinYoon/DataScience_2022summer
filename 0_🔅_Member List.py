import streamlit as st
import sqlite3
import pandas

con = sqlite3.connect('users.db', check_same_thread=False)
cur = con.cursor()

st.markdown("## 회원 목록 🎈")
st.sidebar.markdown("## 회원 목록 🎈")

with st.container():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    df = pandas.DataFrame.from_records(data=rows, columns=cols)
    st.dataframe(df, width=1200)