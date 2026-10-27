# 02 - Plano do Mapeamento de Fontes

## 1. Objetivo

Para cada documento do processo (Edital e anexos), mapear as **fontes internas** (outros documentos do próprio processo) e as **fontes externas** (lei, normas, jurisprudência, bases de dados e prova de mercado) que precisam ser consultadas para decidir se um ponto é impugnável.

O mapeamento parte da base já auditada e corrigida (commits `c29449b`, `eb6431e` e `837df5f`). O trabalho é dividido em fases independentes, para que cada uma caiba em uma sessão e termine com um commit.

## 2. Decisões já tomadas

- **Um arquivo por pasta:** `Fontes - {Documento}.md`, ao lado de `Estrutura` e `Analise`.
- **Catálogo único:** `01 - Catalogo de Fontes.md` na raiz. As fontes externas são citadas nos mapas **só por ID**; o texto da norma e o status ficam no catálogo, que pode ser versionado quando a lei ou a jurisprudência mudar (ver `Minhas observacoes.md`).
- **Status de cada fonte:** `conferido` (texto conferido na fonte oficial) ou `a conferir` (fonte secundária, não localizada ou de memória). Os itens marcados "(a conferir)" nos arquivos de Análise entram como `a conferir`.
- **Campo esfera:** federal, estadual ou municipal. Normas federais (IN SEGES 5/2017, 65/2021, 73/2022, Lei 9.784/1999) devem indicar que o ente do edital pode ter regulamento próprio.
- **Sem dados pessoais** e grafia "Servfaz".

## 3. Formatos

### 3.1 Catálogo (`01 - Catalogo de Fontes.md`)

Fontes internas, ID `INT-*`: `INT-EDITAL`, `INT-TR`, `INT-ETP`, `INT-PLANILHA`, `INT-PESQUISA`, `INT-MINUTA`, `INT-RERI`, `INT-HIST-CONTRATO` (contrato anterior e consumo), `INT-DOTACAO`.

Fontes externas, ID `EXT-{GRUPO}-{CHAVE}` (ex.: `EXT-LEI14133-ART67`, `EXT-TCU-SUM247`, `EXT-BASE-PNCP`), agrupadas em: legislação, normas técnicas e regulatórias, jurisprudência, bases de dados e prova de mercado.

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |

### 3.2 Mapa por documento (`Fontes - {Documento}.md`)

```
# Fontes - {Documento}
Objetivo e como usar (1 parágrafo).

## {N}. {Seção do documento}   ← seções do `Estrutura - {Documento}.md`
Pergunta-chave: "…?"
| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |

## Matriz resumo
| Seção | INT-EDITAL | INT-TR | INT-ETP | INT-PLANILHA | INT-PESQUISA | INT-MINUTA | INT-RERI | Externas principais |
```

A lógica segue `Minhas observacoes.md`: cruzamento, prova e fundamento jurídico.

## 4. Fases

Cada fase lê o que está indicado, produz os arquivos, verifica e termina com commit. Uma fase só depende das anteriores pelo catálogo.

| Fase | Entrega | Entradas | Pronto quando |
| :-- | :-- | :-- | :-- |
| **1. Catálogo** | `01 - Catalogo de Fontes.md` | Os 14 arquivos `Estrutura`/`Analise`; relatório da auditoria | Todas as normas, súmulas, acórdãos e bases citados nos 14 arquivos têm ID, esfera, onde consultar e status. Conferir com uma busca por "art.", "Lei", "Súmula", "Acórdão", "IN " nos arquivos. |
| **2. Edital** | `Edital/Fontes - Edital.md` | Estrutura e Análise do Edital; catálogo | As 13 seções da Estrutura aparecem; as seções 1–5 vêm da Análise e a 6 está marcada como derivada; todo ID usado existe no catálogo. |
| **3. TR e ETP** | `Fontes - Termo de Referencia.md`, `Fontes - ETP.md` | Estrutura e Análise de cada um; catálogo | TR com as 10 seções; ETP com os 13 incisos do art. 18 §1º (obrigatórios marcados); IDs existem no catálogo. |
| **4. Planilha e Pesquisa** | `Fontes - Planilha de Custos.md`, `Fontes - Pesquisa de Precos.md` | Estrutura e Análise de cada um; catálogo | Planilha com os 6 módulos; Pesquisa com os 5 parâmetros do art. 23 §1º e os vícios da Análise; IDs existem. |
| **5. Minuta e RERI** | `Fontes - Minuta Contratual.md`, `Fontes - RERI.md` | Estrutura e Análise de cada um; catálogo | Minuta com as 9 cláusulas; RERI com os 5 checkpoints e o modelo de tabela de controle; IDs existem. |
| **6. Consolidação** | Atualização de `00 - Objetivos_Organizacao.md` e do catálogo | Os 7 mapas e o catálogo | Ver seção 5. |

