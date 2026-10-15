# Fase 2 — Análise do edital e composição de preços

> ⚠️ Orientação técnica de apoio à decisão. A análise **não substitui** a leitura integral
> do edital e seus anexos, nem o parecer de um advogado especialista em direito administrativo.
> Em caso de divergência, o texto oficial do edital e seus anexos sempre prevalecem.
> **Nunca presuma** informação ausente: se um dado não constar dos documentos fornecidos,
> registre como "Não localizado / verificar no edital".

> 📌 **Regra de rastreabilidade (obrigatória em todas as respostas):** **toda** resposta,
> achado ou conclusão deve vir acompanhada da **referência da fonte**, permitindo consultar
> a origem no documento. Use o padrão:
> **`(Documento, item/cláusula, pág. X)`** — ex.: `(Edital, item 6.8, pág. 9)`,
> `(TR, item 9.25, pág. 40)`, `(Minuta, cláusula 12.1, pág. 173)`.
> Quando a informação não for localizada, registre **"Não localizado / verificar no edital"**
> em vez de responder sem fonte. Nunca apresente um dado sem indicar de onde ele veio.

> 🎯 **Regra "extrair, não descrever" (anti-generalização):** sempre extraia o **dado literal**
> presente no edital/anexos — valor, data, e-mail, número de registro (CCT, processo, item),
> percentual, quantidade, nome do cargo. É **proibido substituir um dado que consta no edital por
> descrição genérica**, tais como "parametrizado no sistema", "pisos mínimos das categorias",
> "canal institucional", "kit/conjunto completo", "documentos habituais". Se o dado realmente
> **não existir** nos documentos, escreva **"Não localizado"** — nunca preencha com texto vago.
> Prefira sempre o específico ao genérico (ex.: `R$ 1,00`, não "intervalo mínimo do sistema";
> `seprol@funai.gov.br`, não "e-mail institucional"; `CCT MTE nº DF000042/2025`, não "CCT do DF").

> 📋 **Regra de enumeração de listas (proibido resumir):** quando o edital traz uma **relação de
> itens** — peças de uniforme, materiais/equipamentos, EPIs, postos de trabalho, benefícios da CCT,
> obrigações — **liste item a item em tabela**, com **quantidade e periodicidade** quando o edital
> as fornecer. É **vedado** condensar em expressões como "kit completo", "conjunto de uniformes",
> "materiais de apoio", "benefícios das CCTs". Ex.: em vez de "uniforme completo", listar
> `Camisa social manga longa — 2 un / 12 meses`, `Calça social — 2 un / 12 meses`, etc.

> 🚫 **Trava anti-especulação:** responda **apenas** com o que consta no edital e anexos. **Não
> acrescente** hipóteses, exigências, prazos ou fundamentos que o documento não traga (ex.: supor
> "laudo LTCAT/PGR", "parentesco até terceiro grau", "prazo de mobilização de 15–30 dias" quando
> o edital não os menciona). Se, para responder, for necessário **inferir** algo, marque
> explicitamente como **[inferência]** e explique a base — nunca apresente inferência como se
> fosse texto do edital. Na dúvida entre inferir e omitir, prefira **"Não localizado"**.

---

## 🎯 Objetivo

Transformar um edital de licitação e seus anexos (Termo de Referência, Minuta de Contrato,
Planilhas) em uma análise estruturada que permita ao setor de processos:

1. **Levantar** os dados objetivos necessários à composição de preços
2. **Avaliar criticamente** habilitação, custos, riscos e legalidade das cláusulas
3. **Decidir** sobre participação e identificar o que impugnar/esclarecer

> **Escopo:** a Servfaz atua com **serviços continuados com dedicação de mão de obra**
> (terceirização). Assuma que todo edital analisado é dessa natureza — portanto os itens de
> mão de obra do Modo 1 (jornada, CCT, insalubridade, férias, uniformes, EPI, conta vinculada)
> **sempre se aplicam** e devem ser respondidos. Se algum não constar, marque "Sem previsão".

