# Estado e retomada

Guia do `estado.py` para a skill: o que cada fase espera, cada comando, como registrar a frase do analista, o que cada recusa e cada alerta significam e como retomar uma triagem em sessão nova. Aqui `estado.py` abrevia `<python> <skill>/scripts/estado.py`, e `<pasta>` é a pasta do edital.

Conteúdo:

1. Princípios
2. Arquivos da pasta do edital
3. Fases derivadas e o que destrava cada uma
4. Comandos
5. A frase do analista como evidência
6. Recusas e a resposta certa
7. Alertas do status
8. Retomada em sessão nova
9. Reabrir, itens novos, documentos que chegam depois
10. Validar antes de encerrar

## 1. Princípios

- **O `estado.json` é a fonte de verdade.** O `registro.md` é o resumo legível dele (certame, fase, itens e os últimos 20 eventos), regenerado a cada gravação. Só o `estado.py` escreve os dois. Editar à mão apaga o rastro das decisões e quebra os invariantes que o `validar` confere.
- **Integridade.** Cada gravação deixa o sha256 do `estado.json` em `.estado.sha256` e uma cópia dele em `.estado.gravado.json`. Se o `estado.json` mudar por outro caminho, os comandos que gravam recusam até o analista decidir (seção 7).
- **A fase não é gravada: é derivada dos dados.** Não existe comando para mudar de fase. A fase muda quando você registra o que a destrava.
- **Saída.** Os comandos que gravam devolvem um JSON com `mensagem` e o status completo; leia os dois. Uma recusa sai com código 1, escreve `erro: …` na saída de erro e não grava nada. Opção ou valor inválido (por exemplo, `minuta --acao aprovar`) sai com código 2 e `usage: … error: …`: é erro de digitação no comando, não portão. Corrija e rode de novo.
- **O script confere o formato, não a decisão.** Ele impõe a ordem das fases e só aceita a frase do analista no formato fixo de cada comando (seção 5). Ele não sabe se foi o analista quem a digitou nem se ele viu o que ela decide: isso é com você.
- **Trava.** Cada pasta tem uma trava (`.estado.lock`): chamadas simultâneas esperam a vez. Mesmo assim, deixe as chamadas ao `estado.py` com quem conversa com o analista; subagentes do levantamento devolvem itens, não registram.
- **Caminhos.** O `estado.py` acha a pasta mesmo que você digite o nome em NFC e o disco esteja em NFD.

Campos do `status`:

| Campo | O que traz |
| :-- | :-- |
| `pasta` | O caminho da pasta do edital |
| `certame` | `slug`, `orgao`, `modalidade`, `numero`, `ano` e `esfera` (`null` se não informada) |
| `fase`, `proxima_acao` | A fase derivada e o que fazer agora, em texto; quando a fase pede decisão do analista, traz o formato da frase e um exemplo com os dados da triagem (ilustrativo: seção 6) |
| `documentos` | Presentes, faltas e a decisão de prosseguir (com a frase do analista), ou `null` |
| `prazo` | O JSON do `prazo.py` registrado (com `ato_reri` e `feriados_locais_confirmados`), ou `null` |
| `itens` | `total` e as listas `pendentes`, `incluidos`, `descartados` e `avaliar_depois` |
| `fila_minutas` | Itens incluídos cuja minuta ainda não foi aprovada nem descartada, na ordem de abertura |
| `minuta_em_revisao` | `{id, versao, arquivo, registrada, sha256}` ou `null`; `sha256` é o da versão registrada (`null` antes do registro) |
| `aprovadas` | `{id, versao, sha256}` de cada minuta aprovada |
| `minutas_descartadas` | Itens incluídos cuja minuta foi descartada: não entram na peça |
| `peca` | `{impugnacao, esclarecimento}`, cada um `null` ou a confirmação da peça daquele tipo |
| `estudo_sha256` | O hash do estudo no início da triagem |
| `alertas` | Avisos que vão ao analista (seção 7) |

## 2. Arquivos da pasta do edital

| Arquivo | Quem escreve | Quando |
| :-- | :-- | :-- |
| `estado.json`, `registro.md` | só o `estado.py` | a cada comando que grava |
| `.estado.sha256`, `.estado.gravado.json`, `.estado.lock` | só o `estado.py` | a cada comando que grava (o sha256 e a cópia do `estado.json` da última gravação; a trava) |
| `texto/*.txt`, `texto/inventario.json` | `extrair_texto.py` | Fase 0, e quando chegar documento novo |
| `documentos.md` | a skill | Fase 0, atualizado no portão |
| `mapa-secoes.md` | a skill | início do levantamento |
| `levantamento.md`, `itens.json` | a skill | levantamento (e itens novos depois) |
| `fontes-novas.md` | a skill (quem conversa com o analista) | quando consultar fonte oficial fora do catálogo |
| `minutas/<ID>.md` | a skill | só depois de `minuta --acao abrir` |
| `minutas/historico/<ID>.v<N>.md` | o `estado.py` | ajuste, descarte e reabertura |

