# ANEXO_IA.md — Uso de assistentes de IA (Parte 6)

> ⚠ **Este arquivo foi redigido pelo próprio assistente com base no que aconteceu na sessão. A dupla precisa ler, conferir e completar os campos `[PREENCHER]` com a sua experiência real antes de entregar.** O enunciado zera as Partes 5 e 6 se o anexo for genérico ou fabricado; na arguição vocês terão de sustentar cada linha.

## A.1 Ferramentas usadas e em que partes

- **Claude (Anthropic)**, no chat do claude.ai com ambiente de execução de código. Escreveu o código de `src/` (buscas, busca local, especialista, Bayes, escala, contraexemplo, main), o `RELATORIO.md`, o `README.md` e dividiu o trabalho em 8 commits. Numa primeira versão o projeto era maior (com um gerador automático de relatório); a pedido do aluno, foi simplificado.
- O **`gerador_pomar.py` não foi escrito nem modificado pelo assistente**: foi copiado do enunciado (só se reconstruiu a indentação, que o PDF perdeu).
- Ferramentas e tarefas da dupla (preencher o nome de quem fez cada uma):

**Vitor:** _______________________________________________

**Emylly:** _______________________________________________

Lista de tarefas para dividir entre os dois nomes acima:
  - [V] Instalar dependências (`pip install -r requirements.txt`)
  - [V] Rodar `python src/teste_afericao.py` e conferir "TUDO CERTO"
  - [V] Rodar `python src/main.py <matricula>` com a matrícula real
  - [V] Rodar `python src/escala.py <matricula>` (Parte 2.4)
  - [V] Abrir `resultados/saida.txt` e conferir os números
  - [E] Ler o `RELATORIO.md` inteiro e comparar com o PDF
  - [E] Preencher identificação (nomes/matrículas) no `README.md`
  - [E] Preencher seção 2.4 e item 5 da Parte 5 do `RELATORIO.md`
  - [E] Revisar o `GUIA_ARGUICAO.md`
  - [V] Configurar `git config user.name`/`user.email`
  - [E] Testar o projeto do zero em outra máquina
  - [E] Abrir o repositório numa janela anônima (conferir público)
  - [V] Conferir que não subiu `venv/` nem `__pycache__/`
  - [E] Preencher os campos restantes deste `ANEXO_IA.md` (abaixo)

## A.2 Dois prompts na íntegra, com a resposta recebida

**Prompt 1:**

```
Você é o responsável técnico por me ajudar a desenvolver o projeto acadêmico **Caatinga.AI — Sprint 1**, da disciplina de Inteligência Artificial.

## 1. FONTE PRINCIPAL E REGRA MAIS IMPORTANTE

O arquivo PDF do enunciado da atividade está disponível no projeto.

Antes de escrever qualquer código:

1. Leia o PDF inteiro.
2. Entenda todas as exigências das Partes 1 a 6.
3. Identifique todos os arquivos obrigatórios.
4. Identifique todos os resultados que precisam ser medidos experimentalmente.
5. Identifique todas as regras que podem causar perda de pontos.
6. Não invente resultados.
7. Não invente números de experimentos.
8. Não invente minha matrícula.
9. Não invente nomes de integrantes.
10. Quando uma informação depender da execução do programa, EXECUTE o código e obtenha o valor real.
11. Quando uma informação depender da minha matrícula, peça minha matrícula antes de gerar os resultados finais.

O objetivo não é apenas produzir textos. Quero um projeto Python funcional, reproduzível e que eu consiga explicar durante a arguição.

---

# 2. OBJETIVO DO PROJETO

Implementar o agente Caatinga.AI, que percorre um pomar representado por uma grade de 12×12 talhões.

O agente começa em `(0,0)` e precisa chegar a `(11,11)`.

Tipos de terreno:

* `.` = carreador firme, custo 1
* `~` = solo encharcado / linha de irrigação, custo 4
* `#` = bloqueado, não pode entrar

O custo da rota é a soma dos custos dos talhões em que o agente entra, sem contar o talhão inicial.

O projeto precisa implementar:

* BFS
* DFS
* UCS
* A*
* Busca local por subida de encosta
* Têmpera simulada
* Sistema especialista com encadeamento para trás
* Cálculos de Bayes
* Auditoria das afirmações do fornecedor
* Geração dos arquivos de resultados
* Relatório
* Anexo de uso de IA
* README completo

