<h1 align="center">Sistema de Gerenciamento de Notas Escolares</h1>

<p align="center">Este projeto faz parte da avaliação acadêmica de Estrutura de Dados I - Engenharia de Software, com foco na implementação de algoritmos de ordenação e busca para gerenciar notas escolares. A aplicação foi desenvolvida utilizando Python e Streamlit, permitindo interface interativa para professores e alunos.</p>

---

* **Autenticação de usuários** (professores e alunos)
* **Cadastro de alunos**, **turmas** e **disciplinas**
* **Lançamento**, **atualização** e **remoção** de notas
* **Consulta** de notas pelos alunos

<h2 align="center">Estrutura de Pastas</h2>

```
gerenciamento-notas-streamlit/
├── data/
│   ├── users.csv
│   ├── alunos.csv
│   ├── turmas.csv
│   ├── disciplinas.csv
│   └── notas.csv
├── src/
│   ├── pages/
│   │   ├── aluno_pages/
│   │   │   └── AlunoHome.py
│   │   ├── professor_pages/
│   │   │   ├── ProfessorHome.py
│   │   │   ├── AlunoManagement.py
│   │   │   ├── TurmaManagement.py
│   │   │   ├── DisciplinaManagement.py
│   │   │   ├── NotasPorTurma.py
│   │   │   ├── CriarCadastroAlunos.py
│   │   │   └── PerfilProfessor.py
│   │   └── InfoPage.py
│   └── utils/
│       ├── __init__.py
│       ├── Auth.py
│       ├── Homepage.py
│       └── LoginPage.py
├── .gitignore
├── LICENSE
├── main.py
├── requirements.txt
└── README.md
```

<h2 align="center">Como Executar</h2>

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/BrayanPletsch/gerenciamento-notas-streamlit.git
   cd gerenciamento-notas-streamlit
   ```
2. **Instalar dependências**

   ```bash
   python3 -m venv .venv          # No Windows: python -m venv .venv 
   source .venv/bin/activate      # No Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Rodar a aplicação**

   ```bash
   streamlit run main.py
   ```
4. **Navegar** no navegador para `http://localhost:8501`

<h2 align="center">Visão Geral da Arquitetura</h2>

O sistema organiza os dados em arquivos CSV na pasta `data/`:

* **users.csv**: cadastro de professores e alunos

  ```csv
  id,username,password,user_type,name
  001,professor,123,professor,Kadidja Valéria
  38473585,aluno,123,aluno,Brayan Aragão Pletsch
  ```
* **alunos.csv**: vínculo entre aluno e turma

  ```csv
  user_id,matricula,nome,turma
  002,38473585,Brayan Aragão Pletsch,N1
  003,38465132,João Gabriel Melo Albuquerque,N1
  ```
* **turmas.csv**: lista de turmas disponíveis

  ```csv
  turma,descricao
  N1,Melhor turma da professora Kadidja
  ```
* **disciplinas.csv**: catálogo de disciplinas

  ```csv
  codigo,nome_disciplina
  0001,Estrutura de Dados I
  0002,Banco de Dados
  ```
* **notas.csv**: registro de notas lançadas

  ```csv
  id,matricula,codigo,nota
  001,38473585,0001,10
  ```

Cada página do Streamlit (`src/pages/...`) carrega e valida o CSV correspondente, garantindo criação automática do arquivo com cabeçalho correto quando necessário. A lógica de leitura/gravação foi abstraída em funções reutilizáveis para manter o código organizado.

<h2 align="center">Principais Funcionalidades</h2>

#### Autenticação

* **Login** de professores e alunos via `users.csv`
* **Registro** de novos professores e criação de logins de aluno a partir de `alunos.csv`

#### Painel do Professor

* **Gerenciar Alunos**: criar e remover registros em `alunos.csv`
* **Gerenciar Turmas**: CRUD em `turmas.csv`
* **Gerenciar Disciplinas**: CRUD em `disciplinas.csv`
* **Lançar Notas**: adicionar, atualizar e remover entradas em `notas.csv`
* **Perfil**: exibe turmas e disciplinas disponíveis

#### Área do Aluno

* **Visualizar Dados Pessoais**: nome e turma
* **Consultar Notas**: tabela de disciplinas e notas, agragada por unidade de matrícula

### Tecnologias e Ferramentas

* **Python 3.12+**
* **Streamlit** para construção rápida de interface web
* **Pandas** para manipulação de dados tabulares
* **Arquivos CSV** para persistência leve, sem banco de dados externo

<h2 align="center">Contribuidores</h2>

* Brayan Aragão Pletsch
* Gabriel Ribeiro de Carvalho
* João Gabriel Melo Albuquerque
* João Matheus Bezerra
* João Vitor de Freitas Silva
* Pedro Freire de Farias

<h2 align="center">Licença</h2>

Este projeto está licenciado sob a [MIT License](LICENSE).

>© 2025 Engenharia de Software N1 – Estrutura de Dados I • Licença MIT