Se uma fase acrescentar fonte nova, ela entra primeiro no catálogo, no mesmo commit.

## 5. Verificação final (fase 6)

1. Todo ID `INT-*`/`EXT-*` usado nos 7 mapas existe no catálogo, e todo ID do catálogo é usado em algum mapa (sem órfãos).
2. Cada seção do `Estrutura` de cada documento aparece no respectivo `Fontes`.
3. A matriz é simétrica: se o documento A cruza com B, o mapa de B cruza com A.
4. Nenhum `Fontes - *` cita artigo, súmula ou acórdão por extenso fora do catálogo.
5. O `00 - Objetivos_Organizacao.md` passa a listar o terceiro arquivo de cada pasta, o catálogo e este plano.

## 6. Andamento

| Fase | Status | Commit |
| :-- | :-- | :-- |
| 1. Catálogo | concluída | este commit (`01 - Catalogo de Fontes.md`) |
| 2. Edital | concluída | este commit (`Edital/Fontes - Edital.md`; catálogo: `EXT-LEI14133-ART14`, `ART15`, `ART90`) |
| 3. TR e ETP | concluída | este commit (`Termo de Referência/Fontes - Termo de Referencia.md`, `Estudo Técnico Preliminar/Fontes - ETP.md`; catálogo: `EXT-LEI14133-ART16`, `ART117`, `ART140`, `EXT-TCU-SUM281`, `EXT-MTE-NR15`, `EXT-MTE-NR16`) |
| 4. Planilha e Pesquisa | concluída | este commit (`Planilha de Custos/Fontes - Planilha de Custos.md`, `Pesquisa(Mapa) de Preços/Fontes - Pesquisa de Precos.md`; sem fonte nova; catálogo: siglas PL-F e PP-F) |
| 5. Minuta e RERI | concluída | este commit (`Minuta Contratual/Fontes - Minuta Contratual.md`, `Retificações, Esclarecimentos e Respostas/Fontes - RERI.md`; catálogo: `EXT-LEI14133-ART157`, `ART158`; Nomes de `ART137` e `ART156` ampliados; siglas MC-F e RR-F) |
| 6. Consolidação | concluída | este commit (pendências da seção 7 aplicadas nos 5 mapas anteriores; catálogo: "Usado em" recalculado, observações 7 e 8; `00 - Objetivos_Organizacao.md` atualizado; verificação na seção 8) |

Ao concluir uma fase, atualize esta tabela no mesmo commit.

## 7. Pendências registradas para a Fase 6

Resultado da Fase 6 de cada item na seção 7.3.

Levantadas na revisão da Fase 3 (simetria com o mapa do Edital). A Fase 3 não editou `Edital/Fontes - Edital.md`; estes ajustes ficam para a consolidação.

1. **Matriz do Edital:** nas colunas INT-TR e INT-ETP, trocar o ✓ pelas seções do TR e pelos incisos do ETP cruzados, como nas matrizes do TR e do ETP. Linhas 3 (Recursos orçamentários) e 7 (Julgamento): INT-ETP passa de "—" para os incisos IV e VI. Linha 5 (Envio de propostas): INT-TR passa a citar as seções III e IV.
2. **Seção 2 (Objeto), "Descrição, unidades e quantitativos":** citar INT-ETP (incisos I, IV e VII).
3. **Seção 3, "Orçamento sigiloso":** acrescentar INT-TR (seção IX) e INT-ETP (incisos IV e VI); trocar INT-PLANILHA e INT-PESQUISA sem seção por INT-PLANILHA (Módulos 1 a 6) e INT-PESQUISA (item 3, mapa de preços).
4. **Seção 4:** dividir "Vedação a consórcio ou cooperativa" como no mapa do ETP (consórcio: `EXT-LEI14133-ART15`; cooperativa: `EXT-LEI14133-ART16`, `EXT-TCU-SUM281` a conferir). Em "Tratamento de ME/EPP", acrescentar INT-ETP (incisos IV e VIII); acrescentar a volta do ETP III (motivação de exigências de habilitação).
5. **Seção 5:** em "Declaração de custos trabalhistas", acrescentar INT-TR (seção IV); incluir a volta do TR III (prazo para obter laudo ou catálogo).
6. **Seções 6 e 7:** volta do TR VIII (critério de julgamento e modo de disputa) e INT-TR (seção VIII) na amostra antes dos lances; na seção 7, "Teto unitário versus pesquisa", acrescentar INT-ETP (inciso VI) e trocar INT-PESQUISA (mapa de cotações) por INT-PESQUISA (item 3, mapa de preços) e INT-PLANILHA sem seção por INT-PLANILHA (Módulo 6, preço final).
7. **Seção 8:** acrescentar INT-TR (seção VIII) em "Limitação de tempo, local ou somatório" e em "Tempo de existência versus tempo de experiência"; criar a linha "Atestados só de órgão público" (volta do TR VIII); em "Índices contábeis", trocar INT-ETP (justificativa) por INT-ETP (justificativa das exigências de habilitação, se houver; ver `Fontes - ETP.md`, inciso III); dar a `EXT-PEND-TEMPOEXIST` a mesma ressalva "(a localizar)" usada no TR.
8. **Modo de citar seções:** uniformizar as fontes internas do Edital para `INT-EDITAL (seção N)`, `INT-PLANILHA (Módulo N; submódulo N.N)` e `INT-PESQUISA (item N, …)`, como nos mapas do TR e do ETP.
9. **Catálogo:** acrescentar `ED-F` em "Usado em" das fontes que o mapa do Edital usa e ainda não marcam a sigla (conferir por script, como foi feito para `TR-F` e `ETP-F`).

