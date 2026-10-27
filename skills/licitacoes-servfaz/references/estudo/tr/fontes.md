<!-- Cópia gerada por scripts/sync_estudo.py a partir de briefing/Mapeamento_Analise/Termo de Referência/Fontes - Termo de Referencia.md. Não edite aqui: corrija a origem e rode o sync. -->

# Fontes - Termo de Referência

Este mapa diz, para cada uma das 10 seções de `tr/estrutura.md`, **onde buscar a prova e o fundamento** antes de decidir se um ponto do Termo de Referência (TR) é impugnável. Cada linha cruza o TR com outro documento do processo (fontes `INT-*`, com a seção a abrir), aponta as fontes externas pelo ID do `catalogo-fontes.md` (o texto, a esfera e o status ficam lá) e fecha com o critério de decisão. As seções I a VIII vêm das seções 1 a 7 de `tr/analise.md` e do checklist final (7 perguntas); as seções IX e X vêm só da Estrutura e estão marcadas **[derivada da Estrutura]**. O foco da Servfaz são os serviços com dedicação exclusiva de mão de obra: as perguntas 6 e 7 do checklist (CCT, declaração de custos trabalhistas, posto x produtividade, IMR com glosa proporcional e parcela incontroversa) estão nas seções IV, VI e IX. Antes de citar uma fonte `a conferir` em peça, confira-a no catálogo; as pendências resolvidas (`EXT-PEND-*`, seção 4.4 do catálogo) e as fontes só históricas não fundamentam peça: cite as fontes que as resolvem.

**Como usar:** leia a pergunta-chave, abra as fontes internas na seção indicada e extraia o que a coluna "Prova" pede. Normas federais marcadas `federal (União)` no catálogo cedem ao regulamento do ente (`EXT-REG-ENTE`) quando o edital for estadual ou municipal; em especial, o prazo de pagamento de `EXT-IN77-2022` (até 10 + 10 dias úteis) só vale na esfera da União. Vício do TR que nasce no ETP leva a pedido de **saneamento ou retificação**, não de nulidade (`EXT-LEI14133-ART147`). A impugnação ou o pedido de esclarecimento vai contra o edital (o TR é anexo dele), até 3 dias úteis antes da abertura (`EXT-LEI14133-ART164`, `EXT-LEI14133-ART183`; ver `edital/fontes.md`, seção 9). Se um documento depende de pedido de acesso (`EXT-LEI12527-GERAL`), protocole o esclarecimento dentro desse prazo, sem esperar a resposta da LAI.

---

## I. Definição do Objeto

Base: `tr/analise.md`, seção 1; checklist, pergunta 3.

Pergunta-chave: "O objeto está definido com precisão, é o mesmo no TR, no Edital, no ETP e na Planilha, e a reunião de serviços no mesmo lote está justificada?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Descrição, unidades e quantitativos | INT-TR (seção I e detalhamento nas seções III e IV); INT-EDITAL (seção 2); INT-ETP (incisos I, IV e VII); INT-PLANILHA (quantitativos de postos ou itens; o Módulo 6 dá só o preço unitário) | EXT-TCU-SUM177, EXT-LEI14133-ART6 (XXIII) | Tabela lado a lado: descrição, unidade e quantidade em cada documento; descrição inicial do TR ao lado do detalhamento; necessidade descrita no ETP (inciso I) ao lado do objeto | Objeto vago, descrição inicial contradita pelo detalhamento, divergência de unidade ou quantidade entre os documentos, ou objeto diferente do que a necessidade do ETP justifica (ver `etp/fontes.md`, incisos I, IV e VII) | Descrição e quantitativos idênticos, coerentes com o detalhamento e com a necessidade do ETP |
| Base dos quantitativos | INT-ETP (inciso IV); INT-HIST-CONTRATO | EXT-LEI14133-ART18 (§ 1º, IV), EXT-LEI14133-ART23, EXT-TCU-SUM177, EXT-LEI14133-ART40 (III, compras), EXT-BASE-TRANSPARENCIA, EXT-BASE-PNCP | Memória de cálculo do ETP e consumo ou execução de contratos anteriores | Quantitativo do TR sem memória de cálculo no ETP, ou muito acima do consumo histórico sem justificativa (vício do ETP que contamina o TR; pedido: saneamento ou retificação, EXT-LEI14133-ART147; detalhe em `etp/fontes.md`, inciso IV) | Quantitativos com memória de cálculo e histórico coerentes |
| Aglutinação de serviços distintos ou lote global | INT-TR (seção I); INT-ETP (inciso VIII); INT-EDITAL (seção 2) | EXT-LEI14133-ART40 (V, "b", e §§ 2º e 3º, compras), EXT-LEI14133-ART47 (II e § 1º, serviços), EXT-TCU-SUM247 | Composição do lote e justificativa numérica do ETP para não parcelar | Serviços distintos ou objeto divisível em lote único sem justificativa técnica e econômica no ETP | ETP demonstra, com números, a vantagem do lote único |
| Mercados distintos no mesmo lote | INT-TR (seção I) | EXT-BASE-CNAE, EXT-BASE-CNPJ, EXT-BASE-PNCP | CNAE de cada atividade do lote; empresas que atuam em todas elas; licitações de objeto igual no PNCP divididas por item | Atividades de ramos que não costumam atuar juntos, afunilando a concorrência | Atividades do mesmo ramo, com mercado amplo para o lote |
| Natureza e prazo de vigência | INT-TR (seção I); INT-MINUTA (cl. 1) | EXT-LEI14133-ART106, EXT-LEI14133-ART107 | Natureza (contínuo ou pontual), vigência inicial e regra de prorrogação no TR e na Minuta | Vigência divergente entre TR e Minuta, vigência inicial de serviço contínuo acima do limite de EXT-LEI14133-ART106, ou prorrogação prevista além do limite de EXT-LEI14133-ART107 | Vigência coerente nos dois documentos e dentro dos limites |
| Objeto e quantidade na pesquisa de preços | INT-TR (seção I); INT-PESQUISA (item 1, parâmetros II e IV; item 2, identidade e quantidade) | EXT-LEI14133-ART23, EXT-TCU-SUM177 | Objeto, quantidade e ramo das cotações e das contratações similares ao lado do objeto e dos quantitativos do TR | Pesquisa sobre objeto, porte ou ramo diferente do TR, que distorce o valor estimado (detalhe em `pesquisa/fontes.md`, seções 2, 6, 9 e 10) | Pesquisa sobre o mesmo objeto e porte do TR |
| Natureza do objeto e benefícios de ME/EPP | INT-TR (seção I); INT-EDITAL (seção 4) | EXT-LC123-ART48 (III), EXT-DEC8538-2015 (art. 8º; só União) | Se o TR classifica o objeto como bem divisível ou como serviço | — (o vício, se houver, está na cláusula do edital; ver `edital/fontes.md`, seção 4, "Cota reservada em objeto de serviço") | Natureza clara no TR |
| TR não divulgado com o edital | INT-EDITAL (seção 13); INT-TR | EXT-LEI14133-ART25 (§ 3º), EXT-BASE-PNCP, EXT-BASE-COMPRASGOV, EXT-BASE-SITEORGAO | Rol de anexos do Edital ao lado dos arquivos no PNCP, com data de publicação | TR ausente, publicado depois do edital ou acessível só com cadastro, conste ou não do rol de anexos (o TR integra o edital por EXT-LEI14133-ART25 (§ 3º); mesmo critério de `edital/fontes.md`, seção 13) | TR publicado no mesmo dia do edital, sem cadastro |
| Objeto e vinculação na Minuta | INT-TR (seção I); INT-MINUTA (identificação e execução) | EXT-LEI14133-ART92 (I e II), EXT-LEI14133-ART89 | Objeto, quantidades e documentos vinculados na Minuta ao lado do TR | Objeto da Minuta diferente do TR, ou número de pregão ou processo errado (ver `minuta/fontes.md`, seção complementar "Identificação e execução") | Objeto e identificação iguais |

