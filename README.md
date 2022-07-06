# Project 01 -DS
## Houses in Houses DS
![housesinhouses](https://user-images.githubusercontent.com/102738744/177536819-c9f8e595-a509-4940-8d67-0a49ddb7393c.png)
### 1 - O que buscamos?
Encontrar as melhores oportunidades de compra de imóveis do portfólio 
da House Rocket.

Visando ajudar o CEO em suas decisões de compra e venda dos imóveis dispostos neste portfólio, criamos algumas ferramentas para aprimorar sua tomada de decisões.

### 2 - Os dados:
Os dados foram obtidos do arquivo kc_house_data.csv.
Foram selecionados os imóveis que tiveram uma valorização menor ou igual a 100%, que representa 67,93% do Data Frame.

### 3 - A solução:
Após separarmos os dados, temos dez hipóteses para confirmar, destas 10 vamos separar as cinco principais logo abaixo.
Em seguida comparamos os Zipcodes mais e menos valorizados.
Entre os mais valorizados, separamos os imóveis que estão abaixo do valor da mediana do m² e estão com a condição de conservação maior ou igual a 3, estes imóveis estão recomendados para a compra.
Entre os menos valorizados, definimos alguns imóveis para venda imediata, os quais tiveram uma desvalorização de quase 90% nos últimos anos.
E por fim, dentre os imóveis recomendados para compra, também com base na mediana, informamos o valor do acréscimo possível para venda, 10 ou 30%.
10% para imóveis com valor superior ao valor da mediana;
30% para imóveis com valor inferior ao valor da mediana.

### 4 - Os 3 principais insights dos dados:
    
- O Zipcode que está com tendência de alta é o 98039, e os imóveis com maior potencial de ganho foram baseados na vista e nas boas condições do imóvel.
![mapa1](https://user-images.githubusercontent.com/102738744/177536937-e49fe5ae-e1ee-428d-96d4-26a764aef67c.jpg)

- Enquanto que o Zipcode 98168 teve perdas anuais de quase 100%.
![mapa2](https://user-images.githubusercontent.com/102738744/177536959-8c62cbf1-1cbf-4831-a313-5dfa00813b74.jpg)

- Entre os imóveis com Zipcode de maior valorização, foram separados 10 imóveis com chances de ter um preço menor que a média ter vista e estar em bom estado de conservação, o que traria um bom retorno financeiro.

### 5 - Resultados financeiros para o negócio:
Com base em uma tabela com recomendação de compra, separamos entre os imóveis recomendados para compra, e com base em sua mediana sugerimos 10% ou 30% de acréscimo em sua venda.
Com isso a empresa teria de 10% a 30% de aumento em seu faturamento.

### 6 - Conclusão:
No Data Frame fornecido, existem imóveis com potencial de gerar um aumento de faturamento entre 10 a 30% para esta empresa.

### 7 - Próximos passos
Estes foram os primeiros insights neste Data Frame, teríamos que aprimorar nossos códigos e mapas, bem como adicionar alguns gráficos para melhor visualização e consequentemente melhor tomada de decisão.