---

## 🧩 Fluxo de análise (único)

Esta fase executa **um único fluxo**, sempre na mesma ordem: primeiro o **MODO 1**, em seguida
o **MODO 2** e, por fim, o **Parecer final**. Os dois modos são **etapas sequenciais** de uma
mesma análise — **não** são opções alternativas nem exigem escolha do usuário.

| Ordem | Etapa                                               | Base     | Perfil                                                     |
| ----- | --------------------------------------------------- | -------- | ---------------------------------------------------------- |
| 1º    | **MODO 1 — Levantamento para Composição de Preços** | Prompt 1 | Analista de licitação sênior                               |
| 2º    | **MODO 2 — Parecer Estratégico Completo**           | Prompt 2 | Especialista sênior (Lei 14.133/2021 + jurisprudência TCU) |
| 3º    | **Parecer final**                                   | —        | Consolidação da decisão                                    |

> **Sempre** execute as três etapas na ordem acima (MODO 1 → MODO 2 → Parecer final), ainda que
> o usuário não peça explicitamente. Retorne primeiro o resultado completo do MODO 1 e só então
> o MODO 2.

---

## 📥 Entradas necessárias (input)

| Item                                                | Obrigatório    | Observação                                        |
| --------------------------------------------------- | -------------- | ------------------------------------------------- |
| Edital completo                                     | ✅             | PDF ou texto integral                             |
| Termo de Referência / Projeto Básico                | ✅             | Especificações do objeto                          |
| Minuta de Contrato                                  | ⭕ recomendado | Define obrigações, penalidades e matriz de riscos |
| Planilhas de custos / modelos                       | ⭕ recomendado | Necessário para análise de exequibilidade         |
| Convenção Coletiva (CCT) aplicável                  | ⭕ recomendado | Essencial em serviços com mão de obra             |
| Perfil da empresa (CNAE, porte, atestados, índices) | ⭕ recomendado | Necessário para o checklist de habilitação        |

> 📎 **Observação sobre os anexos:** os documentos (Edital, Termo de Referência, Minuta de
> Contrato, Planilhas, ETP etc.) podem vir **todos reunidos em um único anexo/arquivo** ou
> **distribuídos em dois ou mais anexos/arquivos separados**. Verifique todos os arquivos
> fornecidos antes de responder e, ao citar a fonte, identifique o documento correto mesmo
> quando estiverem consolidados em um só PDF (ex.: `(TR dentro do Edital único, item 9.25, pág. 40)`).

---

## 🧭 Metodologia

> 📚 **Consulta de CCT:** sempre que uma **Convenção Coletiva de Trabalho (CCT)** for citada ou
> identificada no edital/TR (nome do sindicato, número de registro, ex.: `PI000099/2026`), use a
> **capacidade de consulta de CCT** descrita em `references/capacidades.md` para buscar e validar
> pisos salariais, adicionais, benefícios, vigência e data-base **antes** de responder, citando a
> fonte (a CCT e o registro retornado pela consulta).
>
> - Se a capacidade **não estiver disponível**, responda com base no edital/anexos e **sinalize**
>   que os dados da CCT precisam de validação na fonte oficial.
> - Se estiver disponível mas não retornar a CCT, registre "CCT não localizada na base de CCTs /
>   verificar" e **não presuma** valores.

### MODO 1 — Levantamento para Composição de Preços

> Atue como um **analista de licitação sênior**. Extraia do edital e do termo de referência
> as informações abaixo, na ordem, para composição de preços. Responda item a item, **sempre
> com a referência da fonte** no padrão `(Documento, item/cláusula, pág. X)` — sem exceção.
> Quando não houver previsão, escreva **"Sem previsão"** e indique onde verificou.

**Objeto e disputa**

1. Qual o objeto?
2. É adjudicação por **item** ou por **lote/grupo**?
3. Qual o **modo de disputa**?
4. Qual o **intervalo de lances**?
5. Qual a **data limite** para impugnar/esclarecer?
6. Qual o **e-mail** para impugnar/esclarecer?

