# Catálogo de fontes

> Cópia de `briefing/Mapeamento_Analise/01 - Catalogo de Fontes.md`. Os demais arquivos citados abaixo ficam no repositório e não fazem parte do pacote da skill. Use este catálogo para conferir o status de uma fonte antes de citá-la: só fontes com status `conferido` fundamentam peça ou carta.

Catálogo único das fontes citadas nos 14 arquivos `Estrutura - *.md` e `Analise - *.md` desta pasta. Os mapas `Fontes - {Documento}.md` (fases 2 a 5) citam as fontes externas **só pelo ID**; o nome, o local de consulta e o status ficam aqui. Quando a lei ou a jurisprudência mudar, atualize este arquivo, não os mapas (ver `Minhas observacoes.md` e `02 - Plano do Mapeamento de Fontes.md`).

## Como ler

**IDs:** `INT-*` para documentos do próprio processo; `EXT-{GRUPO}-{CHAVE}` para fontes externas. A chave `GERAL` indica a norma citada sem artigo específico. Um ID por artigo: os incisos e parágrafos citados vão na coluna Nome.

**Esfera:** `federal (nacional)` para lei ou súmula que vale para todos os entes; `federal (União)` para norma infralegal federal, quando o ente do edital pode ter regulamento próprio (confira o regulamento do ente, `EXT-REG-ENTE`); `estadual` ou `municipal` quando a fonte é do ente.

**Status:**

- `conferido`: artigo da Lei 14.133/2021 citado nos arquivos sem a ressalva "(a conferir)", depois da auditoria e das correções dos commits `c29449b`, `eb6431e` e `837df5f`. O relatório da auditoria não está no repositório, então o critério é a ausência de ressalva nos arquivos corrigidos. Os arts. 18, 24, 25 e 54 foram conferidos também no texto do Planalto. Antes de citar em peça, confira se o texto da lei mudou.
- `a conferir`: todo o resto, ou seja, artigo ressalvado "(a conferir)" em qualquer um dos arquivos, fonte secundária, fonte não localizada, norma de outra lei e toda jurisprudência. A jurisprudência fica `a conferir` até ser lida no portal do tribunal.
- `n/a`: fontes internas e prova de mercado, que dependem do caso concreto.

**Usado em (siglas dos arquivos):**

| Sigla | Arquivo |
| :-- | :-- |
| ED-E / ED-A | `Edital/Estrutura - Edital.md` / `Edital/Analise - Edital.md` |
| ETP-E / ETP-A | `Estudo Técnico Preliminar/Estrutura - ETP.md` / `Analise - Estudo tecnico Preliminar.md` |
| TR-E / TR-A | `Termo de Referência/Estrutura - Termo de Refencia.md` / `Analise - Termo de Referencia.md` |
| PL-E / PL-A | `Planilha de Custos/Estrutura - Planilha de Custos.md` / `Analise - Planilha de Custos.md` |
| PP-E / PP-A | `Pesquisa(Mapa) de Preços/Estrutura - Pesquisa de Precos.md` / `Analise - Pesquisa de Precos.md` |
| MC-E / MC-A | `Minuta Contratual/Estrutura - Minuta Contratual.md` / `Analise - Minuta Contratual.md` |
| RR-E / RR-A | `Retificações, Esclarecimentos e Respostas/Estrutura - RERI.md` / `Analise - RERI.md` |
| ED-F | `Edital/Fontes - Edital.md` (só para fontes acrescentadas na fase 2) |

---

## 1. Fontes internas

Onde consultar, para todas: arquivos da compra no PNCP (`EXT-BASE-PNCP`), quadro informativo do Compras.gov.br (`EXT-BASE-COMPRASGOV`) ou site do órgão (`EXT-BASE-SITEORGAO`). Documento da fase preparatória que não integrou o edital só vai ao PNCP depois da homologação (`EXT-LEI14133-ART54`); antes disso, o caminho é pedido de esclarecimento ou acesso via LAI (`EXT-LEI12527-GERAL`).

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| INT-EDITAL | Edital da licitação | Documento do processo | do ente licitante | PNCP, Compras.gov.br, site do órgão | todos os 14 arquivos | n/a |
| INT-TR | Termo de Referência (ou Projeto Básico, em obras e serviços de engenharia) | Anexo do edital | do ente licitante | PNCP, Compras.gov.br, site do órgão | ED-E, ED-A, ETP-A, TR-E, TR-A, PL-A, PP-E, PP-A, RR-E, RR-A | n/a |
| INT-ETP | Estudo Técnico Preliminar | Documento da fase preparatória | do ente licitante | PNCP (se anexo ao edital ou após a homologação); pedido de esclarecimento ou LAI | ED-A, ETP-E, ETP-A, TR-E, TR-A | n/a |
| INT-PLANILHA | Planilha de custos e formação de preços (orçamento estimado) | Anexo do edital | do ente licitante | PNCP, site do órgão | ED-A, PL-E, PL-A, TR-A, RR-E, RR-A | n/a |
| INT-PESQUISA | Pesquisa de preços / mapa comparativo de cotações | Documento da fase preparatória ou anexo | do ente licitante | PNCP, site do órgão; pedido de esclarecimento se o orçamento for sigiloso | ED-A, ETP-A, TR-E, PP-E, PP-A | n/a |
| INT-MINUTA | Minuta do contrato | Anexo do edital | do ente licitante | PNCP, Compras.gov.br, site do órgão | ED-A, ETP-A, MC-E, MC-A, PL-A, RR-E, RR-A | n/a |
| INT-RERI | Retificações, esclarecimentos e respostas a impugnações | Atos publicados durante a divulgação | do ente licitante | Quadro informativo do Compras.gov.br, PNCP, Diário Oficial, site do órgão | RR-E, RR-A | n/a |
| INT-HIST-CONTRATO | Contrato anterior e histórico de consumo ou execução | Documento do órgão | do ente licitante | Portal da Transparência do órgão (`EXT-BASE-TRANSPARENCIA`), PNCP (contratos anteriores) | ETP-E, ETP-A | n/a |
| INT-DOTACAO | Dotação orçamentária e fonte de recursos | Indicação no edital, TR ou processo | do ente licitante | Edital, TR (seção de adequação orçamentária), processo | ED-E, ED-A, TR-E, MC-A | n/a |
| INT-PCA | Plano de Contratações Anual (PCA) | Documento de planejamento do órgão | do ente licitante | PNCP (planos de contratação), site do órgão | ETP-E, TR-E | n/a |