## 3. Fases derivadas e o que destrava cada uma

O script testa as condições nesta ordem; a primeira que vale é a fase.

| Fase | Quando o status a mostra | O que a destrava |
| :-- | :-- | :-- |
| `documentos` | Portão não registrado, ou registrado com faltas e sem decisão de prosseguir | `documentos` sem faltas, ou `prosseguir` com a frase do analista |
| `levantamento` | Portão aberto e itens nunca registrados | `itens` (uma lista vazia `[]` registra levantamento sem itens) |
| `selecao` | Algum item pendente | `decidir` até não sobrar pendente |
| `minutas` | Algum item incluído com minuta não aprovada nem descartada | `minuta` (abrir, registrar, decidir) até a fila esvaziar |
| `peca_final` | Há minuta aprovada de um tipo cuja peça não foi confirmada | `peca --acao confirmar` e, confirmada a peça, `montar_peca.py montar` e, com o ok do analista, a skill `gerar-minuta-impugnacao` (SKILL.md, Fase 5); sem modelo em `<skill>/assets/`, a confirmação é recusada e a triagem para aqui |
| `concluido` | Nada pendente, ou nenhuma minuta aprovada | — |

Como a ordem é fixa, a fase pode voltar. Itens novos registrados durante as minutas levam a fase de volta a `selecao`, e a minuta em revisão continua esperando decisão. Um `documentos` registrado de novo com uma falta que o analista não autorizou volta a fase para `documentos`.

## 4. Comandos

| Comando | Quando usar | O que exige |
| :-- | :-- | :-- |
| `slug --orgao --modalidade --numero --ano` | Antes do `iniciar`, para saber o nome da pasta | Ano com 4 dígitos; órgão, modalidade e número com letras ou números. Em `--numero`, só o número (`1`, não `1/2026`) |
| `iniciar --raiz --orgao --modalidade --numero --ano [--esfera] [--slug]` | Triagem nova | Pasta inexistente, ou só com `texto/` e `minutas/`. Grava o hash do estudo do `MANIFEST.json` |
| `status --pasta` | Começo de todo turno | Pasta com `estado.json` |
| `documentos --pasta --presentes --faltas [--esfera]` | Portão documental, e de novo quando chegar documento | Os 6 códigos (EDITAL, TR, ETP, PLANILHA, PESQUISA, MINUTA), cada um em uma lista só. `RERI` é recusado |
| `prosseguir --pasta --evidencia` | O analista decidiu seguir sem o que falta | `documentos` registrado com faltas; frase "prossigo sem <códigos>" com exatamente as faltas registradas (seção 5) |
| `prazo --pasta --dados ARQUIVO\|-` | Fase 0, assim que achar a data de abertura; de novo se a data, os feriados locais, o ato da RERI ou o dia mudarem | O JSON de `prazo.py --json` (campos `abertura`, `data_limite`, `alertas`). Funciona antes do portão |
| `itens --pasta --arquivo ARQUIVO\|-` | Fim do levantamento; depois, só para itens novos (seção 9) | Portão aberto; lista de `{"id", "classe", "titulo"}`; ID `IMP-NN` com classe `impugnacao` ou `ESC-NN` com `esclarecimento`; ID e número inéditos |
| `decidir --pasta --evidencia` | Seleção | Portão aberto; itens registrados; frase com as cláusulas "incluo", "descarto" e "deixo para depois" (seção 5). Uma chamada aplica a frase inteira; item citado não pode ter minuta |
| `minuta --pasta --acao abrir` | Fase `minutas`, sem minuta em revisão | Abre só a primeira da fila |
| `minuta --pasta --id ID --acao registrar` | Logo depois de escrever `minutas/<ID>.md` | Arquivo existente e não vazio; `ID` é a minuta em revisão |
| `minuta --pasta --evidencia [--id ID]` | Depois de apresentar a minuta registrada | Sem `--acao`: a ação vem da frase ("aprovo <ID>", "ajuste <ID>: …" ou "descarto <ID>"), com o ID da minuta em revisão; `--id`, se usado, também. Arquivo igual ao registrado |
| `reabrir --pasta --evidencia` | O analista mudou de ideia sobre item que já tem minuta | Item já decidido ou com minuta; frase "reabro <IDs>: <motivo>" |
| `peca --pasta --acao verificar` | Fase `peca_final` | Só lê; mostra `pronto` (sem pendências, haja modelo ou não), pendências, aprovadas por tipo e modelos |
| `peca --pasta --acao confirmar --evidencia` | Peça final, quando houver modelo | Tudo decidido, minuta aprovada do tipo, `<skill>/assets/modelo-<tipo>.<extensão>` não vazio e a frase "confirmo a peça de …", de onde saem o tipo e o formato. A falta de modelo é recusada antes de conferir a frase |
| `validar --pasta` | Antes de encerrar o turno que gravou algo | Sai com 1 se algum invariante for violado ou se o `estado.json` foi alterado fora do `estado.py` (seção 10) |
| `aceitar-edicao --pasta --evidencia` | O analista mantém uma alteração feita no `estado.json` fora do `estado.py` | Alteração só no título de item ou nos dados do certame, comparada com `.estado.gravado.json`; frase "aceito a edição do estado: <motivo>" (seção 7) |

