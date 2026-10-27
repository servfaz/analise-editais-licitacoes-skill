# Modelos da peça final

Esta pasta guarda os modelos da peça de impugnação e da peça de esclarecimento. Este arquivo é o contrato que eles seguem, para que a skill, os modelos e o script de montagem possam ser feitos em momentos diferentes sem se desencontrar.

**Situação atual:** os modelos `modelo-impugnacao.md` (versão 2: o pedido c) só fala em subsidiários quando há) e `modelo-esclarecimento.md` (versão 1), a partir da peça da FMS, estão nesta pasta, revisados pelo analista, e a Fase 5 do `SKILL.md` monta a peça com eles. O `estado.py` só procura modelo diretamente nesta pasta; rascunho de modelo novo fica em `assets/rascunho/`, que ele não lê.

## Se o modelo faltar: a skill para no passo da peça

Se o modelo de um tipo sumir desta pasta (removido ou renomeado), quando todas as minutas selecionadas estiverem aprovadas ou descartadas, a skill:

1. roda `estado.py peca --pasta <pasta> --acao verificar` e lista ao analista as minutas aprovadas por tipo (ID e versão);
2. lembra os itens em "avaliar depois", com o prazo, e pergunta se ele quer decidir algum agora;
3. informa o analista de que não há modelo em `assets/` e de que a peça final será montada quando ele existir;
4. para aí, sem perguntar o formato da peça, que só faz sentido com modelo.

O `estado.py peca --acao confirmar` recusa a confirmação enquanto não houver modelo, antes mesmo de conferir a frase do analista. Ele procura o modelo só nesta pasta, sem opção para apontar outra, e não olha subpastas como `rascunho/`. A skill não contorna a recusa: não gera PDF, DOCX nem uma "peça consolidada" improvisada, não cria nem altera arquivos nesta pasta e não move os rascunhos. Uma peça montada sem o modelo revisado sairia sem a qualificação, o endereçamento e o fecho conferidos, e poderia ser protocolada assim por engano. As minutas aprovadas em `minutas/` são a entrega desta etapa.

## Arquivos

| Arquivo | Uso |
| :-- | :-- |
| `modelo-impugnacao.md` | Texto da peça de impugnação, com marcadores |
| `modelo-esclarecimento.md` | Texto da peça de pedido de esclarecimento, com marcadores |

O `estado.py peca` só reconhece, nesta pasta, o nome exato `modelo-<tipo>.<extensão>`, com uma extensão só e arquivo não vazio. Cópia de editor (`modelo-impugnacao.md~`, `.bak`, `.swp`), arquivo oculto, arquivo com sufixo a mais ou arquivo em subpasta não conta como modelo: não é o arquivo revisado. Mantenha um arquivo por tipo: se houver mais de um, o script usa o primeiro em ordem alfabética. O timbre não tem o prefixo `modelo-` e não interfere nessa busca.

A referência de estilo é uma só: a peça da Servfaz ao Pregão Eletrônico 111/2026 da Fundação Municipal de Saúde de Teresina (impugnação e esclarecimentos no mesmo arquivo). Os modelos separam as duas partes, porque o contrato prevê uma peça por tipo.

## O que o modelo traz

O modelo é o texto fixo da peça, revisado pelo analista. A skill não escreve nem altera essas partes:

- **Endereçamento:** a autoridade a quem a peça se dirige, o setor e o endereço do órgão e a linha "Referente", com os marcadores do certame. Servidor só pelo cargo, nunca pelo nome.
- **Qualificação da impugnante:** razão social, CNPJ e sede da Servfaz. Hoje há um só bloco; outra empresa do grupo exigiria um bloco condicional próprio, revisado como o resto do modelo.
- **Tempestividade e cabimento:** o parágrafo do art. 164 (`EXT-LEI14133-ART164`), com as datas preenchidas. As minutas não repetem esse parágrafo (`references/minuta-por-ponto.md`, seção 4).
- **Texto de fechamento:** na impugnação, a seção opcional "Da necessidade de saneamento e da republicação" e os pedidos gerais; no esclarecimento, o pedido de divulgação das respostas.
- **Fecho:** local, data e o bloco de assinatura.