---

## 2. Legislação

### 2.1 Lei nº 14.133/2021

Onde consultar, para todas: texto compilado no Planalto, `https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm`. Tipo: lei federal de normas gerais. Esfera: federal (nacional).

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-LEI14133-GERAL | Lei 14.133/2021, referência geral (regime jurídico, preâmbulo do edital; capítulo de contratos, arts. 89 a 154) | Lei | federal (nacional) | Planalto | todos os 14 arquivos | conferido |
| EXT-LEI14133-ART4 | Art. 4º: aplicação da LC 123/2006 e seus limites | Lei | federal (nacional) | Planalto | ED-E, ED-A | a conferir |
| EXT-LEI14133-ART5 | Art. 5º: princípios (razoabilidade, proporcionalidade, julgamento objetivo, segurança jurídica, economicidade, motivação) | Lei | federal (nacional) | Planalto | TR-A, PL-A, PP-A, MC-A, RR-A | conferido |
| EXT-LEI14133-ART6 | Art. 6º, XXIII: definição de termo de referência e alíneas "a" a "j" ("i": estimativa do valor com memória de cálculo; "j": adequação orçamentária) | Lei | federal (nacional) | Planalto | TR-E, TR-A, PL-A | a conferir |
| EXT-LEI14133-ART9 | Art. 9º, I, "a": vedação a cláusulas que restrinjam a competitividade | Lei | federal (nacional) | Planalto | TR-A | conferido |
| EXT-LEI14133-ART11 | Art. 11, III: objetivo de evitar sobrepreço, preços inexequíveis e superfaturamento | Lei | federal (nacional) | Planalto | PL-A, PP-A | conferido |
| EXT-LEI14133-ART14 | Art. 14: impedimentos para disputar a licitação ou participar da execução do contrato | Lei | federal (nacional) | Planalto | ED-F | a conferir |
| EXT-LEI14133-ART15 | Art. 15: participação em consórcio, salvo vedação justificada no processo | Lei | federal (nacional) | Planalto | ED-F | a conferir |
| EXT-LEI14133-ART17 | Art. 17, § 3º: amostra na pré-qualificação / fases do processo | Lei | federal (nacional) | Planalto | TR-A | conferido |
| EXT-LEI14133-ART18 | Art. 18: fase preparatória (caput: compatibilização com as leis orçamentárias; IV: orçamento com composição de custos; X: análise de riscos); § 1º, I a XIII: elementos do ETP; § 2º: elementos obrigatórios | Lei | federal (nacional) | Planalto | ED-E, ED-A, ETP-E, ETP-A, TR-A, PL-A | conferido |
| EXT-LEI14133-ART22 | Art. 22: matriz de riscos (obrigatoriedade conforme porte e regime) | Lei | federal (nacional) | Planalto | MC-E | a conferir |
| EXT-LEI14133-ART23 | Art. 23: valor estimado (caput: compatível com o mercado, bancos de dados públicos, economia de escala; § 1º, I a V: parâmetros para bens e serviços, prazos de 1 ano e 6 meses; § 2º: obras e serviços de engenharia, SINAPI/SICRO) | Lei | federal (nacional) | Planalto | ED-A, ETP-A, PL-A, PP-E, PP-A, RR-A | conferido |
| EXT-LEI14133-ART24 | Art. 24: orçamento sigiloso (só se justificado; quantitativos e dados da proposta continuam públicos) | Lei | federal (nacional) | Planalto | ED-A, ETP-A | conferido |
| EXT-LEI14133-ART25 | Art. 25: conteúdo do edital (caput); § 3º: anexos divulgados na mesma data, sem cadastro; § 7º: reajuste com data-base do orçamento; § 8º, I e II: reajuste e repactuação | Lei | federal (nacional) | Planalto | ED-E, ED-A, MC-E, MC-A, PL-A | conferido |
| EXT-LEI14133-ART40 | Art. 40: compras (III: quantidades pelo consumo provável; V, "b", e §§ 2º e 3º: parcelamento; § 1º: conteúdo do TR em compras) | Lei | federal (nacional) | Planalto | ED-A, ETP-A, TR-E, TR-A | conferido |
| EXT-LEI14133-ART41 | Art. 41: marca e amostra (I: indicação de marca excepcional; II: amostra na pré-qualificação; parágrafo único: amostra só do provisoriamente vencedor) | Lei | federal (nacional) | Planalto | TR-A | conferido |
| EXT-LEI14133-ART47 | Art. 47, II, e § 1º: parcelamento em serviços | Lei | federal (nacional) | Planalto | ED-A, ETP-A, TR-A | conferido |
| EXT-LEI14133-ART54 | Art. 54, caput e § 3º: publicidade no PNCP; documentos da fase preparatória após a homologação | Lei | federal (nacional) | Planalto | ETP-A, RR-A | conferido |
| EXT-LEI14133-ART55 | Art. 55: prazos mínimos de divulgação (8, 15, 10 e 25 dias úteis); § 1º: alteração que afeta propostas exige nova divulgação e reabertura dos prazos | Lei | federal (nacional) | Planalto | ED-A, PL-A, RR-E, RR-A | conferido |
| EXT-LEI14133-ART57 | Art. 57: intervalo mínimo de diferença entre lances | Lei | federal (nacional) | Planalto | ED-A | conferido |
| EXT-LEI14133-ART59 | Art. 59: desclassificação (III: acima do orçamento estimado; §§ 2º a 4º: exequibilidade) | Lei | federal (nacional) | Planalto | ED-A, PL-A, RR-A | conferido |
| EXT-LEI14133-ART60 | Art. 60: critérios de desempate; § 1º: preferências; § 2º: ressalva da LC 123/2006 | Lei | federal (nacional) | Planalto | ED-E | conferido |
| EXT-LEI14133-ART63 | Art. 63: habilitação (§ 1º: declaração de que a proposta cobre os custos trabalhistas; §§ 2º e 3º: vistoria substituível por declaração) | Lei | federal (nacional) | Planalto | ED-A, PL-A, TR-A | conferido |
| EXT-LEI14133-ART67 | Art. 67: qualificação técnica (§ 1º: parcelas de maior relevância; § 2º: limite de 50% e vedação de tempo e local; § 5º: experiência de até 3 anos em serviços contínuos) | Lei | federal (nacional) | Planalto | ED-A, TR-A | conferido |
| EXT-LEI14133-ART69 | Art. 69: qualificação econômico-financeira (II: certidão negativa de falência; § 5º: vedação de índices não usuais; índices devidamente justificados) | Lei | federal (nacional) | Planalto | ED-A | conferido |
| EXT-LEI14133-ART90 | Art. 90: convocação do adjudicatário para assinar o contrato no prazo e nas condições do edital | Lei | federal (nacional) | Planalto | ED-F | a conferir |
| EXT-LEI14133-ART92 | Art. 92: cláusulas necessárias (V: preço, pagamento, reajuste e encargos moratórios; X: prazo de resposta à repactuação; XI: prazo de resposta ao reequilíbrio; § 3º: data-base do reajuste) | Lei | federal (nacional) | Planalto | TR-E, MC-E, MC-A | conferido |
| EXT-LEI14133-ART94 | Art. 94: divulgação no PNCP como condição de eficácia (20 dias úteis na licitação; 10 na contratação direta) | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART96 | Art. 96, § 1º: escolha da modalidade de garantia pelo contratado (arts. 96 a 102: garantias) | Lei | federal (nacional) | Planalto | ED-A, MC-E, MC-A | conferido |
| EXT-LEI14133-ART102 | Art. 102: cláusula de retomada pela seguradora em obras de grande vulto | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART103 | Art. 103: matriz de alocação de riscos; § 5º: exceções à renúncia de reequilíbrio | Lei | federal (nacional) | Planalto | ETP-A, MC-E, MC-A | conferido |
| EXT-LEI14133-ART106 | Art. 106: vigência inicial de até 5 anos em serviços e fornecimentos contínuos (arts. 105 a 114: duração) | Lei | federal (nacional) | Planalto | TR-E, MC-E | a conferir |
| EXT-LEI14133-ART107 | Art. 107: prorrogações sucessivas até 10 anos | Lei | federal (nacional) | Planalto | TR-E, MC-E | a conferir |
| EXT-LEI14133-ART111 | Art. 111: prorrogação automática do contrato por escopo | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART118 | Art. 118: preposto | Lei | federal (nacional) | Planalto | TR-A | conferido |
| EXT-LEI14133-ART121 | Art. 121, § 3º: garantias trabalhistas em dedicação exclusiva (conta vinculada, pagamento direto, condicionamento do pagamento) | Lei | federal (nacional) | Planalto | PL-A, MC-A | conferido |
| EXT-LEI14133-ART124 | Art. 124, I: alterações unilaterais (arts. 124 a 136: alterações e recomposição de preços) | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART125 | Art. 125: limites de acréscimo e supressão (25%; 50% em reformas) | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART135 | Art. 135, I e II: datas-base da repactuação (proposta; acordo, convenção ou dissídio coletivo) | Lei | federal (nacional) | Planalto | PL-A, MC-E, MC-A | conferido |
| EXT-LEI14133-ART137 | Art. 137, § 2º, IV: suspensão ou extinção por atraso de pagamento superior a 2 meses (arts. 137 a 139: extinção) | Lei | federal (nacional) | Planalto | MC-E, MC-A | conferido |
| EXT-LEI14133-ART138 | Art. 138, § 2º: indenização na extinção por culpa exclusiva da Administração | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART141 | Art. 141: ordem cronológica de pagamentos (arts. 141 a 146: pagamentos) | Lei | federal (nacional) | Planalto | TR-A, MC-E, MC-A | a conferir |
| EXT-LEI14133-ART143 | Art. 143: pagamento da parcela incontroversa | Lei | federal (nacional) | Planalto | TR-A, MC-A | conferido |
| EXT-LEI14133-ART147 | Arts. 147 a 150: nulidades; art. 147: avaliação do interesse público antes de declarar nulidade | Lei | federal (nacional) | Planalto | ETP-A | conferido |
| EXT-LEI14133-ART150 | Art. 150: indicação dos créditos orçamentários, sob pena de nulidade | Lei | federal (nacional) | Planalto | ED-E, ED-A, MC-A | conferido |
| EXT-LEI14133-ART151 | Arts. 151 a 154: meios alternativos de resolução de controvérsias (conciliação, mediação, comitê de disputas, arbitragem) | Lei | federal (nacional) | Planalto | MC-E | conferido |
| EXT-LEI14133-ART156 | Art. 156: sanções (advertência, multa, impedimento, inidoneidade); § 3º: multa entre 0,5% e 30% (arts. 155 a 163: infrações e sanções) | Lei | federal (nacional) | Planalto | ED-A, MC-E, MC-A | conferido |
| EXT-LEI14133-ART162 | Art. 162: multa de mora na forma do edital ou contrato | Lei | federal (nacional) | Planalto | MC-A | conferido |
| EXT-LEI14133-ART164 | Art. 164: impugnação e esclarecimento até 3 dias úteis antes da abertura; parágrafo único: resposta em até 3 dias úteis, divulgada no sítio oficial | Lei | federal (nacional) | Planalto | ED-E, ED-A, RR-E, RR-A | conferido |
| EXT-LEI14133-ART165 | Art. 165: recursos (3 dias úteis); § 1º, I: intenção de recorrer "imediatamente" | Lei | federal (nacional) | Planalto | ED-A | conferido |
| EXT-LEI14133-ART170 | Art. 170, § 4º: representação ao tribunal de contas | Lei | federal (nacional) | Planalto | RR-A | conferido |
| EXT-LEI14133-ART183 | Art. 183, III: contagem de prazos em dias úteis | Lei | federal (nacional) | Planalto | ED-A | conferido |

