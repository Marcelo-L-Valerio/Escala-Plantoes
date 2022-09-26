# Criador de escala de médicos

## Marcelo Lopes Valerio - email: mar.valerio@hotmail.com.br

## Projeto pessoal - pedido especial de um familiar

### Tendo os médicos, seus dias disponíveis, e a quantidade de medicos necessaria por dia, gera a escala da semana/mês, priorizando a/as opções com menor desvio padrão dentre um numero pre estabelecido de iterações, levando em conta também se todos os plantões estão preenchidos

### O objetivo desse código, e o desafio que me impus para o mesmo, é o de não usar nenhum framework ou aplicação de banco de dados/requisições, pois o ideal é esse código rodar num PC privado, e baixando o menor numero de programas possível, neste caso me restringi tambem ao uso de bibliotecas, para não precisar criar um ambiente virtual nem nada, apenas baixar e rodar

### No arquivo main.py, existem 3 tipos de listas de médicos que podem ser utilizadas: uma interativa, que pedirá os dados de cada médico no terminal, uma aleatória, que gerará uma lista de acordo com os parâmetros pedidos, e uma lista padrão, utilizada para comparar resultados e melhorias para um caso especifico de 10 dias (5 finais de semana)

### A lógica do programa funciona da seguinte maneira: primeiro é preciso criar uma lista de objetos da classe médicos, utilizando as funções criadas para isso;

### Após isso, deve criar o turno (shift), dando como parâmetros o mês/semana/período, o número de dias do período (utilizar o mesmo que usou para criar a disponibilidade dos médicos), a própria lista de médicos, numero de médicos de dia, e número de médicos de noite (pode ser 0);

### Após chamar o método best_shift da classe shift, com o número de interações desejadas, a lista de médicos passa por uma série de filtros e classificações: no primeiro filtro, são colocados nas listas "available" apenas os médicos disponíveis na data;

### Então, essa lista é passada pelo método priorizador, que levará em consideração quantos dias o médico ainda tem disponível, quantos plantões o médico ja fez, e quantos plantões seria o ideal para que todos os médicos tivessem o mesmo numero de plantões

### No método seletor, o primeiro passo é embaralhar a lista de disponíveis, isso é feito para que qualquer vício do programa seja desfeito, e após 1000 iterações, a chance de ter achado o melhor plantão aumente, pois o seletor leva em conta apenas 2 fatores: se o médico tem um número de prioridade que é o máximo da lista, e ainda se ele não está fazendo dois plantões consecutivos;

### Por ultimo, o best_shift printará no terminal uma das iterações que teve o menor desvio padrão, retornando também uma lista com o nome do médico e o numero de turnos dele