**Mão de obra e condições de trabalho**

7. Há previsão de **insalubridade ou periculosidade**? (indicar o percentual e os cargos afetados)
8. Qual a **jornada de trabalho**? (horas semanais/diárias e dias)
9. Qual a **Convenção Coletiva (CCT)** aplicável? → usar a consulta de CCT quando disponível (ver regra acima). Informar **nº de registro MTE e sindicato, por cargo**.
10. Haverá **substituto** na cobertura de férias? (indicar o mecanismo — planilha/IMR/glosa)
11. Há previsão de **uniformes**? **Liste todas as peças em tabela** (peça · quantidade · periodicidade) — não resumir como "kit completo".
12. Há previsão de **materiais e equipamentos**? **Enumere cada item** (item · quantidade · periodicidade), incluindo equipamentos e eventuais soluções tecnológicas.
13. Há previsão de **EPI**? **Enumere cada EPI/EPC** exigido (item · quantidade · periodicidade, quando houver).
14. Há cláusula de **repactuação**?

**Habilitação e garantias**

15. Quais **documentos de habilitação** devem ser apresentados? Responda **organizado nas
    categorias abaixo** (a estrutura), mas **extraia exaustivamente TODOS os documentos e
    exigências** de cada categoria no edital/TR, citando a fonte — os itens listados são
    **exemplos/parâmetros de referência**, não uma lista fechada. Os valores concretos (anos de
    experiência, % e nº de postos, cargos e escolaridade) **variam por edital** — extraia-os do
    edital analisado:

    - **Habilitação Jurídica:** documento de identidade (RG), registro na Junta Comercial,
      Ato Constitutivo/Estatuto/Contrato Social ou CCMEI, conforme a natureza jurídica.
    - **Habilitação Fiscal, Social e Trabalhista:** prova de CNPJ, Certidão Conjunta de Quitação
      de Tributos Federais e Dívida Ativa da União (RFB/PGFN), CRF/FGTS, CNDT (Certidão Negativa
      de Débitos Trabalhistas) e prova de inscrição e regularidade fiscal Municipal/Distrital.
      _Podem ser substituídos pela consulta cadastral no SICAF._
    - **Qualificação Econômico-Financeira:** certidão negativa de falência/insolvência civil;
      Balanço Patrimonial e Demonstrações Contábeis comprovando índices de:
      - Liquidez Geral (LG) > 1,0;
      - Liquidez Corrente (LC) > 1,0;
      - Solvência Geral (SG) > 1,0.

      _Caso algum índice seja inferior a 1,0, exige-se capital mínimo de 10% do valor estimado
      anual do contrato._ Também é exigida **Declaração de Compromissos Assumidos**, acompanhada
      da **DRE** (Demonstração do Resultado do Exercício).
    - **Qualificação Técnico-Operacional:** atestado(s) de capacidade técnica que comprove(m):
      - experiência mínima (ex.: **2 anos** — conferir no edital); e
      - prestação de serviços em quantidade equivalente a, no mínimo, **50% dos postos** a serem
        contratados (ex.: mínimo de 31 postos — recalcular conforme o nº de postos do edital).
    - **Qualificação Técnico-Profissional:** comprovação dos requisitos formais de instrução e
      experiência profissional prévia dos cargos exigidos (ex.: Assistente — Ensino Médio;
      Técnico — Ensino Médio; Técnico em Secretariado — registro profissional ativo em conselho;
      Secretário Executivo — registro profissional ativo em conselho). Extrair os cargos e
      requisitos do edital analisado.

16. A certidão de **PCD e jovem aprendiz** deve ser apresentada ou apenas marcada em campo próprio do sistema?
17. Deverá apresentar **garantia de proposta**?
18. Qual o **percentual de seguro garantia**?
19. Deverá ser cotado **encargos de conta vinculada**?

---