Dados de pessoa física (nome e cargo de quem assina) **não entram no git**. Eles ficam em `<raiz>/files/representante.json`, fora do controle de versão (`files/` está no `.gitignore`), com as chaves `nome`, `cargo` (como sai na assinatura, por exemplo "Sócia Administradora") e `designacao` (como sai na qualificação, por exemplo "sua sócia administradora"). O modelo só traz os marcadores. Mesmo com esses dados, a skill não assina, não protocola e não envia a peça.

### O catálogo não aparece na peça

O catálogo de fontes é um referenciador interno da skill. A peça, o modelo e a peça montada não o mencionam de forma alguma: nem ID (`EXT-…`, `INT-…`, `NOVA-…`), nem status ("conferido", "a conferir"), nem a palavra "catálogo". A norma aparece na peça só pela citação jurídica usual ("art. 164 da Lei nº 14.133/2021").

- **No modelo:** o texto fixo não leva marcador. Cada norma que ele cita foi conferida no catálogo quando o modelo foi revisado, e o registro dessa conferência fica só aqui, abaixo.
- **Nas minutas:** os marcadores `[ID · status]` existem para a auditoria de cada minuta e são retirados na montagem, junto com o resto do que não vai à Administração (seção "Como os pontos são montados").
- **Trava:** depois de montar, o script procura na peça um ID (`EXT-`, `INT-`, `NOVA-`), um marcador no formato `[… · …]`, "catálogo de fontes" e nomes de arquivos do estudo (`catalogo-fontes`, `indice-fontes`, `references/estudo`, `<documento>/fontes.md`), além de `{{` não preenchido. Se achar algum, para e informa a linha, sem gravar a peça. "Catálogo" sozinho não conta, porque um edital pode citar o Catálogo de Serviços. A correção vai na origem (modelo, ou minuta reaberta pela fase certa), nunca na peça montada.

Normas do texto fixo, conferidas no catálogo na revisão do modelo (registro interno; não vai à peça):

| Norma no modelo | ID | Status | Onde aparece |
| :-- | :-- | :-- | :-- |
| Art. 164 da Lei 14.133/2021 (prazo; resposta divulgada no sítio oficial) | `EXT-LEI14133-ART164` | conferido | Qualificação, tempestividade, pedidos a) e e), pedido final do esclarecimento |
| Art. 55, § 1º, da Lei 14.133/2021 (nova divulgação) | `EXT-LEI14133-ART55` | conferido | Seção de saneamento, pedido d), pedido final do esclarecimento |
| Art. 5º da Lei 14.133/2021 (motivação) | `EXT-LEI14133-ART5` | conferido | Pedido f) |

Nada no texto fixo é citado de memória. Por isso o modelo não traz jurisprudência fixa, e o dever de motivação é citado pelo art. 5º da Lei 14.133 (nacional), não pela Lei 9.784/1999 (federal, União), que cederia ao regulamento do ente.

## Convenções do Markdown dos modelos

O conversor lê só o que está abaixo. O resto do Markdown não é usado nos modelos.

| No modelo | Na peça (.docx) |
| :-- | :-- |
| Bloco `---` no início (front matter) | Ignorado: identifica o modelo e a versão |
| `# TÍTULO` | Seção com numeração romana automática (I., II., III...), negrito e caixa alta |
| Parágrafo comum (separado por linha em branco) | Parágrafo justificado, Times New Roman 12,5 pt |
| Linhas seguidas sem linha em branco | Linhas do mesmo bloco, uma por parágrafo, sem espaço entre elas (assinatura) |
| `> texto` | Citação recuada, em itálico |
| Lista `1.` | Alíneas com numeração automática a), b), c); o último item que sair termina em ponto final, mesmo que o modelo traga ";" |
| `**negrito**`, `_itálico_` | Negrito, itálico |
| `<!-- centralizado -->` … `<!-- /centralizado -->` | Parágrafos centralizados |
| `{{CAMPO}}` | Valor do campo (tabela abaixo) |
| `{{#CAMPO}}` … `{{/CAMPO}}` | O trecho só sai se o campo estiver preenchido ou marcado. Vale dentro da linha e em linhas inteiras |