### 7.1 Levantadas na Fase 4 (Planilha e Pesquisa)

A Fase 4 não editou os mapas do Edital, do TR e do ETP nem os arquivos `Estrutura`/`Analise`. Os mapas da Planilha e da Pesquisa já trazem as linhas de volta de todos os cruzamentos que aqueles mapas fazem com eles.

10. **Catálogo, aviso prévio:** as linhas `EXT-TCU-AC1186-2017` ("percentual de prorrogação superado"), `EXT-MGI-NT35883`, `EXT-TCU-AC58-2026` e a observação 7 da seção 7 ainda tratam o 0,83% como regra vigente, mas o commit `a701461` retirou a Nota Técnica e o Acórdão 58/2026 dos arquivos de estudo e deixou o aviso prévio só com o 1.186/2017. O mapa da Planilha seguiu o commit. Decidir se as duas fontes saem do catálogo ou entram na lista "Não usar", e alinhar o Nome do 1.186/2017.
11. **Mapa do Edital, seção 7, "Serviços com mão de obra: CCT":** trocar INT-PLANILHA (módulos 1 e 2.3) por INT-PLANILHA (Módulo 1; submódulo 2.3); na mesma seção, "BDI e custos diretos" passa a INT-PLANILHA (Módulo 6; submódulos 6.1 e 6.2). Seção 6 (lances): INT-PLANILHA (valor do item) fica, como na seção 7 do mapa da Planilha.
12. **Mapa do Edital, seção 5, "Declaração de custos trabalhistas":** citar INT-PLANILHA (Módulo 1; submódulo 2.3), como o mapa da Planilha (Módulo 1 e Submódulo 2.3).
13. **Mapas do TR e do ETP:** a seção IX do TR e o inciso VI do ETP citam a Pesquisa por "item 3"; o mapa da Pesquisa usa os mesmos itens (1 a 3 da Estrutura) e cria as seções 9 a 13 para os vícios. Se a Fase 6 quiser apontar o vício, trocar "detalhe em `Fontes - Pesquisa de Precos.md`" por "seções 6 e 13" no TR IX ("Parâmetros da pesquisa de preços").
14. **Arquivos de estudo:** `Estrutura - Planilha de Custos.md` ainda diz "Súmula 254 ... fonte secundária; conferir o texto oficial" e marca a Lei 14.973/2024 como "fonte secundária, a conferir", mas as duas estão `conferido` no catálogo; `Analise - Planilha de Custos.md` (grupo 4) ainda cita o esclarecimento do MEC como "fonte secundária", já conferido (`EXT-ADM-MEC-2024`). `Analise - Pesquisa de Precos.md` (vício 5) marca a IN 65/2021 e o Acórdão 1.445/2015 como "a conferir", já conferidos. Os módulos 4.1-D e 4.1-E (acidente e maternidade) não têm fonte no catálogo.
15. **Catálogo, siglas:** `EXT-IN65-GERAL` não é usado por nenhum mapa (os mapas usam `ART5` e `ART6`); verificar órfãos na Fase 6.

### 7.2 Levantadas na Fase 5 (Minuta e RERI)

A Fase 5 não editou os mapas anteriores nem os arquivos `Estrutura`/`Analise`. Os mapas da Minuta e da RERI já trazem as linhas de volta de todos os cruzamentos que os mapas anteriores fazem com eles.