### MODO 2 — Parecer Estratégico Completo

> Atue como **especialista sênior em licitações públicas, direito administrativo e gestão de
> contratos** (foco na Lei 14.133/2021 e jurisprudência do TCU). Faça uma análise crítica,
> detalhada e estratégica do edital e seus anexos, estruturada **obrigatoriamente** nos 7 tópicos.
> Cada achado deve trazer a **referência da fonte** no padrão `(Documento, item/cláusula, pág. X)`;
> quando citar dispositivo legal, indique o artigo (e não invente jurisprudência).

**1. Visão geral do objeto e regras do jogo**

> Responda **todos** os subcampos abaixo (cada um com fonte). Só "feche" o ponto quando todos
> estiverem preenchidos ou marcados "Não localizado" — nenhum pode ser omitido.

- **Órgão licitante:** nome, UASG e unidade responsável.
- **Modalidade e legislação:** modalidade, nº do edital, nº do processo e lei regente.
- **Objeto:** descrição + **regime** (dedicação exclusiva) + **composição de postos por cargo**
  (quantidade de cada cargo e total de postos).
- **Critério de julgamento e formato:** critério (menor preço / maior desconto) e se é por item
  ou por grupo/lote.
- **Modo de disputa (mecânica completa):** tipo (aberto / aberto e fechado) e a **dinâmica de
  tempos** (duração da fase aberta, prorrogação, fase fechada) e o **intervalo mínimo de lances**.
- **Prazo de execução e prorrogações:** **vigência inicial** (em meses) e **limite de prorrogação**
  (ex.: até 10 anos), com a base legal. _(Campo crítico para precificação — nunca omitir.)_
- **Valor estimado:** **valor global** e **valor mensal**, e se o orçamento é sigiloso ou não.

**2. Requisitos de habilitação (checklist de riscos)**

> 📌 Contemple de forma exaustiva e completa todos os aspectos dos **Requisitos de Habilitação
> (Checklist de Riscos)** e estruture de forma clara, subdividindo em tópicos.

> Desenvolva **obrigatoriamente** nos blocos A, B e C abaixo, cada exigência com a **referência
> da fonte**. Os blocos A/B/C são a **estrutura** (categorias legais de habilitação); **dentro de
> cada bloco, extraia exaustivamente TODAS as exigências** que o edital/TR trouxer — os itens
> listados são **exemplos/parâmetros de referência**, não uma lista fechada. Os valores concretos
> (anos, % e nº de postos, valor de 10%, CBOs, escolaridade, tempo de experiência) **variam por
> edital** — extraia-os do edital analisado.

**A. Regularidade Jurídica, Fiscal, Social e Trabalhista**

- **Apresentação:** habilitação jurídica regular (Contrato Social/Estatuto), prova de inscrição
  no CNPJ, Certidão Conjunta Negativa de Tributos Federais e Dívida Ativa da União (RFB/PGFN),
  Certidão de Regularidade do FGTS (CRF), Certidão Negativa de Débitos Trabalhistas (CNDT) e
  prova de inscrição e regularidade fiscal Municipal/Distrital.
- **Uso do SICAF:** a documentação cadastrada no SICAF substitui os comprovantes habituais,
  cabendo ao pregoeiro a verificação direta no sistema.

**B. Qualificação Econômico-Financeira**

- **Certidões:** certidão negativa de falência ou recuperação judicial/insolvência civil emitida
  pelo distribuidor da sede da empresa.
- **Índices Contábeis:** comprovação dos índices de Liquidez Geral (LG), Liquidez Corrente (LC) e
  Solvência Geral (SG) superiores a 1,0, extraídos do Balanço Patrimonial e DRE (conferir o nº de
  exercícios exigido no edital, ex.: últimos 2 exercícios sociais).
- **Capital Social ou Patrimônio Líquido Mínimo:** caso algum índice seja igual ou inferior a 1,0,
  exige-se Capital Social Mínimo ou Patrimônio Líquido de 10% do valor estimado anual da
  contratação (calcular o valor a partir do edital — ex.: R$ 771.713,72).
