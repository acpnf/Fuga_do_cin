## A Fuga do CIn

## Descrição do Projeto:
Este projeto é um jogo de labirinto onde o personagem principal, Seu Jailson, precisa coletar os crachás de três professores renomados (Juliano Iyoda, Ricardo Massa e Sergio Soares) e encontrar a saída do labirinto.
O jogo desafia o jogador a navegar por um labirinto e coletar todos os itens necessários para finalmente escapar do labirinto. Cada crachá coletado representa um marco no progresso do jogador. Além disso, tudo no jogo é gerado de forma randômica: as paredes do labirinto, os crachás e a posição da porta. Tudo isso contribui para que cada jogatina seja uma experiência única e emocionante!

## Participantes do Projeto:
- André Polo Norte
- Ikelvys Kauê
- João Pedro Lima
- Pablo Nunes
- Roni Oliveira
- Theo Egito

## Organização e Desenvolvimento de Jogo:
Dividimos a equipe para o desenvolver o jogo de forma mais eficiente e mais rapidamente. Assim, alguns trabalharam mais na parte gráfica, enquanto outros ficaram responsáveis pelos códigos. Além disso, a equipe se reuniu tanto presencialmente, como remotamente para alinhas as ideias e melhorar a estruturação do jogo, sendo assim todo mundo participou contribuindo ativamente e auxiliando os colegas.

## Divisão de tarefas:
| **Equipe** | **Tarefas** |
| :---: |:--:|
| André Polo Norte | Desenvolvimento das interfaces inicial e final |
| Ikelvys Kauê  | Criação das animações dos coletáveis e do player |
| João Pedro Lima | Desenvolvimento da classe do jogador e das funções em geral |
| Pablo Nunes | Criação das animações do ambiente e do player |
| Roni Victor | Desenvolvimento da classe do jogador e das funções em geral |
| Theo Marcos | Desenvolvimento da classe do jogador e das funções em geral, Modularização do código |


