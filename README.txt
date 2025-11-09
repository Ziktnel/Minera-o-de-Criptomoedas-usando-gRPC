GABRIEL BASTOS ZIKTNEL
RONIEL REICH
KAYO SANCHES


Atividade 1 – Mineração de Criptomoedas usando gRPC
1. Introdução

Esta atividade teve como objetivo o desenvolvimento de um protótipo de sistema de mineração de criptomoedas utilizando o modelo cliente-servidor baseado em chamadas de procedimento remoto (gRPC). A proposta visa compreender o funcionamento básico de uma rede de mineração, onde diversos clientes competem para resolver desafios criptográficos gerados por um servidor central.

Por meio da tecnologia gRPC e da linguagem Python, foi possível implementar uma comunicação eficiente e escalável entre o servidor e os clientes mineradores, simulando o processo de descoberta de blocos em um ambiente controlado.

2. Objetivos

O principal objetivo foi construir um sistema que reproduzisse o conceito de mineração, aplicando a arquitetura RPC para comunicação entre os participantes. Os objetivos específicos foram:

Implementar um servidor capaz de gerenciar transações e desafios criptográficos.

Criar clientes que tentam resolver os desafios enviando soluções para o servidor.

Utilizar funções de hash (SHA-1) para representar o mecanismo de prova de trabalho (Proof of Work).

Registrar resultados de mineração e identificar o cliente vencedor de cada desafio.

3. Arquitetura e Funcionamento do Sistema

O sistema foi desenvolvido com base na arquitetura cliente-servidor.
O servidor gRPC é responsável por:

Gerar novos desafios (chamados “transactions”) com diferentes níveis de dificuldade.

Manter uma tabela de registro contendo as colunas: TransactionID, Challenge, Solution e Winner.

Receber e validar soluções enviadas pelos clientes.

Atualizar o registro do vencedor quando um cliente encontra a solução correta.

Os clientes gRPC desempenham o papel dos mineradores. Cada cliente conecta-se ao servidor e tenta encontrar uma solução válida para o desafio atual. Essa solução consiste em uma string que, quando aplicada à função de hash SHA-1, satisfaz as condições impostas pelo desafio.

O processo é iterativo:

O servidor gera um novo desafio (Transaction 0, 1, 2...).

Os clientes começam a testar soluções possíveis.

Caso encontrem uma solução válida, enviam-na ao servidor.

O servidor valida e registra o vencedor.

Um novo desafio é então iniciado.

4. Execução e Resultados

Durante os testes, o sistema apresentou o seguinte comportamento:

O servidor iniciou corretamente com a Transaction 0, gerando um desafio aleatório de dificuldade 13.

Os clientes mineradores realizaram até 5000 tentativas para encontrar a solução correspondente.

Ao final desse processo, o servidor registrou que nenhum cliente conseguiu resolver o desafio dentro do limite de tentativas, exibindo a mensagem:

Transaction 0 - Challenge 13
Não encontrou em 5000 tentativas.


Esse resultado demonstra o funcionamento esperado do mecanismo de prova de trabalho: quanto maior o desafio (dificuldade), mais tentativas são necessárias para encontrar uma solução válida.

Em execuções subsequentes, novos desafios foram gerados com diferentes níveis de dificuldade, e os resultados variaram de acordo com a sorte e capacidade computacional de cada cliente.

5. Análise e Discussão

O protótipo demonstrou de forma satisfatória os princípios fundamentais da mineração em blockchain:

A relação direta entre dificuldade do desafio e o tempo de processamento.

A competição entre clientes por encontrar uma solução válida.

O registro transparente das transações resolvidas pelo servidor.

A comunicação via gRPC mostrou-se eficiente, permitindo escalabilidade para múltiplos clientes conectados simultaneamente. Além disso, o uso da função SHA-1 como base para o desafio criptográfico simulou adequadamente o conceito de “Proof of Work”, embora de forma simplificada.

6. Conclusão

A implementação realizada atingiu os objetivos propostos, fornecendo uma simulação funcional de um ambiente de mineração distribuída utilizando gRPC em Python.
O exercício permitiu compreender na prática os conceitos de RPC, comunicação assíncrona e desafios criptográficos, além de reforçar noções sobre tolerância a falhas e coordenação entre processos distribuídos.

Como possível aprimoramento, recomenda-se:

Implementar uma interface de monitoramento em tempo real das transações.

Permitir que múltiplos desafios sejam processados em paralelo.

Armazenar os registros em banco de dados para análise posterior.

Em síntese, a atividade cumpriu com sucesso seu papel didático, evidenciando o potencial do gRPC na construção de sistemas distribuídos e na compreensão dos mecanismos que fundamentam a mineração de criptomoedas.