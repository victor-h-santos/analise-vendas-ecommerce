"""
Limpeza e tratamento da base bruta de vendas de e-commerce.

Problemas identificados e tratados:
1. Datas em 3 formatos diferentes -> padronizadas para datetime
2. Status do pedido com capitalização inconsistente -> padronizado
3. Espaços em branco extras em nomes de produto -> removidos (strip)
4. Preços nulos -> imputados pela mediana da categoria/produto
5. Preços negativos (erro de digitação) -> corrigidos para valor absoluto
6. Linhas duplicadas -> removidas
7. Canal de aquisição nulo -> categorizado como "Não rastreado"
8. Avaliação nula -> mantida como nula (não imputamos avaliação subjetiva)
9. Coluna calculada de receita (preco_unitario * quantidade) criada
"""
import pandas as pd
import numpy as np

df = pd.read_csv("/home/claude/portfolio_ecommerce/data/vendas_raw.csv")

print("=" * 60)
print("DIAGNÓSTICO INICIAL")
print("=" * 60)
print(f"Total de linhas: {len(df)}")
print(f"Linhas duplicadas: {df.duplicated().sum()}")
print(f"Valores nulos por coluna:\n{df.isnull().sum()}")
print(f"Preços negativos: {(df['preco_unitario'] < 0).sum()}")
print(f"Formatos de status únicos: {df['status_pedido'].unique()}")

# 1. Remove duplicados exatos
df = df.drop_duplicates()

# 2. Padroniza nomes de produto (remove espaços extras)
df["produto"] = df["produto"].str.strip()

# 3. Padroniza status do pedido
df["status_pedido"] = df["status_pedido"].str.strip().str.capitalize()

# 4. Padroniza datas (3 formatos diferentes na base bruta)
def parse_data(valor):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return pd.to_datetime(valor, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["data_pedido"] = df["data_pedido"].apply(parse_data)

# 5. Corrige preços negativos (erro de digitação -> valor absoluto)
df["preco_unitario"] = df["preco_unitario"].abs()

# 6. Imputa preços nulos pela mediana da categoria+produto
df["preco_unitario"] = df.groupby(["categoria", "produto"])["preco_unitario"].transform(
    lambda x: x.fillna(x.median())
)
# fallback: se ainda restar nulo (produto raro sem outras referências), usa mediana da categoria
df["preco_unitario"] = df.groupby("categoria")["preco_unitario"].transform(
    lambda x: x.fillna(x.median())
)

# 7. Canal de aquisição nulo -> categoria explícita
df["canal_aquisicao"] = df["canal_aquisicao"].fillna("Não rastreado")

# 8. Remove linhas sem data válida (não dá pra analisar sem isso)
antes = len(df)
df = df.dropna(subset=["data_pedido"])
print(f"\nLinhas removidas por data inválida: {antes - len(df)}")

# 9. Cria coluna de receita
df["receita"] = (df["preco_unitario"] * df["quantidade"]).round(2)

# 10. Colunas derivadas úteis para análise / Power BI
df["ano_mes"] = df["data_pedido"].dt.to_period("M").astype(str)
df["mes"] = df["data_pedido"].dt.month
df["dia_semana"] = df["data_pedido"].dt.day_name()
df["pedido_valido"] = ~df["status_pedido"].isin(["Cancelado", "Devolvido"])

print("\n" + "=" * 60)
print("RESULTADO APÓS LIMPEZA")
print("=" * 60)
print(f"Total de linhas: {len(df)}")
print(f"Valores nulos restantes:\n{df.isnull().sum()}")
print(f"Status únicos: {df['status_pedido'].unique()}")

df.to_csv("/home/claude/portfolio_ecommerce/data/vendas_limpo.csv", index=False)
print("\nArquivo limpo salvo em data/vendas_limpo.csv")