16. **Coluna INT-MINUTA nas matrizes:** nos mapas do Edital e do TR, trocar o ✓ pelas cláusulas cruzadas (Edital: seção 5 → cl. 1; seção 11 → cl. 1 e 4; seção 12 → cl. 7; seção 13 → cl. 1, 3 e 9. TR: I → cl. 1, 3 e 6; V → cl. 2; VI → cl. 2 e 7; VII → cl. 2, 5 e 8; X → cl. 2). No ETP, inciso X → cl. 4 e 5.
17. **Voltas que faltam nos mapas anteriores:** o mapa da Minuta cruza com lugares que ainda não o citam. Edital, seção 2 (natureza do objeto e regime: cl. 1 e 5) e seção 13 (previsão de prorrogação e critério de reajuste: cl. 1 e 3). TR, seção IV (dedicação exclusiva: cl. 3; riscos da execução: cl. 5). ETP, inciso X (percentual da garantia acima de 5% justificado pelos riscos: cl. 4). Planilha, Módulos 2 e 4 (troca da provisão de férias nas prorrogações: cl. 1), Módulo 6 (preço do posto como base da retenção e da multa de mora: cl. 2 e 7) e Módulo 2 (provisões e conta vinculada: cl. 2). Pesquisa, item 3 (data do mapa de preços como data-base do reajuste: cl. 3), sem linha no mapa da Pesquisa.
18. **Coluna INT-RERI:** os mapas anteriores dizem que `INT-RERI` "vale para todas as seções". O mapa da RERI faz a volta pelos checkpoints 1 e 3 (Edital seção 8; TR III, IV, VII e VIII; ETP IV e VI; Planilha Módulos 1 a 6; Pesquisa itens 1 a 3; Minuta cl. 3 e 4). A Fase 6 decide se basta a regra geral ou se as matrizes passam a marcar essas seções.
19. **Arquivos de estudo da Minuta e da RERI:** `Estrutura - Minuta Contratual.md` ainda marca "a conferir" o art. 141 (2.3) e o art. 22 (5.3), já conferidos, e não cita os artigos da defesa prévia de 15 dias úteis (7.2), que são os arts. 157 e 158 (`EXT-LEI14133-ART157`, `ART158`). `Estrutura - RERI.md` diz "fundamento jurisprudencial a localizar" para o efeito vinculante do esclarecimento, já resolvido por `EXT-TCU-AC915-2009`; `Analise - RERI.md` marca "a conferir" os Acórdãos 2.032/2021, 2.078/2014 e 930/2008, já conferidos.
20. **Catálogo:** a coluna "Usado em" de `EXT-TCU-AC7184-2018` passou de "—" para MC-F; o órfão que restava nela deixa de existir. Na verificação de órfãos da Fase 6, considerar MC-F e RR-F.

### 7.3 Resultado na Fase 6

Cada item foi conferido no mapa de origem e no catálogo antes de ser aplicado.

