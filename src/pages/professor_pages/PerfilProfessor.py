import streamlit as st
import pandas as pd
import os

# Caminhos para os arquivos CSV
CSV_DIR = "data"
TURMAS_CSV_PATH = os.path.join(CSV_DIR, "turmas.csv")
DISCIPLINAS_CSV_PATH = os.path.join(CSV_DIR, "disciplinas.csv")

# Garante a existência dos arquivos CSV com cabeçalhos adequados
def _ensure_csv_files():
    os.makedirs(CSV_DIR, exist_ok=True)
    if not os.path.exists(TURMAS_CSV_PATH) or os.path.getsize(TURMAS_CSV_PATH) == 0:
        pd.DataFrame(columns=["turma"]).to_csv(TURMAS_CSV_PATH, index=False)
    if not os.path.exists(DISCIPLINAS_CSV_PATH) or os.path.getsize(DISCIPLINAS_CSV_PATH) == 0:
        pd.DataFrame(columns=["nome_disciplina"]).to_csv(DISCIPLINAS_CSV_PATH, index=False)

# Interface principal do perfil do professor
def show_meu_perfil():
    current_user = st.session_state.get("current_user", "Desconhecido")
    
    st.markdown("""
        <h1 style='color:#facc15; text-align: center;'>👨‍🏫 Meu Perfil</h1>
        <p><strong>Nome do Professor:</strong> {}</p>
    """.format(current_user), unsafe_allow_html=True)

    _ensure_csv_files()

    # Leitura dos dados
    turmas_df = pd.read_csv(TURMAS_CSV_PATH, dtype=str, keep_default_na=False)
    turmas = turmas_df["turma"].str.strip().tolist()

    disciplinas_df = pd.read_csv(DISCIPLINAS_CSV_PATH, dtype=str, keep_default_na=False)
    disciplinas = disciplinas_df["nome_disciplina"].str.strip().tolist()

    # Exibição das turmas
 

    # Resumo visual
    if turmas or disciplinas:
        st.markdown("---")
        st.markdown("### 📚 Turmas e Disciplinas Disponíveis em seu Perfil")

        items = [{"type": "Turma", "value": t, "color": "#facc15"} for t in turmas] + \
                [{"type": "Disciplina", "value": d, "color": "#3b82f6"} for d in disciplinas]

        cols = st.columns(min(4, len(items)))
        for idx, item in enumerate(items):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                    <div style="background-color:#1e293b; padding:16px; border-radius:10px; margin:8px 0; text-align:center;">
                        <h4 style="color:{item['color']}; margin:5px 0;">{item['type']}</h4>
                        <p style="color:white; margin:0;">{item['value']}</p>
                    </div>
                """, unsafe_allow_html=True)
