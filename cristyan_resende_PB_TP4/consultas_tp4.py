import sqlite3
import pandas as pd

conn = sqlite3.connect('banco_para_tp.db')

# Consulta 1: Média dos salários dos funcionários responsáveis por projetos concluídos, agrupados por departamento
consulta1 = '''
SELECT 
    d.Nome_departamento AS Departamento,
    AVG(c.Salario_base) AS Media_Salarial
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_responsavel = f.Id
JOIN Departamentos d ON f.Departamento_id = d.Id
JOIN Cargos c ON f.Cargo_id = c.Id
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_departamento
'''
resultado1 = pd.read_sql_query(consulta1, conn)
print("Consulta 1: Média dos salários por departamento:\n", resultado1)
resultado1.to_json('jsons_para_looker/consulta1.json', orient='records', indent=4)
print("O arquivo json da consulta 1 foi criado com sucesso!")
print("-"*85)

# Consulta 2: Três recursos materiais mais usados nos projetos
consulta2 = '''
SELECT 
    Descricao AS Recurso,
    SUM(Quantidade) AS Total_Usado
FROM Recursos_do_projeto
GROUP BY Descricao
ORDER BY Total_Usado DESC
LIMIT 3
'''
resultado2 = pd.read_sql_query(consulta2, conn)
print("Consulta 2: Três recursos materiais mais usados:\n", resultado2)
resultado2.to_json('jsons_para_looker/consulta2.json', orient='records', indent=4)
print("O arquivo json da consulta 2 foi criado com sucesso!")
print("-"*85)

# Consulta 3: Custo total dos projetos por departamento (apenas os 'Concluídos')
consulta3 = '''
SELECT 
    d.Nome_departamento AS Departamento,
    SUM(p.Custo_projeto) AS Custo_Total
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_responsavel = f.Id
JOIN Departamentos d ON f.Departamento_id = d.Id
WHERE p.Status = 'Concluído'
GROUP BY d.Nome_departamento
'''
resultado3 = pd.read_sql_query(consulta3, conn)
print("Consulta 3: Custo total dos projetos por departamento:\n", resultado3)
resultado3.to_json('jsons_para_looker/consulta3.json', orient='records', indent=4)
print("O arquivo json da consulta 3 foi criado com sucesso!")
print("-"*85)

# Consulta 4: Projetos em execução com detalhes
consulta4 = '''
SELECT 
    p.Nome_projeto AS Projeto,
    p.Custo_projeto AS Custo,
    p.Data_inicio AS Data_Inicio,
    p.Data_conclusao AS Data_Conclusao,
    f.Nome AS Responsavel
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_responsavel = f.Id
WHERE p.Status = 'Em Execução'
'''
resultado4 = pd.read_sql_query(consulta4, conn)
print("Consulta 4: Projetos em execução:\n", resultado4)
print("-"*85)

# Consulta 5: Projeto com o maior número de dependentes
consulta5 = '''
SELECT 
    p.Nome_projeto AS Projeto,
    COUNT(d.Id) AS Total_Dependentes
FROM Projetos_Desenvolvidos p
JOIN Funcionarios f ON p.Funcionario_responsavel = f.Id
JOIN Dependentes d ON f.Id = d.Funcionario_id
GROUP BY p.Nome_projeto
ORDER BY Total_Dependentes DESC
LIMIT 1
'''
resultado5 = pd.read_sql_query(consulta5, conn)
print("Consulta 5: Projeto com o maior número de dependentes:\n", resultado5)
print("-"*85)

conn.close()
