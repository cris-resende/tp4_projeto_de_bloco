import pandas as pd
import sqlite3

conn = sqlite3.connect('banco_para_tp.db')

cursor = conn.cursor()

# 1.Listar individualmente as tabelas de: Funcionários, Cargos, Departamentos, Histórico de Salários e Dependentes em ordem crescente.

query_funcionarios = "SELECT * FROM Funcionarios ORDER BY Nome ASC"
df_funcionarios = pd.read_sql_query(query_funcionarios, conn)
print("Funcionários em ordem crescente")
print(df_funcionarios)

query_cargos = "SELECT * FROM Cargos ORDER BY Nome_cargo ASC"
df_cargos = pd.read_sql_query(query_cargos, conn)
print("Cargos em ordem crescente")
print(df_cargos)

query_departamentos = "SELECT * FROM Departamentos ORDER BY Nome_departamento ASC"
df_departamentos = pd.read_sql_query(query_departamentos, conn)
print("Departamentos em ordem crescente")
print(df_departamentos)

query_historicos = "SELECT * FROM Historico_de_salarios ORDER BY Mes ASC"
df_historicos = pd.read_sql_query(query_historicos, conn)
print("Históricos de salários em ordem crescente")
print(df_historicos)

query_dependentes = "SELECT * FROM Dependentes ORDER BY Nome_dependente ASC"
df_dependentes = pd.read_sql_query(query_dependentes, conn)
print("Dependentes em ordem crescente")
print(df_dependentes)

#2. Listar os funcionários, com seus cargos, departamentos e os respectivos dependentes.

query_dados_completos = """
SELECT Funcionarios.Nome, Cargos.Nome_cargo, Departamentos.Nome_departamento, Dependentes.Nome_dependente
FROM Funcionarios
JOIN Cargos ON Funcionarios.Cargo_id = Cargos.Id
JOIN Departamentos ON Funcionarios.Departamento_id = Departamentos.Id
LEFT JOIN Dependentes ON Funcionarios.Id = Dependentes.Funcionario_id;
"""
df_dados_completos = pd.read_sql(query_dados_completos, conn)
print("Funcionário, cargos, departamentos e dependentes:")
print(df_dados_completos)

#4. Listar a média de idade dos filhos dos funcionários por departamento. 

query_idade_media_filhos = """
SELECT Departamentos.Nome_departamento, AVG(Dependentes.Idade) AS Media_Idade_Filhos
FROM Funcionarios
JOIN Dependentes ON Funcionarios.Id = Dependentes.Funcionario_id
JOIN Departamentos ON Funcionarios.Departamento_id = Departamentos.Id
WHERE Dependentes.Relacao IN ('Filho', 'Filha')
GROUP BY Departamentos.Nome_departamento;
"""
df_idade_media_filhos = pd.read_sql(query_idade_media_filhos, conn)
print("Média de idade dos filhos por departamento:")
print(df_idade_media_filhos)

#6. Listar o funcionário que teve o salário médio mais alto. 

query_maior_salario_medio = """
SELECT Funcionarios.Nome, AVG(Historico_de_salarios.Salario) AS salario_medio
FROM Funcionarios
JOIN Historico_de_salarios ON Funcionarios.Id = Historico_de_salarios.Funcionario_id
GROUP BY Funcionarios.Nome
ORDER BY salario_medio DESC
LIMIT 1
"""
df_maior_salario_medio = pd.read_sql_query(query_maior_salario_medio, conn)
print('Maior salário médio:')
print(df_maior_salario_medio)

#10. Listar a média de salário por departamento em ordem decrescente.

query_media_salario_dp = """
SELECT Departamentos.Nome_departamento, AVG(Historico_de_salarios.Salario) AS salario_medio_dp
FROM Funcionarios
JOIN Historico_de_salarios ON Funcionarios.Id = Historico_de_salarios.Funcionario_id
JOIN Departamentos ON Funcionarios.Departamento_id = Departamentos.Id
GROUP BY Departamentos.Nome_departamento
ORDER BY salario_medio_dp ASC
"""
df_salario_medio_dp = pd.read_sql_query(query_media_salario_dp, conn)
print("Média de salários por departamento:")
print(df_salario_medio_dp)

conn.close()