- **Compromissos Assumidos:** Declaração de Compromissos Assumidos acompanhada da DRE do último
  exercício, demonstrando que 1/12 do valor total dos contratos vigentes não excede o Patrimônio
  Líquido do licitante.
- **Capital Social por Empregado:** na assinatura do contrato, comprovação de Capital Social
  integralizado compatível com o quantitativo de empregados (art. 4º-B da Lei nº 6.019/1974).

**C. Qualificação Técnica (Operacional e Profissional)**

- **Atestado Técnico-Operacional (quantitativo e tempo):** atestado de capacidade técnica
  comprovando prestação de serviços similares por período mínimo (ex.: 2 anos) e abrangendo, no
  mínimo, 50% do quantitativo de postos a contratar (ex.: mínimo de 31 postos — recalcular pelo
  nº de postos do edital). Admite-se o somatório de atestados de períodos ou contratos
  concomitantes.
- **Requisitos Qualitativos do Pessoal (Técnico-Profissional):** extrair os cargos, CBOs,
  escolaridade, registro profissional e experiência exigidos no edital. Exemplos de referência:
  - Assistente Administrativo (CBO 4110-10): ensino médio completo e experiência mínima de 6 meses em rotinas de apoio administrativo.
  - Técnico em Secretariado (CBO 3515-05): formação técnica em secretariado, registro profissional ativo no MTE/Conselho (Lei nº 7.377/1985) e experiência mínima de 6 meses.
  - Secretário Executivo (CBO 2523-05): ensino superior em Secretariado Executivo, registro profissional ativo (Lei nº 7.377/1985) e experiência mínima de 6 meses.
- **Vedações:** verificar proibições de participação — sociedades cooperativas (por haver dedicação
  exclusiva de mão de obra), empresas em consórcio não autorizadas, empresas sancionadas com
  impedimento/inidoneidade e pessoas jurídicas cujos sócios tenham vínculo de parentesco com
  agentes públicos do órgão.

**3. Proposta de preços e planilha de custos**

> 📌 Contemple de forma exaustiva e completa todos os aspectos da **Proposta de Preços e Planilha
> de Custos** e estruture de forma clara, subdividindo em tópicos.

> Desenvolva nos blocos A, B e C abaixo, cada dado com a **referência da fonte**. Os blocos são a
> **estrutura**; **dentro de cada um, extraia exaustivamente TODOS os custos, pisos, benefícios e
> encargos** previstos — os itens listados são **exemplos/parâmetros de referência**, não lista
> fechada. Pisos, CCTs e benefícios **variam por edital** — extraia do edital/anexos e, para dados
> de CCT, **use a consulta de CCT quando disponível** (ver regra na Metodologia).

**A. Estrutura e Adequação da Planilha**

- A composição dos custos segue o modelo oficial do Anexo VII-D da IN SEGES/MP nº 05/2017. As
  propostas devem adotar compulsoriamente os custos unitários mínimos fixados pela Administração
  (conferir o anexo de planilha do edital).

**B. Convenções Coletivas Paradigma e Pisos Salariais** _(extrair do edital + validar na consulta de CCT)_

- Identificar, por cargo: a **CCT/aditivos aplicáveis** (nº de registro MTE e sindicato), o
  **piso salarial**, o **auxílio-alimentação** e o **auxílio-transporte**. Exemplos de referência:
  - Assistente Administrativo: CCT MTE nº DF000042/2025 + Aditivos DF000199/2025 e DF000026/2026 (SINDISERVICOS/DF) — piso R$ 2.749,18; auxílio-alimentação R$ 1.020,36 (22 dias úteis); auxílio-transporte R$ 275,93.
  - Técnico em Secretariado: CCT MTE nº DF000045/2025 + Aditivo DF000024/2026 (Sind. das Secretárias do DF) — piso R$ 3.280,70; auxílio-alimentação R$ 1.034,00; auxílio-transporte R$ 244,04.
  - Secretário Executivo: CCT MTE nº DF000045/2025 + Aditivo DF000024/2026 (Sind. das Secretárias do DF) — piso R$ 6.256,66; auxílio-alimentação R$ 1.034,00; auxílio-transporte R$ 244,04.