---

## II. Justificativa e Fundamentação da Contratação

Base: `tr/analise.md`, seção 1 (confronto TR x ETP); a previsão no PCA vem da Estrutura.

Pergunta-chave: "A justificativa do TR tem lastro no ETP e no PCA, inclusive para as escolhas que restringem a disputa?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Necessidade e interesse público | INT-TR (seção II); INT-ETP (incisos I, IX e XIII) | EXT-LEI14133-ART18 (§ 1º, I e XIII; § 2º), EXT-LEI14133-ART6 (XXIII) | Problema descrito no TR ao lado da necessidade e da conclusão de viabilidade do ETP | — (justificativa genérica, sozinha, pede esclarecimento; vira impugnação quando sustenta uma restrição sem lastro, ver linha abaixo) | Justificativa remete ao ETP e é coerente com ele |
| Previsão no PCA | INT-PCA; INT-ETP (inciso II) | EXT-LEI14133-ART18 (§ 1º, II; § 2º), EXT-BASE-PNCP, EXT-REG-ENTE | Item da contratação no PCA publicado no PNCP; ou a justificativa da ausência no ETP | Contratação fora do PCA sem justificativa da ausência no ETP (vício formal do ETP; pedido: saneamento, EXT-LEI14133-ART147; ver `etp/fontes.md`, inciso II) | Contratação prevista no PCA, ou ausência justificada no ETP |
| Justificativa do agrupamento e da solução escolhida | INT-TR (seção II); INT-ETP (incisos V e VIII) | EXT-LEI14133-ART47, EXT-TCU-SUM247, EXT-TCU-AC248-2017 | Trecho do ETP que motiva o lote único ou a solução (comparação efetiva de alternativas e custos) | Justificativa do TR sem correspondência no ETP, ou ETP sem análise de parcelamento ou de alternativas (pedido: saneamento ou retificação, EXT-LEI14133-ART147) | Motivação técnica e econômica no ETP, refletida no TR |

---

## III. Descrição da Solução e Requisitos da Contratação (Especificações Técnicas)

Base: `tr/analise.md`, seção 2; checklist, pergunta 1.

Pergunta-chave: "A especificação é tão detalhada que só um fabricante atende, ou exige certificação sem base em norma oficial?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| "Digital de fabricante" (especificação direcionada) | INT-TR (seção III); INT-ETP (incisos III, V e VII) | EXT-LEI14133-ART9 (I, "a"), EXT-LEI14133-ART41 (I), EXT-TCU-AC248-2017, EXT-MERC-FICHAS | Quadro lado a lado da especificação com as fichas técnicas dos 3 ou 4 principais fabricantes, destacando o detalhe que só um atende | Detalhe irrelevante que só um fabricante atende, sem justificativa técnica no ETP | Dois ou mais fabricantes atendem, ou o detalhe tem justificativa técnica no ETP |
| Indicação de marca | INT-TR (seção III); INT-ETP (inciso V) | EXT-LEI14133-ART41 (I), EXT-LEI14133-ART9 (I, "a") | Marca citada e a justificativa no processo | Marca sem justificativa enquadrada nas hipóteses de EXT-LEI14133-ART41 (I) | Indicação justificada numa das hipóteses de EXT-LEI14133-ART41 (I) |
| Parâmetros acima ou fora das normas oficiais | INT-TR (seção III); INT-ETP (inciso III) | EXT-NORMA-ABNT, EXT-REG-INMETRO, EXT-REG-ANVISA, EXT-MTE-NR17 | Norma oficial aplicável ao produto ao lado do parâmetro exigido no TR | Parâmetro superior ou diferente da norma oficial, sem justificativa técnica no ETP | Parâmetro igual à norma ou justificado no ETP |
| Critérios de sustentabilidade (critérios verdes) [derivada da Estrutura] | INT-TR (seção III); INT-ETP (inciso XII) | EXT-LEI14133-ART9 (I, "a"), EXT-NORMA-ABNT, EXT-REG-INMETRO, EXT-MERC-FICHAS | Critério verde exigido no TR, sua origem nos impactos ambientais e medidas mitigadoras do ETP e os produtos que o atendem | Critério ambiental sem justificativa técnica no ETP que reduz o mercado a 1 produto ou fabricante (ver `etp/fontes.md`, inciso XII) | Critério justificado no ETP e atendido por mais de um fabricante |
| Produto nacional ou certificação privada exclusiva | INT-TR (seção III) | EXT-LEI14133-ART9 (I, "a"), EXT-NORMA-ABNT, EXT-REG-INMETRO | Cláusula que veda importados ou exige certificação emitida só por entidade privada | Proibição de importados sem previsão legal, ou certificação privada sem respaldo em norma oficial | Exigência com base legal ou em norma oficial |
| Laudos, certificações e registro em conselho | INT-TR (seção III); INT-EDITAL (seção 8) | EXT-REG-ANVISA, EXT-REG-INMETRO, EXT-REG-ANATEL, EXT-NORMA-ABNT, EXT-REG-CONSELHOS, EXT-BASE-CNAE | Catálogo do órgão regulador: se a certificação existe e se aplica ao produto; atividade principal do objeto e competência privativa do conselho exigido | Certificação inexistente ou inaplicável ao produto; conselho sem competência sobre a atividade | Certificação exigida pelo regulador; conselho competente |
| Prazo para obter laudo ou catálogo | INT-TR (seção III); INT-EDITAL (seções 1 e 5) | EXT-LEI14133-ART5, EXT-MERC-DECLARACOES | Intervalo entre publicação e sessão ao lado do prazo usual de emissão do documento (declaração do fabricante) | Laudo ou catálogo que não pode ser emitido antes da sessão | Prazo compatível com a emissão usual |
| Especificação versus item pesquisado | INT-TR (seção III); INT-PESQUISA (item 1, código do catálogo; item 2, identidade do objeto) | EXT-BASE-CATMAT, EXT-TCU-SUM177 | Código CATMAT/CATSER e descrição das cotações ao lado da especificação do TR | Preço estimado com item de especificação diferente da exigida no TR (detalhe em `pesquisa/fontes.md`, seções 1 e 6) | Mesmo item e mesma especificação |
| Equipamentos e materiais da especificação na planilha | INT-TR (seção III); INT-PLANILHA (Módulo 5; submódulos 5.1 a 5.3) | EXT-LEI14133-ART6 (XXIII, "i"), EXT-LEI14133-ART23 | Equipamentos, materiais e EPIs exigidos na especificação ao lado dos itens do Módulo 5 | Item exigido na especificação sem custo na planilha (ver seção VII) | Todo item com rubrica e valor |
| Garantia de execução e remissão da Minuta | INT-TR (seção III, garantia); INT-MINUTA (cl. 4); INT-EDITAL (seção 11) | EXT-LEI14133-ART96 (§§ 1º a 3º), EXT-LEI14133-ART98, EXT-LEI14133-ART121 (§ 3º, I) | Modalidades, percentual, base anual, prazo do seguro-garantia e cobertura trabalhista no TR, quando a Minuta remete a ele | TR que omite alguma das 4 modalidades, calcula sobre o valor plurianual ou dá menos de 1 mês para o seguro-garantia (ver `minuta/fontes.md`, seção 4) | Regras legais no TR e na Minuta |