| Item | Resultado | Observação |
| :-- | :-- | :-- |
| 1 | resolvida, com ajuste | Matriz do Edital refeita a partir das tabelas, com seções do TR, incisos do ETP, módulos da Planilha, itens da Pesquisa e cláusulas da Minuta. Linha 3: ETP IV e VI. Linha 7: só o ETP VI. O ETP IV cruza com a seção 7 pela linha "Orçamento sigiloso" da seção 3 ("seções 3 e 7"), e a seção 7 não tem ponto de quantitativos. Linha 5: TR III e IV. |
| 2 | resolvida | INT-ETP (incisos I, IV e VII). |
| 3 | resolvida | |
| 4 | resolvida | Consórcio e cooperativa em linhas separadas, com o texto do mapa do ETP. A Súmula 281 vai como "súmula em reanálise, ver catálogo" e não como "a conferir": o status no catálogo é `conferido`. O mesmo ajuste foi feito no mapa do ETP. A volta do ETP III é a linha nova "Motivação das exigências de habilitação". |
| 5 | resolvida | Linha nova "Prazo para obter laudo ou catálogo". |
| 6 | resolvida | O Edital não tinha linha de amostra. Foi criada "Amostra ou prova de conceito" na seção 7, onde o TR VIII a cruza. |
| 7 | resolvida em parte | Feita a linha "Atestados só de órgão público", com `EXT-PEND-ATESTPRIV (a localizar)`, como no TR. **Rejeitada** a ressalva "(a localizar)" para `EXT-PEND-TEMPOEXIST`: o mapa do TR não cita esse ID, e o catálogo o dá como resolvido (`EXT-TCU-AC733-2026`). O TR-F foi retirado do "Usado em" dele. |
| 8 | resolvida | Todas as referências do Edital a si mesmo passaram a `INT-EDITAL (seção N)`. |
| 9 | resolvida | ED-F marcada por script em todas as fontes do mapa. |
| 10 | resolvida | Decisão da usuária (2026-10-15): manter `EXT-MGI-NT35883` e `EXT-TCU-AC58-2026`. O 0,83% por prorrogação (só União) voltou à Estrutura e à Análise da Planilha e aos mapas da Planilha e da Minuta; o 1.186/2017 ficou como regra anterior (catálogo, observação 7). |
| 11, 12 | resolvidas | |
| 13 | resolvida, com ajuste | "seções 6, 10 e 13", e não "6 e 13": a linha do TR IX cita também a economia de escala (seção 10 do mapa da Pesquisa). |
| 14 | resolvida | Marcas de "fonte secundária"/"a conferir" retiradas das fontes já conferidas (Súmula 254, Lei 14.973/2024, Tema 846, esclarecimento do MEC, IN 65/2021, Acórdãos 1.445/2015 e 2.637/2015). Os itens 4.1-D e 4.1-E ganharam base legal conferida: `EXT-LEI8213-ART60` (§ 3º) e `EXT-CLT-ART392`, citados também no mapa da Planilha. |
| 15 | decidida | `EXT-IN65-GERAL` fica, com nota (catálogo, observação 8). |
| 16 | resolvida, com ajuste | Edital: além do previsto, seção 2 → cl. 1 e 5. TR: as células vêm da tabela do próprio TR (I → cl. 1; IV → cl. 3 e 5; VII → cl. 2 e 5). A Minuta cruza cl. 3 e 6 com o TR I e cl. 8 com o TR VII, e as voltas estão no TR I (cl. 1) e no TR IV (cl. 3). ETP X → cl. 4 e 5. |
| 17 | resolvida | Voltas criadas no Edital (seções 2 e 13), no TR IV, no ETP X, na Planilha (Módulos 2, 4, 5 e 6) e na Pesquisa (seção 8). |
| 18 | decidida | Fica a regra geral ("vale para todas as seções"). O mapa da RERI faz a volta pelos checkpoints 1 e 3, e a legenda da matriz do Edital passou a dizer isso. |
| 19 | resolvida | Estrutura da Minuta: art. 141 § 2º (apuração de responsabilidade), art. 22 (matriz facultativa; § 3º) e arts. 157 e 158 (defesa prévia de 15 dias úteis). RERI: efeito vinculante do esclarecimento pelo Acórdão 915/2009 e Acórdãos 930/2008, 2.032/2021 e 2.078/2014 sem "a conferir". |
| 20 | resolvida | Órfãos verificados com MC-F e RR-F (seção 8). |

## 8. Verificação final da Fase 6

Feita por script sobre os 7 mapas e o catálogo:

1. **IDs:** todo `INT-*`/`EXT-*` dos mapas existe no catálogo. Ficam sem uso em mapa, com nota na observação 8 do catálogo: `EXT-IN65-GERAL`, `EXT-TCU-AC2622-2013`, `EXT-TJ-GERAL`, `EXT-TCU-AC1182-2020` (não usar), `EXT-MGI-NT35883` e `EXT-TCU-AC58-2026` (decisão pendente, item 10) e os oito `EXT-PEND-*` já resolvidos.
2. **Seções:** cada seção da `Estrutura` aparece no mapa: Edital 13, TR 10, ETP 13 incisos e o checklist, Planilha 6 módulos e a planilha como um todo, Pesquisa 3 itens (seções 1 a 8) e os 5 vícios, Minuta 9 cláusulas, RERI 3 atos, 5 checkpoints e a tabela de controle.
3. **Simetria:** se a seção S do mapa de A cita INT-B na seção L, a seção L do mapa de B cita INT-A. Isso vale para todos os pares, menos a RERI, que segue a regra geral (item 18). Para a Planilha, a seção 7 (planilha como um todo) responde por "Módulos 1 a 6". Para a Pesquisa, os itens 1, 2 e 3 correspondem às seções 1 a 5, 6 e 7, e as seções 8 a 13 respondem pelo conjunto. As matrizes resumo batem com as tabelas. Na conferência por seção exata da origem, ficam cruzamentos que a volta cobre por outra seção do mesmo mapa (exemplo: a Minuta cl. 6 cita o TR I, e o TR I volta só pela cl. 1).
4. **Citação por extenso:** nenhum mapa cita artigo, súmula, acórdão, lei ou IN por número fora do ID.
5. **"Usado em":** as siglas ED-F a RR-F do catálogo coincidem com o uso real nos mapas.