Não há opção para apontar outra pasta: o modelo da peça vale só em `<skill>/assets/` e o estudo só em `references/estudo/MANIFEST.json`. Enquanto o `estado.json` estiver alterado fora do `estado.py`, todos os comandos que gravam recusam, menos o `aceitar-edicao`.

**Prazo.** Rode sempre com a data do dia em `--hoje` e encadeie:

```bash
<python> <skill>/scripts/prazo.py --abertura 2026-11-03 --hoje "$(date +%F)" --json \
  | estado.py prazo --pasta <pasta> --dados -
```

Acrescente ao `prazo.py` as opções que valem para o certame:

- `--feriado-local AAAA-MM-DD:nome`, uma vez para cada feriado local informado;
- `--sem-feriado-local`, se o analista confirmou que não há feriado local no período: registra a confirmação (`feriados_locais_confirmados`) e troca o alerta "feriados locais não informados" por "analista confirmou que não há feriado local no período". Não combina com `--feriado-local`;
- `--ato-reri`, se houver ato da RERI no material (em arquivo próprio ou em páginas de outro arquivo, conforme `documentos.md`): acrescenta o alerta "a data de abertura pode ter mudado: conferir no processo da RERI".

Por exemplo, com ato da RERI e sem feriado local:

```bash
<python> <skill>/scripts/prazo.py --abertura 2026-11-03 --hoje "$(date +%F)" --json --ato-reri --sem-feriado-local \
  | estado.py prazo --pasta <pasta> --dados -
```

Registrar o prazo de novo substitui o anterior, por isso todo recálculo repete todas as opções: sem `--ato-reri`, o alerta da RERI some. O `prazo` do status mostra `ato_reri` e `feriados_locais_confirmados` do último registro. Se o `prazo.py` falhar (por exemplo, com `--feriado-local` e `--sem-feriado-local` juntos), o `estado.py prazo` recusa a entrada vazia: corrija o erro do primeiro comando e rode os dois de novo.

## 5. A frase do analista como evidência

A `--evidencia` é o registro de que o analista, e não a skill, tomou a decisão. Por isso cada comando que registra decisão tem uma frase de formato fixo, que o analista digita:

| Comando | Formato | Exemplo |
| :-- | :-- | :-- |
| `prosseguir` | `prossigo sem <códigos>` | prossigo sem ETP e PESQUISA |
| `decidir` | `incluo <IDs>`, `descarto <IDs>`, `deixo para depois <IDs>`, separadas por `;` | incluo IMP-01, IMP-03 e ESC-02; descarto os demais |
| `minuta` | `aprovo <ID>`, `descarto <ID>` ou `ajuste <ID>: <o que mudar>` | aprovo IMP-01 |
| `reabrir` | `reabro <IDs>: <motivo>` | reabro IMP-01: o patrimônio líquido exigido está dentro do limite legal |
| `peca --acao confirmar` | `confirmo a peça de impugnação\|esclarecimento em formato único\|por ponto` | confirmo a peça de esclarecimento em formato por ponto |
| `aceitar-edicao` | `aceito a edição do estado: <motivo>` | aceito a edição do estado: corrigi o título do ESC-02 à mão |

**Como o script compara.** Maiúsculas, acentos, espaços repetidos, o artigo antes de ID ou de código ("a IMP-01", "o ETP") e a pontuação final ("." ou "!") não importam. Vírgula e "e" separam os itens de uma lista; no `decidir`, ";" separa as cláusulas. "IMP-1" vale IMP-01. Os códigos de documento são EDITAL, TR, ETP, PLANILHA, PESQUISA e MINUTA: "pesquisa de preços" por extenso não vale. A instrução do ajuste e os motivos têm pelo menos 10 caracteres. Fora isso, o script não interpreta nada: o que não está no formato é recusado com o formato e um exemplo preenchido com os dados da triagem.

**Por comando:**

- **prosseguir:** exatamente as faltas registradas, nem mais nem menos. Se o analista envia parte do que falta, registre `documentos` de novo e peça a frase só com o que resta.
- **decidir:** uma chamada aplica a frase inteira. No lugar dos IDs, "os demais" (ou "todos", "todas") são os pendentes que a frase não cita; vale numa cláusula só. Para incluir todos os pendentes, a frase é "incluo todos" (ou "incluo os demais"). Cada ID aparece uma vez. O item que a frase não cita continua pendente. Item com minuta é recusado: use `reabrir` (seção 9).
- **minuta:** um ID só, o da minuta em revisão. A mesma frase com outro ID serve à outra minuta, quando ela for apresentada.
- **reabrir:** um ou mais IDs, dois-pontos e o motivo nas palavras do analista.
- **peca:** uma frase e uma chamada por tipo; o tipo e o formato saem da frase.
- **aceitar-edicao:** o motivo diz o que foi alterado e por que fica (seção 7).

