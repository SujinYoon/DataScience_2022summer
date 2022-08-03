import streamlit as st
import sqlite3
import pandas
from datetime import datetime

con = sqlite3.connect('users.db', check_same_thread=False)
cur = con.cursor()

def dbcon():
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    return cur

def check_uid(uid):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE uid='{uid}'")
    res = cur.fetchone()
    return res[0]

def check_uemail(uemail):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE uid='{uemail}'")
    res = cur.fetchone()
    return res[0]

st.markdown("## 회원 가입 ❄️")
st.sidebar.markdown("## 회원 가입 ❄️")

form1 = st.form('my_form', clear_on_submit=True)
form1.info('다음 양식을 모두 입력 후 제출합니다.')
uid = form1.text_input('아이디', max_chars=12).strip()
uname = form1.text_input('성명', max_chars=18).strip()
uemail = form1.text_input('이메일').strip()
upw = form1.text_input('비밀번호', type='password').strip()
upw_ck = form1.text_input('비밀번호 확인', type='password').strip()
ubirth = form1.date_input('생년월일')
ugender = form1.radio('성별', options=['남', '여'], horizontal=True)

submitted = form1.form_submit_button('제출')
print(1, submitted)
if submitted:
    if upw != upw_ck:
        st.warning('비밀번호가 다릅니다. 다시 입력하세요.')
        st.stop()
    if check_uid(uid):
        st.warning('동일한 아이디가 존재합니다.')
        st.stop()
    if check_uemail(uemail):
        st.warning('동일한 이메일이 존재합니다.')
        st.stop()

    cur.execute(f"INSERT INTO users VALUES ('{uid}', '{uname}','{uemail}','{upw}', '{ubirth}', '{ugender}', CURRENT_DATE)")
    con.commit()
    st.success(f'가입 완료: {uid} {uname} {uemail} {upw} {ubirth} {ugender}')
