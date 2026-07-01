"""
Carrega a base limpa em SQLite e executa as queries de análise.
Salva os resultados como CSV (para usar no Power BI) e imprime no console.
"""
import sqlite3
import pandas as pd

df = pd.read_csv("/home/claude/portfolio_ecommerce/data/vendas_limpo.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("vendas", conn, index=False, if_exists="replace")

queries = {
    "receita_por_mes": """
        SELECT
            ano_mes,
            ROUND(SUM(receita), 2) AS receita_total,
            COUNT(DISTINCT pedido_id) AS total_pedidos,
            ROUND(SUM(receita) / COUNT(DISTINCT pedido_id), 2) AS ticket_medio
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY ano_mes
        ORDER BY ano_mes;
    """,
    "top_produtos": """
        SELECT
            produto,
            categoria,
            COUNT(*) AS total_vendas,
            ROUND(SUM(receita), 2) AS receita_total
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY produto, categoria
        ORDER BY receita_total DESC
        LIMIT 10;
    """,
    "receita_por_categoria": """
        SELECT
            categoria,
            ROUND(SUM(receita), 2) AS receita_total,
            ROUND(AVG(receita), 2) AS receita_media_pedido,
            COUNT(*) AS total_pedidos
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY categoria
        ORDER BY receita_total DESC;
    """,
    "receita_por_estado": """
        SELECT
            estado,
            ROUND(SUM(receita), 2) AS receita_total,
            COUNT(*) AS total_pedidos
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY estado
        ORDER BY receita_total DESC;
    """,
    "canal_aquisicao_performance": """
        SELECT
            canal_aquisicao,
            COUNT(*) AS total_pedidos,
            ROUND(SUM(receita), 2) AS receita_total,
            ROUND(AVG(avaliacao), 2) AS avaliacao_media
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY canal_aquisicao
        ORDER BY receita_total DESC;
    """,
    "taxa_cancelamento_devolucao": """
        SELECT
            status_pedido,
            COUNT(*) AS total,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM vendas), 2) AS percentual
        FROM vendas
        GROUP BY status_pedido
        ORDER BY total DESC;
    """,
}

for nome, query in queries.items():
    resultado = pd.read_sql_query(query, conn)
    print(f"\n{'=' * 60}\n{nome.upper()}\n{'=' * 60}")
    print(resultado.to_string(index=False))
    resultado.to_csv(f"/home/claude/portfolio_ecommerce/data/{nome}.csv", index=False)

# salva o arquivo .sql com as queries formatadas, para colocar no GitHub
with open("/home/claude/portfolio_ecommerce/sql/analises.sql", "w") as f:
    for nome, query in queries.items():
        f.write(f"-- {nome.replace('_', ' ').title()}\n")
        f.write(query.strip() + "\n\n")

print("\nQueries salvas em sql/analises.sql")
print("Resultados salvos em data/*.csv")
