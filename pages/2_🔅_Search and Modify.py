import streamlit as st
import sqlite3
import pandas
from datetime import datetime

con = sqlite3.connect('users.db', check_same_thread=False)
cur = con.cursor()

def check_uid(uid):
    cur.execute(f"SELECT COUNT(*) FROM users WHERE uid='{uid}'")
    res = cur.fetchone()
    return res[0]

def mod(s_uid, uname, uemail, upw, upw_ck, ubirth, ugender):
    if upw != upw_ck:
        st.warning('비밀번호가 다릅니다. 다시 입력하세요.')
        st.stop()

    cur.execute(
        f"UPDATE users SET uname='{uname}', uemail='{uemail}', upw='{upw}', ubirth='{ubirth}', ugender='{ugender}' WHERE uid='{s_uid}'")
    con.commit()
    st.success(f'수정 완료: {s_uid} {uname} {uemail} {upw} {ubirth} {ugender}')


st.markdown("## 회원 검색 및 수정 🎉")
st.sidebar.markdown("## 회원 검색 및 수정 🎉")

if 'search' not in st.session_state:
    st.session_state['search'] = False

col1, *col2 = st.columns(3)
with col1:
    s_uid = st.text_input('아이디')
col1, col2, *col3 = st.columns(5)
with col1:
    s_btn = st.button('검색')
with col2:
    d_btn = st.button('삭제')

print('검색', s_btn)

if s_btn:
    if check_uid(s_uid) == 0:
        st.warning('해당 아이디는 존재하지 않습니다.')
        st.session_state['search'] = False
        st.stop()
    else:
        st.session_state['search'] = True

if d_btn:
    st.session_state['search'] = False
    if check_uid(s_uid) == 0:
        st.warning('해당 아이디는 존재하지 않습니다.')
        st.stop()
    cur.execute(
        f"DELETE FROM users WHERE uid='{s_uid}'")
    con.commit()
    st.success(f'삭제 완료: {s_uid}')


try:
    if st.session_state['search']:
        cur.execute(f"SELECT * FROM users WHERE uid='{s_uid}'")
        rows = cur.fetchall()
        res = rows[0]
        index = 0
        if res[5]=='여':
            index = 1

        with st.container():
            print('search')
            form2 = st.form('my_form_mod')
            suname = form2.text_input('성명', max_chars=18, value=res[1]).strip()
            suemail = form2.text_input('이메일', value=res[2]).strip()
            supw = form2.text_input('비밀번호', type='password', value=res[3]).strip()
            supw_ck = form2.text_input('비밀번호 확인', type='password', value=res[3]).strip()
            subirth = form2.date_input('생년월일', value=datetime.strptime(res[4], "%Y-%m-%d"))
            sugender = form2.radio('성별', options=['남', '여'], horizontal=True, index=index)

            submitted2 = form2.form_submit_button('수정')
            print(2, submitted2)
            if submitted2:
                mod(s_uid, suname, suemail, supw, supw_ck, subirth, sugender)
except:
    pass