### 2.2 Constituição e outras leis

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-CF88-ART5 | CF/88, art. 5º, LIV e LV: devido processo legal, contraditório e ampla defesa | Constituição | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm` | ED-A | a conferir |
| EXT-CF88-ART37 | CF/88, art. 37, caput (princípios da Administração) e XXI (manutenção das condições efetivas da proposta) | Constituição | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm` | ED-A, MC-A | a conferir |
| EXT-LC123-ART44 | LC 123/2006, art. 44: empate ficto de ME/EPP | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm` | ED-E | a conferir |
| EXT-LC123-ART47 | LC 123/2006, art. 47: tratamento diferenciado de ME/EPP nas contratações públicas | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm` | ED-A | a conferir |
| EXT-LC123-ART48 | LC 123/2006, art. 48: itens exclusivos até R$ 80 mil; III: cota reservada de até 25% para bens divisíveis | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm` | ED-E, ED-A | a conferir |
| EXT-LC123-ART49 | LC 123/2006, art. 49: exceções ao tratamento diferenciado | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm` | ED-E, ED-A | a conferir |
| EXT-LEI11101-GERAL | Lei 11.101/2005: recuperação judicial e falência | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm` | ED-A | a conferir |
| EXT-LEI9784-GERAL | Lei 9.784/1999: processo administrativo federal (vista dos autos, decisão motivada). Estados e municípios podem ter lei própria; cite a do ente | Lei | federal (União) | `https://www.planalto.gov.br/ccivil_03/leis/l9784.htm` | ED-A, RR-A | a conferir |
| EXT-LEI9784-ART50 | Lei 9.784/1999, art. 50: dever de motivação | Lei | federal (União) | `https://www.planalto.gov.br/ccivil_03/leis/l9784.htm` | RR-A | a conferir |
| EXT-LEI9784-ART66 | Lei 9.784/1999, art. 66: contagem de prazos em dias contínuos | Lei | federal (União) | `https://www.planalto.gov.br/ccivil_03/leis/l9784.htm` | ED-A | a conferir |
| EXT-LEI8666-GERAL | Lei 8.666/1993 (revogada): art. 48 (inexequibilidade) e sorteio como desempate. Uso só histórico, para datar súmulas antigas | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/l8666cons.htm` | ED-E, ED-A | a conferir |
| EXT-LEI12527-GERAL | Lei 12.527/2011 (LAI): pedido de acesso a documentos não publicados | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm` | ETP-A | a conferir |
| EXT-CC-ART393 | Código Civil, art. 393: caso fortuito e força maior | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm` | MC-A | a conferir |
| EXT-CLT-ART73 | CLT, art. 73, § 1º: hora noturna reduzida (52min30s) | Decreto-lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm` | PL-E | a conferir |
| EXT-CLT-ART192 | CLT, art. 192: adicional de insalubridade (10%, 20%, 40%) | Decreto-lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm` | PL-E | a conferir |
| EXT-CLT-ART193 | CLT, art. 193: adicional de periculosidade (30%) | Decreto-lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm` | PL-E | a conferir |
| EXT-CLT-ART473 | CLT, art. 473: ausências legais remuneradas | Decreto-lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm` | PL-E | a conferir |
| EXT-LEI7418-GERAL | Lei 7.418/1985: vale-transporte (desconto de até 6% do salário-base) | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/l7418.htm` | PL-E, PL-A | a conferir |
| EXT-LC110-GERAL | LC 110/2001: contribuição social adicional de 10% sobre o FGTS (extinta). Uso só histórico | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp110.htm` | PL-E, PL-A | a conferir |
| EXT-LEI13932-ART12 | Lei 13.932/2019, art. 12: extinção dos 10% adicionais do FGTS a partir de 01/01/2020 | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13932.htm` | PL-E, PL-A | a conferir |
| EXT-LEI12506-GERAL | Lei 12.506/2011: aviso prévio proporcional (3 dias por ano, até 90 dias) | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12506.htm` | PL-E, PL-A | a conferir |
| EXT-LC116-ART3 | LC 116/2003, art. 3º: local de incidência do ISS e exceções por item da lista | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm` | PL-A | a conferir |
| EXT-LEI12546-GERAL | Lei 12.546/2011: CPRB (desoneração da folha) | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12546.htm` | PL-E | a conferir |
| EXT-LEI14973-GERAL | Lei 14.973/2024: transição da desoneração da folha (2025 a 2028) | Lei | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14973.htm` | PL-E | a conferir |
| EXT-LC214-ART348 | LC 214/2025, art. 348, § 1º: ano-teste de CBS e IBS (2026) | Lei complementar | federal (nacional) | `https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm` | PL-E | a conferir |
| EXT-ISS-MUNICIPAL | Lei do ISS do município competente (alíquota por item da lista de serviços) | Lei municipal | municipal | Site da prefeitura ou câmara municipal do município competente | PL-E, PL-A | a conferir |

