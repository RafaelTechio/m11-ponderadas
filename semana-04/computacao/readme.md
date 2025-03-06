# Ponderada Semana 4 | Criação de Dashboard de Telemetria do Data Lake e Data Warehouse

- Yuri Toledo
- Rafael Techio
- Luiz Covas


## Resumo
Este relatório descreve o processo de criação de um dashboard de telemetria para monitoramento da utilização do Data Lake no Supabase Storage, com o uso de Prometheus e Grafana. O objetivo principal foi integrar as métricas de acesso e desempenho de armazenamento em uma interface visual clara e intuitiva, possibilitando a análise eficiente dos dados. As métricas escolhidas incluem o total de requisições, acessos aos buckets e a duração das requisições, fornecendo uma visão abrangente sobre a utilização do sistema.

## Desenvolvimento
O desenvolvimento envolveu três etapas principais: compreensão dos dados, seleção das métricas e integração com as ferramentas de monitoramento. Inicialmente, foram selecionados dados chave sobre o desempenho do armazenamento, como o número total de requisições, acessos aos buckets e tempo de resposta das operações. A partir dessas métricas, foram escolhidos os contadores e histogramas do Prometheus, como **app_requests_total**, **supabase_storage_access_total** e **supabase_storage_request_duration_seconds**, para fornecer uma visão precisa sobre a utilização e a performance do sistema. Em seguida, o Prometheus foi configurado para coletar as métricas expostas pela aplicação Python, com o Grafana sendo integrado para visualização em tempo real. As queries no Grafana foram otimizadas para garantir eficiência nas análises.

**API do Prometheus expondo métricas**:

![image](https://github.com/user-attachments/assets/51b4cb10-3844-40e5-a222-2646bb4552bd)

**Pacote docker**:

![image](https://github.com/user-attachments/assets/ee5f4430-c425-4e91-b479-33fdb64a38a6)


**Prometheus integrado**:

![image](https://github.com/user-attachments/assets/bf493a32-054c-48c9-b80b-c0d0df539284)


O dashboard foi desenvolvido com um design focado em usabilidade, com gráficos intuitivos e um layout organizado para facilitar a leitura dos dados. Foram utilizados gráficos de linha do tempo para monitoramento do número de requisições e acessos, histogramas para a análise do tempo de resposta e indicadores chave para monitoramento em tempo real. A paleta de cores foi padronizada para destacar as informações mais relevantes.


**Gráficos Grafana**:
![image](https://github.com/user-attachments/assets/0e494676-02cc-4f40-a42b-71f552086088)

## Conclusão
O dashboard criado oferece uma visão detalhada e clara sobre a utilização do Data Lake no Supabase Storage, atendendo aos objetivos de monitoramento e análise. A integração entre Prometheus, Grafana e Supabase Storage permitiu a coleta e visualização eficaz dos dados, possibilitando insights valiosos sobre o desempenho do sistema. A análise dos dados revelou padrões de acesso previsíveis e identificou possíveis gargalos em momentos específicos, fornecendo informações cruciais para a otimização contínua do sistema. O projeto resultou em uma ferramenta poderosa para a melhoria da performance e a tomada de decisões.
