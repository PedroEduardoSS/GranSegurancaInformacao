# C Lab

Criada em 1972 por Dennis Ritchie nos laboratórios Bell, a linguagem C é frequentemente chamada de "a mãe das linguagens modernas". Ela é a base de sistemas operacionais como Windows, Linux e macOS, além de ser a escolha principal para sistemas embarcados e motores de jogos.

Por que aprender C hoje?

**Performance**: Você tem controle total sobre o que o processador faz.

**Gestão de Memória**: Você decide onde e como os dados são guardados (olá, ponteiros!).

**Portabilidade**: Um código bem escrito em C roda em quase qualquer lugar, de torradeiras a supercomputadores.

## Desafios de Prática (Do Básico ao Avançado)

### Nível Iniciante

1. **Olá, Usuário**: Peça o nome do usuário e sua idade, e imprima uma mensagem personalizada.

2. **Calculadora de IMC**: Calcule o Índice de Massa Corporal usando a fórmula $IMC = \frac{peso}{altura^2}$.

3. **Par ou Ímpar**: Receba um número inteiro e diga se ele é par ou ímpar usando o operador de resto (%).

### Nível Intermediário (Lógica e Laços)

4. **Tabuada Dinâmica**: Peça um número e exiba sua tabuada de 1 a 10 usando um laço for.

5. **Sequência de Fibonacci**: Gere os primeiros $n$ números da sequência, onde cada número é a soma dos dois anteriores.

6. **Inversor de Strings**: Leia uma palavra e a exiba de trás para frente (sem usar funções prontas de bibliotecas externas).

### Nível avançado (Ponteiros e Estruturas)

7. **Troca com Ponteiros**: Crie uma função que receba dois endereços de memória e troque os valores das variáveis originais entre si.

8. **Gestão de Alunos (Structs)**: Crie uma estrutura Aluno com nome, nota e matrícula. Armazene 5 alunos em um array e mostre quem tem a maior nota.

9. **Alocação Dinâmica**: Peça ao usuário o tamanho de um vetor, aloque memória usando malloc(), preencha-o e depois libere a memória com free().

### Desafio Final

10. **Mini Banco de Dados em TXT**: Crie um programa que permita salvar nomes e telefones em um arquivo .txt e depois consiga ler e exibir esses dados ao reiniciar o programa.

### Comandos do GCC

Dominar o GCC (GNU Compiler Collection) é essencial para qualquer pessoa que queira programar em C de verdade. Ele é uma ferramenta poderosa com dezenas de opções.

Aqui estão os comandos e flags que você mais vai usar no dia a dia:

1. O Básico: Compilar e Nomear
Por padrão, o GCC gera um arquivo chamado a.out. Para dar um nome decente ao seu programa, use a flag -o.

Exemplo: gcc programa.c -o programa

Rode o programa: ./programa

2. Ativando os "Avisos" (Seu melhor amigo)
O C permite que você faça muitas bobagens sem reclamar. Essas flags forçam o compilador a ser mais rígido e te avisar onde o código está "estranho".

-Wall: Habilita a maioria dos avisos de construção.

-Wextra: Habilita avisos adicionais que o -Wall ignora.

Exemplo: gcc -Wall -Wextra programa.c -o programa

3. Debugging (Depuração)
Se o seu programa está dando erro e você quer usar o GDB para entender o porquê, você precisa da flag -g. Ela inclui informações de depuração no binário.

Exemplo: gcc -g programa.c -o programa

4. Linkando Bibliotecas (Matemática)
Se você usar a biblioteca <math.h>, o GCC muitas vezes não consegue encontrar as implementações sozinho. Você precisa avisá-lo para linkar a biblioteca matemática com -lm.

Exemplo: gcc programa.c -o programa -lm

**Entendendo o Processo**
O GCC não faz tudo de uma vez; ele passa por etapas. Você pode "parar" o processo em qualquer uma delas:

-E (Pré-processamento): Apenas expande os #include e #define. Gera código-fonte puro.

-S (Compilação): Transforma seu C em código Assembly. Ótimo para curiosos.

-c (Montagem): Gera o arquivo objeto (.o). Útil quando você tem muitos arquivos e não quer re-compilar tudo do zero.

#### Recursos

Bóson Treinamentos: https://www.youtube.com/watch?v=cZRuFwzjJ8E&list=PLucm8g_ezqNqzH7SM0XNjsp25AP0MN82R

Cheatsheet: https://cheatsheets.zip/c

Documentação: https://en.cppreference.com/w/c.html