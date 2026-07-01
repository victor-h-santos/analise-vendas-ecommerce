import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["font.family"] = "DejaVu Sans"
CORES = ["#2E5EAA", "#4C9F70", "#E8871E", "#C13B3B", "#8E5FA3", "#3B9C9C"]

BASE = "/home/claude/portfolio_ecommerce"

# 1. Receita por mês (linha)
receita_mes = pd.read_csv(f"{BASE}/data/receita_por_mes.csv")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(receita_mes["ano_mes"], receita_mes["receita_total"], marker="o", color=CORES[0], linewidth=2)
ax.set_title("Receita Mensal - 2025", fontsize=13, fontweight="bold")
ax.set_ylabel("Receita (R$)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x/1000:.0f}k"))
plt.xticks(rotation=45)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{BASE}/charts/receita_mensal.png", dpi=130)
plt.close()

# 2. Top produtos (barra horizontal)
top_produtos = pd.read_csv(f"{BASE}/data/top_produtos.csv").sort_values("receita_total")
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top_produtos["produto"], top_produtos["receita_total"], color=CORES[1])
ax.set_title("Top 10 Produtos por Receita", fontsize=13, fontweight="bold")
ax.set_xlabel("Receita (R$)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{BASE}/charts/top_produtos.png", dpi=130)
plt.close()

# 3. Receita por categoria (pizza/donut)
receita_cat = pd.read_csv(f"{BASE}/data/receita_por_categoria.csv")
fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    receita_cat["receita_total"], labels=receita_cat["categoria"],
    autopct="%1.1f%%", colors=CORES, startangle=90,
    wedgeprops=dict(width=0.4)
)
ax.set_title("Participação de Receita por Categoria", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{BASE}/charts/receita_categoria.png", dpi=130)
plt.close()

# 4. Canal de aquisição (barra)
canal = pd.read_csv(f"{BASE}/data/canal_aquisicao_performance.csv").sort_values("receita_total")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(canal["canal_aquisicao"], canal["receita_total"], color=CORES[2])
ax.set_title("Receita por Canal de Aquisição", fontsize=13, fontweight="bold")
ax.set_xlabel("Receita (R$)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{BASE}/charts/canal_aquisicao.png", dpi=130)
plt.close()

# 5. Status dos pedidos (barra)
status = pd.read_csv(f"{BASE}/data/taxa_cancelamento_devolucao.csv")
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(status["status_pedido"], status["percentual"], color=CORES[:4])
ax.set_title("Distribuição de Status dos Pedidos (%)", fontsize=13, fontweight="bold")
ax.set_ylabel("% do total")
for bar in bars:
    height = bar.get_height()
    ax.annotate(f"{height:.1f}%", xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(f"{BASE}/charts/status_pedidos.png", dpi=130)
plt.close()

print("5 gráficos gerados em charts/")