**Para todas:**

- **Não converta resposta livre.** Se ele responde fora do formato, não monte a frase por ele, nem acrescente o verbo ou o ID para ela passar. Mostre a frase exata, preenchida com os dados, e espere que ele a digite:

  | O analista escreveu | Mostre |
  | :-- | :-- |
  | "não tenho ETP nem pesquisa, pode seguir" | responda: prossigo sem ETP e PESQUISA |
  | "inclui a 1 e a 3, o resto descarta" | responda: incluo IMP-01 e IMP-03; descarto os demais |
  | "pode aprovar essa" | responda: aprovo IMP-01 |
  | "aprovo, mas troca o pedido subsidiário" | é ajuste; responda: ajuste IMP-01: <o que mudar no pedido subsidiário> |

- **Copie a frase como ele escreveu**, sem trocar, acrescentar nem tirar palavras. O script grava a frase só com os espaços repetidos reduzidos. Se ela veio como sentença à parte numa mensagem maior (por exemplo, no pedido inicial), ou entre as aspas da sua pergunta, a `--evidencia` é só essa sentença, sem mudança e sem as aspas que a cercam: o script recusa a mensagem inteira e a frase entre aspas. Se o resto da mensagem a condiciona ou pede mudança, ela não decide: mostre a frase certa e espere.
- **Pergunte com a frase pronta.** No portão: "Para prosseguir, responda: prossigo sem ETP e PESQUISA". Na minuta: "aprovo IMP-01 / ajuste IMP-01: <o que mudar> / descarto IMP-01".
- **A decisão vale depois que ele viu o objeto**: o relatório do portão, a tabela de itens ou a minuta na versão atual. "Já inclui tudo" no primeiro pedido não decide itens que ainda não foram apresentados. A exceção é o `prosseguir`: a frase no formato, escrita antes do relatório, vale se citar exatamente as faltas encontradas.
- **Aspas no shell.** Use aspas simples e troque cada aspa simples da frase por `'\''`. Por exemplo, a frase `ajuste IMP-01: troque 'empresa' por 'licitante' no pedido` vira `--evidencia 'ajuste IMP-01: troque '\''empresa'\'' por '\''licitante'\'' no pedido'`. Aspas duplas não servem: dentro delas, o shell troca `$4` por vazio e "R$4.800,00" seria gravado como "R.800,00".

## 6. Recusas e a resposta certa

Toda recusa diz o que falta. A resposta certa é explicar ao analista e pedir a decisão que falta; nunca contornar. A coluna da esquerda traz um trecho da mensagem do script, que pode vir depois de um ID ou de um caminho.

**Frase do analista.** Toda recusa de frase termina com `Formato esperado: … Exemplo com os dados desta triagem: "…". Peça ao analista que digite a frase nesse formato; não converta uma resposta livre.` Mostre ao analista a frase pronta para o que ele quer decidir e espere que ele a digite. O exemplo do script (o da recusa e o da `proxima_acao`) é ilustrativo: a frase que você mostra leva os IDs que o analista indicou e, no ajuste, `<o que mudar>` em branco, nunca a instrução do exemplo ("cite a página do TR no pedido"), que não é dele. Sem item pendente, não use "os demais", mesmo que o exemplo o traga: o script recusa.

| Trecho da mensagem | O que significa | O que fazer |
| :-- | :-- | :-- |
| `não está no formato do prosseguir` / `do decidir (cláusula "…")` / `da decisão sobre a minuta` / `do reabrir` / `da confirmação da peça` / `do aceite` | Resposta livre, verbo fora do formato ("inclui", "aprova"), ID que falta ou frase vazia | Mostre a frase no formato, com os dados, e espere |
| `a frase precisa citar exatamente as faltas registradas (…): não cita …` / `cita …, que não falta` | O prosseguir esquece uma falta ou cita documento presente | Mostre a frase com as faltas do portão; se ele não quer seguir sem alguma, peça o documento |
| `"…" não é código de documento` | Nome por extenso ("pesquisa de preços") ou `RERI` | Mostre a frase com os códigos |
| `… não está registrado` | ID que não existe no levantamento (`decidir`, `reabrir`) | Confira o ID com o analista |
| `… aparece mais de uma vez na frase` | O mesmo ID em duas cláusulas | Pergunte qual decisão vale para ele |
| `"os demais" aparece em mais de uma cláusula` | Duas cláusulas com "os demais" | Peça a frase com "os demais" numa cláusula só |
| `"os demais" não tem a que se referir` | Nenhum pendente fora dos citados | Peça a frase sem "os demais"; se tudo já foi decidido, nada a registrar |
| `a frase precisa citar um ID só, o da minuta em revisão` | Decisão sobre mais de uma minuta ("aprovo IMP-01 e IMP-03") | Cada minuta é decidida depois de lida: peça a frase só sobre a em revisão |
| `a frase cita ESC-02, mas a minuta em revisão é IMP-01` | Frase de outra minuta | A decisão agora é só sobre a IMP-01; o outro ponto vem na vez dele |
| `a instrução do ajuste tem menos de 10 caracteres` | Ajuste sem dizer o que mudar | Pergunte o que ele quer mudar na minuta |
| `o motivo tem menos de 10 caracteres` | Reabrir ou aceite sem motivo | Peça o motivo nas palavras dele |