---

## IV. Modelo de Execução do Objeto (A Operação)

Base: `tr/analise.md`, seção 3; checklist, perguntas 2, 6 e 7.

Pergunta-chave: "Prazos, locais e forma de execução são exequíveis e estão cobertos pela planilha, inclusive a CCT e o modelo de posto ou de produtividade?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Prazo de entrega | INT-TR (seção IV) | EXT-LEI14133-ART5, EXT-MERC-DECLARACOES | Declarações formais de fabricantes e transportadoras com os prazos usuais de fabricação e entrega para o volume licitado | Prazo que fabricantes e transportadoras declaram não conseguir cumprir para o volume licitado (inexequível pelas vias normais), comprovado pelas declarações (o prazo curto, sozinho, é indício, não prova) | Prazo compatível com as declarações |
| Locais, rotas e quantitativos por polo | INT-TR (seção IV); INT-PLANILHA (linhas de frete, diárias e combustível, que ficam fora do modelo de 6 módulos; em serviços, Módulo 5, submódulos 5.2 e 5.3) | EXT-TCU-SUM177, EXT-LEI14133-ART40 (§ 1º, compras), EXT-LEI14133-ART18 (caput, IV) | Lista de endereços, distâncias e quantidades por polo; custos de deslocamento na planilha | Locais indefinidos ("quaisquer unidades"), ou execução pulverizada sem custo correspondente na planilha | Endereços e quantidades por polo definidos e custeados |
| Condições do local e dependências não previstas | INT-TR (seções IV e VII); INT-ETP (incisos X e XI; análise de riscos, se constar dele ou de documento próprio); INT-PCA | EXT-LEI14133-ART18 (§ 1º, X), EXT-LEI14133-ART18 (caput, X), EXT-MERC-VISTORIA, EXT-BASE-PNCP | Vistoria ou levantamento técnico do local de execução (ex.: rede elétrica precária, licença ambiental não obtida) e se a execução descrita no TR depende de providência prévia ou de contratação correlata que o ETP não prevê | Execução que depende de providência prévia ou de contratação correlata omitida no ETP e no TR, com o encargo posto na contratada (pedido: que a Administração assuma a providência; ver `etp/fontes.md`, incisos X e XI) | Condições do local declaradas, e providência ou contratação correlata prevista e assumida pela Administração |
| CCT e categoria (dedicação exclusiva) | INT-TR (seção IV); INT-PLANILHA (cabeçalho, CCT e data-base; Módulo 1, submódulos 1.1 e 1.6; submódulo 2.3); INT-EDITAL (seções 5 e 7) | EXT-NORMA-CCT, EXT-BASE-MEDIADOR, EXT-LEI14133-ART63 (§ 1º), EXT-LEI14133-ART23, EXT-LEI14133-ART59 (III) | Categoria e CCT indicadas no TR; CCT vigente registrada no Mediador; piso, data-base e benefícios ao lado da planilha | TR sem categoria ou CCT, ou planilha com CCT vencida, categoria errada ou piso e benefícios abaixo da CCT vigente, o que inviabiliza a declaração de cobertura dos custos trabalhistas | Categoria e CCT vigente indicadas e refletidas na planilha; CCT homologada depois da data do orçamento se resolve por repactuação (EXT-LEI14133-ART25 (§ 8º, II), EXT-LEI14133-ART135) |
| Posto de trabalho x produtividade | INT-TR (seções IV e VI); INT-PLANILHA (Módulos 1, 4 e 5); INT-ETP (inciso VII) | EXT-IN5-2017, EXT-REG-ENTE, EXT-LEI14133-ART18 (caput, IV), EXT-LEI14133-ART6 (XXIII, "i") | Unidade de execução e de medição no TR (posto, área, produtividade) ao lado da unidade e das quantidades da planilha | Modelo de execução incoerente com a planilha (ex.: TR mede por produtividade e a planilha precifica por posto, ou o contrário) | Mesmo modelo e mesma unidade no TR e na planilha |
| Produtividade de referência | INT-TR (seção IV); INT-PLANILHA (Módulo 1, quantidade de postos); INT-ETP (inciso IV) | EXT-IN5-2017 (Anexo VI-B, itens 3 e 11, limpeza e conservação; Anexo VII-A, item 7.3) (só União), EXT-REG-ENTE | Área por tipo (interna, externa, esquadrias, banheiros), produtividade exigida por servente e postos resultantes; justificativa da produtividade no ETP; se o edital admite que o licitante proponha produtividade diferente | Produtividade acima da faixa de referência sem justificativa no ETP, postos da planilha insuficientes para a área, ou edital que não admite produtividade diferenciada do licitante (com comprovação de exequibilidade fora da faixa) | Produtividade dentro da faixa de referência do regulamento aplicável, ou diferente e justificada no ETP, com postos coerentes com a área |
| Condições do posto que geram adicional | INT-TR (seção IV); INT-PLANILHA (Módulo 1, submódulos 1.2 a 1.5) | EXT-CLT-ART192, EXT-CLT-ART193, EXT-CLT-ART73 (caput e § 1º), EXT-TST-SUM448, EXT-TST-SUM60, EXT-MTE-NR15 (Anexo 14), EXT-MTE-NR16, EXT-NORMA-CCT | Atividade e horário exigidos no TR (banheiros de grande circulação, ronda armada, trabalho noturno) ao lado dos adicionais da planilha; enquadramento e grau do adicional por EXT-MTE-NR15 ou EXT-MTE-NR16, por laudo ou pela CCT | TR exige atividade insalubre, perigosa ou noturna e a planilha zera o adicional correspondente | Adicionais previstos na planilha |
| Local e porte das contratações similares | INT-TR (seção IV); INT-PESQUISA (item 1, parâmetro II) | EXT-LEI14133-ART23 | Local de execução e quantidades por polo do TR ao lado do local e do porte das contratações usadas na pesquisa | Contratações similares de local ou porte muito diferente, sem ajuste (detalhe em `pesquisa/fontes.md`, seção 2) | Similares compatíveis em local e porte |
| Dedicação exclusiva e instituto de equilíbrio | INT-TR (seção IV); INT-MINUTA (cl. 3) | EXT-LEI14133-ART25 (§ 8º, I e II), EXT-LEI14133-ART135 | Se o TR define a execução com dedicação exclusiva ou predominância de mão de obra, ao lado do instituto previsto na Minuta (reajuste por índice ou repactuação) | Serviço com dedicação exclusiva só com reajuste por índice, sem repactuação (detalhe em `minuta/fontes.md`, seção 3) | Repactuação prevista para a mão de obra |
| Riscos da execução e matriz | INT-TR (seção IV); INT-MINUTA (cl. 5); INT-ETP (inciso X) | EXT-LEI14133-ART103, EXT-LEI14133-ART22 | Riscos que o modelo de execução traz (local, licenças, dependências) ao lado da alocação na matriz da Minuta, se houver | Risco da execução descrito no TR que a Minuta atribui à contratada sem que ela possa geri-lo (detalhe em `minuta/fontes.md`, seção 5) | Risco alocado a quem pode geri-lo, com reflexo no preço |
| Prazo de substituição (produto ou empregado) | INT-TR (seções IV e VII); INT-PLANILHA (Módulo 4) | EXT-LEI14133-ART5, EXT-LEI14133-ART40 (§ 1º, compras), EXT-MERC-DECLARACOES | Prazo de troca do produto com defeito ou de reposição do empregado faltoso no TR; prazos usuais declarados por fabricantes; custo de reposição do profissional ausente na planilha | Prazo de reposição inexequível, comprovado pelas declarações, ou reposição de empregado exigida sem custo de reposição na planilha | Prazo compatível com as declarações e reposição custeada no Módulo 4 |

