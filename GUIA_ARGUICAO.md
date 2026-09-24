# Guia para a arguição

Este arquivo não é para entregar como parte da nota — é para vocês estudarem antes dos 10 minutos de arguição. Na hora, vocês recebem uma semente nova e precisam rodar o próprio código e responder perguntas sobre decisões dele. Os números de exemplo abaixo são da matrícula de referência do enunciado, **20231045** (a mesma da caixa de aferição), obtidos rodando `python src/main.py 20231045`. Troquem mentalmente pelos números da sua semente quando forem explicar.

## Como cada busca funciona, em uma frase

- **BFS:** anda em "camadas" a partir do portão, visitando primeiro tudo que está a 1 passo, depois a 2 passos, etc. Para na primeira vez que alcança o objetivo. Não olha custo, só a quantidade de passos.
- **DFS:** desce por um caminho até o fim antes de tentar outro. Usa uma pilha em vez de uma fila. Guardamos os estados já visitados para não entrar em loop.
- **UCS:** como a BFS, mas em vez de tirar o próximo da fila por ordem de chegada, tira sempre o de **menor custo acumulado**. Isso garante achar a rota mais barata.
- **A\*:** igual ao UCS, mas prioriza por `custo acumulado + estimativa do que falta` (`g + h`). Se a estimativa nunca superestima, ele continua achando a rota ótima, só que explorando menos nós.

## Por que a BFS pode ser mais cara que a UCS

Na nossa semente de referência: BFS custou **55** com **22** passos; UCS custou **34**, também com **22** passos.

A BFS escolhe a rota com **menos passos**, não a de menor custo. No nosso pomar um passo custa 1 (`.`) ou 4 (`~`), então uma rota "curta em passos" pode passar por vários talhões caros e sair mais cara no total. A BFS só seria ótima em custo se todo passo custasse o mesmo — no enunciado, isso não acontece. Essa é exatamente a hipótese da Aula 03 que o item 2.3 do relatório cita: **custo de passo uniforme**, violada aqui.

*Se perguntarem "isso é bug?":* não. É esperado, e o próprio enunciado pede para explicar por quê (item 2.3).

## Como a UCS encontra o menor custo

A UCS usa uma fila de prioridade (`heapq` no nosso código) ordenada por `g(n)`, o custo acumulado desde o início. Ela expande sempre o nó mais barato da fronteira. Quando descobre um caminho mais barato para um estado que já tinha visto, ela **atualiza** o custo e recoloca o estado na fila (no código, isso é a condição `if g_novo < melhor_g.get(viz, infinito)`). Por isso ela nunca "trava" numa rota ruim: sempre existe a chance de substituir por algo mais barato antes de fechar o estado.

## Como o A\* funciona

O A\* soma dois números para decidir o que expandir primeiro: `g(n)` (quanto já custou chegar até ali) e `h(n)` (quanto o algoritmo *estima* que falta). Ele expande o nó de menor `g + h`. Quando `h(n) = 0` sempre, o A\* vira exatamente a UCS — é por isso que **h1** (a heurística zero) dá o mesmo custo e o mesmo número de nós expandidos que a UCS na nossa tabela (ambos: custo 34, 111 nós).

## Por que h2 é admissível

h2(n) é a distância de Manhattan até o objetivo: `|11−i| + |11−j|`. Uma heurística é admissível quando **nunca superestima** o custo real que falta.

Prova simples: para sair de um talhão (i,j) até (11,11), o agente precisa fazer no mínimo `|11−i| + |11−j|` movimentos (não tem como fazer menos, mesmo em linha reta na grade). Cada movimento entra em um talhão que custa **pelo menos 1** (o carreador `.` é o mais barato que existe). Então o custo real de qualquer caminho é `≥ 1 × Manhattan(n) = h2(n)`. Como h2 nunca passa do valor real, ela é admissível.

Na nossa execução, o A\* com h2 achou a mesma rota ótima da UCS (custo 34) expandindo só 90 nós, contra 111 da UCS — mais rápido e ainda garantidamente ótimo.

## Por que h3 pode não ser admissível

h3(n) = 4 × Manhattan(n). Ela multiplica a estimativa por 4, e isso pode passar do custo real. No nosso pomar, o talhão (0,0) tem Manhattan = 22 até o objetivo, então h3 estima **88**. Mas o custo real de sair de (0,0) até o objetivo é só **34** (o valor da UCS). Como 88 > 34, h3 **superestima**, e isso é o suficiente para provar que ela é inadmissível — não precisa checar todos os estados, um caso concreto já basta.

*Curiosidade que vale saber:* mesmo sendo inadmissível, h3 pode ainda "acertar" o custo ótimo em algumas grades (foi o que aconteceu na nossa semente de referência: custo 34, igual ao UCS). Isso **não prova** que ela é admissível — é só sorte daquela grade. Se perguntarem isso, a resposta certa é "não, admissibilidade é uma garantia para todo estado, não uma observação de um caso".

## Diferença entre estado e nó

**Estado** é a posição (i,j) no pomar — só isso. **Nó** é um "registro" de busca: guarda o estado, mas também de onde veio (o pai) e quanto já custou chegar ali. O mesmo estado pode aparecer em vários nós diferentes durante a busca, se houver mais de um jeito de chegar até ele. É exatamente por isso que a DFS pode "descobrir" o mesmo talhão duas vezes por caminhos diferentes: são nós diferentes carregando o mesmo estado. Se a busca não guarda quais estados já visitou, ela pode ficar repetindo o mesmo lugar para sempre (loop infinito) — por isso todas as nossas buscas guardam um conjunto de "explorados".