---

# 3. NÃO ALTERAR O GERADOR

O arquivo:

`src/gerador_pomar.py`

é um contrato do professor.

NÃO ALTERE esse arquivo.

Copie exatamente o código fornecido no enunciado.

Não "melhore", não reorganize, não formate, não renomeie variáveis e não faça nenhuma alteração.

Todos os demais arquivos podem ser criados normalmente.

---

# 4. ESTRUTURA OBRIGATÓRIA

Crie exatamente uma estrutura equivalente a:

caatinga-ai-sprint1/
├── README.md
├── RELATORIO.md
├── ANEXO_IA.md
├── requirements.txt
├── src/
│   ├── gerador_pomar.py
│   ├── buscas.py
│   ├── busca_local.py
│   ├── especialista.py
│   ├── bayes.py
│   └── main.py
└── resultados/
├── resultados.csv
├── grafico.png
└── pomar.txt

Também crie um `.gitignore` apropriado para Python.

Não coloque `venv/`, `__pycache__/` ou arquivos desnecessários no repositório.

---

# 5. ARQUITETURA DO CÓDIGO

Quero código organizado, legível e modular.

## `buscas.py`

Implemente:

* BFS
* DFS
* UCS
* A*
* heurística h1
* heurística h2
* heurística h3

Todas as estratégias devem trabalhar com a mesma representação de estado.

Cada busca deve registrar:

* custo da rota
* número de passos
* nós expandidos
* tamanho máximo da fronteira
* rota encontrada
* tempo de execução

Defina claramente o que significa "nó expandido".

Não conte incorretamente nós duplicados.

Controle estados visitados/fechados adequadamente.

Para UCS e A*, utilize uma fila de prioridade apropriada.

Para algoritmos que podem encontrar um estado novamente com custo menor, trate corretamente essa situação.

---

# 6. ORDEM DOS VIZINHOS

Escolha uma ordem fixa de expansão dos vizinhos.

Exemplo:

Norte, Sul, Oeste, Leste.

Você pode escolher outra ordem, mas:

* declare qual foi escolhida;
* use exatamente a mesma em todas as estratégias;
* coloque essa informação no README;
* coloque também no relatório.

Essa decisão é importante porque afeta principalmente os resultados da DFS.

---

# 7. BFS

A BFS deve encontrar uma rota com o menor número de passos, mas não necessariamente a rota de menor custo, porque os terrenos possuem custos diferentes.

Não tente "corrigir" isso fazendo BFS considerar custos.

A BFS deve permanecer uma busca em largura tradicional.

Registre:

* custo
* passos
* nós expandidos
* fronteira máxima

---

# 8. DFS

Implemente DFS corretamente.

Tome cuidado com:

* ciclos;
* estados repetidos;
* estados que podem aparecer em diferentes nós;
* ordem dos vizinhos.

O enunciado chama atenção para a diferença entre estado e nó.

A DFS precisa funcionar para diferentes sementes/matrículas, não somente para o caso usado no relatório.

---

# 9. UCS

Implemente Uniform Cost Search corretamente.

A prioridade deve ser o custo acumulado `g(n)`.

Quando existir um caminho mais barato para um estado já descoberto, trate isso corretamente.

O resultado do UCS será utilizado como referência de custo ótimo.

Não simplesmente copie ou force o resultado esperado do exemplo do professor.

---

# 10. A*

Implemente A* com três heurísticas:

### h1

`h1(n) = 0`

### h2

Distância Manhattan até o objetivo.

### h3

`4 × distância Manhattan até o objetivo`

A função deve permitir selecionar a heurística.

Registre:

* custo
* nós expandidos
* rota
* passos
* fronteira máxima
* tempo

Também deixe claro no código se nós são reabertos quando um caminho melhor é encontrado.

---

# 11. HEURÍSTICAS

Para h2:

Considere que cada movimento entra em um novo talhão.

Como o menor custo de entrada possível é 1, a distância Manhattan fornece um limite inferior para o custo restante.

A explicação formal da admissibilidade deve aparecer no relatório.

Para h3:

Não diga apenas que ela é inadmissível.

Depois de executar com a matrícula real, procure dois talhões concretos onde:

`h3(n) > custo real ótimo restante`

Registre as coordenadas e os valores reais.