---

## V. Modelo de Gestão e Fiscalização Contratual

Base: `tr/analise.md`, seção 4.

Pergunta-chave: "O TR exige preposto ou equipe além do que o objeto pede, sem custo previsto na planilha?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Preposto fixo e exclusivo | INT-TR (seção V); INT-PLANILHA (rubrica do profissional: Módulo 1 ou custos indiretos do submódulo 6.1) | EXT-LEI14133-ART118, EXT-LEI14133-ART5 | Exigência de dedicação (horas, local, formação) e a rubrica correspondente na planilha | Custo ausente da planilha (omissão de custo relevante), ou presente mas desproporcional ao objeto (fornecimento comum, manutenção periódica) | Preposto só como interlocutor, ou dedicação justificada e custeada |
| Preposto transformado em posto de trabalho | INT-TR (seções V e VII); INT-PLANILHA (Módulo 1) | EXT-LEI14133-ART118 | Tarefas atribuídas ao preposto além da interlocução formal | Preposto com tarefas de funcionário permanente do órgão, sem custo previsto | Papel limitado à interlocução |
| Papéis do gestor e dos fiscais | INT-TR (seção V); INT-MINUTA (cl. 2) | EXT-LEI14133-ART117, EXT-REG-ENTE | Atribuições do gestor, do fiscal técnico e do fiscal administrativo; quem atesta e quem pode dar ordens | — (falta de definição pede esclarecimento) | Papéis definidos |
| Fiscalização trabalhista em dedicação exclusiva | INT-TR (seção V); INT-MINUTA (cl. 2) | EXT-LEI14133-ART121 (§ 3º), EXT-IN5-2017, EXT-REG-ENTE | Documentos que o fiscal administrativo vai exigir (salários, FGTS) e garantias previstas (conta vinculada, pagamento direto) | — (as garantias de EXT-LEI14133-ART121 (§ 3º) são lícitas; impugnável só a retenção desvinculada, ver seção VI) | Exigências ligadas às verbas trabalhistas do próprio contrato |
| Modelo de gestão na Minuta | INT-TR (seção V); INT-MINUTA (identificação e execução) | EXT-LEI14133-ART92 (XVIII), EXT-LEI14133-ART117 | Cláusula de gestão e fiscalização da Minuta ao lado do TR | Minuta e TR divergentes sobre fiscal, atribuições ou prazos (ver `minuta/fontes.md`, seção complementar "Identificação e execução") | Remissão ao TR ou texto igual |

---