**Fluxo e arquivos**

| Trecho da mensagem | O que significa | O que fazer |
| :-- | :-- | :-- |
| `o portão documental não foi resolvido` | Itens, decisão ou minuta antes do portão | Volte à Fase 1 |
| `o portão documental ainda não foi registrado` / `não há faltas no portão` | `prosseguir` fora de hora | Rode `documentos`; sem faltas, não há o que autorizar |
| `a RERI … está fora do escopo desta skill` | `RERI` em `--presentes` ou `--faltas` | Tire o código; registre o ato em `documentos.md` como encaminhado |
| `faltou classificar` / `não pode estar em --presentes e em --faltas` / `código de documento desconhecido` | Classificação incompleta ou errada | Corrija a lista e rode de novo |
| `fora do formato IMP-NN ou ESC-NN` / `incoerente com o ID` / `título vazio` | `itens.json` malformado | Corrija o arquivo |
| `já existe: os IDs são estáveis` / `repete o número de` | ID reaproveitado, ou o `itens.json` completo reenviado | Os IDs são estáveis: mande só os itens novos, com o próximo número livre (seção 9) |
| `nenhum item novo no arquivo` | `itens` repetido sem nada novo | Nada a registrar |
| `nenhum item registrado` | `decidir` ou `reabrir` antes do `itens` | Termine o levantamento e registre os itens |
| `já tem minuta aberta ou decidida: a decisão não muda pelo "decidir"` | Mudança de decisão em item com minuta | Seção 9: a pedido do analista, com a frase do reabrir |
| `já está em revisão` | Tentativa de abrir a segunda | Apresente a em revisão e peça a decisão |
| `não há minuta a abrir na fase …` / `a próxima da fila é …` | Fora de fase ou fora de ordem | Siga a `proxima_acao`; a fila é IMP por número, depois ESC |
| `nenhuma minuta em revisão` | `registrar` ou decisão sem minuta aberta | Na fase `minutas`, abra a próxima com `minuta --acao abrir`; fora dela, siga a `proxima_acao` |
| `não existe: escreva a minuta antes de registrar` / `está vazio` | Registro antes de escrever | Escreva o arquivo e registre |
| `ainda não foi registrada` | Decisão sobre minuta não registrada | Registre e apresente antes de pedir a decisão |
| `mudou (ou sumiu) depois do registro` | O arquivo não é o que foi registrado | Registre de novo e apresente a versão atual: o analista decide sobre o texto que viu |
| `a minuta em revisão é …, não …` / `informe --id` | `--id` errado, ou `--acao registrar` sem `--id` | Use o ID de `minuta_em_revisao` |
| `--evidencia vai sem --acao` | `minuta` com `--acao` e `--evidencia` juntos | Tire `--acao`: a frase diz a decisão |
| `informe --acao abrir\|registrar ou --evidencia` | `minuta` sem ação nem frase | Corrija o comando |
| `já está pendente: não há o que reabrir` | Reabertura sem necessidade | Peça a decisão na frase do `decidir` |
| `a peça ainda não pode ser confirmada; pendências` | Algo não decidido | Resolva cada pendência na fase dela |
| `nenhuma minuta aprovada` | Pendência do `peca --acao verificar` (e da recusa do `confirmar`) quando todas as minutas foram descartadas ou nenhum item foi incluído | Não se resolve: não há peça a gerar. Diga isso ao analista, lembre os itens em "avaliar depois" com o prazo, rode `validar` e encerre |
| `não há minuta de … aprovada` | Peça de um tipo sem aprovadas | Não há peça desse tipo |
| `não há modelo de … em assets/ da skill` | Falta o modelo em `<skill>/assets/` (removido ou renomeado). A recusa vem antes de conferir a frase | Informe que a peça final só sai com o modelo e pare; não peça a frase de confirmação, não gere a peça por outro meio e não crie modelo |
| `informe --evidencia com a frase do analista que confirma a peça` | `peca --acao confirmar` sem a frase (esta recusa vem antes da do modelo) | Sem modelo, não há o que confirmar (linha anterior); com modelo, peça a frase ao analista |
| `entrada vazia` | O comando antes do pipe falhou (em geral o `prazo.py`) | Leia o erro do primeiro comando, corrija e rode os dois de novo |
| `já existe: retome com "status --pasta` | `iniciar` numa triagem existente | Retome (seção 8) |
| `já existe sem estado.json e tem …` | Pasta ocupada por outros arquivos | Mostre ao analista; use outro `--slug` só se ele concordar |
| `existe, mas não tem estado.json` | `iniciar` interrompido | Rode o `iniciar` que a mensagem sugere, com os dados do certame |
| `não é JSON válido` / `campo ausente ou inválido` | `estado.json` corrompido ou editado à mão | Rode `validar` e mostre as violações ao analista. Mesmo que ele diga "corrija", não edite o `estado.json`: peça que ele decida entre restaurar uma cópia do arquivo (a da última gravação fica em `.estado.gravado.json`) ou começar uma pasta nova com outro `--slug` (a triagem recomeça do portão) |