---

## 3. Normas técnicas e regulatórias

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-REG-ENTE | Regulamento próprio do ente licitante (decreto estadual ou municipal de licitações, pesquisa de preços, pagamentos, modelo de planilha, processo administrativo) | Decreto / regulamento | estadual ou municipal | Diário Oficial e site do ente; legislação citada no preâmbulo do edital | ED-A, TR-E, PL-E, PP-E, PP-A, MC-E, MC-A, RR-A | a conferir |
| EXT-IN73-GERAL | IN SEGES/ME 73/2022: licitação de bens e serviços (modos de disputa, prorrogação de lances) | Instrução normativa | federal (União) | Portal de Compras do Governo Federal, `https://www.gov.br/compras` (Legislação) | ED-A | a conferir |
| EXT-IN65-GERAL | IN SEGES/ME 65/2021: procedimento de pesquisa de preços | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PP-E | a conferir |
| EXT-IN65-ART5 | IN SEGES/ME 65/2021, art. 5º, § 1º: prioridade aos parâmetros I e II | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PP-E, PP-A | a conferir |
| EXT-IN65-ART6 | IN SEGES/ME 65/2021, art. 6º, caput (média, mediana ou menor valor; descarte de inexequíveis, inconsistentes e excessivos) e § 6º (limite da mediana do Painel) | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PP-E, PP-A | a conferir |
| EXT-IN5-2017 | IN SEGES/MPDG 5/2017: serviços com dedicação exclusiva; modelo de planilha de custos (Anexo VII-D) | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PL-E | a conferir |
| EXT-IN7-2018 | IN 7/2018: alteração da IN 5/2017 (modelo de planilha) | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PL-E | a conferir |
| EXT-IN98-2022 | IN SEGES/ME 98/2022: aplicação da IN 5/2017 às contratações da Lei 14.133/2021 | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PL-E | a conferir |
| EXT-IN77-2022 | IN SEGES 77/2022: prazo de pagamento (esfera federal) | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | TR-E | a conferir |
| EXT-IN5-2014 | IN SLTI/MP 5/2014 (revogada): pesquisa de preços. Uso só histórico, para datar o Acórdão 1.445/2015 | Instrução normativa | federal (União) | `https://www.gov.br/compras` (Legislação) | PP-A | a conferir |
| EXT-MGI-NT35883 | Nota Técnica SEI 35883/2026/MGI: provisão de aviso prévio em prorrogações (fonte secundária) | Nota técnica | federal (União) | `https://www.gov.br/compras` (a localizar) | PL-E | a conferir |
| EXT-AGU-MODELOS | Modelos padronizados da AGU (termo de referência, edital, contrato) | Modelo de documento | federal (União) | `https://www.gov.br/agu` (modelos de licitações e contratos) | TR-E | a conferir |
| EXT-NORMA-CCT | Convenção Coletiva de Trabalho da categoria (piso, benefícios, data-base, adicionais) | Instrumento coletivo de trabalho | por base territorial do sindicato | Sistema Mediador do MTE (`EXT-BASE-MEDIADOR`); sindicatos da categoria | ED-A, TR-A, PL-E, PL-A, MC-E, MC-A, RR-A | a conferir |
| EXT-MTE-NR17 | Norma Regulamentadora NR-17 (ergonomia) do MTE | Norma regulamentadora | federal (nacional) | `https://www.gov.br/trabalho-e-emprego` (Normas Regulamentadoras) | TR-E | a conferir |
| EXT-NORMA-ABNT | Normas técnicas ABNT (NBR) aplicáveis ao objeto | Norma técnica | nacional | `https://www.abntcatalogo.com.br` | ED-A, TR-E, TR-A | a conferir |
| EXT-REG-INMETRO | Portarias e certificações do INMETRO | Regulamento técnico | federal (nacional) | `https://www.gov.br/inmetro` | ED-A, TR-E, TR-A | a conferir |
| EXT-REG-ANVISA | Registros e regulamentos da ANVISA | Regulamento sanitário | federal (nacional) | `https://www.gov.br/anvisa` | ED-A, TR-E | a conferir |
| EXT-REG-ANATEL | Homologações e regulamentos da ANATEL | Regulamento de telecomunicações | federal (nacional) | `https://www.gov.br/anatel` | ED-A | a conferir |
| EXT-REG-CONSELHOS | Legislação dos conselhos profissionais (CONFEA/CREA, CAU, CRA, CFC): atividades privativas e registro | Lei e resolução de conselho | federal (nacional) | `https://www.confea.org.br`, `https://caubr.gov.br`, `https://cfa.org.br`, `https://cfc.org.br` | ED-A | a conferir |
| EXT-REG-CFC | Normas contábeis do CFC (índices de liquidez e solvência) | Norma contábil | federal (nacional) | `https://cfc.org.br` | ED-A | a conferir |

