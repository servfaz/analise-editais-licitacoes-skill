# Fase 4 — Análise de PCFP da concorrente arrematante

## O que esta fase faz e o que não faz

Esta fase apoia o time comercial da Servfaz na fase de licitação em que a empresa concorrente arrematante é obrigada a reapresentar sua planilha de custos ajustada ao valor final ofertado. A fase compara essa planilha com a planilha modelo de referência, encontra inconsistências e, quando encontra pelo menos uma, redige um rascunho de carta de contestação ao pregoeiro.

A decisão de enviar essa carta ao órgão, ou de guardar o apontamento para uma futura intenção de recurso, é sempre humana. Não tome essa decisão nem sugira qual escolher — apresente a lista de inconsistências e o rascunho, e deixe a decisão para o analista/coordenador responsável.

Fora do escopo desta fase: análise de habilitação da concorrente, decisão sobre participar ou não de um edital, e a conversão da planilha modelo de PDF para Excel quando o órgão só disponibiliza o modelo em PDF (isso é trabalho manual da equipe, anterior a esta fase — se receber apenas um PDF sem estrutura de planilha, peça a versão em Excel em vez de tentar reconstruir as fórmulas).

## Princípio que rege toda a análise: semântica, não posição

Nunca identifique ou julgue um item da planilha pelo número do módulo ("módulo 1", "módulo 4.1", "item 3.2"). A numeração muda entre a IN 05, a IN 08 e as planilhas específicas de cada edital — a mesma posição aponta para conteúdo diferente dependendo do template. Identifique cada item pelo que ele representa (é um valor de salário? um percentual de encargo? uma base de cálculo de tributo?), não por onde está posicionado.

Reconhecer o tipo de planilha (IN 05, IN 08, planilha de grupo) é útil como atalho de busca, para achar o conteúdo mais rápido — mas nunca use esse tipo como critério para decidir se uma regra se aplica. A regra se aplica pelo conteúdo, não pelo template.

## Visão geral do fluxo

O fluxo completo tem três etapas, e cada uma pode ser executada de forma independente dependendo do que o analista já tem em mãos:

1. **Primeira entrada** — a partir do edital (e da planilha modelo), extrai os critérios de julgamento. Acontece antes de a concorrente virar arrematante, então normalmente ainda falta a CCT.
2. **Segunda entrada** — quando a concorrente arrematante reapresenta a planilha ajustada, compara essa planilha com a modelo e julga as diferenças usando os critérios (agora completos com a CCT).
3. **Validação e decisão final** — humana, fora do escopo desta fase.

Se a Fase 2 já tiver sido executada nesta conversa, reaproveite o levantamento dela (CCT, benefícios, encargos, conta vinculada, insalubridade, base tributária) como ponto de partida da etapa 1 e extraia apenas o que faltar, conferindo cada dado na fonte.

Se o analista já chegar com tudo em mãos (edital, planilha modelo, CCT e planilha da concorrente), rode a etapa 1 e a etapa 2 em sequência na mesma conversa. Se só tiver o edital, pare ao final da etapa 1 e explique o que falta para seguir.

## Etapa 1: primeira entrada (a partir do edital)

**Entrada esperada:** o edital e a planilha modelo (a planilha modelo já traz os valores de referência usados na comparação; costuma vir dentro do próprio edital). Se o analista só tiver a planilha modelo em PDF, sem Excel, não tente extrair fórmulas de dentro do PDF — avise que esse preparo é manual e peça a versão em Excel.

1. **Converta o edital para markdown.** Remova cabeçalho e rodapé repetidos em cada página, mas mantenha todo o restante do texto sem alterar uma palavra, e formate as tabelas corretamente. Depois de converter, confira o número de linhas e colunas de cada tabela extraída contra o PDF original — um erro de tabela aqui contamina toda a extração de regras que vem a seguir, então vale a pena essa checagem antes de seguir.

2. **Extraia os critérios de julgamento do edital**, identificando cada um pelo conteúdo semântico (ver `references/fase-4-pcfp/regras-conteudo.md` para as categorias e o que procurar em cada uma). Essa extração fica parcial nesta etapa: falta a CCT, que só chega na etapa 2, então itens que dependem dela (vale-alimentação, auxílio-creche, etc.) ficam marcados como pendentes.

3. **Verifique documentos referenciados e não enviados.** Se o edital citar um documento anexo (decreto, anexo remissivo) que não foi enviado junto, pare e peça esse documento ao analista antes de prosseguir. Quando ele chegar, reprocesse a conversão do edital incluindo esse documento — não pule direto para a extração de critérios com informação faltando.

4. **Verifique se a base de cálculo dos tributos está definida no edital.** Se não estiver explícita, pergunte ao analista usando exatamente estas três opções fixas (sem espaço para resposta livre — a ambiguidade aqui contamina o julgamento de diferenças mais adiante):
   - **Opção 1:** a base de cálculo incide sobre a soma de remuneração, benefícios e encargos sociais (padrão da maioria dos órgãos federais).
   - **Opção 2:** a base de cálculo incide apenas sobre a remuneração, com os encargos dos demais itens calculados em linhas separadas (modelo usado por empresas responsáveis por hospitais federais).
   - **Opção 3:** pausar e registrar necessidade de questionamento formal ao órgão antes de prosseguir.

   Ao apresentar essas opções, inclua a nota de contexto que está em `references/fase-4-pcfp/regras-conteudo.md` sobre o trade-off da opção 3 — ela não é sempre a mais segura do ponto de vista comercial, e quem responde precisa saber disso, não só ler o rótulo. Se a opção 3 for escolhida, não force uma continuação: registre que o fluxo aguarda resposta do órgão e pare a etapa 1 aqui. Se for a opção 1 ou 2, esse é o parâmetro de cálculo usado na etapa 2.