## VI. Critérios de Medição, Avaliação e Pagamento (SLA / IMR)

Base: `tr/analise.md`, seção 5; checklist, pergunta 7.

Pergunta-chave: "O IMR/SLA tem indicadores objetivos e glosa proporcional, e o pagamento tem prazo certo, sem reter a parcela incontroversa?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Indicadores subjetivos ou inexequíveis | INT-TR (seções IV e VI); INT-ETP (inciso IX) | EXT-LEI14133-ART5 | Fórmula de cada indicador, quem o mede e as condições do local de execução; resultados pretendidos no ETP ao lado dos indicadores (incoerência, sozinha, cabe esclarecimento; ver `etp/fontes.md`, inciso IX) | Indicador "a critério exclusivo do fiscal", ou meta impossível nas condições do local | Indicadores objetivos, mensuráveis e compatíveis com o local |
| Glosa desproporcional | INT-TR (seção VI); INT-MINUTA (cl. 2 e 7) | EXT-LEI14133-ART143, EXT-LEI14133-ART5 | Faixas de glosa e base de cálculo (item falho x fatura total) | Falha pontual que autoriza desconto de 30% ou 50% da fatura inteira, ou glosa que não recai sobre o não executado nem é penalidade proporcional e motivada (confisco arbitrário) | Glosa restrita ao não executado, ou penalidade proporcional e motivada (ex.: faixas do IMR com indicadores objetivos) |
| IMR em dedicação exclusiva | INT-TR (seções IV e VI); INT-PLANILHA (Módulo 6, preço final do posto) | EXT-LEI14133-ART143, EXT-IN5-2017, EXT-REG-ENTE | Indicadores do IMR, faixas de ajuste e efeito sobre a fatura mensal; parcela que continua incontroversa | IMR sem indicadores objetivos ou sem glosa proporcional; retenção da fatura toda por falta pontual | IMR objetivo, glosa proporcional e pagamento da parcela incontroversa |
| Pagamento condicionado a repasse | INT-TR (seções VI e X); INT-MINUTA (cl. 2); INT-DOTACAO | EXT-LEI14133-ART141, EXT-LEI14133-ART150, EXT-LEI14133-ART92 (V) | Cláusula que liga o pagamento a repasse de convênio ou ministério | Pagamento subordinado a evento incerto de terceiro, sem prazo limite certo | Prazo certo de pagamento e dotação indicada |
| Prazos de recebimento e pagamento | INT-TR (seção VI); INT-MINUTA (cl. 2, subitens 2.1, 2.2 e 2.4) | EXT-LEI14133-ART92 (V), EXT-LEI14133-ART140, EXT-IN77-2022 (só União), EXT-REG-ENTE | Prazos de recebimento provisório e definitivo, prazo de pagamento e encargos moratórios no TR e na Minuta; regulamento do ente | Prazo aberto ou excessivo, divergência entre TR e Minuta, ou falta de encargos moratórios; na esfera da União, prazo além do fixado em EXT-IN77-2022 (até 10 + 10 dias úteis) | Prazos certos, coerentes com a Minuta e com o regulamento do ente |
| Ordem cronológica de pagamentos | INT-TR (seção VI); INT-MINUTA (cl. 2) | EXT-LEI14133-ART141, EXT-IN77-2022 (só União), EXT-REG-ENTE | Previsão de pagamento pela ordem cronológica e hipóteses de quebra | Cláusula que admite pagar fora da ordem sem as hipóteses justificadas | Ordem cronológica prevista |
| Retenção por irregularidade fiscal ou documento acessório | INT-TR (seção VI); INT-MINUTA (cl. 2) | EXT-TCU-AC964-2012, EXT-TCU-AC1505-2026, EXT-LEI14133-ART143, EXT-LEI14133-ART121 (§ 3º) | Cláusula que retém pagamento por certidão vencida ou documento acessório | Retenção do pagamento de serviço executado por irregularidade fiscal (EXT-TCU-AC964-2012, EXT-TCU-AC1505-2026); ou retenção da fatura inteira por atraso de documento acessório, além da parcela controvertida (EXT-LEI14133-ART143) | Retenção vinculada às verbas trabalhistas do próprio contrato (EXT-LEI14133-ART121 (§ 3º)) |
| Repactuação ou reajuste | INT-TR (seções I e VI); INT-MINUTA (cl. 3); INT-PLANILHA (Módulos 1 a 6) | EXT-LEI14133-ART25 (§§ 7º e 8º), EXT-LEI14133-ART135, EXT-LEI14133-ART92 (X), EXT-AGU-TR-2026 | Instituto previsto (repactuação com dedicação exclusiva ou predominância de mão de obra; reajuste nos demais), datas-base (proposta e CCT) e prazo de resposta | Serviço com dedicação exclusiva sem repactuação, reajuste por índice em lugar da repactuação, ou data-base diferente da lei | Instituto e datas-base conforme a lei, iguais aos da Minuta |
| Conta vinculada ou pagamento pelo fato gerador | INT-TR (seções V e VI); INT-MINUTA (cl. 2); INT-PLANILHA (Módulos 2, 3 e 4) | EXT-LEI14133-ART121 (§ 3º), EXT-IN5-2017, EXT-AGU-TR-2026, EXT-REG-ENTE | Rubricas retidas (férias, 13º, rescisão), percentuais, banco, regras de liberação e de saldo ao fim do contrato | Retenção sem regra de liberação, percentuais acima das rubricas provisionadas na planilha, ou retenção de parcelas sem relação com verbas trabalhistas | Regras completas e percentuais iguais às provisões da planilha |
| Regras que a Minuta remete ao TR | INT-TR (seção VI); INT-MINUTA (cl. 2 e 3) | EXT-AGU-CONTRATO-DEMO-2025, EXT-LEI14133-ART92 (V, VI e X) | Se o TR traz o prazo de pagamento, a conta vinculada, a repactuação e o prazo de resposta que a Minuta não repete | Regra necessária ausente no TR e na Minuta (ver `minuta/fontes.md`, cl. 2, "Remissão ao TR") | Regra completa no TR |
| Interregno da repactuação: TR x Minuta | INT-TR (seção VI); INT-MINUTA (cl. 3); INT-EDITAL (seção 11) | EXT-LEI14133-ART135 (§ 3º) | Marco do primeiro ano da repactuação no TR, no edital e na Minuta | TR com marco diferente do art. 135, § 3º, ou diferente da Minuta (ver `minuta/fontes.md`, cl. 3, "Interregno da repactuação") | Mesmo marco legal nos três |