---

## 4. Jurisprudência

Toda a jurisprudência fica `a conferir` até ser lida no portal do tribunal. Súmulas e acórdãos do TCU vinculam a esfera federal; em estados e municípios, servem como reforço, ao lado da jurisprudência do tribunal de contas do ente.

### 4.1 Súmulas do TCU

Onde consultar: Pesquisa de Jurisprudência do TCU, `https://pesquisa.apps.tcu.gov.br`.

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-TCU-SUM177 | Súmula 177: definição precisa do objeto e dos quantitativos | Súmula | federal | Pesquisa TCU | ETP-A, TR-A, PP-A | a conferir |
| EXT-TCU-SUM247 | Súmula 247: adjudicação por item quando o objeto é divisível | Súmula | federal | Pesquisa TCU | ED-A, ETP-A, TR-A | a conferir |
| EXT-TCU-SUM254 | Súmula 254: IRPJ e CSLL fora do BDI do orçamento-base (paráfrase de fonte secundária) | Súmula | federal | Pesquisa TCU | PL-E, PL-A | a conferir |
| EXT-TCU-SUM262 | Súmula 262: prazo para o licitante demonstrar a exequibilidade antes da desclassificação (firmada sob a Lei 8.666/1993) | Súmula | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-TCU-SUM263 | Súmula 263: quantitativos mínimos proporcionais nas parcelas de maior relevância | Súmula | federal | Pesquisa TCU | ED-A, TR-A | a conferir |
| EXT-TCU-SUM275 | Súmula 275: capital social, patrimônio líquido ou garantias, de forma não cumulativa | Súmula | federal | Pesquisa TCU | ED-A | a conferir |

