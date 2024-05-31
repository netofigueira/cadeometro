import pandas as pd


metro = pd.read_csv("linhas_metro_google.csv")
cptm = pd.read_csv("linhas_cptm_google.csv")

df = pd.concat([metro, cptm])


df.estacao = df.estacao.str.lstrip("Estação")
df.estacao = df.estacao.str.title()
df.linha = df.linha.str.title()
df[['estacao','endereco','linha','linhaID','latitude','longitude'
]].to_csv("base_estacoes.csv")

