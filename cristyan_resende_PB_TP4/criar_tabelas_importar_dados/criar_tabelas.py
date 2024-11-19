import sqlite3

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('banco_para_tp.db')

# Criar um cursor
cursor = conn.cursor()

# Criar tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Funcionarios (
    Id INTEGER PRIMARY KEY,
    Nome TEXT NOT NULL,
    Idade INTEGER NOT NULL,
    Cargo_id INTEGER,
    Departamento_id INTEGER,
    FOREIGN KEY (Cargo_id) REFERENCES Cargos(Id),
    FOREIGN KEY (Departamento_id) REFERENCES Departamentos(Id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Cargos (
    Id INTEGER PRIMARY KEY,
    Nome_cargo TEXT NOT NULL,
    Salario_base INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Departamentos (
    Id INTEGER PRIMARY KEY,
    Nome_departamento TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Historico_de_salarios (
    Id INTEGER PRIMARY KEY,
    Mes DATE NOT NULL,
    Salario INTEGER NOT NULL,
    Funcionario_id INTEGER,
    FOREIGN KEY (Funcionario_id) REFERENCES Funcionarios(Id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Dependentes (
    Id INTEGER PRIMARY KEY,
    Nome_dependente TEXT,
    Idade INTEGER,
    Relacao TEXT,
    Funcionario_id INTEGER,
    FOREIGN KEY (Funcionario_id) REFERENCES Funcionarios(Id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projetos_desenvolvidos (
    Id INTEGER PRIMARY KEY,
    Nome_projeto TEXT NOT NULL,
    Descricao_projeto TEXT NOT NULL,
    Data_inicio DATE,
    Data_conclusao DATE,
    Funcionario_responsavel INTEGER,
    Custo_projeto REAL,
    Status TEXT CHECK(Status IN('Em Planejamento', 'Em Execução', 'Concluído', 'Cancelado')),
    FOREIGN KEY (Funcionario_responsavel) REFERENCES Funcionarios(Id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Recursos_do_projeto (
    Id INTEGER PRIMARY KEY,
    Projeto_Id INTEGER NOT NULL,
    Descricao TEXT NOT NULL,
    Tipo TEXT CHECK(Tipo IN('Financeiro', 'Material', 'Humano')),
    Quantidade REAL NOT NULL,
    Data_utilizacao DATE NOT NULL,
    Custo_total REAL NOT NULL,
    FOREIGN KEY (Projeto_id) REFERENCES Projetos_desenvolvido(Id)
)
''')

# Salvar (commit) as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados e tabelas criados com sucesso!")