### 4.2 Acórdãos e informativos do TCU

Onde consultar: Pesquisa de Jurisprudência do TCU, `https://pesquisa.apps.tcu.gov.br`.

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-TCU-AC930-2008 | Acórdão 930/2008-Plenário: reabertura do prazo do edital original após alteração | Acórdão | federal | Pesquisa TCU | RR-E, RR-A | a conferir |
| EXT-TCU-AC2078-2014 | Acórdão 2.078/2014-Plenário: republicação e reabertura de prazo | Acórdão | federal | Pesquisa TCU | RR-A | a conferir |
| EXT-TCU-AC1445-2015 | Acórdão 1.445/2015-Plenário: prioridade ao Comprasnet e às contratações similares (sob a IN 5/2014) | Acórdão | federal | Pesquisa TCU | PP-A | a conferir |
| EXT-TCU-AC2637-2015 | Acórdão 2.637/2015-Plenário: pesquisa restrita a poucos fornecedores (segundo fonte secundária) | Acórdão | federal | Pesquisa TCU | PP-A | a conferir |
| EXT-TCU-AC1186-2017 | Acórdão 1.186/2017-Plenário: aviso prévio trabalhado de 1,94% no 1º ano | Acórdão | federal | Pesquisa TCU | PL-E | a conferir |
| EXT-TCU-AC1101-2020 | Acórdão 1.101/2020-Plenário: vedação de limitar o somatório de atestados | Acórdão | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-TCU-AC1182-2020 | Acórdão 1.182/2020-Plenário: duplicidade de provisão de férias (não localizado) | Acórdão | federal | Pesquisa TCU | PL-A | a conferir |
| EXT-TCU-AC1201-2020 | Acórdão 1.201/2020: participação de empresa em recuperação judicial | Acórdão | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-TCU-AC2032-2021 | Acórdão 2.032/2021-Plenário: republicação e reabertura de prazo | Acórdão | federal | Pesquisa TCU | RR-A | a conferir |
| EXT-TCU-AC58-2026 | Acórdão 58/2026-Plenário: provisão de aviso prévio em contratos prorrogados (fonte secundária) | Acórdão | federal | Pesquisa TCU | PL-E, PL-A | a conferir |
| EXT-TCU-INFO2026-INDICES | Informativo do TCU de 2026: índices contábeis acima de 1 cumulados com PL de até 10% | Informativo de jurisprudência | federal | `https://portal.tcu.gov.br` (Informativos de Licitações e Contratos) | ED-A | a conferir |

### 4.3 Outros tribunais e precedentes administrativos

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-STF-SV4 | Súmula Vinculante 4 do STF: salário mínimo como base de cálculo (adicional de insalubridade) | Súmula vinculante | federal (nacional) | `https://portal.stf.jus.br` (Súmulas Vinculantes) | PL-E | a conferir |
| EXT-STF-SV21 | Súmula Vinculante 21 do STF: inconstitucional exigir depósito ou arrolamento prévio para recurso administrativo | Súmula vinculante | federal (nacional) | `https://portal.stf.jus.br` (Súmulas Vinculantes) | ED-A | a conferir |
| EXT-STF-TEMA846 | Tema 846 da repercussão geral do STF: constitucionalidade da contribuição de 10% da LC 110/2001 até a extinção (fonte secundária) | Tese de repercussão geral | federal (nacional) | `https://portal.stf.jus.br` (Repercussão Geral) | PL-A | a conferir |
| EXT-TST-SUM60 | Súmula 60 do TST: integração do adicional noturno habitual | Súmula | federal (nacional) | `https://www.tst.jus.br` (Súmulas) | PL-E | a conferir |
| EXT-TST-SUM172 | Súmula 172 do TST: horas extras habituais no DSR | Súmula | federal (nacional) | `https://www.tst.jus.br` (Súmulas) | PL-E | a conferir |
| EXT-TST-SUM448 | Súmula 448 do TST: insalubridade na limpeza de banheiros de uso público | Súmula | federal (nacional) | `https://www.tst.jus.br` (Súmulas) | PL-A | a conferir |
| EXT-STJ-RESP1733688 | REsp 1.733.688/SC (retenção de pagamento): **não localizado; não usar** até achar precedente verificado (ver `EXT-PEND-RETENCAO`) | Acórdão | federal (nacional) | `https://scon.stj.jus.br` | MC-A | a conferir |
| EXT-TCESP-SUM50 | Súmula 50 do TCE/SP: recuperação judicial (reforço só quando o órgão for paulista) | Súmula | estadual (SP) | `https://www.tce.sp.gov.br` (Súmulas) | ED-A | a conferir |
| EXT-TJ-GERAL | Precedentes dos tribunais de justiça (genérico; localizar por tema e estado do ente) | Acórdão | estadual | Portal de jurisprudência do TJ do estado do ente | ED-A | a conferir |
| EXT-ADM-MEC-2024 | Esclarecimento do MEC em pregão de 2024: provisão de férias e substituto como alternativas (fonte secundária) | Precedente administrativo | federal (União) | PNCP / Compras.gov.br (a localizar) | PL-A | a conferir |

### 4.4 Fundamentos a localizar

