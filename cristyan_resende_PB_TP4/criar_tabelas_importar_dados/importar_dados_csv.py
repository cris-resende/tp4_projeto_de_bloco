import sqlite3
import pandas as pd

conn = sqlite3.connect('banco_para_tp.db')


df_funcionarios = pd.read_csv('csv/funcionarios.csv')
df_funcionarios.drop_duplicates(inplace=True)
ids_existentes = pd.read_sql_query("SELECT Id FROM Funcionarios", conn)['Id'].tolist()
df_funcionarios_novos = df_funcionarios[~df_funcionarios['Id'].isin(ids_existentes)]
if not df_funcionarios_novos.empty:
    df_funcionarios_novos.to_sql('Funcionarios', conn, if_exists='append', index=False)
    print(f"Novos registros de Funcionários inseridos: {len(df_funcionarios_novos)}")
else:
    print("Nenhum registro novo encontrado para a tabela Funcionários.")


df_departamentos = pd.read_csv('csv/departamentos.csv')
df_departamentos.drop_duplicates(inplace=True)
ids_departamentos_existentes = pd.read_sql_query("SELECT Id FROM Departamentos", conn)['Id'].tolist()
df_departamentos_novos = df_departamentos[~df_departamentos['Id'].isin(ids_departamentos_existentes)]
if not df_departamentos_novos.empty:
    df_departamentos_novos.to_sql('Departamentos', conn, if_exists='append', index=False)
    print(f"Novos registros de Departamentos inseridos: {len(df_departamentos_novos)}")
else:
    print("Nenhum registro novo encontrado para a tabela Departamentos.")


df_dependentes = pd.read_csv('csv/dependentes.csv')
df_dependentes.drop_duplicates(inplace=True)
ids_dependentes_existentes = pd.read_sql_query("SELECT Id FROM Dependentes", conn)['Id'].tolist()
df_dependentes_novos = df_dependentes[~df_dependentes['Id'].isin(ids_dependentes_existentes)]
if not df_dependentes_novos.empty:
    df_dependentes_novos.to_sql('Dependentes', conn, if_exists='append', index=False)
    print(f"Novos registros de Dependentes inseridos: {len(df_dependentes_novos)}")
else:
    print("Nenhum registro novo encontrado para a tabela Dependentes.")


df_cargos = pd.read_csv('csv/cargos.csv')
df_cargos.drop_duplicates(inplace=True)
ids_cargos_existentes = pd.read_sql_query("SELECT Id FROM Cargos", conn)['Id'].tolist()
df_cargos_novos = df_cargos[~df_cargos['Id'].isin(ids_cargos_existentes)]
if not df_cargos_novos.empty:
    df_cargos_novos.to_sql('Cargos', conn, if_exists='append', index=False)
    print(f"Novos registros de Cargos inseridos: {len(df_cargos_novos)}")
else:
    print("Nenhum registro novo encontrado para a tabela Cargos.")


df_historico_salarios = pd.read_csv('csv/historicos_salarios.csv')
df_historico_salarios.drop_duplicates(inplace=True)
ids_historico_existentes = pd.read_sql_query("SELECT Id FROM Historico_de_salarios", conn)['Id'].tolist()
df_historico_novos = df_historico_salarios[~df_historico_salarios['Id'].isin(ids_historico_existentes)]
if not df_historico_novos.empty:
    df_historico_novos.to_sql('Historico_de_salarios', conn, if_exists='append', index=False)
    print(f"Novos registros de Histórico de Salários inseridos: {len(df_historico_novos)}")
else:
    print("Nenhum registro novo encontrado para a tabela Histórico de Salários.")


df_projetos_desenvolvidos = pd.read_csv('csv/projetos_desenvolvidos.csv')
df_projetos_desenvolvidos.drop_duplicates(inplace=True)
df_projetos_desenvolvidos.to_sql('Projetos_desenvolvidos', conn, if_exists='append', index=False)
print("Dados de Projetos Desenvolvidos inseridos com sucesso!")


df_recursos_do_projeto = pd.read_csv('csv/recursos_projetos.csv')
df_recursos_do_projeto.drop_duplicates(inplace=True)
df_recursos_do_projeto.to_sql('Recursos_do_projeto', conn, if_exists='append', index=False)
print("Dados de Recursos do Projeto inseridos com sucesso!")


conn.commit()
conn.close()