Não invente esse exemplo.

---

# 12. VALIDAÇÃO COM O CASO DO PROFESSOR

Antes de usar minha matrícula, crie/teste uma validação com a matrícula fictícia:

`20231045`

O enunciado fornece como referência:

* UCS: custo ótimo = 34
* BFS: custo = 55
* BFS: 22 passos
* UCS: aproximadamente 112 nós expandidos
* A* Manhattan: aproximadamente 93 nós expandidos

Os custos e passos devem bater exatamente.

Os nós expandidos podem variar devido ao critério de desempate.

Use isso apenas como teste de validação, nunca como resultado da minha matrícula.

Se algo não bater, investigue e corrija antes de continuar.

---

# 13. EXPERIMENTO DE ESCALA

Implemente um experimento que aumente o tamanho do pomar:

12 → 40 → 100 → ...

até uma das estratégias falhar por:

* memória;
* stack overflow;
* tempo superior a 60 segundos.

Não invente o ponto de falha.

Execute o experimento de verdade.

Registre:

* `n`
* estratégia
* tempo
* resultado
* tipo de falha, se houver

Relacione o resultado com a fórmula teórica discutida no enunciado.

Se uma execução for muito pesada para o ambiente atual, explique isso claramente em vez de fabricar o resultado.

---

# 14. BUSCA LOCAL

No arquivo `busca_local.py`, implemente:

* subida de encosta;
* têmpera simulada.

Problema:

O agente tem 6 horas de bateria e não consegue visitar todos os talhões livres.

Modele:

* estado;
* vizinhança;
* função objetivo.

Use `K = 15`.

Execute cada algoritmo 30 vezes.

Calcule:

* média;
* desvio padrão;
* melhor valor.

Use sementes controladas para permitir reprodutibilidade.

Não invente os resultados.

A análise deve explicar por que aceitar temporariamente uma piora pode ajudar a têmpera simulada a escapar de ótimos locais.

---

# 15. SISTEMA ESPECIALISTA

No arquivo `especialista.py`, implemente de 5 a 8 regras no formato:

SE condição ENTÃO conclusão.

As regras devem decidir o manejo de um talhão.

Implemente encadeamento para trás.

O programa precisa imprimir a cadeia de regras utilizada para chegar à conclusão.

Exemplo conceitual:

Objetivo:
`inspecionar_prioridade_alta`

↓

Regra X

↓

`armadilha_positiva`

↓

`umidade_alta`

etc.

Depois crie um caso legítimo do domínio que a base classifique incorretamente.

Adicione uma regra para corrigir o problema sem contradizer as demais.

Mostre no relatório:

* caso antes;
* cadeia de regras antes;
* nova regra;
* cadeia depois.

---

# 16. BAYES

No arquivo `bayes.py`, utilize EXATAMENTE os parâmetros gerados pela função:

`parametros_sensor(matricula)`

Não escolha valores manualmente.

Calcule:

P(infestado | sensor positivo)

usando:

P(I|+) = [P(+|I) P(I)] / [P(+|I)P(I) + P(+|¬I)P(¬I)]

Depois calcule:

* percentual de alertas falsos;
* número de falsos positivos por semana;
* horas gastas por semana, considerando 12 minutos por inspeção;
* novo valor preditivo positivo caso a sensibilidade seja aumentada para 99,9%, mantendo a taxa de falsos positivos.

Mostre as substituições numéricas no relatório.

Não arredonde prematuramente.

---

# 17. AUDITORIA DO LAUDO

No relatório, analise as cinco afirmações do fornecedor AgroVision.

Para cada uma:

* classifique como correta, parcialmente correta ou incorreta;
* explique tecnicamente;
* cite a teoria relevante;
* utilize números REALMENTE MEDIDOS pelo programa quando o enunciado exigir evidência experimental.

Não use apenas explicações genéricas.

---

# 18. RECOMENDAÇÃO FINAL

O enunciado solicita um parágrafo de recomendação para a diretoria.

Não escreva essa recomendação antes de termos os resultados reais das Partes 2, 3 e 4.

Depois de executar tudo, escreva o parágrafo com base nas evidências obtidas e inclua a condição técnica que poderia mudar a conclusão.

---

# 19. RESULTADOS CSV

Gere:

`resultados/resultados.csv`

com as colunas:

estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms

