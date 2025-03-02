# Atividade Ponderada - Matemática | Semana 4
> Rafael Techio

## Atividade:

> Problema de Modelagem de Dados com Relações 1:N e N:N:
> 
> Proposta de Problema de Modelagem de Dados:
> 
> Crie um cenário de modelagem de dados que inclua pelo menos uma relação 1:N (um-para-muitos) e uma relação N:N (muitos-para-muitos). Por exemplo:
> 
> Relação 1:N: "Mecânicos e os carros que eles consertam em uma oficina".
> 
> Relação N:N: "Peças utilizadas nos carros".
> 
> As entidades envolvidas devem ter mais de um atributo não-chave. Pelo menos um desses atributos deve ser de valor contínuo, como o "preço da peça".
>
> 
> Consulta Envolvendo as Entidades:
> 
> Proponha uma consulta SQL que envolva as três entidades (ou mais) e que filtre elementos com base em critérios específicos nas relações 1:N e N:N. Por exemplo, uma consulta pode ser: "Liste quantas peças os mecânicos de nível "Júnior" consertaram em carros da categoria "Compacto", onde o preço das peças estava entre 100 e 200".

> Exemplo de consulta SQL:
> 
> Obs.: As aspas duplas devem ser substituídas por aspas simples

```
SELECT COUNT(c.ID), a.Nome
FROM Mecanicos a
JOIN Carros b ON a.ID = b.MecanicoID
JOIN Pecas c ON b.ID = c.CarroID
WHERE a.Nivel = "Júnior"
AND b.Categoria = "Compacto"
AND c.Preco BETWEEN 100 AND 200
GROUP BY a.Nome;
```

> Mostre a conversão desta consulta em SQL uma equação usando álgebra relacional.
> Por exemplo: π NOME (σ c.preco > 500 (A â¨Â (B â¨Â C)))
> Como um desafio além, faça a organização desta equação da forma mais eficiente possível.


## Resposta

### Modelagem:

A modelagem do exercício representa as relações de um e-commerce contendo:

- Uma tabela para usuários do sistema
- Uma tabela para produtos a serem vendidos
- Uma tabela de pedido (order) que representa as compras dos usuários
  - Uma tabela de relacionamento pedido-produto (order_item) que permite que um pedido agregue a compra de vários produtos diferentes

Dessa forma, um diagrama DER ou pé de galinha foi criado para representar as entidades do sistema:

![image](https://github.com/user-attachments/assets/b4c99486-1139-4f75-95fd-b8fc4977e0f4)

### Consulta SQL e Equação

Já a consulta SQL realizada para resgatar os dados do sistema possui o objetivo:

> Obter nome, email, categoria de produto e ticket médio da categoria de produto das compras que tiveram valor total acima de R$ 100 feitas por usuários do sexo feminino.

Resultando no SQL:

```sql
SELECT user.name, user.email, product.category, AVG(order_item.total_price) as ticket_medio
FROM user
  JOIN order ON user.id = order.user_id
  JOIN order_item ON order.id = order_item.order_id
  JOIN product ON order_item.product_id = product.id
WHERE user.gender = 'F'
  AND product.category = 'Eletrônicos'
  AND order.total_price > 100
GROUP BY user.id, product.category;
```

A escrita da equação da consulta pode ser feita dessa forma

$$
\pi_{user.name, user.email, product.category, \text{AVG}(order\_item.total\_price)}
\left( \sigma_{user.gender = 'F' \land product.category = 'Eletrônicos' \land order.total\_price > 100} 
(user \bowtie order \bowtie order\_item \bowtie product) \right)
$$

### Otimização

Um dos tipos de otimização mais comuns é a filtragens dos dados desnecessários em uma query, garantindo que tudo aquilo que não for importante, seja descartado dos cálculos. Nesse sentido, iremos trocar os joins por inner joins, garantindo que apenas casos que atendem a todos os critérios de filtragem sejam resgatados:

```sql
SELECT user.name, user.email, product.category, AVG(order_item.total_price) as ticket_medio
FROM user
  INNER JOIN order ON user.id = order.user_id
  INNER JOIN order_item ON order.id = order_item.order_id
  INNER JOIN product ON order_item.product_id = product.id
WHERE user.gender = 'F'
  AND product.category = 'Eletrônicos'
  AND order.total_price > 100
GROUP BY user.id, product.category;
```

Dessa maneira, a equação ficará assim:

$$
\pi_{user.name, user.email, product.category, \text{AVG}(order\_item.total\_price)}
\left( \sigma_{user.gender = 'F' \land product.category = 'Eletrônicos' \land order.total\_price > 100} 
(user \bowtie_{user.id = order.user_id} order \bowtie_{order.id = order_item.order_id} order\_item \bowtie_{order_item.product_id = product.id} product) \right)
$$