- **Benefícios sociais obrigatórios das CCTs:** verificar seguro de vida/funeral, auxílio
  odontológico, plano ambulatorial e reembolso-creche (ex.: seguro R$ 3,78; odontológico
  R$ 14,25–14,28; ambulatorial R$ 209,40–212,00; reembolso-creche R$ 105,33).

**C. Riscos Financeiros e Tributários na Formação de Preços**

- **Vedações Tributárias:** proibição do regime **Simples Nacional** para participantes — a
  contratação configura cessão de mão de obra (art. 17, XII, da LC nº 123/2006), exigindo
  comunicação formal de exclusão à Receita Federal.
- **PIS/COFINS (regime não-cumulativo):** licitantes no Lucro Real/Não-Cumulativo devem cotar a
  **média efetiva** dos recolhimentos dos últimos 12 meses, comprovada por EFD-Contribuições.
- **Conta-Depósito Vinculada:** obrigatoriedade de retenção mensal e depósito em conta bloqueada
  das provisões: 13º salário (8,33%), férias e 1/3 constitucional (11,11%), multa rescisória do
  FGTS (4,00%) e encargos sociais sobre 13º e férias (7,18%) — conferir os percentuais no edital.
- **Insumos e Solução Tecnológica:** a proposta deve absorver o custo de uniforme (kit anual
  completo), relógio de ponto eletrônico, crachás e eventual **solução tecnológica** (aplicação
  web + app mobile) para fiscalização operacional e trabalhista, quando exigida.
- **Desequilíbrios/inexequibilidade:** apontar subestimação de custos ou exigências inexequíveis
  pelo órgão.

**4. Benefícios e vantagens competitivas**

> 📌 Contemple de forma exaustiva e completa todos os aspectos dos **Benefícios e Vantagens
> Competitivas** e estruture de forma clara, subdividindo em tópicos.

> **Busca exaustiva (não use lista fechada):** identifique **TODOS** os benefícios e vantagens
> competitivas previstos no edital e anexos, varrendo o documento inteiro — **não se limite** aos
> exemplos abaixo. Os itens a seguir são **apenas exemplos do tipo** de cláusula que configura um
> benefício/vantagem, para calibrar o que procurar; sempre que o edital trouxer outros, inclua-os.
> Para cada vantagem encontrada, explique **por que** favorece a estratégia da empresa e cite a fonte.

_Exemplos de benefícios/vantagens a procurar (rol ilustrativo, não exaustivo):_ tratamento
favorecido/margem de preferência ME/EPP (LC 123/2006); regras de subcontratação (a vedação pode
proteger empresas operacionais contra intermediadoras); cotas sociais (mulheres vítimas de
violência doméstica, PCD, aprendizes); cláusula de transição/continuidade de pessoal (reduz custo
de recrutamento da sucessora); condições que ampliem competitividade ou reduzam custo/risco.

**5. Análise de riscos contratuais e operacionais**

> 📌 Contemple de forma exaustiva e completa todos os aspectos da **Análise de Riscos Contratuais
> e Operacionais** e estruture de forma clara, subdividindo em tópicos.

> **Busca exaustiva (não use lista fechada):** identifique **TODOS** os riscos contratuais e
> operacionais do edital/TR/Minuta, varrendo o documento inteiro — **não se limite** aos exemplos
> abaixo, que servem apenas para **calibrar o tipo** de risco a procurar. Sempre que houver risco
> não listado, inclua-o. Para cada risco, **extraia os valores/prazos concretos** e cite a fonte.