## O que significa "reabrir" um estado

Nas nossas UCS e A\*, quando encontramos um caminho **mais barato** para um estado que já tínhamos visto, nós atualizamos o custo dele e colocamos ele de volta na fronteira, mesmo que já tivesse sido expandido antes. Isso é "reabrir". Sem isso, o algoritmo poderia ficar preso numa rota subótima só porque chegou primeiro naquele estado por um caminho caro.

## Por que a têmpera simulada aceita pioras

A subida de encosta só troca de estado se o vizinho for **melhor**. Isso significa que, assim que todo vizinho é pior, ela para — mesmo que exista uma solução melhor "do outro lado" de um vale que ela precisaria atravessar piorando primeiro. É o problema clássico do **ótimo local**.

A têmpera simulada aceita um vizinho pior com uma certa probabilidade, que cai com o tempo (a "temperatura" esfria). No começo (T alto) ela aceita pioras com mais facilidade, o que permite atravessar esses vales; no fim (T baixo) ela quase só aceita melhorias, refinando a solução como a subida de encosta faria. Na nossa execução de referência, ela aceitou centenas de movimentos piores por execução — e isso é o mecanismo funcionando, não um erro.

## Sensibilidade x Valor Preditivo Positivo (VPP)

São duas perguntas diferentes:
- **Sensibilidade** = "se o talhão está infestado, qual a chance do sensor dar positivo?" (`P(+|infestado)`)
- **VPP** = "se o sensor deu positivo, qual a chance do talhão estar realmente infestado?" (`P(infestado|+)`)

O laudo do fornecedor (Parte 5) confunde essas duas coisas, dizendo que 99% de sensibilidade significa que 99% dos alertas são verdadeiros. Isso está errado porque o VPP depende também da **prevalência** (quão rara é a praga) e da **taxa de falso positivo**. Quando a doença é rara, mesmo um sensor bom gera muitos alertas falsos, porque o número de talhões *sadios* é muito maior que o de infestados — e mesmo uma taxa pequena de falso positivo sobre esse número grande produz bastante alerta errado.

## Como o sistema especialista faz encadeamento para trás

O programa começa pela **conclusão que quer provar** (por exemplo, "inspecionar com prioridade alta?") e procura, entre as regras, uma cuja conclusão seja essa. Depois tenta provar cada premissa dessa regra, uma por uma — e cada premissa pode ser um fato dado direto ou a conclusão de **outra** regra, que é provada do mesmo jeito, recursivamente. Se todas as premissas forem provadas, a conclusão é aceita e a regra entra na "cadeia" que sustenta a resposta. É "para trás" porque a busca começa no objetivo e vai regredindo até os fatos, ao contrário de sair dos fatos e ver aonde eles levam.

---

## Perguntas que o professor pode fazer, com resposta curta baseada no nosso código

**"Por que a fronteira máxima da BFS é esse número e não o dobro?"**
Porque a fronteira só guarda nós **gerados e ainda não expandidos**. Os nós já expandidos saem da fronteira e ficam só no dicionário de "pais", que não conta. Na semente de referência a fronteira máxima da BFS foi 13, bem menor que os 114 nós expandidos no total.

**"Sua DFS reabre estados?"**
Não. A nossa DFS usa um conjunto de "explorados" e nunca revisita um estado que já colocou nesse conjunto. Só a UCS e o A\* reabrem (atualizam o custo de um estado já visto se acham caminho mais barato).

**"Por que vocês usam busca em grafo e não em árvore?"**
Porque em árvore (sem lembrar visitados) o número de nós pode explodir exponencialmente, já que o agente pode ir e voltar entre dois talhões vizinhos infinitas vezes. Guardando os visitados, o número de nós fica limitado ao número de estados (aqui, no máximo 144 talhões).

**"O que aconteceria se vocês trocassem a ordem dos vizinhos?"**
A BFS, UCS e A\* continuariam achando o mesmo custo ótimo (a ordem só muda o **desempate** entre rotas de custo igual). Já a DFS pode mudar bastante, porque ela segue o primeiro vizinho da lista até o fim antes de voltar — é por isso que o enunciado pede para declarar e manter fixa a ordem, e é a base do contraexemplo do bônus.

**"Por que o A\* com h1 dá exatamente os mesmos números que a UCS?"**
Porque h1(n) = 0 sempre. Nesse caso a fórmula do A\* (`g + h`) vira só `g`, que é exatamente o critério da UCS. A\* com h1 **é** a UCS, só com outro nome.

**"Como vocês sabem que o VPP calculado está certo?"**
Aplicamos direto a fórmula de Bayes com os números que `parametros_sensor(matricula)` devolveu (não escolhemos nenhum valor à mão), e mostramos a substituição passo a passo no relatório (item 4.3a), sem arredondar no meio da conta.

**"Por que vocês modelaram a busca local como troca de um talhão por outro, e não de outro jeito?"**
Porque o problema pede escolher **exatamente K talhões** de um conjunto maior — trocar um dentro pelo um fora é o jeito mais simples de gerar vizinhos que sempre respeitam esse tamanho fixo, sem precisar de nenhuma correção extra depois.
