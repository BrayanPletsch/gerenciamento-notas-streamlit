import streamlit as st
import pandas as pd
import os

CSV_DIR                  = "data"
USERS_CSV                = os.path.join(CSV_DIR, "users.csv")
PROF_TURMAS_CSV          = os.path.join(CSV_DIR, "professor_turmas.csv")
PROF_DISCIPLINAS_CSV     = os.path.join(CSV_DIR, "professor_disciplinas.csv")

def _ensure_professor_turmas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["professor", "turma"]
    if (not os.path.exists(PROF_TURMAS_CSV)) or (os.path.getsize(PROF_TURMAS_CSV) == 0):
        pd.DataFrame(columns=header).to_csv(PROF_TURMAS_CSV, index=False)

def _ensure_professor_disciplinas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["professor", "disciplina"]
    if (not os.path.exists(PROF_DISCIPLINAS_CSV)) or (os.path.getsize(PROF_DISCIPLINAS_CSV) == 0):
        pd.DataFrame(columns=header).to_csv(PROF_DISCIPLINAS_CSV, index=False)

def show_meu_perfil():
    current_user = st.session_state.get("current_user", "Desconhecido")
    st.title("Meu Perfil")
    st.write(f"**Nome do Professor:** {current_user}")

    # Garante que existam os CSVs de vinculação
    _ensure_professor_turmas_csv()
    _ensure_professor_disciplinas_csv()

    # Lista de turmas vinculadas
    df_turmas = pd.read_csv(PROF_TURMAS_CSV, dtype=str, keep_default_na=False)
    df_turmas["professor"] = df_turmas["professor"].str.strip()
    df_turmas["turma"] = df_turmas["turma"].str.strip()
    turmas_do_prof = df_turmas[df_turmas["professor"] == current_user]["turma"].tolist()

    # Lista de disciplinas vinculadas
    df_disc = pd.read_csv(PROF_DISCIPLINAS_CSV, dtype=str, keep_default_na=False)
    df_disc["professor"]    = df_disc["professor"].str.strip()
    df_disc["disciplina"]   = df_disc["disciplina"].str.strip()
    disciplinas_do_prof = df_disc[df_disc["professor"] == current_user]["disciplina"].tolist()

    st.subheader("Turmas Vinculadas")
    if turmas_do_prof:
        for t in turmas_do_prof:
            st.markdown(f"- **{t}**")
    else:
        st.info("Nenhuma turma vinculada.")

    st.subheader("Disciplinas Vinculadas")
    if disciplinas_do_prof:
        for d in disciplinas_do_prof:
            st.markdown(f"- **{d}**")
    else:
        st.info("Nenhuma disciplina vinculada.")

    # Visual criativo: exibe cards simples para cada turma/disciplina
    st.write("---")
    if turmas_do_prof or disciplinas_do_prof:
        st.subheader("Resumo Visual")
        cols = st.columns( max(1, len(turmas_do_prof + disciplinas_do_prof)) )
        idx = 0
        for t in turmas_do_prof:
            with cols[idx]:
                st.markdown(f"""
                    <div style="background-color:#1e293b; padding:10px; border-radius:8px; text-align:center;">
                        <h4 style="color:#facc15; margin:5px;">Turma</h4>
                        <p style="color:white; margin:5px;">{t}</p>
                    </div>
                """, unsafe_allow_html=True)
            idx += 1
        for d in disciplinas_do_prof:
            with cols[idx]:
                st.markdown(f"""
                    <div style="background-color:#1e293b; padding:10px; border-radius:8px; text-align:center;">
                        <h4 style="color:#3b82f6; margin:5px;">Disciplina</h4>
                        <p style="color:white; margin:5px;">{d}</p>
                    </div>
                """, unsafe_allow_html=True)
            idx += 1