**Integridade do `estado.json`**

| Trecho da mensagem | O que significa | O que fazer |
| :-- | :-- | :-- |
| `estado.json foi alterado fora do estado.py (…): nada foi gravado` / `… ou .estado.sha256 foi apagado` | O `estado.json` mudou por outro caminho, ou o arquivo de controle sumiu; todo comando que grava recusa | Seção 7, primeira linha |
| `não há alteração a aceitar` | `aceitar-edicao` sem edição pendente, ou em pasta anterior ao controle | Nada a registrar |
| `a alteração mexe em …` / `a alteração deixou o estado.json com violações que o aceite não corrige` | A edição vai além do título de item e dos dados do certame | Mostre ao analista: ele desfaz a edição, e a mudança que ele quer vai pelo comando dela (seção 7) |
| `não há cópia legível da última gravação (.estado.gravado.json)` | A cópia sumiu ou não se lê, e o aceite não tem como conferir o que mudou | O analista desfaz a edição ou a triagem recomeça numa pasta nova (última linha da tabela acima) |

## 7. Alertas do status

Leve os alertas ao analista no começo da resposta, uma vez por sessão para os que se repetem.

| Alerta | O que fazer |
| :-- | :-- |
| `estado.json foi alterado fora do estado.py` (ou `… .estado.sha256 foi apagado`) | Alguém mudou o `estado.json` sem o `estado.py`. Até o analista decidir, os comandos que gravam recusam, o `validar` sai com 1 e a `proxima_acao` só fala disso. Não edite o `estado.json` para destravar, nem regrave `.estado.sha256` ou `.estado.gravado.json`: isso apagaria o alerta sem a decisão do analista. Mostre a alteração ao analista ("Como mostrar a alteração", logo abaixo). Se ele a mantém e ela mexe só no título de item ou nos dados do certame (órgão, modalidade, número, ano, esfera; o slug não), peça a frase "aceito a edição do estado: <motivo>", registre com `estado.py aceitar-edicao --pasta <pasta> --evidencia '...'` e rode `validar`. Se mexe em outra coisa (decisão, minuta, prazo, evento), o aceite é recusado: o analista desfaz a edição (por exemplo, restaurando a cópia `.estado.gravado.json`) e a mudança que ele quer vai pelo comando dela (`decidir`, `reabrir`, `prazo`). |
| `esta pasta é anterior ao controle de integridade` | A pasta foi criada antes do `.estado.sha256`, que nasce na próxima gravação. Avise o analista, uma vez, de que uma edição à mão anterior a ela não seria detectada. |
| `o estudo mudou desde o início da triagem` | Avise. Para cada item ainda não aprovado, abra na cópia atual a linha do mapa citada em "regra do estudo" e confira se o critério continua igual. Anote o resultado nas pendências do `levantamento.md`. Item que deixou de valer: proponha descartar (ou `reabrir`, se já tem minuta); a decisão é do analista. Minuta aprovada que cita linha alterada: mostre e pergunte se ele quer reabrir. O alerta continua enquanto o hash for diferente; não há comando que o apague. |
| `o hash do estudo não foi registrado no início` / `MANIFEST.json do estudo não encontrado` | A cópia do estudo está incompleta ou foi movida. Avise; quem mantém o estudo roda `sync_estudo.py --check`. Não recrie o manifesto. |
| `minuta X alterada ou removida depois de aprovada` | A versão aprovada não está mais em `minutas/`. Se você sabe exatamente o que mudou (por exemplo, uma edição sua nesta sessão), desfaça e confira com `validar`. Se não, conte ao analista e proponha `reabrir`; reabra só com a frase dele ("reabro <ID>: <motivo>"). Não há "registrar" para minuta aprovada. |
| `minuta X alterada depois do registro` | A minuta em revisão mudou. Registre de novo e apresente a versão atual antes de pedir decisão. |
| `prazo de impugnação vencido em …` / `hoje é o último dia do prazo` | Conta feita com a data de hoje sobre o prazo registrado. Diga isso no início da resposta, numa linha, e siga a fase: o script só alerta, e decidir se ainda vale protocolar é do analista. Se a fase já pede uma decisão dele (portão, seleção, minuta), a pergunta sobre seguir vai junto, sem parar antes. |
| `prazo: ATENÇÃO: …` | Urgência calculada na data em que o `prazo.py` rodou ("data de referência"). Se a sessão é de outro dia, recalcule o prazo (seção 4, com as mesmas opções) antes de repetir o alerta. |
| `prazo: conferir o horário-limite no edital` | Procure no edital a hora-limite do protocolo e cite-a no relatório. |
| `prazo: feriados locais não informados` | Pergunte ao analista ou veja o calendário do órgão. Recalcule com `--feriado-local` para cada feriado informado ou, se ele confirmar que não há feriado local no período, com `--sem-feriado-local`, repetindo as outras opções (seção 4). |
| `prazo: analista confirmou que não há feriado local no período` | O prazo foi registrado com `--sem-feriado-local`. Não pergunte de novo; num recálculo, repita a opção. |
| `prazo: feriados locais de ano fora da contagem (…) não alteraram o prazo` | Um feriado informado caiu fora do período da contagem, em geral por ano digitado errado. Confira a data com o analista e recalcule. |
| `prazo: a data-limite depende do expediente nos pontos facultativos` | Informe as duas datas; na dúvida, vale a mais cedo (`data_limite`). |
| `prazo: a abertura … cai em dia sem expediente` | Confira a data no edital. |
| `prazo: a data de abertura pode ter mudado: conferir no processo da RERI` | O prazo foi registrado com `--ato-reri`, porque há ato da RERI no material: diga que a data deve ser conferida no processo à parte. |