O modelo não usa marcador de fonte `[ID · status]` (ver "O catálogo não aparece na peça").

Campo sem valor que não esteja dentro de um bloco condicional interrompe a montagem, com a lista do que falta. A peça não sai com `{{...}}` no texto.

## Campos

| Marcador | O que vai | De onde vem |
| :-- | :-- | :-- |
| `{{DESTINATARIO}}` | Cargo e órgão do destinatário, em maiúsculas, com o artigo: "PREGOEIRO DA FUNDAÇÃO MUNICIPAL DE SAÚDE DE TERESINA" | `dados-peca.json` |
| `{{SETOR_ORGAO}}` | Setor responsável pela licitação | `dados-peca.json` |
| `{{ENDERECO_ORGAO}}` | Endereço do órgão | `dados-peca.json` |
| `{{CERTAME}}` | Modalidade, número e ano: "Pregão Eletrônico nº 111/2026" | `estado.json` (certame) |
| `{{PROCESSO}}` | Processo administrativo; vazio se "não informado" | `documentos.md`, linha "Processo administrativo" |
| `{{UASG}}` | Código da UASG, se houver | `dados-peca.json` |
| `{{ITEM_IMPUGNACAO}}` | Item do edital que regula impugnação e esclarecimento, iniciado por substantivo masculino: "item 19.1" | `dados-peca.json` |
| `{{OBJETO}}` | Objeto da licitação, em minúscula inicial, como no edital | `dados-peca.json` |
| `{{DATA_ABERTURA}}` | Data da sessão pública, dd/mm/aaaa | `estado.json` (prazo, `abertura`) |
| `{{DATA_LIMITE}}` | Data-limite do art. 164, dd/mm/aaaa | `estado.json` (prazo, `data_limite`) |
| `{{DATA_PECA}}` | Data da peça, dd/mm/aaaa | Dia da montagem |
| `{{DATA_PECA_EXTENSO}}` | Data da peça por extenso: "9 de setembro de 2026" | Dia da montagem |
| `{{REPRESENTANTE_NOME}}`, `{{REPRESENTANTE_CARGO}}`, `{{REPRESENTANTE_DESIGNACAO}}` | Quem assina | `files/representante.json`; nunca a skill |
| `{{PONTOS}}` | Os pontos, montados das minutas aprovadas (seção abaixo) | `minutas/<ID>.md`, versão aprovada |
| `{{QUADRO_RESUMO}}` | Tabela # / Cláusula impugnada / Vício / Pedido principal (impugnação, formato único) | Cabeçalho das minutas IMP aprovadas |
| `{{FAIXA_PONTOS}}` | Remissão aos tópicos: "dos itens III.1 a III.8" ou "do item III.1" | Número de pontos montados |

Blocos condicionais:

| Bloco | Quando sai | De onde vem |
| :-- | :-- | :-- |
| `{{#PROCESSO}}`, `{{#UASG}}` | Campo preenchido | Como na tabela de campos |
| `{{#FORMATO_UNICO}}` | Peça em formato único | Frase de confirmação do analista (`estado.json`, `peca`) |
| `{{#SUBSIDIARIOS}}` | Alguma minuta da peça tem pedido subsidiário (o pedido c) fala em "pedidos principais e subsidiários"; sem ele, só em "pedidos") | Minutas aprovadas da peça, seção "Pedido subsidiário" |
| `{{#ATUAL_PRESTADORA}}` | A Servfaz é a atual prestadora dos serviços ao órgão | Escolha do analista, a cada peça |
| `{{#REPUBLICACAO}}` | Seção "Da necessidade de saneamento e da republicação" e, no pedido d), a nova divulgação com reabertura do prazo. Sem ela, a seção sai inteira e as seguintes são renumeradas | Escolha do analista, a cada peça: cabe quando as correções pedidas alteram a formulação das propostas |
| `{{#EFEITO_SUSPENSIVO}}` | Pedido de suspensão da sessão | Escolha do analista, a cada peça |
| `{{#PROVA_DOCUMENTAL}}` | Pedido de produção de prova documental | Escolha do analista, a cada peça |
| `{{#PROTESTO}}` | Protesto por medidas judiciais e controle externo | Escolha do analista, a cada peça |

