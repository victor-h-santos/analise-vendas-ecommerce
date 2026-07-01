"""
Gera um dataset sintético de vendas de e-commerce com problemas reais
de qualidade de dados (nulos, duplicados, formatos inconsistentes),
simulando o tipo de base "suja" que aparece em projetos reais.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 5000

categorias = ["Eletrônicos", "Moda", "Casa e Decoração", "Beleza", "Esporte", "Livros"]
produtos_por_categoria = {
    "Eletrônicos": ["Fone Bluetooth", "Carregador USB-C", "Smartwatch", "Caixa de Som", "Mouse Gamer"],
    "Moda": ["Camiseta Básica", "Jaqueta Jeans", "Tênis Casual", "Bermuda", "Boné"],
    "Casa e Decoração": ["Luminária LED", "Jogo de Panelas", "Almofada", "Vaso Decorativo", "Tapete"],
    "Beleza": ["Kit Skincare", "Perfume", "Secador de Cabelo", "Base Líquida", "Protetor Solar"],
    "Esporte": ["Tênis de Corrida", "Garrafa Térmica", "Kit Halteres", "Bicicleta Ergométrica", "Colchonete Yoga"],
    "Livros": ["Romance Best-seller", "Livro de Autoajuda", "Quadrinhos", "Livro Técnico", "Biografia"],
}

estados = ["SP", "RJ", "MG", "BA", "PR", "RS", "PE", "CE", "SC", "GO", "DF", "AM", "PA"]
canais = ["Instagram Ads", "Google Ads", "Orgânico", "Indicação", "E-mail Marketing", None]  # None = não rastreado

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    categoria = np.random.choice(categorias)
    produto = np.random.choice(produtos_por_categoria[categoria])
    preco_base = {
        "Eletrônicos": 150, "Moda": 90, "Casa e Decoração": 80,
        "Beleza": 60, "Esporte": 120, "Livros": 45,
    }[categoria]
    preco = round(np.random.normal(preco_base, preco_base * 0.3), 2)
    preco = max(preco, 10)

    qtd = np.random.choice([1, 1, 1, 2, 2, 3, 5], p=[0.4, 0.15, 0.15, 0.15, 0.05, 0.05, 0.05])
    data_pedido = start_date + timedelta(days=int(np.random.exponential(scale=date_range_days/2.2)) % date_range_days)

    # formatos de data inconsistentes de propósito (problema real comum)
    if np.random.random() < 0.15:
        data_str = data_pedido.strftime("%d/%m/%Y")
    elif np.random.random() < 0.3:
        data_str = data_pedido.strftime("%Y-%m-%d")
    else:
        data_str = data_pedido.strftime("%d-%m-%Y")

    estado = np.random.choice(estados)
    canal = np.random.choice(canais, p=[0.25, 0.2, 0.25, 0.1, 0.1, 0.1])

    # nome de cliente com inconsistência de capitalização (sujeira proposital)
    cliente_id = f"CLI{np.random.randint(1000, 3000)}"

    status = np.random.choice(
        ["Entregue", "entregue", "ENTREGUE", "Cancelado", "Em transporte", "Devolvido"],
        p=[0.55, 0.1, 0.05, 0.08, 0.15, 0.07]
    )

    avaliacao = np.random.choice([1, 2, 3, 4, 5, np.nan], p=[0.03, 0.05, 0.12, 0.3, 0.35, 0.15])

    rows.append({
        "pedido_id": f"PED{100000+i}",
        "cliente_id": cliente_id,
        "categoria": categoria,
        "produto": produto,
        "preco_unitario": preco,
        "quantidade": qtd,
        "data_pedido": data_str,
        "estado": estado,
        "canal_aquisicao": canal,
        "status_pedido": status,
        "avaliacao": avaliacao,
    })

df = pd.DataFrame(rows)

# injeta duplicados de propósito (problema real comum)
dup_idx = np.random.choice(df.index, size=120, replace=False)
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# injeta alguns preços nulos e negativos por erro de digitação (problema real)
null_idx = np.random.choice(df.index, size=60, replace=False)
df.loc[null_idx, "preco_unitario"] = np.nan

neg_idx = np.random.choice(df.index, size=15, replace=False)
df.loc[neg_idx, "preco_unitario"] = -df.loc[neg_idx, "preco_unitario"].abs()

# espaços em branco extras em algumas colunas de texto (sujeira comum de import)
space_idx = np.random.choice(df.index, size=200, replace=False)
df.loc[space_idx, "produto"] = df.loc[space_idx, "produto"] + "  "

df = df.sample(frac=1, random_state=1).reset_index(drop=True)
df.to_csv("/home/claude/portfolio_ecommerce/data/vendas_raw.csv", index=False)
print(f"Dataset gerado: {len(df)} linhas")
print(df.head())