Inclua os resultados relevantes de:

* BFS
* DFS
* UCS
* A* h1
* A* h2
* A* h3

Use valores reais da execução.

---

# 20. GRÁFICO

Gere:

`resultados/grafico.png`

O gráfico deve mostrar claramente:

* nós expandidos;
* comparação entre estratégias;
* eixos rotulados;
* legenda quando necessária.

Não faça um gráfico enganoso.

---

# 21. POMAR.TXT

Gere:

`resultados/pomar.txt`

Contendo:

* primeira linha: matrícula utilizada como semente;
* depois, a grade do pomar.

---

# 22. MAIN.PY

Crie:

`python src/main.py <matricula>`

Esse deve ser o comando principal do projeto.

Ao executar, ele deve:

1. receber a matrícula;
2. gerar o pomar;
3. gerar os parâmetros do sensor;
4. executar as buscas;
5. executar os experimentos necessários;
6. executar os cálculos;
7. gerar os resultados;
8. gerar `resultados.csv`;
9. gerar `grafico.png`;
10. gerar `pomar.txt`.

O projeto deve funcionar com uma matrícula diferente da usada durante o desenvolvimento.

Não faça código específico para uma única matrícula.

---

# 23. README

Crie um README.md seguindo exatamente a ordem exigida pelo professor:

1. identificação;
2. descrição do projeto;
3. como instalar;
4. como executar;
5. tabela-resumo;
6. ordem dos vizinhos;
7. comportamento de reabertura do A*;
8. mapa dos arquivos;
9. limitações conhecidas.

Não coloque números falsos.

Os números da tabela devem ser gerados pelo programa.

---

# 24. RELATORIO.MD

Crie um relatório completo contendo:

## Parte 1

* PEAS;
* classificação do ambiente;
* evidências retiradas do cenário;
* dimensões discutíveis;
* tipo de agente;
* métrica perversa.

## Parte 2

* formulação do problema;
* número de estados;
* BFS;
* DFS;
* UCS;
* tabela de resultados;
* explicação da diferença BFS/UCS;
* experimento de escala.

## Parte 3

* A*;
* h1;
* h2;
* h3;
* admissibilidade;
* exemplo concreto da h3;
* comparação com UCS;
* busca local.

## Parte 4

* parâmetros do sensor;
* sistema especialista;
* caso que quebra a base;
* Bayes;
* falsos positivos;
* análise da mudança de sensibilidade;
* decisão que deve permanecer como regra explícita.

## Parte 5

* auditoria das cinco afirmações;
* recomendação final.

Todas as partes que dependem de experimentos devem usar os resultados reais.

---

# 25. ANEXO_IA.MD

Crie o arquivo:

`ANEXO_IA.md`

Mas NÃO invente o conteúdo sobre o uso da IA.

Estruture o arquivo para conter:

### A.1

Ferramentas de IA utilizadas e em quais partes.

### A.2

Dois prompts utilizados integralmente e as respostas recebidas.

### A.3

Pelo menos um erro, imprecisão ou invenção que uma IA cometeu neste trabalho.

IMPORTANTE:

Não invente um erro.

Depois que o projeto estiver funcionando, procure deliberadamente possíveis erros nas respostas da IA comparando-as com os resultados experimentais.

Se encontrar um erro real, documente:

* o que a IA afirmou;
* por que parecia correto;
* qual foi o resultado real;
* qual experimento desmentiu a afirmação.

### A.4

Uma frase explicando o que foi descoberto após executar o código que não era possível saber apenas lendo uma resposta de IA.

---

# 26. QUALIDADE ACADÊMICA

Este é um projeto que será defendido oralmente.

Portanto:

* não esconda a lógica em funções excessivamente complexas;
* não utilize bibliotecas desnecessárias;
* prefira Python padrão quando possível;
* escreva código que um aluno consiga explicar;
* coloque comentários somente quando ajudarem;
* não gere código gigantesco sem necessidade;
* não faça "mágica";
* não coloque resultados hardcoded;
* não crie condições especiais para a matrícula do professor;
* não copie os números de referência para o resultado final.

---

# 27. TESTES

Crie testes internos ou uma forma clara de validar:

* geração do pomar;
* BFS;
* DFS;
* UCS;
* A*;
* heurísticas;
* Bayes;
* especialista.

Primeiro valide com `20231045`.