Os cinco opcionais nunca vêm marcados por padrão: o analista escolhe cada um a cada peça, e a escolha fica em `dados-peca.json`.

### `dados-peca.json`

Fica na pasta do edital. A skill o preenche na Fase 5 a partir do edital (com o localizador de cada dado) e o analista confere antes da montagem:

```json
{
  "destinatario": "PREGOEIRO DA FUNDAÇÃO MUNICIPAL DE SAÚDE DE TERESINA",
  "setor_orgao": "Diretoria de Compras Públicas",
  "endereco_orgao": "Rua Exemplo, 100, Bairro, Cidade/UF, CEP 00.000-000",
  "uasg": "977337",
  "item_impugnacao": "item 19.1",
  "objeto": "a contratação de empresa especializada na prestação de serviços ...",
  "opcionais": {
    "atual_prestadora": false,
    "republicacao": false,
    "efeito_suspensivo": false,
    "prova_documental": false,
    "protesto": false
  }
}
```

## Como os pontos são montados

Ficam de fora da peça o cabeçalho da minuta (salvo os campos do quadro), as "Provas e anexos indicados" e as "Pendências de conferência". Os subtítulos internos saem e os parágrafos são renumerados, ou seja, perdem o número. Os marcadores `[ID · status]` são retirados, com o espaço que os precede, e a trava de referências internas roda sobre o resultado. A página vai como a Administração a vê: "página PDF 23" vira "página 23" e, com a impressa ao lado ("página PDF 52, página impressa 18"), fica só a impressa ("página 18"). Citações (`>`) continuam recuadas.

**Impugnação.** Cada minuta IMP aprovada, na ordem dos IDs, vira um tópico do item III:

1. subtítulo em negrito e caixa alta: "III.<n> – <TÍTULO DA MINUTA>";
2. texto corrido, nesta ordem: "Dos fatos", "Normas e jurisprudência", "Aplicação ao caso" e "Resposta ao contraponto da Administração";
3. fecho do tópico: "Desta forma, **IMPUGNA-SE** o edital e seus anexos, requerendo-se:", seguido do pedido principal e, se houver, do subsidiário, iniciado por "subsidiariamente,";
4. se houver redação retificadora: "Sugere-se a seguinte redação:", seguida das redações em citação recuada.

O quadro resumo usa três campos do cabeçalho da minuta IMP: "Cláusula", "Vício (resumo)" e "Pedido (resumo)". O analista os aprova junto com a minuta (`references/minuta-por-ponto.md`, seção 3; item 17 do checklist de `auditoria-minuta.md`).

**Esclarecimento.** Cada minuta ESC aprovada, na ordem dos IDs, vira um quesito da seção II:

1. subtítulo em negrito: "QUESITO <n> – <título da minuta>";
2. texto corrido de "Da dúvida" e "Do fundamento". Sai o parágrafo de "Do fundamento" cujo único marcador é `EXT-LEI14133-ART164`, porque a tempestividade da peça já cita o art. 164;
3. "Indaga-se:", seguido das perguntas de "Da pergunta" como alíneas a), b), c).

## Os dois formatos