_Exemplos de riscos a procurar (rol ilustrativo, não exaustivo):_ garantia de execução (percentual,
modalidades, prazo/momento e eventual preclusão); IMR/glosas (faixas de desconto sobre a fatura,
gatilhos e reincidência); prazos de substituição de pessoal (reposição de ausente e substituição
definitiva); repactuação/reajuste (interregno, marco inicial e índice, ex.: IPCA); multas e
penalidades (faixas e gatilhos); matriz de riscos desequilibrada e obrigações excessivas; critério
de inexequibilidade e diligências; e quaisquer outros riscos, evidentes ou ocultos.

**6. Pontos críticos para impugnação e esclarecimentos**

> 📌 Contemple de forma exaustiva e completa todos os aspectos dos **Pontos Críticos para
> Impugnação e Esclarecimentos** e estruture de forma clara, subdividindo em tópicos.

> **Busca exaustiva (não use lista fechada):** como especialista, varra o edital inteiro e
> identifique **TODOS** os dispositivos passíveis de questionamento formal, separados em
> **A) Impugnação** e **B) Pedido de Esclarecimento**. Os exemplos abaixo servem apenas para
> **calibrar o tipo** de cláusula problemática — **não se limite a eles**; inclua todo ponto
> encontrado, cada um com a **referência da fonte**.
> 🚫 **Não invente** fundamento legal, acórdão ou jurisprudência: cite o artigo apenas quando
> tiver segurança e, se não tiver, sinalize que **exige validação jurídica humana**.

**A. Pontos de Impugnação (cláusulas restritivas ou ilegais)**

1. **Exigência de tempo mínimo de experiência da empresa em atestado técnico** (ex.: item 9.34.1.1 do TR):
   - **Ocorrência:** exigência de comprovação de experiência mínima de 2 anos do fornecedor.
   - **Fundamento jurídico:** o TCU tem jurisprudência no sentido de que exigir tempo mínimo de
     existência/experiência prévia da empresa em atestados de capacidade técnico-operacional
     afronta o art. 67 da Lei nº 14.133/2021 e limita a competitividade — o atestado deve
     comprovar aptidão em quantitativo e complexidade similares, sem fixar tempo de mercado.
2. **Exigência de apresentar o seguro-garantia antes da assinatura, sob pena de preclusão** (ex.: item 4.4 do TR):
   - **Ocorrência:** determinação de que o seguro-garantia seja apresentado no máximo até a data
     de assinatura do contrato, sob pena de perda do direito de opção.
   - **Fundamento jurídico:** a Lei nº 14.133/2021 não condiciona a opção da modalidade de
     garantia à entrega prévia do documento antes da assinatura, devendo ser facultado o prazo
     regular de prestação após a formalização do ajuste.

**B. Pontos para Pedido de Esclarecimento**

1. **Atribuição financeira da solução tecnológica (aplicação web + app mobile)** (ex.: item 5.4.4 do TR):
   - **Objeto de questionamento:** em qual rubrica da planilha (BDI ou Insumos) a Administração
     orçou os custos de desenvolvimento e manutenção da solução tecnológica exigida — para
     garantir que não haja omissão de valores orçados pelo órgão.
2. **Prazo e canal para esclarecimentos e impugnações:**
   - Confirmar que o pedido/impugnação deve ser protocolado **até 3 dias úteis antes** da abertura
     do certame e por qual canal (ex.: e-mail `seprol@funai.gov.br` ou protocolo na sede do órgão).

**7. Principais obrigações da contratada**

> 📌 Contemple de forma exaustiva e completa todos os aspectos das **Principais Obrigações da
> Contratada** e estruture de forma clara, subdividindo em tópicos.

> **Busca exaustiva (não use lista fechada):** varra o TR e a Minuta e liste **TODAS** as
> obrigações relevantes/onerosas da contratada, com a **referência da fonte** e, quando houver,
> os **parâmetros concretos** (prazos, quantidades, periodicidade). Os exemplos abaixo servem só
> para **calibrar o tipo** de obrigação a procurar — **não se limite a eles**.