5. Com o documento faltante resolvido (se houve) e a base de cálculo definida (opção 1 ou 2), a etapa 1 está concluída. Resuma para o analista: os critérios extraídos até aqui, o que ainda depende da CCT, e o parâmetro de base de cálculo escolhido.

## Etapa 2: segunda entrada (comparação e julgamento)

Esta etapa só começa quando a concorrente arrematante reapresenta a planilha de custos ajustada ao valor final do lance — hoje esse acompanhamento é manual, então normalmente é o próprio analista que avisa que a planilha chegou.

**Entrada esperada:** a CCT aplicável e a planilha do concorrente.

1. **Complete os critérios pendentes da etapa 1 usando a CCT** — os itens que dependiam dela (valor de referência do vale-alimentação, exigência ou não de auxílio-creche, e outros listados em `references/fase-4-pcfp/regras-conteudo.md`). Use a capacidade de consulta de CCT descrita em `references/capacidades.md`; se ela não estiver disponível ou não retornar a CCT, use a CCT enviada pelo analista e registre a pendência de validação.

2. **Compare a planilha do concorrente com a planilha modelo, item a item, por conteúdo semântico** — não por posição/linha. Trate como o mesmo item dois valores que representam a mesma coisa mesmo que estejam em linhas ou módulos diferentes entre as duas planilhas.

3. **Julgue cada diferença encontrada contra os critérios completos**, classificando-a como:
   - **Inconsistência real** — viola um critério (valor fixo divergente sem justificativa, fora da faixa de tolerância, base de cálculo não condizente com o parâmetro definido na etapa 1, etc.)
   - **Variação aceitável** — dentro de faixa de tolerância documentada (ex.: RAT ajustado pelo FAP entre 0,5% e 6%; demais faixas em `references/fase-4-pcfp/regras-conteudo.md`) ou justificada por diferença legítima de estratégia/regime.

   Preste atenção especial ao padrão mais comum apontado pelo time: concorrentes mudando a base de cálculo dos tributos para conseguir um preço menor, sem manter a mesma referência — isso é o tipo de inconsistência que mais embasa contestação.

4. **Gere a saída:**
   - Se houver pelo menos uma inconsistência real: produza (a) a lista de inconsistências e (b) um rascunho de carta de contestação (ver formatos abaixo).
   - Se não houver nenhuma: avise o analista de que a planilha do concorrente não apresentou inconsistências frente aos critérios aplicados e apresente a lista de variações aceitáveis examinadas. Não gere rascunho de carta neste caso.

### Formato da lista de inconsistências

Apresente como tabela, uma linha por inconsistência, com estas colunas: **Item** (identificado por conteúdo semântico, nunca por número de módulo) | **Critério violado** | **Planilha modelo** | **Planilha do concorrente** | **Classificação** (inconsistência real ou variação aceitável, com a variação aceitável também listada para transparência, mas deixada fora da carta). Isso deixa rastreável exatamente o que embasa cada ponto da carta. Nas colunas de critério e de valores, indique a fonte no padrão `(Documento, item/cláusula, pág. X)` ou a célula/linha da planilha.

### Formato do rascunho de carta

Não existe template fixo para a carta — ela é sempre gerada a partir da lista de inconsistências daquela licitação específica, não preenchida em um molde genérico. Ainda assim, siga estes princípios ao redigir:

- Tom formal e respeitoso, dirigido ao pregoeiro.
- Vai no corpo do e-mail, não como documento anexo separado — o time técnico do órgão já sabe localizar os pontos indicados no corpo do texto.
- Organizada como listagem das inconsistências identificadas, cada uma explicando objetivamente o que diverge e por quê (o critério, não o número do módulo).
- Cite a fonte de cada critério (edital, CCT, comprovante) conforme `references/regras-gerais.md`. Fundamento legal só entra se constar do material ou de `references/estudo/catalogo-fontes.md` com status conferido; caso contrário, omita ou marque como pendente de validação jurídica.
- Não inclua nenhuma recomendação sobre enviar a carta ou guardá-la para recurso — isso é decisão humana, fora do escopo desta fase.

## Etapa 3: validação e decisão final (fora do escopo automatizado)

Depois de gerar a lista de inconsistências e o rascunho, o trabalho desta fase termina. Informe que, se o analista optar pelo recurso, a Fase 5 usa esta lista como base. A validação do conteúdo e a decisão de enviar a carta ao pregoeiro (por e-mail, com cópia para o comercial) ou guardar o apontamento para uma futura intenção de recurso são sempre do analista, sem etapa de aprovação de coordenador nesse fluxo. Não tome essa decisão por eles nem sugira qual escolher.

## Referências

- `references/fase-4-pcfp/regras-conteudo.md` — as categorias semânticas de itens da planilha (remuneração, benefícios, encargos sociais, tributos), a fonte de cada critério (CCT, edital, comprovante) e a regra de julgamento, mais a nota de contexto completa sobre o trade-off da opção 3 da base de cálculo. Consulte sempre que for extrair critérios ou julgar uma diferença — é a base de todo o julgamento da etapa 2.
