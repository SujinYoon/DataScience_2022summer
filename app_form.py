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

def mod(s_uid, uname, uemail, upw, upw_ck, ubirth, ugender):
    if upw != upw_ck:
        st.warning('비밀번호가 다릅니다. 다시 입력하세요.')
        st.stop()

    st.success(f'{s_uid} {uname} {uemail} {upw} {ubirth} {ugender}')
    print(f'{s_uid} {uname} {uemail} {upw} {ubirth} {ugender}')
    cur.execute(
        f"UPDATE users SET uname='{uname}', uemail='{uemail}', upw='{upw}', ubirth='{ubirth}', ugender='{ugender}' WHERE uid='{s_uid}'")
    con.commit()

if 'refresh' not in st.session_state:
    st.session_state['refresh'] = False

st.subheader('회원 가입 폼')

with st.container():
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

        st.success(f'{uid} {uname} {uemail} {upw} {ubirth} {ugender}')
        cur.execute(f"INSERT INTO users VALUES ('{uid}', '{uname}','{uemail}','{upw}', '{ubirth}', '{ugender}', CURRENT_DATE)")
        con.commit()

st.subheader('회원 목록')
with st.container():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    st.text(cur.description)
    df = pandas.DataFrame.from_records(data=rows, columns=cols)
    st.dataframe(df)

if 'search' not in st.session_state:
    st.session_state['search'] = False

st.subheader('회원 검색')

col1, col2, col3 = st.columns(3)
with col1:
    s_uid = st.text_input('아이디')
with col2:
    s_btn = st.button('검색')
    d_btn = st.button('삭제')
print('검색', s_btn)
if s_btn:
    if check_uid(s_uid) == 0:
        st.warning('해당 아이디는 존재하지 않습니다.')
        st.session_state['search'] = False
        st.stop()
    else:
        st.session_state['search'] = True

if st.session_state['search']:
    cur.execute(f"SELECT * FROM users WHERE uid='{s_uid}'")
    rows = cur.fetchall()
    res = rows[0]
    index = 0
    if res[5]=='여':
        index = 1

    with st.container():
        form2 = st.form('my_form_mod', clear_on_submit=True)
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