Depois execute com minha matrícula.

Se encontrar discrepância, investigue antes de continuar.

---

# 28. PROCESSO DE TRABALHO

NÃO tente fazer tudo de uma vez sem verificar.

Trabalhe nesta ordem:

FASE 1 — analisar o PDF e planejar arquitetura.

FASE 2 — criar estrutura do projeto.

FASE 3 — implementar o gerador intacto.

FASE 4 — implementar BFS/DFS/UCS.

FASE 5 — validar com 20231045.

FASE 6 — implementar A* e heurísticas.

FASE 7 — implementar busca local.

FASE 8 — implementar especialista.

FASE 9 — implementar Bayes.

FASE 10 — gerar experimentos reais.

FASE 11 — gerar resultados.csv, grafico.png e pomar.txt.

FASE 12 — escrever README e RELATORIO.

FASE 13 — preparar ANEXO_IA.md sem inventar informações.

FASE 14 — executar tudo do zero.

FASE 15 — revisar se todos os requisitos do PDF foram cumpridos.

---

# 29. REGRA FUNDAMENTAL SOBRE RESULTADOS

Sempre que você puder executar o código para descobrir uma resposta, EXECUTE.

Não responda:

"provavelmente será X".

Descubra X executando.

Não escreva:

"aproximadamente 100 nós"

se podemos medir o número.

Não invente:

* custos;
* número de passos;
* nós expandidos;
* fronteira máxima;
* tempos;
* resultados da busca local;
* parâmetros do sensor;
* exemplos de coordenadas;
* resultados de Bayes.

---

# 30. ARGUMENTAÇÃO PARA A PROVA

Ao final do desenvolvimento, crie também um arquivo ou seção chamada:

`GUIA_ARGUICAO.md`

Nele, explique de maneira simples:

* como BFS funciona;
* como DFS funciona;
* por que BFS pode ser mais cara que UCS;
* como UCS encontra o menor custo;
* como A* funciona;
* por que h2 é admissível;
* por que h3 pode não ser admissível;
* diferença entre estado e nó;
* o que significa reabrir um estado;
* por que têmpera simulada aceita pioras;
* diferença entre sensibilidade e valor preditivo positivo;
* como o sistema especialista faz encadeamento para trás.

Inclua possíveis perguntas que o professor poderia fazer e respostas curtas baseadas NO NOSSO código.

---

# 31. NÃO FAÇA ISSO

Nunca:

* invente dados;
* altere `gerador_pomar.py`;
* use números da matrícula fictícia como meus resultados;
* coloque resultados diretamente no código;
* faça o programa funcionar somente para uma matrícula;
* omita limitações;
* diga que algo foi testado quando não foi;
* diga que algo foi executado quando não foi;
* escreva no relatório que eu fiz algo que não fiz;
* invente conteúdo para o ANEXO_IA.

---

# 32. ANTES DE COMEÇAR

Primeiro leia o PDF inteiro e faça uma análise dos requisitos.

Depois me diga:

1. quais arquivos serão criados;
2. quais partes do trabalho serão implementadas em cada arquivo;
3. quais informações você precisa de mim;
4. quais experimentos precisarão ser executados;
5. quais pontos apresentam maior risco de erro.

NÃO comece a escrever todos os arquivos ainda.

Depois dessa análise, aguarde minha confirmação.

Quando eu confirmar, implemente o projeto fase por fase, executando e validando cada etapa antes de avançar.
Leia esse prompt e faca a correcao com base no projeto que nos desenvolvemos ate agora. Oq esta incorreto me avise.
```

**Resposta recebida (íntegra, texto do assistente; omitidas só as linhas de execução de comando):**

```
Vou conferir o projeto de verdade contra esse roteiro, arquivo por arquivo, em vez de responder de memória.

Bom, o projeto está intacto (essa é a versão pré-commit da matrícula real, antes do rebase de autoria que você fez no seu VS Code — o meu ambiente aqui é isolado do seu computador). Vou auditar item por item contra o roteiro que você mandou.

Auditei o projeto inteiro contra as 32 seções desse roteiro. A notícia boa: quase tudo que ele exige já está certo. Achei duas coisas reais para corrigir, e o resto são pontos que já estavam OK.

O que está incorreto ou faltando

