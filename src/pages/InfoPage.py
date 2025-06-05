import streamlit as st

def show_info():
    
    st.markdown(
    "<h1 style='text-align: center;'>Sobre o Projeto</h1>",
    unsafe_allow_html=True)
    st.write("""
    Este projeto faz parte da avaliação acadêmica de **Estrutura de Dados I – Engenharia de Software**,
    com foco na implementação de algoritmos de ordenação e busca para gerenciar notas escolares.
    A aplicação foi desenvolvida utilizando **Python** e **Streamlit**, permitindo interface 
    interativa para professores e alunos.
    """)

    st.header("Objetivo do Trabalho")
    st.write("""
    - Demonstrar a aplicação de algoritmos de ordenação (como Quick Sort, Merge Sort) e busca (como Busca Binária).
    - Construir um sistema de gerenciamento de notas que permite:
      1. Cadastro e autenticação de usuários (professores e alunos).
      2. Gerenciamento de alunos, turmas, disciplinas e lançamentos de notas.
      3. Visualização dos dados de forma ordenada e buscas rápidas em grandes listas.
    - Proporcionar uma interface amigável, permitindo que professores:
      - Cadastrem alunos, turmas, disciplinas.
      - Insiram e atualizem notas por turma.
      - Visualizem relatórios de desempenho.
    - E que alunos possam:
      - Consultar suas próprias notas e disciplinas.
      - Acompanhar seu desempenho acadêmico.
    """)

    st.header("Quem Somos")
    st.write("""
    Este trabalho foi desenvolvido por:
    - **Brayan Aragão Pletsch**  
    - **Gabriel Ribeiro de Carvalho**  
    - **João Gabriel Melo Albuquerque**  
    - **João Matheus Bezerra**  
    - **João Vitor de Freitas Silva**
    - **Pedro Freire de Farias**
    """)

    st.write("---")
    st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Engenharia de Software N1 – Estrutura de Dados I • Licença MIT</p>",
    unsafe_allow_html=True)