**Como mostrar a alteração.** `diff <pasta>/.estado.gravado.json <pasta>/estado.json` compara com a última gravação e só lê. Se ele mostrar o arquivo quase inteiro diferente (um editor reindentou o JSON), compare por campos, o que também só lê: `diff <(<python> -m json.tool --sort-keys <pasta>/.estado.gravado.json) <(<python> -m json.tool --sort-keys <pasta>/estado.json)`. Se nenhum campo mudou (o diff sai vazio porque só o `.estado.sha256` sumiu, ou a diferença era só de formatação), diga isso ao analista e peça a mesma frase do aceite; não recrie o arquivo de controle. A `proxima_acao` desse alerta sugere comparar com o `registro.md` e desfazer a alteração "se você sabe exatamente qual foi": siga esta seção. A comparação é com `.estado.gravado.json`, e quem desfaz a edição é o analista.

## 8. Retomada em sessão nova

A memória da conversa anterior não existe; o estado, sim.

1. **Ache a pasta.** Na raiz das triagens (`files/triagens/` ou a que o analista indicar), liste as pastas e compare com o certame. O slug depende de como o número foi digitado no `iniciar`, então não confie só em recalculá-lo. Se o analista der o caminho, use-o. Não crie pasta nova para um certame que já tem uma.
2. **Rode `status`** e leve os alertas ao analista. Com o alerta de `estado.json` alterado fora do `estado.py`, resolva-o antes de tudo (seção 7): até lá, nenhum comando grava.
3. **Leia o `registro.md`** para ver o que foi decidido e os últimos eventos.
4. **Leia o que a fase pede:**
   - `documentos`: `documentos.md`. Se o portão tem faltas sem decisão, apresente o relatório de novo e pergunte.
   - `levantamento`: `documentos.md`, `mapa-secoes.md` e o `levantamento.md` parcial, se houver. A seção "Progresso" dele diz quais documentos já foram examinados até o fim (`references/levantamento.md`, seção 12): continue do primeiro que não tem a linha "examinado". Documento sem essa linha é refeito, mesmo que haja rascunho dele. Só refaça um documento já examinado se o sha256 do arquivo no `texto/inventario.json` mudou.
   - `selecao`: os itens pendentes no `levantamento.md`. Apresente só esses e peça a frase do `decidir`.
   - `minutas`: o item da minuta em revisão no `levantamento.md` e o arquivo `minutas/<ID>.md`. Se `registrada` é `false`, termine a minuta conforme `minuta-por-ponto.md` e registre. Se é `true`, apresente de novo com o checklist e peça a decisão. Se o analista disser que já tinha aprovado, explique que a aprovação não foi registrada e peça a frase de novo ("aprovo IMP-02"). Sem minuta em revisão, abra a próxima.
   - `peca_final` ou `concluido`: siga a Fase 5 do `SKILL.md` (primeiro `peca --acao verificar`, depois os itens em "avaliar depois").
5. **Recalcule o prazo** se a sessão anterior foi em outro dia (seção 4), com as mesmas opções: o `prazo` do status mostra `ato_reri` e `feriados_locais_confirmados`, e os feriados locais informados ficam na linha "Feriados locais" do `documentos.md` (a partir do levantamento, também no cabeçalho do `levantamento.md`). O prazo registrado não guarda essa lista.
6. **Diga ao analista** em que etapa a triagem está e o que você precisa dele.

Uma triagem iniciada antes dos formatos fixos guarda frases livres: o `validar` só confere que elas existem, e o status avisa, até a próxima gravação, que a pasta é anterior ao controle de integridade. As decisões novas seguem os formatos da seção 5.