1. Falta o GUIA_ARGUICAO.md (Seção 30). Esse roteiro pede um arquivo separado, com explicações simples de BFS, DFS, UCS, A*, admissibilidade de h2/h3, estado vs. nó, reabertura, têmpera simulada, sensibilidade vs. VPP e encadeamento para trás — mais perguntas que o professor poderia fazer. Eu nunca criei esse arquivo. Isso é uma falta real, não uma opinião: vou criar agora.

2. O README não avisa que o gerador_pomar.py teve a indentação reconstruída. A Seção 3 desse roteiro é enfática: "não altere, copie exatamente". Eu expliquei isso a você em conversa, mas nunca documentei isso no arquivo. O PDF original perdeu a indentação do código na hora de virar texto (todas as linhas ficaram com um espaço só), e eu tive que deduzir onde cada if, while e return deveriam ficar. A lógica bate com a caixa de aferição do enunciado, mas isso deveria estar escrito no README como limitação, não só dito de boca. Vou corrigir.

O que já estava certo (conferido de novo agora)
gerador_pomar.py não foi alterado no sentido de lógica — só a indentação foi inferida (ponto 2 acima).
Nenhuma matrícula fica hardcoded no main.py; ele recebe por sys.argv e funciona com qualquer semente (testei com 8 sementes diferentes ao longo da conversa).
bayes.py não arredonda no meio do cálculo — só na hora de mostrar o texto.
A seção 2.4 do relatório e o item 5 da Parte 5 ainda estão com aviso de "a preencher" para a sua matrícula real, exatamente como a Seção 29 desse roteiro exige (nunca inventamos o ponto de falha da sua semente).
BFS não foi "consertada" para considerar custo — continua BFS pura, como a Seção 7 pede.
UCS e A* tratam corretamente reabertura de estado com custo menor, e isso está comentado no código, como a Seção 10 pede.
h3: o exemplo concreto de superestimativa vem de execução real (B.superestimacoes), não foi inventado, como pede a Seção 11.

Vou agora corrigir os dois pontos.

Resumo da auditoria

Passei o projeto pelas 32 seções desse roteiro. A conclusão: o projeto atende quase tudo. Achei 2 coisas reais, já resolvidas.

1. Faltava o GUIA_ARGUICAO.md (Seção 30 do roteiro). Acabei de criar. Ele explica BFS, DFS, UCS, A*, admissibilidade de h2/h3, estado vs. nó, reabertura, têmpera simulada, sensibilidade vs. VPP, encadeamento para trás, e uma lista de perguntas prováveis com resposta curta. Os exemplos numéricos vêm da execução real da semente de referência (20231045), não inventei nada — conferi rodando o código de novo agora antes de escrever.

2. O README não avisava sobre a reconstrução do gerador_pomar.py. Eu já tinha te contado isso em conversa, mas nunca ficou escrito no arquivo, e a Seção 3 desse roteiro é rígida sobre "não altere, copie exatamente". Não vou te mandar um README novo, porque o seu já está com os nomes de vocês e a matrícula 24114060 preenchidos, e eu não quero sobrescrever isso. Em vez disso, adicione esta linha na seção "Limitações conhecidas" do seu README:

- **`gerador_pomar.py`:** o PDF do enunciado perdeu a indentação do código ao virar texto (todas as linhas apareceram com o mesmo recuo). Reconstruímos a indentação seguindo a lógica óbvia do algoritmo (a lógica é a mesma; só a formatação foi inferida). Os resultados batem com a caixa de aferição do enunciado (matrícula 20231045: UCS=34, BFS=55/22 passos), o que confirma que a lógica ficou igual à do professor. Se o professor disponibilizar o arquivo original, substituam o nosso por ele e rodem `python src/teste_afericao.py` de novo.
O que já estava certo (conferi de novo, não é só repetição)
gerador_pomar.py não tem a lógica alterada, nenhuma matrícula fica hardcoded no código, bayes.py não arredonda no meio da conta, BFS continua pura (sem considerar custo), UCS/A* tratam reabertura corretamente e isso está comentado no código, o exemplo de h3 superestimando vem de execução real, e a seção 2.4 do relatório continua honestamente marcada como "a preencher" para a matrícula de vocês (não inventamos nenhum ponto de falha).
Como aplicar
Baixe o GUIA_ARGUICAO.md e arraste para a raiz do seu projeto no VS Code, do mesmo jeito que fez com o README e RELATORIO.
Adicione a linha acima no README, manualmente.
```

**Prompt 2:**

```
deixe o projeto mais simples pois existem coisas que nao entendo
```

**Resposta recebida (íntegra, texto do assistente; omitidas só as linhas de execução de comando):**

```
Vou fazer uma versão bem mais simples: código curto e comentado, sem gerador automático de
relatório e sem processos paralelos. O relatório passa a ser um texto que você edita.
Primeiro guardo a versão antiga e recomeço o repositório.