---

## VII. Obrigações da Contratada e da Contratante

Base: `tr/analise.md`, seção 6; checklist, pergunta 4. Seção do modelo da AGU (`EXT-AGU-MODELOS`), sem alínea própria em `EXT-LEI14133-ART6`.

Pergunta-chave: "Toda obrigação cara imposta à contratada tem quantitativo e custo na planilha, e nenhuma obrigação do órgão foi transferida?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Cláusula "guarda-chuva" (lista aberta) | INT-TR (seção VII); INT-PLANILHA (Módulo 5) | EXT-LEI14133-ART18 (caput, IV), EXT-LEI14133-ART6 (XXIII, "i"), EXT-LEI14133-ART5 | Trecho da cláusula aberta ("mesmo que não listados") e a falta de quantitativo | Obrigação aberta, sem quantitativo, que impede propostas comparáveis | Lista fechada e quantificada |
| Obrigação do TR sem custo na planilha | INT-TR (seções III, IV e VII); INT-PLANILHA (Módulo 4, substitutos; Módulo 5, uniformes, materiais e equipamentos) | EXT-LEI14133-ART6 (XXIII, "i"), EXT-LEI14133-ART23, EXT-LEI14133-ART18 (caput, IV) | Lista lado a lado: equipamentos, materiais, uniformes e substituições exigidos no TR x itens da planilha | Obrigação cara com custo zero ou genérico na planilha | Toda obrigação com rubrica e valor |
| Transferência de obrigações da Administração | INT-TR (seção VII); INT-ETP (inciso X) | EXT-LEI14133-ART5, EXT-AGU-MODELOS | Obrigação própria do órgão (reforma do prédio, equipamentos dos servidores) imposta à contratada | Despesa própria do órgão transferida à contratada, sem relação com o objeto | Obrigação ligada ao objeto e custeada |
| Riscos imprevistos atribuídos à contratada | INT-TR (seção VII); INT-MINUTA (cl. 5); INT-ETP (inciso X; análise de riscos, se constar dele ou de documento próprio) | EXT-LEI14133-ART124 (II, "d"), EXT-CF88-ART37 (XXI), EXT-LEI14133-ART103, EXT-LEI14133-ART22, EXT-LEI14133-ART18 (caput, X) | Cláusula do tipo "quaisquer reformas estruturais imprevistas" e a matriz de riscos, se houver | Cláusula aberta que atribui à contratada risco imprevisível, sem matriz que o aloque e precifique, afastando o reequilíbrio | Risco alocado na matriz, com reflexo no preço |
| Obrigações do órgão (acesso, ateste, pagamento em dia) | INT-TR (seções VI e VII); INT-MINUTA (cl. 2) | EXT-AGU-MODELOS, EXT-LEI14133-ART92 (V) | Obrigações da contratante listadas e coerência com a seção VI | — (omissão pede esclarecimento) | Obrigações do órgão previstas e coerentes |
| Obrigações na Minuta | INT-TR (seção VII); INT-MINUTA (obrigações das partes) | EXT-LEI14133-ART92 (XIV, XVI e XVII), EXT-AGU-CONTRATO-DEMO-2025 | Obrigações do TR ao lado das da Minuta (no modelo da AGU, ficam na Minuta) | Obrigações divergentes entre TR e Minuta, ou criadas só na Minuta sem custo na planilha (ver `minuta/fontes.md`, seção complementar "Obrigações das partes") | Obrigações iguais, ou só na Minuta e precificadas |

---

## VIII. Critérios de Seleção do Fornecedor e Parâmetros de Habilitação

Base: `tr/analise.md`, seção 7; checklist, pergunta 5.

Pergunta-chave: "A amostra e os atestados respeitam a lei e se limitam às parcelas de maior relevância?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Amostra ou prova de conceito antes dos lances | INT-TR (seção VIII); INT-EDITAL (seção 7) | EXT-LEI14133-ART41 (II e parágrafo único), EXT-LEI14133-ART17 (§ 3º) | Momento em que a amostra ou a prova de conceito é exigida e de quem; justificativa da necessidade no TR | Amostra ou prova de conceito exigida de todos antes da disputa, fora da pré-qualificação | Amostra só do provisoriamente vencedor, ou na pré-qualificação permanente |
| Parcelas de maior relevância e quantitativo dos atestados | INT-TR (seções I e VIII); INT-EDITAL (seção 8); INT-ETP (justificativa das exigências de habilitação, se houver) | EXT-LEI14133-ART67 (§§ 1º e 2º), EXT-TCU-SUM263 | Parcela definida no TR e quantitativo do atestado como percentual do total; justificativa da parcela no TR ou no ETP (ver `etp/fontes.md`, inciso III) | Exigência acima de 50% ou em parcela que não é de maior relevância | Parcela crítica justificada e quantitativo proporcional |
| Restrição geográfica, temporal ou de somatório | INT-TR (seção VIII); INT-EDITAL (seção 8) | EXT-LEI14133-ART67 (§ 2º), EXT-TCU-AC1101-2020 | Cláusula que exige serviço no mesmo estado, cidade ou raio, ou atestado emitido ou executado em período determinado (ex.: últimos 2 anos), ou que veda a soma de atestados | Limitação de tempo (época do atestado) ou de local; vedação de somatório ou limite de número de atestados sem justificativa técnica no processo | Sem limitação de época ou local, e somatório admitido ou vedado com justificativa técnica; exigência de experiência mínima de até 3 anos em serviço contínuo é lícita (EXT-LEI14133-ART67 (§ 5º); ver linha "Tempo de experiência x tempo de existência") |
| Atestados só de órgão público | INT-TR (seção VIII); INT-EDITAL (seção 8) | EXT-CF88-ART37 (XXI), EXT-LEI14133-ART9 (I, "a"), EXT-LEI14133-ART67 (II), EXT-TCU-GUIA-HABTEC, EXT-TCU-AC2971-2016, EXT-TCU-AC2215-2026 | Cláusula que recusa atestado de cliente particular | Atestado aceito só de pessoa jurídica de direito público, sem motivação técnica no processo | Atestados de clientes particulares aceitos |
| Tempo de experiência x tempo de existência | INT-TR (seção VIII); INT-EDITAL (seção 8) | EXT-LEI14133-ART67 (§ 5º), EXT-LEI14133-ART65 (§ 1º), EXT-TCU-AC1094-2004 (apoio parcial), EXT-TCU-AC733-2026 | Se o TR exige tempo de experiência (até 3 anos em serviço contínuo) ou tempo de existência da empresa, e se o ETP justifica essa exigência | Experiência acima de 3 anos, ou tempo mínimo de existência da empresa sem justificativa no ETP (EXT-TCU-AC733-2026; EXT-LEI14133-ART65 (§ 1º)) | Só tempo de experiência, de até 3 anos em serviço contínuo, sem exigência de tempo de existência |
| Atestado em dedicação exclusiva (gestão de mão de obra) | INT-TR (seção VIII); INT-EDITAL (seção 8) | EXT-IN5-2017 (Anexo VII-A, itens 10.6, "b" e "c", 10.6.1, 10.7 e 10.7.1) (só União), EXT-REG-ENTE, EXT-LEI14133-ART67 (§§ 2º e 5º) | Número de postos licitados e de postos exigidos nos atestados; se o TR aceita atestado de gestão de serviços de terceirização compatíveis com o objeto ou exige o mesmo serviço; tempo de experiência exigido e se admite somatório de atestados e períodos não contínuos | Na contratação por postos, exige execução do mesmo serviço e recusa atestado de gestão de terceirização compatível; exige postos acima do parâmetro de referência (mais de 40 postos: até 50% deles; até 40: número equivalente) ou experiência acima de 3 anos; ou veda somatório de atestados ou de períodos — sem justificativa no processo | Atestado de gestão de mão de obra dentro desses limites, ou regra do regulamento do ente (EXT-REG-ENTE) observada |
| Vistoria técnica | INT-TR (seção VIII); INT-EDITAL (seção 8) | EXT-LEI14133-ART63 (§§ 2º e 3º) | Se a vistoria pode ser substituída por declaração do responsável técnico | Vistoria presencial obrigatória sem alternativa de declaração | Vistoria facultativa ou substituível por declaração |
| Critério de julgamento e modo de disputa | INT-TR (seção VIII); INT-EDITAL (seções 1, 6 e 7) | EXT-LEI14133-GERAL, EXT-REG-ENTE | Critério de seleção e, se o TR o indicar, modo de disputa, ao lado do preâmbulo, das regras da sessão e das regras de julgamento do edital | Critério ou modo divergente entre TR e edital | Critério e modo idênticos |