_Exemplos de obrigações a procurar (rol ilustrativo, não exaustivo):_ preposto (dedicação,
presença mínima, vedações de alocação); fornecimento e manutenção de uniformes, materiais,
equipamentos e solução tecnológica; controle de frequência e comprovação de recolhimentos
trabalhistas/previdenciários; termo de quitação anual trabalhista (art. 507-B da CLT); plano de
programação de férias; transição contratual; SLAs, relatórios e reuniões; manutenção de
regularidade e das condições de habilitação durante a vigência.

---

## 📤 Formato de saída (output)

### Cabeçalho (sempre)

| Campo                               | Conteúdo    | Fonte               |
| ----------------------------------- | ----------- | ------------------- |
| Órgão/Entidade                      | _a extrair_ | _(Doc, item, pág.)_ |
| Nº do edital / processo             | _a extrair_ |                     |
| Modalidade / critério de julgamento | _a extrair_ |                     |
| Objeto                              | _a extrair_ |                     |
| Adjudicação (item ou lote/grupo)    | _a extrair_ |                     |
| Valor estimado                      | _a extrair_ |                     |
| Data/hora da sessão                 | _a extrair_ |                     |
| Plataforma                          | _a extrair_ |                     |

A saída segue **sempre** a ordem única do fluxo: **Cabeçalho → MODO 1 → MODO 2 → Parecer final**.

- **MODO 1** → responder os 19 itens na ordem, em tabela **Pergunta | Resposta | Fonte** (a
  fonte é obrigatória em cada linha; o item 15 sai nas categorias de habilitação definidas acima).
- **MODO 2** → desenvolver os 7 tópicos, cada achado com **referência da fonte** + implicação estratégica.
- **Parecer final** → consolidação da decisão (ver abaixo).

### Parecer final

- ✅ Participar / ⚠️ Participar com ressalvas / ❌ Não participar — com justificativa objetiva,
  cada argumento remetendo à **fonte** que o sustenta
- Lista de **pendências de esclarecimento** e **pontos a impugnar** (do Tópico 6), com a
  referência da cláusula de origem `(Documento, item/cláusula, pág. X)`
- Lista de **dados não localizados** que exigem verificação no edital

---

## ✅ Checklist de extração mínima

- [ ] Objeto e forma de adjudicação (item ou lote/grupo)
- [ ] Modalidade, critério de julgamento e modo de disputa
- [ ] Valor estimado / de referência
- [ ] Data/hora da sessão, prazo e e-mail para impugnar/esclarecer
- [ ] Requisitos de habilitação (jurídica, fiscal, social, trabalhista, técnica, econômico-financeira)
- [ ] Condições de mão de obra (jornada, CCT, insalubridade/periculosidade, férias)
- [ ] Uniformes, materiais, equipamentos e EPI
- [ ] Repactuação / reajuste
- [ ] Garantia de proposta e seguro garantia (percentual)
- [ ] Conta vinculada
- [ ] Penalidades, multas e matriz de riscos
- [ ] Benefícios ME/EPP aplicáveis

---

## 🚩 Sinais de alerta (red flags)

- Cláusulas **restritivas à competitividade** (atestados com quantitativos excessivos, exigências direcionadas)
- **Matriz de riscos desequilibrada** ou multas desproporcionais na Minuta
- **Subestimação de custos** pelo órgão (planilha de referência inexequível)
- Exigências **ilegais** ou em conflito com a Lei 14.133/2021 e a jurisprudência do TCU
- Ambiguidades que possam gerar **desclassificação indevida**
- Prazos de execução/transição incompatíveis com a operação

---

## 🔗 Referências

| Recurso                                  | Link                                                                                       |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Lei 14.133/2021                          | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm) |
| Lei 13.303/2016 (Estatais)               | [planalto.gov.br](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/l13303.htm) |
| PNCP — busca de editais                  | [pncp.gov.br/app/editais](https://pncp.gov.br/app/editais)                                 |
