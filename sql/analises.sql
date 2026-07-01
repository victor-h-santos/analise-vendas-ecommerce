-- Receita Por Mes
SELECT
            ano_mes,
            ROUND(SUM(receita), 2) AS receita_total,
            COUNT(DISTINCT pedido_id) AS total_pedidos,
            ROUND(SUM(receita) / COUNT(DISTINCT pedido_id), 2) AS ticket_medio
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY ano_mes
        ORDER BY ano_mes;

-- Top Produtos
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

-- Receita Por Categoria
SELECT
            categoria,
            ROUND(SUM(receita), 2) AS receita_total,
            ROUND(AVG(receita), 2) AS receita_media_pedido,
            COUNT(*) AS total_pedidos
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY categoria
        ORDER BY receita_total DESC;

-- Receita Por Estado
SELECT
            estado,
            ROUND(SUM(receita), 2) AS receita_total,
            COUNT(*) AS total_pedidos
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY estado
        ORDER BY receita_total DESC;

-- Canal Aquisicao Performance
SELECT
            canal_aquisicao,
            COUNT(*) AS total_pedidos,
            ROUND(SUM(receita), 2) AS receita_total,
            ROUND(AVG(avaliacao), 2) AS avaliacao_media
        FROM vendas
        WHERE pedido_valido = 1
        GROUP BY canal_aquisicao
        ORDER BY receita_total DESC;

-- Taxa Cancelamento Devolucao
SELECT
            status_pedido,
            COUNT(*) AS total,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM vendas), 2) AS percentual
        FROM vendas
        GROUP BY status_pedido
        ORDER BY total DESC;

