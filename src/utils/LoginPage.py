import streamlit as st
import time
from src.utils.Auth import login_user_from_csv, register_professor, logout


def render_login_tab():
    if st.session_state.logged_in and st.session_state.user_type in ["professor", "aluno"]:
        st.success(f"Você está logado como {st.session_state.current_user} ({st.session_state.user_type})")
        if st.button("Logout"):
            logout()
        return

    with st.form(key="login_form", clear_on_submit=True):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        if st.form_submit_button("Entrar"):
            with st.spinner("Verificando credenciais..."):
                time.sleep(1)
                if login_user_from_csv(usuario, senha):
                    st.success("Login efetuado com sucesso!")
                    time.sleep(0.6)
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")


def render_register_tab():
    if st.session_state.logged_in and st.session_state.user_type == "professor":
        st.success(f"Professor {st.session_state.current_user} já está cadastrado e logado")
        if st.button("Logout", key="logout_prof"):
            logout()
        return

    st.write("Apenas professores podem se cadastrar. Se você é aluno, peça ao administrador que crie sua conta.")
    with st.form(key="register_form", clear_on_submit=True):
        username = st.text_input("Novo usuário (ex.: seu nome de login)")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")
        is_prof = st.checkbox("Sou professor")
        if st.form_submit_button("Cadastrar"):
            if not is_prof:
                st.error("Somente professores podem se cadastrar. Se você for aluno, contate o administrador.")
            elif not username or not password or not confirm_password:
                st.error("Preencha todos os campos.")
            elif password != confirm_password:
                st.error("As senhas não coincidem.")
            elif register_professor(username, password):
                st.success("Professor cadastrado com sucesso! Você já pode fazer login.")


def show_login_page():
    st.set_page_config(page_title="Login ‐ Sistema de Notas", page_icon="📝", layout="centered")
    login_tab, register_tab = st.tabs(["Entrar", "Cadastrar"])
    with login_tab:
        render_login_tab()
    with register_tab:
        render_register_tab()