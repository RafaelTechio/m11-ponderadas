# Ponderada Semana 6 - Matemática
> Rafael Techio

### **Modelagem**
Em um sistema de e-commerce:  


![image](https://github.com/user-attachments/assets/09168480-28a8-429e-ad31-4be0481739df)

- Cada **usuário** pode realizar múltiplos **pedidos** (relação 1:N).  
- Cada **pedido** pode conter múltiplos **produtos**, e cada **produto** pode estar presente em diversos **pedidos** (relação N:N), modelada pela tabela intermediária `order_item`.  

Dessa forma, as seguintes tabelas são criadas:

1. **Usuário (`user`)**  
   - `id`: Identificador único do usuário (PK)  
   - `name`: Nome do usuário (VARCHAR)
   - `gender`: Gênero do usuário (VARCHAR)
   - `email`: Email do usuário (VARCHAR)  
   - `birth_date`: Data de nascimento (TIMESTAMP)  

2. **Pedido (`order`)**  
   - `id`: Identificador único do pedido (PK)  
   - `user_id`: Usuário que fez o pedido (FK referenciando `user.id`)  
   - `total_price`: Valor total do pedido (NUMERIC)
   - `created_at`: Data de criação do pedido (TIMESTAMP)  

3. **Produto (`product`)**  
   - `id`: Identificador único do produto (PK)  
   - `name`: Nome do produto (VARCHAR)  
   - `category`: Categoria do produto (VARCHAR)  
   - `description`: Descrição do produto (TEXT)  
   - `price`: Preço do produto (NUMERIC)  

4. **Itens do Pedido (`order_item`)**  
   - `order_id`: Pedido ao qual o item pertence (FK referenciando `order.id`)  
   - `product_id`: Produto adicionado ao pedido (FK referenciando `product.id`)
   - `total_price`: Valor total (preço x quantidade) (NUMERIC)    
   - `product_price`: Preço unitário do produto no momento da compra (NUMERIC)  
   - `product_quantity`: Quantidade do produto no pedido (INTEGER)  
   - `created_at`: Data de adição do item ao pedido (TIMESTAMP)  

---

## **Consulta SQL**
A consulta exibe:  
- Todos os usuários e os pedidos que eles fizeram (LEFT JOIN)  
- Usuários que nunca fizeram pedidos (LEFT JOIN)  
- Produtos que nunca foram comprados (RIGHT JOIN)  

```sql
SELECT 
    u.name AS "Nome do Usuário", 
    o.id AS "ID do Pedido", 
    p.name AS "Nome do Produto", 
    oi.product_quantity AS "Quantidade", 
    o.total_price AS "Preço Total"
FROM user u
LEFT JOIN "order" o ON u.id = o.user_id
LEFT JOIN order_item oi ON o.id = oi.order_id
RIGHT JOIN product p ON oi.product_id = p.id;
```

---

## **Equação da Álgebra Relacional**
$$
π_{u.name, o.id, p.name, oi.product\_quantity, o.total\_price} \Big( (user ⟕_{u.id=o.user\_id} order) ⟕_{o.id=oi.order\_id} order\_item ⟖_{oi.product\_id=p.id} product \Big)
$$
