import os

import pandas as pd
import streamlit as st


CSV_PATH=os.path.join('data','users.csv')


def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in=False
    if 'user_type' not in st.session_state:
        st.session_state.user_type=None
    if 'current_user' not in st.session_state:
        st.session_state.current_user=None
    if 'user_id' not in st.session_state:
        st.session_state.user_id=None


def check_auth()->bool:
    return st.session_state.logged_in


def _ensure_csv_header(path):
    header=['id','username','password','user_type','name']
    os.makedirs(os.path.dirname(path),exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path)==0:
        pd.DataFrame(columns=header).to_csv(path,index=False)
        return
    try:
        cols=pd.read_csv(path,nrows=0).columns.tolist()
        if set(cols)!=set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(path,index=False)


def login_user_from_csv(username,password,path=CSV_PATH)->bool:
    _ensure_csv_header(path)
    try:
        df=pd.read_csv(path,dtype=str,keep_default_na=False)
    except Exception as e:
        st.error(f'Erro ao ler users.csv: {e}')
        return False
    df=df.apply(lambda c:c.str.strip())
    user=username.strip()
    pwd=password.strip()
    match=df.query('username==@user and password==@pwd')
    if not match.empty:
        st.session_state.logged_in=True
        st.session_state.user_id=match.iloc[0]['id']
        st.session_state.current_user=match.iloc[0]['name']
        st.session_state.user_type=match.iloc[0]['user_type']
        return True
    return False


def register_professor(username,password,name,path=CSV_PATH)->bool:
    _ensure_csv_header(path)
    try:
        df=pd.read_csv(path,dtype=str,keep_default_na=False)
    except Exception as e:
        st.error(f'Erro ao ler users.csv: {e}')
        return False
    df=df.apply(lambda c:c.str.strip())
    user=username.strip()
    if user in df['username'].tolist():
        st.error('Já existe um usuário com esse nome. Tente outro.')
        return False
    if df.empty:
        new_id='001'
    else:
        df['id']=pd.to_numeric(df['id'],errors='coerce').fillna(0).astype(int)
        new_id=str(df['id'].max()+1).zfill(3)
    new_row=pd.DataFrame([{
        'id':new_id,
        'username':user,
        'password':password.strip(),
        'user_type':'professor',
        'name':name.strip()
    }])
    df=pd.concat([df,new_row],ignore_index=True)
    df.to_csv(path,index=False)
    return True


def logout():
    st.session_state.logged_in=False
    st.session_state.user_type=None
    st.session_state.current_user=None
    st.session_state.user_id=None
    if hasattr(st,'rerun'):
        st.rerun()
    else:
        st.stop()