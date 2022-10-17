# Criador de escala de médicos

## Marcelo Lopes Valerio - email: mar.valerio@hotmail.com.br

## Projeto pessoal - pedido especial de um familiar

### Tendo os médicos, seus dias disponíveis, e a quantidade de medicos necessaria por dia, gera a escala da semana/mês, priorizando a/as opções com menor desvio padrão dentre um numero pre estabelecido de iterações, levando em conta também se todos os plantões estão preenchidos

## Regras de negócio:

### - Um médico não pode fazer plantões de 36 horas (dia-noite-dia consecutivos, por exemplo).
### - Idealmente, o melhor turno é aquele no qual o numero de turnos de todos os médicos é igual.
### - Se não for possível preencher todas as vagas de plantão, o melhor plantão deve obrigatóriamente conter o maior numero possível de vagas ocupadas, mesmo que isso deixe a distribuição desigual.
### - Deve ter a opção de escolher entre turnos diários e noturnos, ou apenas diários.
### - A usabilidade do software deve ser simples, podendo rodar em qualquer máquina, com o mínimo de programas auxiliares possiveis, entretanto, preferencialmente utilizando excel.

## Para rodar o código:

### Para rodar o código, há duas opções; a primeira é colocar o arquivo do excel como o do exemplo dado preenchido dentro da pasta do código (pode ser no mesmo nível que a pasta src), ou é possível pegar apenas o arquivo .exe (dentro de dist), e rodá-lo numa pasta com a planilha excel preenchida (nos dois casos, necessariamente a planilha deve chamar "escala_plantao.xlsx).

### Simples assim, surgirá um novo arquivo excel na pasta, chamado Turnos.xlsx, que terá uma opção de turno em cada aba, de acordo com o número de opções solicitado. Além disso, o resultado aparecerá no terminal.

### Instruções de preenchimento da planilha na primeira aba da mesma - é recomendado manter o arquivo original como exemplo e utilizar cópias do mesmo.

## Funcionamento do código - encadeamento de funções

### Para a utilização simplificada desse software, o mesmo foi integrado com uma planilha de excel, de onde vem o input de dados. A mesma está documentada de tal modo que qualquer um possa utilizala, sabendo apenas o mínimo de excel, e o programa tem uma versão .exe para que o mesmo seja utilizado em maquinas pessoais, sem a necessidade de instalação de qualquer recurso adicional

### O software pega os dados fornecidos pela planilha, como numero de opções de turnos, nome, disponibilidade dos médicos, os formata para a correta utilização, e então chama uma serie de funções: a primeira, import data, que em conjunto com a excel list, irá gerar uma lista de objetos Médicos, com as respectivas disponibilidades e nomes, que são então passados como argumentos a seguir:

### Primeiro a função passa pelo availability_filter, que, dado um dia, irá retornar os médicos que têm, em sua disponibilidade, o dia em questão. Depois disso, os disponíves passam pelo priorizer, que levará em consideração quantos dias o médico ainda tem disponível, quantos plantões o médico ja fez, e quantos plantões seria o ideal para que todos os médicos tivessem o mesmo numero de plantões.

### O resultado ainda passa pelo seletor, que fará uma serie de validações para averiguar que o médico escolhido é realmente válido para o dia iterado. Esse método, antes de tudo, embaralha a lista, para garantir que cada iteração, dentro do possível, seja diferente da anterior, e então aumentar as chances de encontrar o plantão perfeito.

### A função create_shift é responsável por pegar os médicos selecionados e colocá-los em uma lista de modo que possam ser manipulados. Além disso, ela utiliza o metodo setup no inicio de cada criação, e no final de cada dia realiza a zeragem dos plantões consecutivos daqueles que não realizaram plantões no dia em questão.

### A função multi_shift_generator ira auxiliar na impressão dos resultados de maneira organizada no terminal, além de converter os resultados obtidos em um novo arquivo excel, que salvará em abas diferentes as tabelas com as opções de turno geradas, de acordo com um numero estabelecido. Além disso, ela chama o método best_shift, que gerará 1000 iterações de criação de turno, para escolher as que obtiverem o menor numero de plantões preenchidos, e melhor desvio padrão, e printar uma das opções. A função print_shift é uma função auxiliar que formata os dados do turno em um DataFrame Pandas, e o printa no terminal

### A função best_shift ainda chama a função responsável por criar a pontuação do turno, que percorre a lista de médicos e atribui mais ou menos pontos de acordo com a qualificação do médico, e quantas vezes ele fará turnos. Essa função é a create_shift_list, que cria os 1000 turnos, e atribui aos mesmos essa pontuação. Além disso, ela cria um dicionário com o turno bruto, e dados como desvio padrão e a pontuação para acessá-los mais facilmente.