Teses que os arquivos usam sem fonte localizada. Os mapas podem citar estes IDs, mas a peça só cita a tese depois que o fundamento for achado e conferido.

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-PEND-TEMPOEXIST | Vedação de exigir tempo mínimo de existência da empresa | Jurisprudência a localizar | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-PEND-BDI | BDI e custos diretos no julgamento de propostas | Jurisprudência a localizar | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-PEND-EXEQ14133 | Continuidade da presunção relativa de inexequibilidade (Súmula 262) sob a Lei 14.133/2021, em acórdão posterior a 2021 | Jurisprudência a localizar | federal | Pesquisa TCU | ED-A | a conferir |
| EXT-PEND-VINCESCLAR | Resposta a esclarecimento vincula a Administração e os licitantes quanto à interpretação do edital | Jurisprudência a localizar | federal | Pesquisa TCU | RR-E | a conferir |
| EXT-PEND-ATESTPRIV | Vedação de aceitar só atestados emitidos por pessoa jurídica de direito público | Jurisprudência a localizar | federal | Pesquisa TCU | TR-A | a conferir |
| EXT-PEND-MOTIVCOMP | Obrigatoriedade de motivação comparativa de soluções no ETP | Jurisprudência a localizar | federal | Pesquisa TCU | ETP-A | a conferir |
| EXT-PEND-FRAUDECOT | Fraude na pesquisa de preços por vínculo entre cotistas | Jurisprudência a localizar | federal | Pesquisa TCU | PP-A | a conferir |
| EXT-PEND-REAJUSTE | Reajuste como direito do contratado, não como faculdade da Administração | Jurisprudência a localizar | federal | Pesquisa TCU | MC-A | a conferir |
| EXT-PEND-RETENCAO | Ilegalidade da retenção total do pagamento por falha pontual (substitui o REsp não localizado) | Jurisprudência a localizar | federal | Pesquisa TCU; `https://scon.stj.jus.br` | MC-A | a conferir |

---

## 5. Bases de dados

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-BASE-PNCP | Portal Nacional de Contratações Públicas: editais, anexos, contratos, histórico de participantes e preços homologados | Base de dados pública | federal (nacional) | `https://pncp.gov.br`; API de consulta em `https://pncp.gov.br/api/consulta` | ED-A, ETP-A, MC-E, PP-E, PP-A, RR-A | a conferir |
| EXT-BASE-PAINELPRECOS | Painel de Preços do Governo Federal (consulta por CATMAT/CATSER) | Base de dados pública | federal (União) | `https://paineldeprecos.planejamento.gov.br` | PP-E, PP-A | a conferir |
| EXT-BASE-PAINELCONTRAT | "Painel de Contratações Públicas" citado no ETP (identificar se é o PNCP ou outro painel de compras) | Base de dados pública | federal | A identificar | ETP-A | a conferir |
| EXT-BASE-BPS | Banco de Preços em Saúde | Base de dados pública | federal (União) | `https://www.gov.br/saude` (Banco de Preços em Saúde) | PP-E | a conferir |
| EXT-BASE-NFE | Base nacional de notas fiscais eletrônicas (parâmetro V do art. 23, § 1º); acesso do licitante a confirmar | Base de dados | federal (nacional) | A confirmar | PP-E | a conferir |
| EXT-BASE-CATMAT | Catálogo de materiais e serviços (CATMAT/CATSER) | Catálogo público | federal (União) | `https://catalogo.compras.gov.br` | PP-A | a conferir |
| EXT-BASE-COMPRASGOV | Compras.gov.br: portal da sessão, regulamento do portal, quadro informativo (avisos, esclarecimentos, impugnações), registros de instabilidade | Portal eletrônico | federal (União) | `https://www.gov.br/compras`; quadro informativo público em `https://cnetmobile.estaleiro.serpro.gov.br/comprasnet-web/public/compras/quadro-informativo?compra=<idCompra>` | ED-E, ED-A | a conferir |
| EXT-BASE-SITEORGAO | Sítio eletrônico oficial do órgão licitante (respostas a esclarecimentos, anexos, avisos) | Site oficial | do ente licitante | Site do órgão | RR-E | a conferir |
| EXT-BASE-DIARIO | Diário Oficial do ente (avisos de retificação) | Publicação oficial | federal, estadual ou municipal | Diário Oficial do ente | RR-A | a conferir |
| EXT-BASE-TRANSPARENCIA | Portal da Transparência do órgão (execução e consumo de contratos anteriores) | Base de dados pública | do ente licitante | Portal do ente; na esfera federal, `https://portaldatransparencia.gov.br` | ETP-A | a conferir |
| EXT-BASE-CNPJ | Cadastro CNPJ da Receita Federal / RedeSim: QSA, endereço, CNAE principal e secundários. Registrar só o vínculo encontrado, sem nomes nem CPF | Base de dados pública | federal (nacional) | `https://solucoes.receita.fazenda.gov.br` (comprovante de CNPJ); dados abertos do CNPJ | ED-A, PP-A | a conferir |
| EXT-BASE-CNAE | Classificação Nacional de Atividades Econômicas (CNAE) | Classificação oficial | federal (nacional) | `https://concla.ibge.gov.br` | ED-A, TR-A, PP-A | a conferir |
| EXT-BASE-MEDIADOR | Sistema Mediador do MTE: CCTs registradas | Base de dados pública | federal (nacional) | `https://www3.mte.gov.br/sistemas/mediador` | ED-A, PL-E, PL-A | a conferir |
| EXT-BASE-FPAS | Tabela de códigos FPAS da Receita Federal (alíquotas de terceiros por atividade) | Tabela oficial | federal (nacional) | Receita Federal (a localizar) | PL-E, PL-A | a conferir |
| EXT-BASE-SINAPI | SINAPI (Caixa): custos e índices da construção civil | Sistema oficial de custos | federal (nacional) | `https://www.caixa.gov.br/sinapi` | ED-A, PP-E, PP-A, MC-E | a conferir |
| EXT-BASE-SICRO | SICRO (DNIT): custos de obras rodoviárias | Sistema oficial de custos | federal (nacional) | `https://www.gov.br/dnit` (SICRO) | ED-A, PP-E | a conferir |
| EXT-BASE-IBGE | Índices do IBGE (IPCA, INPC) | Índice oficial | federal (nacional) | `https://www.ibge.gov.br` | MC-E, PP-A | a conferir |
| EXT-BASE-FGV | Índices e tabelas da FGV (IGP-M e outros) | Índice de referência | nacional | `https://portal.fgv.br` (FGV IBRE) | MC-E, PP-E, PP-A | a conferir |
| EXT-BASE-ANP | Levantamento de preços de combustíveis da ANP | Tabela oficial | federal (nacional) | `https://www.gov.br/anp` | PP-E, PP-A | a conferir |
| EXT-BASE-FIPE | Tabela FIPE (veículos) | Tabela de referência | nacional | `https://veiculos.fipe.org.br` | PP-E | a conferir |
| EXT-BASE-SUSEP | SUSEP: seguradoras autorizadas (seguro-garantia) | Base de dados pública | federal (nacional) | `https://www.gov.br/susep` | MC-E | a conferir |

