# ANEXO_IA.md — Uso de assistentes de IA (Parte 6)

> ⚠ **Este arquivo foi redigido pelo próprio assistente com base no que aconteceu na sessão. A dupla precisa ler, conferir e completar os campos `[PREENCHER]` com a sua experiência real antes de entregar.** O enunciado zera as Partes 5 e 6 se o anexo for genérico ou fabricado; na arguição vocês terão de sustentar cada linha.

## A.1 Ferramentas usadas e em que partes

- **Claude (Anthropic)**, no chat do claude.ai com ambiente de execução de código. Escreveu o código de `src/` (buscas, busca local, especialista, Bayes, escala, contraexemplo, main), o `RELATORIO.md`, o `README.md` e dividiu o trabalho em 8 commits. Numa primeira versão o projeto era maior (com um gerador automático de relatório); a pedido do aluno, foi simplificado.
- O **`gerador_pomar.py` não foi escrito nem modificado pelo assistente**: foi copiado do enunciado (só se reconstruiu a indentação, que o PDF perdeu).
- `[PREENCHER]` Outras ferramentas usadas pela dupla e o que cada integrante fez, rodou e revisou.

## A.2 Dois prompts na íntegra, com a resposta recebida

**Prompt 1** (com o PDF do enunciado anexado):

```
faca, e divida em 8 commits
```

**Prompt 2:**

```
deixa mais simples, pq n sou tao bom assim em python haha
```

**Respostas recebidas:** `[PREENCHER: colar aqui as respostas do chat na íntegra. O assistente não consegue reproduzir o texto exato das mensagens anteriores da conversa; copiem do histórico do chat.]`

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