## Ferramentas Utilizadas:
- Pygame (Biblioteca focada no desenvolvimento de jogos 2D que nos forneceu os recursos necessários) ;
- Pyamaze (Biblioteca utilizada para criar o labirinto;
- Piskel (Site voltado para a criação de artes em pixels);
- VSCode (Ambiente usado para a programação em Python);
- IA's (Auxiliaram em dúvidas e transformaram fotos em pixel art)
- GitHub (Repositório que permitia o acesso ao código a todos membros do grupo).

## Arquitetura do Projeto
### funcoes_labirinto.py
As funções criam um labirinto aleatório, desenham a porta e determinam o posicionamento da saída, as cores das paredes e o fundo do jogo.
### funcoes_coletaveis.py
Essas funções geram os crachás, criam o placar que apresenta o status do jogo e verifica tanto a coleta dos crachás, como a fuga do CIn.
### funcoes_personagem.py
Tais funções carregam as animações de Seu Jailson, atualiza as direções do personagem, verifica as movimentações e processa os eventos do jogo.
### funcoes_telas_jogo.py
Carregam as telas inicial e final do jogo

## Principais Objetivos do Projeto
- Utilizar bibliotecas para criar um jogo funcional (Pygame e Pyamaze);
- Aplicar tudo o que aprendemos durante o período no código do jogo;
- Melhorar a colaboração em equipe dos integrantes do projeto.

## Conceitos da Cadeira Utilizados no Projeto
- Funções: Utilizadas para modularizar o jogo com intuito de dividir o código em partes independentes.
- Classes: Gerar as animações do personagem principal.
- Listas: Criação e denominação das chaves e definição das instruções do jogo
- Dicionários: Denominação das chaves
- Laços de Repetição: Geração das imagens e das animações, desenho do labirinto, criação e desenho das chaves, geração da saída, verificações da coleta de crachás e da vitória e processamento dos eventos.
- Condicionais: Movimentação do personagem, geração e desenho do labirinto e das chaves, verificação da coleta dos crachás e da vitória, processamento de eventos, exibição das telas
- Tuplas: Determinação de variáveis constantes, como as cores. 

## Desafios e Erros:
A complexidade e a falta de conhecimento prévio das ferramentas dificultou muito o andamento do projeto, em muitos momentos precisamos recorrer a instrumentos de pesquisa para aprender a desenvolver alguma parte do jogo. Ademais, a organização dos códigos, o compartilhamento de informações, a comunicação e o GitHub foram problemas que mais afetaram o andamento do trabalho. Tais problemas geraram bastante confusão, resultando em códigos desconexos ou incompletos, mistura de informações e perda de arquivos. 

## Como Jogar:
- Use as teclas de seta (↑ ↓ ← →) ou (W A S D) para mover Seu Jailson pelo labirinto
- Colete os 3 crachás dos professores espalhados pelo labirinto
- Encontre a saída após coletar todos os itens

## Imagens do Jogo:
### Fundo
Inspirado no piso do CIn.
![fundo2](https://github.com/user-attachments/assets/614b2404-13cc-4cca-9e9a-f19174706d30)
### Tela Inicial
![tela inicial](https://github.com/user-attachments/assets/adcc0751-6e63-4773-a04d-58047036aedd)
### Seu Jailson 
Animação baseada no ilustre funcionário do Laboratório de Harware, Seu Jailson!
![jogador_andando_esquerda_3](https://github.com/user-attachments/assets/a421158d-2c14-4d82-a652-e35402a330e8)
![jogador_andando_esquerda_2](https://github.com/user-attachments/assets/06419107-5e0d-4899-87b3-def27f1082da)
![jogador_andando_esquerda_1](https://github.com/user-attachments/assets/ec8406f5-2db3-4eaa-ac4b-478bf479b5fe)
![jogador_andando_direita_3](https://github.com/user-attachments/assets/8fbc50b9-6211-4bf9-8f7b-e7610f495061)
![jogador_andando_direita_2](https://github.com/user-attachments/assets/630c869e-46e6-4fb3-b119-64804fc6a511)
![jogador_andando_direita_1](https://github.com/user-attachments/assets/08fff7d2-14f1-4614-8630-f6715abb0421)
### Crachá Iyoda
Animação baseada no querido professor, Juliano Iyoda!
![sprite_IYODA3](https://github.com/user-attachments/assets/6f0a09ce-0de2-4ec0-aaba-950479b7d000)
![sprite_IYODA2](https://github.com/user-attachments/assets/2f58e5e3-e512-4a58-969b-4bea7054e543)
![sprite_IYODA1](https://github.com/user-attachments/assets/88db0037-bb80-4b25-9e4d-c33ec4cd6091)
![sprite_IYODA0](https://github.com/user-attachments/assets/e998368a-ea7c-48d9-a2f7-a1ce5821f71a)
### Crachá Massa
Animação baseada no grande professor, Ricardo Massa!
![sprite_RICARDO3](https://github.com/user-attachments/assets/e6f16bb0-0df0-4cf4-9bca-e9cc8ca7f15f)
![sprite_RICARDO2](https://github.com/user-attachments/assets/1963cb3a-e6dc-4512-af11-01deb58f90d5)
![sprite_RICARDO1](https://github.com/user-attachments/assets/90eaf8af-825a-4d68-8b8f-0fca1fd807b1)
![sprite_RICARDO0](https://github.com/user-attachments/assets/8ae2fc31-4b2e-44a8-80d0-7b3eb02b27d8)
### Crachá Soares
Animação baseada no prestigiado professor, Sérgio Soares!
![sprite_SERGIO3](https://github.com/user-attachments/assets/d40adca0-c90d-4cf6-9c07-76789c20b1ba)
![sprite_SERGIO2](https://github.com/user-attachments/assets/64c04885-bcf6-4ca8-a103-d9cce2069e94)
![sprite_SERGIO1](https://github.com/user-attachments/assets/c449207c-1ae0-45f2-9c8a-104c28eaf988)
![sprite_SERGIO0](https://github.com/user-attachments/assets/eac591e1-4644-436f-9783-0f8747620248)
### Porta
![porta fechada](https://github.com/user-attachments/assets/3143ed09-36dd-4796-9137-18466491ebb6)
![porta aberta](https://github.com/user-attachments/assets/120095ea-cf00-4a34-b11e-0bac938919ce)
### Tela Final
![tela final](https://github.com/user-attachments/assets/97453c90-080d-4d23-84ec-50a26dcc501d)

## Captura de Tela
![Screenshot 2025-04-09 102845](https://github.com/user-attachments/assets/abb0f059-ce3c-43fa-be26-04002bc857c0)