Simplifiquei o projeto e refiz o repositório do zero, ainda com 8 commits. Testei num clone
limpo e com 7 sementes diferentes. Roda tudo e bate com a caixa de aferição do enunciado.

O que mudou
- Código: caiu de cerca de 1.480 para 870 linhas.
- Menos sofisticação: saiu o gerador automático de relatório, os processos paralelos e as
  estruturas mais avançadas do Python. Ficaram if, for, funções e dicionários, com
  comentários em português.
- Relatório: agora o RELATORIO.md é um texto normal, com os números da matrícula de exemplo
  (20231045).
- main.py: imprime tudo e grava em resultados/saida.txt, para você copiar os números.
- Experimento de escala: separado em python src/escala.py <matricula>, porque é o único
  trecho pesado.
- Bug corrigido: achei um erro no main.py que só apareceria com algumas sementes, e já está
  corrigido.

O que você ainda precisa fazer
- Rodar com a matrícula do integrante mais velho.
- Trocar os números do RELATORIO.md e da tabela do README pelos de resultados/saida.txt.
- Preencher a identificação no README e os campos [PREENCHER] do ANEXO_IA.md.
- Fazer o push e trocar o autor dos commits. O colega precisa commitar do próprio usuário.
```

## A.3 Erros e imprecisões do assistente, com a evidência que os desmentiu

1. **Explicação errada do contraexemplo da DFS (bônus).** O assistente escreveu que a DFS desceria a coluna 0 e seguiria pela linha 7 (custo ≈ 53). **Evidência:** `python src/contraexemplo.py` deu custo **95**, com rota em *serpentina* (em (7,1) o Norte ainda está livre e vem antes do Leste). O contraexemplo continuava válido (95 > 2 × 14), mas o raciocínio estava errado e foi corrigido.
2. **Afirmação imprecisa sobre reabertura de nós** (primeira versão do texto): dizia que, para h3, reabrir nós “evita piorar a rota”. Errado: h3 é inadmissível e a reabertura não restaura a garantia de otimalidade. Corrigido antes da versão final.
3. **Na primeira versão (depois removida),** o relatório gerado automaticamente saiu com: “memória por estado ≈ 0 bytes” (erro de unidade: MB × 1024 em vez de × 1024²; **evidência:** leitura do `RELATORIO.md` gerado, e a previsão de limite de n só bateu com a medida depois da correção); e “118 estados; todos os 117 são alcançáveis” (**evidência:** o talhão (3,0) está cercado por `#`).
4. **Estatística fraca apresentada como evidência (primeira versão):** “em 30 de 30 execuções o melhor estado veio depois de uma piora aceita”. Com T0 alto quase toda execução aceita piora no início, então isso é quase tautológico. Passou a valer a comparação pareada (têmpera melhor em 22 de 30).
5. **Bug latente no `main.py` (simplificação):** ele assumia que o talhão (10,11) é livre, o que não vale para toda semente. **Evidência:** revisão do código antes de testar outras sementes; corrigido para usar um vizinho livre do objetivo.
6. **Formatação (simplificação):** a primeira saída do especialista escrevia as premissas em maiúsculas (`.upper()` demais), o que dificultava a leitura. Notado ao ver a saída real.
7. `[Falhou na atualização dos arquivos]` Algum erro que **a dupla** encontrou ao rodar/revisar. Se não acharam nenhum além dos acima, escrevam isso; se afirmarem que “o assistente não errou em nada”, terão de sustentar na arguição.

## A.4 O que eu sabia depois de rodar o código que não sabia lendo a resposta do assistente

`Só rodando o experimento de escala vimos que a DFS usa muito mais memória que a BFS, não menos. Antes de medir, parecia o contrário — a fronteira da DFS chegou a ser quase 900 vezes maior que a da BFS.`