---

## 6. Prova de mercado

Provas produzidas pela Servfaz para cada caso. Não têm texto a conferir; o cuidado é guardar data, origem e, nas cotações, CNPJ e descrição exata do item.

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-MERC-COTACOES | Cotações e orçamentos formais de fornecedores (data, CNPJ, descrição exata do item) | Prova de mercado | n/a | Solicitação formal aos fornecedores | PP-E, PP-A | n/a |
| EXT-MERC-DECLARACOES | Declarações de fabricantes e transportadoras (prazos de fabricação e entrega, preço de custo) | Prova de mercado | n/a | Solicitação formal aos fabricantes e transportadoras | ED-A, TR-A, PP-A | n/a |
| EXT-MERC-FICHAS | Fichas técnicas e catálogos dos principais fabricantes (comparação com a especificação do TR) | Prova de mercado | n/a | Sites e catálogos dos fabricantes | TR-A | n/a |
| EXT-MERC-ALTERNATIVAS | Levantamento de soluções alternativas de mercado e de como outros órgãos resolveram o mesmo problema | Prova de mercado | n/a | Fabricantes, contratações de outros órgãos no PNCP | ETP-A | n/a |
| EXT-MERC-SITES | Preços em sites de comércio eletrônico, com data, hora e URL | Prova de mercado | n/a | Sites de domínio amplo | PP-E, PP-A | n/a |
| EXT-MERC-MIDIA | Pesquisa publicada em mídia especializada | Prova de mercado | n/a | Publicações do setor | PP-E | n/a |
| EXT-MERC-BOLSAS | Cotações de bolsas de mercadorias (insumos como cobre e combustível) | Prova de mercado | n/a | Bolsas de mercadorias | PP-A | n/a |
| EXT-MERC-VISTORIA | Vistoria ou levantamento técnico do local de execução | Prova de mercado | n/a | Visita técnica ou declaração do responsável técnico | ETP-A | n/a |

---

## 7. Observações

1. **Faixas de artigos nos títulos da Minuta.** Os títulos de `Estrutura - Minuta Contratual.md` citam faixas (arts. 89 a 154, 105 a 114, 141 a 146, 96 a 102, 124 a 136, 155 a 163, 137 a 139). No catálogo, cada faixa aponta para o artigo citado no corpo: 105–114 → `ART106`, `ART107`, `ART111`; 141–146 → `ART141`, `ART143`; 96–102 → `ART96`, `ART102`; 124–136 → `ART124`, `ART125`, `ART135`; 155–163 → `ART156`, `ART162`; 137–139 → `ART137`, `ART138`; 151–154 → `ART151`; 89–154 → `GERAL`. Se um mapa precisar de um artigo da faixa que não está aqui, ele entra primeiro no catálogo.
2. **Mesmo número, leis diferentes.** "Art. 5º" na Análise do Edital é da CF/88 (`EXT-CF88-ART5`); nas demais Análises, é da Lei 14.133 (`EXT-LEI14133-ART5`). "Arts. 5º e 6º" na Estrutura da Pesquisa são da IN 65/2021. "Art. 66" é da Lei 9.784/1999 e "art. 48" aparece na LC 123/2006 e na Lei 8.666/1993.
3. **Fontes só históricas:** `EXT-LEI8666-GERAL`, `EXT-LC110-GERAL`, `EXT-IN5-2014`. Servem para datar súmulas e acórdãos antigos, não como fundamento.
4. **Não usar até localizar:** `EXT-STJ-RESP1733688` e `EXT-TCU-AC1182-2020` (não localizados) e todos os `EXT-PEND-*`.
5. **Fonte interna nova.** `INT-PCA` não estava na lista do plano; foi acrescentada porque o ETP (inciso II) e o TR (seção II) pedem o cruzamento com o Plano de Contratações Anual.
6. **URLs.** Os endereços do Planalto seguem o padrão do texto compilado; os demais apontam para o portal oficial do órgão quando o caminho exato não foi confirmado. Confira o link ao trocar o status para `conferido`.

## 8. Como foi verificado

Busca nos 14 arquivos por `art.`/`arts.`, `Lei`, `LC`, `Súmula`, `Acórdão`, `IN `, `Tema`, `REsp`, `Nota Técnica`, `NR-` e pelos nomes das bases (PNCP, Painel, SINAPI, SICRO, Mediador, RedeSim, CNAE, FPAS, ANP, FIPE, IPCA, IGP-M, CATMAT). Cada ocorrência foi associada a um ID deste catálogo. Os casos ambíguos estão na seção 7.