O analista escolhe o formato separadamente para impugnação e para esclarecimento, digitando uma frase que traz o tipo e o formato: "confirmo a peça de impugnação em formato único" (ou "de esclarecimento", "em formato por ponto"). A skill registra a frase como veio, com `estado.py peca --pasta <pasta> --acao confirmar --evidencia '<frase do analista>'`, e o script tira dela o tipo e o formato (`unico` ou `por_ponto` no `estado.json`). Resposta fora do formato não confirma nada: a skill mostra a frase exata e espera que ele a digite.

- **Peça única (`unico`):** uma peça por tipo, com todos os pontos aprovados daquele tipo na ordem dos IDs. Na impugnação, sai o quadro resumo.
- **Uma peça por ponto (`por_ponto`):** uma peça para cada minuta aprovada, com o seu ponto e os pedidos gerais do modelo. Na impugnação, não sai o quadro.

Nos dois formatos, só entram as versões aprovadas, conferidas pelo sha256 registrado. Se uma minuta mudou depois de aprovada, o `estado.py peca --acao verificar` aponta a pendência e a montagem não segue.

## Montagem e conversão

`scripts/montar_peca.py`, com a lógica em `scripts/montagem/` (`modelo.py`: campos, blocos e trava; `pontos.py`: minuta → ponto; `montar.py`: conferências e gravação). A conversão em .docx não é desta skill: é da skill `gerar-minuta-impugnacao`. Duas etapas separadas:

1. **Montagem** (`montar_peca.py montar --pasta <pasta> --tipo impugnacao|esclarecimento`): só roda com a peça do tipo confirmada no `estado.py`, sem pendências, com a data da peça até a data-limite do art. 164 (o texto fixo afirma a tempestividade), com `modelo-<tipo>.md` em `assets/` e com cada minuta igual à versão aprovada (sha256). Grava `<pasta>/peca/peca-<tipo>.md` (formato único) ou `peca-<tipo>-<ID>.md` (por ponto). O texto das minutas entra como foi aprovado; só saem subtítulos, numeração de parágrafo e marcadores. É esse arquivo que o analista confere antes da conversão.
2. **Conversão** (skill `gerar-minuta-impugnacao`, `gerar_minuta.py <peça>.md`): grava o `.docx` ao lado, sobre o timbre da Servfaz, seguindo as convenções acima. Ela só converte e para se achar `{{` ou referência interna na peça.

O arquivo do representante é procurado em `files/representante.json`, duas pastas acima da pasta do edital (`files/triagens/<slug>/`); `--representante` aponta outro. A data da peça é a do dia; `--data AAAA-MM-DD` a fixa. A modalidade sai por extenso para PE, PP, CC e CE; outra exige `"modalidade_extenso"` em `dados-peca.json`.

A separação permite trocar o visual sem mexer na regra de quais minutas entram e conferir o texto montado antes de gerar o .docx. Nenhuma das etapas assina, protocola ou envia.

O timbre, o gerador do .docx e o `criar_timbre.py` ficam na skill `gerar-minuta-impugnacao`. Se uma convenção da tabela acima mudar, o `gerar_minuta.py` muda junto.

## Para quem criar ou alterar um modelo

Esta seção é para quem mantém a skill, fora de uma triagem. A skill em execução não cria nem altera modelo, mesmo que o analista peça: um modelo improvisado para destravar a peça contornaria a revisão que o portão exige.

1. Trabalhe em `assets/rascunho/`, que o `estado.py` não lê.
2. Use só os marcadores e as convenções deste arquivo; não escreva no modelo texto que dependa do certame.
3. Deixe de fora qualquer dado de pessoa física. Cite norma só na forma jurídica usual, depois de conferi-la no catálogo, e registre a conferência na tabela "Normas do texto fixo"; o modelo em si não leva ID, status nem menção ao catálogo.
4. Depois da revisão do analista, mova o arquivo para `assets/` com o nome exato (`modelo-<tipo>.md`) e suba a `versao` do front matter.
5. Rode `estado.py peca --pasta <pasta> --acao verificar` numa triagem de teste e confira que o campo `modelos` mostra o arquivo.
6. Atualize este LEIA-ME e o passo da peça no `SKILL.md`.
