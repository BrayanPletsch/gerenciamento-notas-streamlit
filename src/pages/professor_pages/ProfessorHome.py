import streamlit as st

from src.pages.professor_pages.AlunoManagement import show_aluno_management
from src.pages.professor_pages.DisciplinaManagement import show_disciplina_management
from src.pages.professor_pages.TurmaManagement import show_turma_management
from src.pages.professor_pages.NotasPorTurma import show_notas_por_turma
from src.pages.professor_pages.CriarCadastroAlunos import show_criar_cadastro_alunos
from src.pages.professor_pages.PerfilProfessor import show_meu_perfil
from src.pages.InfoPage import show_info
from src.utils.Auth import logout


def show_professor_home():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "ProfessorHome"

    st.set_page_config(page_title="Painel do Professor", page_icon="👩‍🏫", layout="wide")

    st.sidebar.title(f"Bem-vindo, {st.session_state.current_user}!")
    st.sidebar.divider()
    if st.sidebar.button("Home", use_container_width=True):
        st.session_state.current_page = "ProfessorHome"
    if st.sidebar.button("Meu Perfil", use_container_width=True):
        st.session_state.current_page = "PerfilProfessor"
    if st.sidebar.button("Criar Cadastro Alunos", use_container_width=True):
        st.session_state.current_page = "CriarCadastroAlunos"
    if st.sidebar.button("Informações do Projeto", use_container_width=True):
        st.session_state.current_page = "InfoPage"
    st.sidebar.divider()
    if st.sidebar.button("Sair", use_container_width=True):
        logout()

    page = st.session_state.current_page

    if page == "ProfessorHome":
        st.title("Painel do Professor")
        st.write(f"Olá, Professor **{st.session_state.current_user}**!")
        st.write("---")
        st.subheader("Selecione uma funcionalidade:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👥 Gerenciar Alunos", use_container_width=True):
                st.session_state.current_page = "GerenciarAlunos"
                st.rerun()
            if st.button("📚 Gerenciar Disciplinas", use_container_width=True):
                st.session_state.current_page = "GerenciarDisciplinas"
                st.rerun()
        with col2:
            if st.button("🏷️ Gerenciar Turmas", use_container_width=True):
                st.session_state.current_page = "GerenciarTurmas"
                st.rerun()
            if st.button("📝 Notas por Turma", use_container_width=True):
                st.session_state.current_page = "NotasPorTurma"
                st.rerun()
        st.write("---")
        st.caption("Sistema de Gerenciamento de Notas Escolares  •  Versão Acadêmica")

    elif page == "GerenciarAlunos":
        show_aluno_management()
    elif page == "GerenciarDisciplinas":
        show_disciplina_management()
    elif page == "GerenciarTurmas":
        show_turma_management()
    elif page == "NotasPorTurma":
        show_notas_por_turma()
    elif page == "PerfilProfessor":
        show_meu_perfil()
    elif page == "CriarCadastroAlunos":
        show_criar_cadastro_alunos()
    elif page == "InfoPage":
        show_info()