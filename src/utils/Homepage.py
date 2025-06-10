import streamlit as st

from src.pages.professor_pages.ProfessorHome import show_professor_home
from src.pages.aluno_pages.AlunoHome import show_aluno_home

def show_homepage():
    user_type = st.session_state.get("user_type", None)

    if user_type == "professor":
        show_professor_home()
    elif user_type == "aluno":
        show_aluno_home()
    else:
        st.warning("Usuário sem perfil válido. Faça login novamente.")
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.current_user = None
        st.stop()
