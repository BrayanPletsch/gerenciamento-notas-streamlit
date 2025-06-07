<h1 align="center">Sistema de Gerenciamento de Notas Escolares</h1>

Este projeto faz parte da avaliação acadêmica de **Estrutura de Dados I - Engenharia de Software**, com foco na implementação de algoritmos de ordenação e busca para gerenciar notas escolares. A aplicação foi desenvolvida utilizando **Python** e **Streamlit**, permitindo interface interativa para professores e alunos.

## 🎯 Objetivo do Trabalho

* **Demonstrar a aplicação de algoritmos de ordenação** (como Quick Sort, Merge Sort) e busca (como Busca Binária).
* **Construir um sistema de gerenciamento de notas que permita**:
  1. Cadastro e autenticação de usuários (professores e alunos).
  2. Gerenciamento de alunos, turmas, disciplinas e lançamentos de notas.
  3. Visualização dos dados de forma ordenada e buscas rápidas em grandes listas.
* **Proporcionar uma interface amigável, permitindo que professores**:
  * Cadastrem alunos, turmas, disciplinas.
  * Insiram e atualizem notas por turma.
* **E que alunos possam**:
  * Consultar suas próprias notas e disciplinas.
  * Acompanhar seu desempenho acadêmico.

## 🚀 Funcionalidades

* **Cadastro de Usuários**: Professores podem criar contas de alunos e gerenciar suas informações.
* **Gerenciamento de Alunos**: O professor pode adicionar, remover ou atualizar informações de alunos.
* **Gerenciamento de Disciplinas**: Cadastro e gerenciamento das disciplinas que os professores lecionam.
* **Gerenciamento de Turmas**: Cadastramento e atualização de turmas em que o professor está envolvido.
* **Lançamento de Notas**: Professores podem inserir, atualizar e remover notas dos alunos por turma e disciplina.
* **Visualização de Notas**: Os professores podem ver as notas dos alunos.

## 💻 Tecnologias Utilizadas

* **Python**: Linguagem de programação utilizada para implementar a lógica do sistema.
* **Streamlit**: Framework utilizado para criar a interface web interativa.
* **Pandas**: Biblioteca para manipulação e análise de dados, utilizada para carregar e gerenciar os arquivos CSV com os dados de alunos, turmas, disciplinas e notas.
* **CSV**: Os dados são armazenados em arquivos CSV simples, o que facilita a leitura, escrita e manipulação dos dados sem a necessidade de banco de dados.

## 🔧 Como Rodar

1. Clone o repositório:
   ```bash
   git clone https://github.com/BrayanPletsch/gerenciamento-notas-streamlit.git
   ```
   
2. Navegue até a pasta do projeto:
   ```bash
   cd gerenciamento-notas-streamlit
   ```
   
3. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
4. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
   
5. Execute o aplicativo:
   ```bash
   streamlit run main.py
   ```

## 👥 Contribuidores

* **Brayan Aragão Pletsch**
* **Gabriel Ribeiro de Carvalho**
* **João Gabriel Melo Albuquerque**
* **Pedro Freire de Farias**
* **João Matheus Bezerra**
* **João Vitor de Freitas Silva**

## 📝 Licença

Este projeto está sob a licença MIT.

Este projeto é parte de uma avaliação acadêmica da disciplina de Estrutura de Dados I do curso de Engenharia de Software.

---

⭐ Projeto desenvolvido para fins educacionais
