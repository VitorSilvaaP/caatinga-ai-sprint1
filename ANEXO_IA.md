# ANEXO_IA.md — Uso de assistentes de IA (Parte 6)

> ⚠ **Este arquivo foi redigido pelo próprio assistente com base no que aconteceu na sessão. A dupla precisa ler, conferir e completar os campos `[PREENCHER]` com a sua experiência real antes de entregar.** O enunciado zera as Partes 5 e 6 se o anexo for genérico ou fabricado; na arguição vocês terão de sustentar cada linha.

## A.1 Ferramentas usadas e em que partes

- **Claude (Anthropic)**, no chat do claude.ai com ambiente de execução de código. Escreveu o código de `src/` (buscas, busca local, especialista, Bayes, escala, contraexemplo, main), o `RELATORIO.md`, o `README.md` e dividiu o trabalho em 8 commits. Numa primeira versão o projeto era maior (com um gerador automático de relatório); a pedido do aluno, foi simplificado.
- O **`gerador_pomar.py` não foi escrito nem modificado pelo assistente**: foi copiado do enunciado (só se reconstruiu a indentação, que o PDF perdeu).
- Ferramentas e tarefas da dupla (preencher o nome de quem fez cada uma):

**Vitor:** _______________________________________________

**Emylly:** _______________________________________________

Lista de tarefas para dividir entre os dois nomes acima:
  - [ ] Instalar dependências (`pip install -r requirements.txt`)
  - [ ] Rodar `python src/teste_afericao.py` e conferir "TUDO CERTO"
  - [ ] Rodar `python src/main.py <matricula>` com a matrícula real
  - [ ] Rodar `python src/escala.py <matricula>` (Parte 2.4)
  - [ ] Abrir `resultados/saida.txt` e conferir os números
  - [ ] Ler o `RELATORIO.md` inteiro e comparar com o PDF
  - [ ] Preencher identificação (nomes/matrículas) no `README.md`
  - [ ] Preencher seção 2.4 e item 5 da Parte 5 do `RELATORIO.md`
  - [ ] Revisar o `GUIA_ARGUICAO.md`
  - [ ] Configurar `git config user.name`/`user.email`
  - [ ] Clonar o repositório
  - [ ] Fazer commits e `git push`
  - [ ] Testar o projeto do zero em outra máquina
  - [ ] Abrir o repositório numa janela anônima (conferir público)
  - [ ] Conferir que não subiu `venv/` nem `__pycache__/`
  - [ ] Preencher os campos restantes deste `ANEXO_IA.md` (abaixo)

## A.2 Dois prompts na íntegra, com a resposta recebida

**Prompt 1:**

```
confira se esta tudo correto de acordo com o pdf q te mandei no comeco. Se voce tiver trocado alguma coisa me diga.
```

**Resposta recebida (íntegra, texto do assistente; omitidas só as linhas de execução de comando):**

```
Vou conferir item por item contra o PDF, olhando os arquivos de verdade e não só a minha
memória.

Estrutura e formatos batem. Agora o conteúdo do relatório contra o que cada item pede.

Conferi contra o PDF. O repositório atende quase tudo, mas encontrei 4 lacunas (já
corrigidas) e alguns pontos que você precisa saber. O commit final foi refeito (--amend),
então continuam 8 commits, e o zip foi atualizado.

Lacunas que corrigi
- Bônus (Liga de IA): o PDF pede a grade, a rota da DFS, a rota ótima e os dois custos. Eu só
  tinha descrito a rota da DFS em palavras. Agora está a rota completa (56 passos, custo 95)
  e a ótima (custo 14).
- 4.2: o PDF pede "mostre o traço de execução antes e depois". Eu só tinha um resumo. Agora
  os dois traços estão no relatório.
- Recomendação da Parte 5: o limite é 8 linhas e o meu texto tinha uns 9. Encurtei para 656
  caracteres.
- Unidades nas tabelas: o PDF desconta 0,2 por tabela sem unidade. Acrescentei "(nº)" em
  "Passos" e "Nós expandidos".

O que estava certo
- Estrutura: todos os arquivos pedidos existem, e o cabeçalho do resultados.csv é
  exatamente o do enunciado.
- pomar.txt: a matrícula está na 1ª linha.
- Gráfico: tem eixos rotulados.
- Caixa de aferição: os valores batem.
- README: os 7 itens, na ordem pedida.
- Regras: 8 regras (limite do PDF é 8), 30 execuções na busca local e os quatro contadores
  nas buscas.
- Parte 5: as 5 afirmações têm veredito com número medido.

O que eu troquei ou assumi
- gerador_pomar.py: o PDF perdeu a indentação, então reconstruí com 4 espaços. A lógica é a
  mesma (os números batem), mas os bytes podem diferir do original.
- Semente: usei a matrícula fictícia 20231045, não a de vocês.
- Aulas 02 a 05: não tenho o material. Assumi as seis dimensões, os cinco tipos de agente e
  as fórmulas de complexidade do AIMA.
- Experimento de escala (2.4): o limite de 60 s é checado dentro do código, a memória não é
  medida.
- Busca local (3.4): o mapa de risco, a conversão de 3 min por unidade de custo e a
  penalidade são invenções minhas, declaradas como premissas no relatório.
- Condição da 3.3 (limites de 200 ms e 10%): são valores que eu propus, marcados como "a
  validar".
- Regras do especialista: troquei o exemplo do PDF por fatos booleanos.
- Fronteira máxima do UCS/A*: conto estados distintos esperando, não o tamanho bruto da
  fila.

Pontos que ainda não atendem o PDF
- Histórico de commits: os 8 commits foram feitos por mim, todos no mesmo autor. O PDF
  exige commits distribuídos e de ambos os integrantes, no próprio usuário.
- ANEXO_IA.md: tinha campos [PREENCHER].
- README e RELATORIO.md: tinham nomes, matrículas e números da semente de exemplo.
- PDF do AVA: não gerado.
```

**Prompt 2:**

```
deixa mais simples, pq n sou tao bom assim em python haha
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
7. `[PREENCHER]` Algum erro que **a dupla** encontrou ao rodar/revisar. Se não acharam nenhum além dos acima, escrevam isso; se afirmarem que “o assistente não errou em nada”, terão de sustentar na arguição.

## A.4 O que eu sabia depois de rodar o código que não sabia lendo a resposta do assistente

`[PREENCHER — uma frase da dupla com algo que só o experimento mostrou. Exemplos de fatos que este experimento revela (escolham só se for verdade para vocês): a BFS pode devolver rota 62% mais cara que a ótima mesmo com o menor número de passos; a DFS estoura o tempo antes da BFS por causa da fronteira enorme.]`