---

## IX. Estimativa do Valor da Contratação

**[derivada da Estrutura]** — sem seção correspondente em `tr/analise.md` (o tema aparece só na seção 6 da Análise, pela memória de cálculo). Pelo catálogo (seção 9.1), `EXT-LEI14133-ART6` (XXIII, "i") manda a estimativa com memória de cálculo constar de **documento separado e classificado**.

Pergunta-chave: "O valor estimado tem memória de cálculo, remete à pesquisa e à planilha, é o mesmo nos demais documentos e, se sigiloso, o sigilo é válido?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Documento da estimativa e memória de cálculo | INT-TR (seção IX); INT-PLANILHA (Módulos 1 a 6); INT-PESQUISA (item 3, tratamento dos dados; conteúdo mínimo; dedicação exclusiva) | EXT-LEI14133-ART6 (XXIII, "i"), EXT-LEI14133-ART18 (caput, IV), EXT-LEI14133-ART54, EXT-LEI12527-GERAL | Onde está a estimativa (corpo do TR ou documento separado e classificado) e se há memória de cálculo e composição de custos | Estimativa sem memória de cálculo nem composição de custos no processo, com a ausência demonstrada; se o documento separado for classificado e não estiver acessível, pedir antes esclarecimento ou acesso (EXT-LEI12527-GERAL, EXT-LEI14133-ART54) | Memória de cálculo existente, no TR ou em documento separado (o valor fora do corpo do TR não é vício, por si) |
| Sigilo do orçamento | INT-TR (seção IX); INT-EDITAL (seção 3); INT-PLANILHA (Módulos 1 a 6); INT-PESQUISA (item 3, mapa de preços) | EXT-LEI14133-ART24, EXT-LEI12527-GERAL | Justificativa do sigilo; se quantitativos e dados necessários à proposta foram divulgados | Sigilo sem justificativa, ou que oculta quantitativos e informações necessárias à proposta | Sigilo motivado com quantitativos divulgados, ou orçamento público |
| Parâmetros da pesquisa de preços | INT-PESQUISA (parâmetros I a V; item 2, validade das cotações) | EXT-LEI14133-ART23, EXT-IN65-ART5 (só União), EXT-IN65-ART6 (só União), EXT-REG-ENTE, EXT-BASE-PNCP, EXT-BASE-PESQPRECOS | Fontes usadas, datas (1 ano para contratações similares, 6 meses para cotações) e identidade com o objeto do TR | Estimativa apoiada em cotações vencidas, em objeto diferente do TR ou em quantidade incompatível (sem economia de escala); detalhe em `pesquisa/fontes.md`, seções 6, 10 e 13 | Cesta de preços válida e compatível com o TR |
| Coerência do valor entre documentos | INT-TR (seção IX); INT-ETP (inciso VI); INT-PESQUISA (item 3, mapa de preços); INT-PLANILHA (Módulo 6, preço final); INT-EDITAL (seção 7) | EXT-LEI14133-ART23, EXT-LEI14133-ART59 (III) | Valor global e unitário no TR, no ETP, na planilha e no teto do edital, ao lado do menor valor da própria pesquisa | Divergência de valor entre TR, planilha e teto do edital, ou discrepância grande do ETP sem explicação no processo; ou teto abaixo do menor valor da própria pesquisa | Valores coerentes (o do ETP é preliminar e pode ter sido atualizado com memória) |
| Valor x obrigações e custos trabalhistas | INT-TR (seções IV e VII); INT-PLANILHA (Módulos 1 a 6) | EXT-LEI14133-ART11 (III), EXT-LEI14133-ART23, EXT-NORMA-CCT, EXT-BASE-MEDIADOR | Valor estimado e rubricas da planilha (Módulos 1 a 6) ao lado do custo das obrigações exigidas nas seções IV e VII do TR e do piso, dos benefícios e da data-base da CCT vigente registrada no Mediador | Valor estimado que não cobre as obrigações do TR ou a CCT vigente, induzindo preço inexequível | Valor cobre as obrigações e a CCT (ver seções IV e VII) |

