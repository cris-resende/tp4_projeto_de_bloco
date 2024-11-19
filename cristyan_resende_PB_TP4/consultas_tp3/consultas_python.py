import pandas as pd
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('banco_para_tp.db')

#3. Listar os funcionários que tiveram aumento salarial nos últimos 3 meses. 

df_historico = pd.read_sql_query("SELECT * FROM Historico_de_salarios", conn)
df_historico['Mes'] = pd.to_datetime(df_historico['Mes'])
ultimo_mes = df_historico['Mes'].max()
meses_atras = ultimo_mes - timedelta(days=90)
df_ultimos_3_meses = df_historico[df_historico['Mes'].between(meses_atras, ultimo_mes)]
resultados = []
for funcionario_id, grupo in df_ultimos_3_meses.groupby('Funcionario_id'):
    salario_inicial = grupo['Salario'].min()
    salario_final = grupo['Salario'].max()
    if salario_final > salario_inicial:
        nome_funcionario = pd.read_sql_query(f"SELECT Nome FROM Funcionarios WHERE Id = {funcionario_id}", conn).iloc[0]['Nome']
        resultados.append({
            'Nome': nome_funcionario,
            'Salario_Inicial': salario_inicial,
            'Salario_Final': salario_final
        })

df_resultados = pd.DataFrame(resultados)
print("Funcionários com aumento salarial nos últimos 3 meses:")
print(df_resultados)

#5. Listar qual estagiário possui filho. 

df_funcionarios = pd.read_sql_query("SELECT * FROM Funcionarios", conn)
df_cargos = pd.read_sql_query("SELECT * FROM Cargos", conn)
df_dependentes = pd.read_sql_query("SELECT * FROM Dependentes", conn)
df_estagiarios = df_funcionarios[df_funcionarios['Cargo_id'].isin(
    df_cargos[df_cargos['Nome_cargo'] == 'Estagiário']['Id']
)]
df_estagiarios_com_filhos = pd.merge(df_estagiarios, df_dependentes, left_on='Id', right_on='Funcionario_id')
df_estagiarios_com_filhos = df_estagiarios_com_filhos[df_estagiarios_com_filhos['Relacao'].isin(['Filho', 'Filha'])]
resultados = df_estagiarios_com_filhos[['Nome', 'Nome_dependente']]
resultados.columns = ['Nome_Estagiario', 'Nome_Filho']
print("Estagiários com filhos:")
print(resultados)

#7. Listar o analista que é pai de 2 (duas) meninas. 

df_funcionarios = pd.read_sql_query("SELECT * FROM Funcionarios", conn)
df_dependentes = pd.read_sql_query("SELECT * FROM Dependentes", conn)
df_cargos = pd.read_sql_query("SELECT * FROM Cargos", conn)
df_analistas = pd.merge(df_funcionarios, df_cargos, left_on='Cargo_id', right_on='Id')
df_analistas_dependentes = pd.merge(df_analistas, df_dependentes, left_on='Id_x', right_on='Funcionario_id')
df_analistas = df_analistas_dependentes[df_analistas_dependentes['Nome_cargo'] == 'Analista']
df_analistas_filhas = df_analistas[df_analistas['Relacao'] == 'Filha']
df_analistas_filhas_contagem = df_analistas_filhas.groupby('Nome').size().reset_index(name='qtd_filhas')
df_analistas_duas_filhas = df_analistas_filhas_contagem[df_analistas_filhas_contagem['qtd_filhas'] == 2]
if df_analistas_duas_filhas.empty:
    print("Nenhum dos analistas possui exatamente 2 filhas.")
else:
    print("Analistas que têm exatamente 2 filhas:")
    print(df_analistas_duas_filhas)

#8. Listar o analista que tem o salário mais alto, e que ganhe entre 5000 e 9000. 

df_funcionarios = pd.read_sql_query("SELECT * FROM Funcionarios", conn)
df_cargos = pd.read_sql_query("SELECT * FROM Cargos", conn)
df_historico_salarios = pd.read_sql_query("SELECT * FROM Historico_de_salarios", conn)
df_analistas = df_funcionarios[df_funcionarios['Cargo_id'].isin(df_cargos[df_cargos['Nome_cargo'] == 'Analista']['Id'])]
df_salarios_analistas = pd.merge(df_analistas[['Id', 'Nome']], df_historico_salarios, left_on='Id', right_on='Funcionario_id', how='inner')
df_salarios_analistas = df_salarios_analistas[(df_salarios_analistas['Salario'] >= 5000) & (df_salarios_analistas['Salario'] <= 9000)]
if not df_salarios_analistas.empty:
    df_maior_salario_analista = df_salarios_analistas.loc[df_salarios_analistas['Salario'].idxmax()]
    print("Analista com o maior salário entre 5000 e 9000:")
    print(f"Nome: {df_maior_salario_analista['Nome']}, Salário: {df_maior_salario_analista['Salario']}")
else:
    print("Nenhum analista possui salário entre 5000 e 9000.")

#9. Listar qual departamento possui o maior número de dependentes. 

df_funcionarios = pd.read_sql_query("SELECT * FROM Funcionarios", conn)
df_dependentes = pd.read_sql_query("SELECT * FROM Dependentes", conn)
df_combined = pd.merge(df_dependentes, df_funcionarios, left_on='Funcionario_id', right_on='Id')
df_count_dependents = df_combined.groupby('Departamento_id').size().reset_index(name='qtd_dependentes')
df_departamentos = pd.read_sql_query("SELECT * FROM Departamentos", conn)
df_final = pd.merge(df_count_dependents, df_departamentos, left_on='Departamento_id', right_on='Id')
departamento_maior_dependentes = df_final.loc[df_final['qtd_dependentes'].idxmax()]
print("Departamento com o maior número de dependentes:")
print(departamento_maior_dependentes[['Nome_departamento', 'qtd_dependentes']])

conn.close()