Se uma sessão caiu no meio de um ajuste ou de um descarte, com o arquivo já no histórico e o estado ainda não gravado, o próximo comando que grava devolve o arquivo a `minutas/` sozinho e anota `minuta_restaurada` no registro.

## 9. Reabrir, itens novos, documentos que chegam depois

**Reabrir.** Use quando o analista muda de ideia sobre um item que já tem minuta, em revisão, aprovada ou descartada. Reabra só com a frase dele, "reabro <IDs>: <motivo>". Se a proposta é sua (por exemplo, quando uma minuta aprovada foi alterada e a versão aprovada não pode ser restaurada), mostre a frase pronta, com o ID, e espere que ele a digite com o motivo dele. Reabrir desfaz uma decisão dele, e o motivo registrado precisa ser dele.

```bash
estado.py reabrir --pasta <pasta> --evidencia 'reabro IMP-01: o patrimônio líquido exigido está dentro do limite legal'
```

- O item volta a pendente e a minuta atual vai para `minutas/historico/<ID>.v<N>.md`. A versão não recomeça: a próxima abertura será a `v<N+1>`.
- A confirmação da peça do mesmo tipo, se houver, é desfeita.
- O motivo tem pelo menos 10 caracteres e vai nas palavras do analista, entre aspas simples como na seção 5.
- Depois, peça a nova decisão na frase do `decidir`.
- Para item sem minuta, não precisa reabrir: uma nova frase de `decidir` basta.

**Itens novos.** Quando o analista pede para examinar outro ponto, ou quando surge um achado depois do levantamento:

1. Acrescente o item ao `levantamento.md` com o próximo número livre da classe. Nunca renumere nem reaproveite um ID.
2. Mande ao script só os itens novos, num arquivo à parte (`<pasta>/itens-novos.json`) ou pela entrada padrão (`--arquivo -`), e rode `itens`. Reenviar o `itens.json` completo é recusado inteiro ("já existe"), porque o script não pula os IDs já registrados.
3. Atualize `<pasta>/itens.json` com a lista completa, para que ele continue espelhando o `levantamento.md`.
4. A fase volta a `selecao`. Uma minuta em revisão continua esperando a decisão dela.

**Documentos que chegam depois.** Trate cada arquivo novo como na Fase 0 do `SKILL.md`. Antes de extrair, olhe o título e, se preciso, só a primeira página: é por aqui que um ato da RERI costuma chegar, porque retificações e respostas saem dias depois do edital. Ato da RERI não é extraído nem analisado: registre-o em `documentos.md` como "ato da RERI: encaminhado ao processo à parte", avise o analista e registre o prazo de novo com `--ato-reri` (seção 4). Os demais arquivos: extraia, confira os erros do `inventario.json`, atualize `documentos.md` e rode `documentos` com a classificação nova. Depois examine o documento novo como no levantamento e registre o que surgir como itens novos.

## 10. Validar antes de encerrar

Rode `estado.py validar --pasta <pasta>` antes de encerrar todo turno em que gravou algo, antes da peça final e ao concluir. Ele devolve `{"valido": true|false, "violacoes": [...]}` e sai com 1 se houver violação.

| Violação | O que fazer |
| :-- | :-- |
| `arquivo inesperado em minutas/` ou `minuta não aberta ou já descartada` | Arquivo escrito fora do fluxo, por exemplo uma minuta adiantada. Mova-o para fora de `minutas/` (sem apagar) e avise o analista; quando chegar a vez do item, abra a minuta pelo fluxo. |
| `o item … não está incluído` | Minuta de item que não foi incluído. Mova o arquivo para fora de `minutas/` (sem apagar) e confira a seleção com o analista. |
| `minuta aprovada alterada ou removida` | Ver o alerta correspondente (seção 7). |
| `estado.json foi alterado fora do estado.py` (ou `… .estado.sha256 foi apagado`) | Ver o alerta correspondente (seção 7). |
| `… sem evidência` / `com evidência fora do formato` / `sem o evento "decidir" correspondente` / `sem o evento minuta_… dessa versão` / `sem o evento "prosseguir" correspondente` / `sem a decisão correspondente no histórico` / `sem o evento de registro` / `mais de uma minuta em revisão` / `ID repetido` | O `estado.json` foi editado fora do `estado.py`. Não corrija à mão: mostre as violações ao analista e pare até ele decidir entre restaurar uma cópia ou começar uma pasta nova (seção 6, linha `não é JSON válido`). O `aceitar-edicao` não cobre essas alterações. |
| `peça … confirmada com itens não decididos` ou `com versões que não batem` | A confirmação da peça não vale mais. Avise o analista. |

Um `validar` limpo não aprova nada nem prova que as decisões vieram do analista. Ele detecta a edição à mão pelo sha256 e confere que cada frase gravada está no formato do comando e tem o evento dele, mas não sabe quem digitou a frase. Por isso a regra continua: nunca editar o `estado.json`, e a `--evidencia` é sempre a frase do analista.