---

## X. Adequação Orçamentária

**[derivada da Estrutura]** — sem seção correspondente em `tr/analise.md`; corresponde a `EXT-LEI14133-ART6` (XXIII, "j").

Pergunta-chave: "Há dotação e fonte de recursos indicadas, iguais às do edital e compatíveis com o objeto e com as leis orçamentárias?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Indicação da dotação e da fonte de recursos | INT-DOTACAO; INT-TR (seção X); INT-EDITAL (seção 3) | EXT-LEI14133-ART6 (XXIII, "j"), EXT-LEI14133-ART150 | Rubrica e fonte de recursos no TR e no edital | Ausência de dotação, rubrica incompatível com o objeto ou divergente da do edital | Dotação indicada, compatível e igual à do edital |
| Compatibilidade com as leis orçamentárias | INT-DOTACAO; INT-PCA; INT-TR (seção X) | EXT-LEI14133-ART18 (caput) | Previsão no PCA e menção às leis orçamentárias | — (esclarecimento) | Compatibilidade declarada |
| Pagamento dependente de recurso externo | INT-TR (seções VI e X); INT-MINUTA (cl. 2); INT-DOTACAO | EXT-LEI14133-ART150, EXT-LEI14133-ART141 | Fonte de recursos (convênio, repasse) e se o pagamento foi condicionado a ela | Pagamento condicionado ao repasse, sem prazo certo (ver seção VI) | Dotação indicada e prazo de pagamento certo |

---

## Seção complementar: Infrações e Sanções Administrativas

**[derivada da Estrutura]** — sem alínea do art. 6º, XXIII; seção própria no modelo de TR da AGU (item 8) e presente nos 4 TRs da pasta de editais. Citada nos outros mapas como `INT-TR (sanções)`.

Pergunta-chave: "As infrações e sanções do TR são as mesmas do Edital e da Minuta e respeitam a faixa legal?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Coerência entre TR, Edital e Minuta | INT-TR (sanções); INT-EDITAL (seção 12); INT-MINUTA (cl. 7) | EXT-LEI14133-ART156, EXT-AGU-TR-2026 | Tabela lado a lado das infrações, sanções e percentuais nos três documentos | Percentuais ou sanções divergentes entre os documentos | Textos coincidentes |
| Faixa legal da multa | INT-TR (sanções); INT-MINUTA (cl. 7) | EXT-LEI14133-ART156 (§ 3º), EXT-LEI14133-ART162 | Percentual da multa sancionatória e base da multa de mora | Multa fora de 0,5% a 30% do valor do contrato, ou mora calculada sobre o valor global | Multas dentro da faixa e mora sobre a parcela em atraso |
| Processo sancionador | INT-TR (sanções); INT-EDITAL (seção 12) | EXT-LEI14133-ART157, EXT-LEI14133-ART158, EXT-CF88-ART5 | Prazo de defesa e procedimento antes da sanção | Sanção sem defesa prévia ou sem o processo do art. 158 | Defesa e procedimento previstos |

---

## Matriz resumo

✓ = cruzamento usado na seção. Na coluna `INT-EDITAL`, o número indica a seção do edital a cruzar (numeração de `edital/estrutura.md`); na coluna `INT-TR`, o algarismo romano indica outra seção do próprio TR; na coluna `INT-ETP`, o algarismo romano indica o inciso do ETP a cruzar (`etp/fontes.md` tem a volta no mesmo inciso), e "justificativa" indica a justificativa das exigências de habilitação, cruzada em `etp/fontes.md`, inciso III; na coluna `INT-MINUTA`, a cláusula (`minuta/fontes.md` tem a volta na mesma cláusula). `INT-DOTACAO` (seções VI e X), `INT-PCA` (seções II, IV e X) e `INT-HIST-CONTRATO` (seção I) aparecem só nas tabelas.

| Seção | INT-EDITAL | INT-TR | INT-ETP | INT-PLANILHA | INT-PESQUISA | INT-MINUTA | Externas principais |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| I. Objeto | 2, 4, 13 | III, IV | I, IV, VII, VIII | ✓ | ✓ | 1, identificação | EXT-TCU-SUM177, EXT-LEI14133-ART47, EXT-TCU-SUM247 |
| II. Justificativa | — | — | I, II, V, VIII, IX, XIII | — | — | — | EXT-LEI14133-ART18, EXT-LEI14133-ART47, EXT-TCU-AC248-2017 |
| III. Solução e requisitos | 1, 5, 8, 11 | — | III, V, VII, XII | ✓ | ✓ | 4 | EXT-LEI14133-ART9, EXT-LEI14133-ART41, EXT-NORMA-ABNT |
| IV. Modelo de execução | 5, 7 | VI, VII | IV, VII, X, XI | ✓ | ✓ | 3, 5 | EXT-NORMA-CCT, EXT-LEI14133-ART63, EXT-TCU-SUM177 |
| V. Gestão e fiscalização | — | VII | — | ✓ | — | 2, identificação | EXT-LEI14133-ART118, EXT-LEI14133-ART117, EXT-LEI14133-ART121 |
| VI. Medição e pagamento | 11 | IV, X | IX | ✓ | — | 2, 3, 7 | EXT-LEI14133-ART143, EXT-LEI14133-ART141, EXT-IN77-2022, EXT-LEI14133-ART135, EXT-LEI14133-ART121 |
| VII. Obrigações | — | III, IV, VI | X | ✓ | — | 2, 5, obrigações | EXT-LEI14133-ART18, EXT-LEI14133-ART6, EXT-LEI14133-ART103 |
| VIII. Seleção e habilitação | 1, 6, 7, 8 | I | justificativa | — | — | — | EXT-LEI14133-ART41, EXT-LEI14133-ART67, EXT-TCU-SUM263 |
| IX. Estimativa do valor [derivada] | 3, 7 | IV, VII | VI | ✓ | ✓ | — | EXT-LEI14133-ART6, EXT-LEI14133-ART23, EXT-LEI14133-ART24 |
| X. Adequação orçamentária [derivada] | 3 | VI | — | — | — | 2 | EXT-LEI14133-ART6, EXT-LEI14133-ART150, EXT-LEI14133-ART18 |
| Sanções [complementar] | 12 | — | — | — | — | 7 | EXT-LEI14133-ART156, EXT-LEI14133-ART157, EXT-LEI14133-ART158 |
