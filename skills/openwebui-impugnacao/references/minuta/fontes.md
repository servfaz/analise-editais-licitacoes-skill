<!-- Cópia gerada por scripts/sync_estudo.py a partir de briefing/Mapeamento_Analise/Minuta Contratual/Fontes - Minuta Contratual.md. Não edite aqui: corrija a origem e rode o sync. -->

# Fontes - Minuta Contratual

Este mapa diz, para cada cláusula de `minuta/estrutura.md`, **onde buscar a prova e o fundamento** antes de decidir se uma cláusula da minuta do contrato é impugnável. Cada linha cruza a Minuta com outro documento do processo (fontes `INT-*`, com a seção a abrir), aponta as fontes externas pelo ID do `catalogo-fontes.md` (o texto, a esfera e o status ficam lá) e fecha com o critério de decisão. As cláusulas seguem os 7 focos e o checklist de bolso de `minuta/analise.md` (foco 1 → cláusula 3; focos 2 e 5 → cláusula 2; foco 3 → cláusula 4; foco 4 → cláusula 7; foco 6 → cláusula 5; foco 7 → cláusula 8); as cláusulas 1, 6 e 9 e as linhas que vêm só da Estrutura estão marcadas **[derivada da Estrutura]**. O foco da Servfaz são os serviços contínuos com dedicação exclusiva de mão de obra: repactuação (e não reajuste) com as datas-base da proposta e da CCT, garantia com as 4 modalidades à escolha da contratada, retenção só da parcela controvertida com a ressalva das garantias trabalhistas, matriz de riscos facultativa salvo nas hipóteses obrigatórias, e multa de mora sobre a parcela em atraso dentro da faixa da multa sancionatória. Antes de citar uma fonte `a conferir` em peça, confira-a no catálogo.

**Como usar:** leia a pergunta-chave, abra a Minuta na cláusula indicada e as fontes internas na seção indicada, e extraia o que a coluna "Prova" pede. No modelo da AGU para dedicação exclusiva (`EXT-AGU-CONTRATO-DEMO-2025`), pagamento, repactuação, garantia e sanções só remetem ao TR: quando a minuta remete, aplique as linhas destas cláusulas ao texto do TR (seção III para a garantia, seção VI para pagamento e repactuação e seção complementar de sanções). As cláusulas necessárias estão no art. 92 (`EXT-LEI14133-ART92`); as que não cabem nas cláusulas 1 a 9 estão nas duas seções complementares, antes da matriz. A Minuta quase sempre repete o TR (seções I, V, VI e VII) e o Edital (seções 11 e 12): toda divergência entre eles é, no mínimo, ponto de esclarecimento, e vira impugnação quando a versão da Minuta é a ilegal. Anote a **data-base do orçamento** (`INT-PLANILHA`, Módulo 1; `EXT-LEI14133-ART25`, § 7º): é ela que ancora o reajuste e, na repactuação, a data da proposta e a da CCT (`EXT-LEI14133-ART135`). Prazos de recebimento não estão na lei: o art. 140, § 3º, remete-os ao regulamento do ente ou ao contrato (`EXT-LEI14133-ART140`, `EXT-REG-ENTE`). O prazo de pagamento também vem do regulamento do ente (`EXT-REG-ENTE`) ou, na União, de `EXT-IN77-2022`. A impugnação vai contra o edital, de que a Minuta é anexo, até 3 dias úteis antes da abertura (`EXT-LEI14133-ART164`, `EXT-LEI14133-ART183`; ver `edital/fontes.md`, seção 9): cláusula não impugnada a tempo vincula a empresa na execução.

---

## 1. Cláusula de Vigência, Eficácia e Prorrogação [derivada da Estrutura]

Base: `minuta/estrutura.md`, cláusula 1 (subitens 1.1 a 1.4). A Análise não tem foco próprio para esta cláusula.

Pergunta-chave: "A vigência, a eficácia e a prorrogação da Minuta seguem a natureza do objeto definida no TR e os limites da lei, sem obrigar a empresa a prorrogar?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Natureza e prazo de vigência (1.2) | INT-MINUTA (cl. 1, subitem 1.2); INT-TR (seção I); INT-EDITAL (seção 2) | EXT-LEI14133-ART106, EXT-LEI14133-ART107, EXT-LEI14133-ART111 | Natureza do objeto (contínuo ou por escopo) e vigência inicial no TR e na Minuta | Vigência divergente entre TR e Minuta, vigência inicial de serviço contínuo acima do limite de EXT-LEI14133-ART106, ou contrato por escopo sem a prorrogação automática de EXT-LEI14133-ART111 quando o atraso é da Administração (volta de `tr/fontes.md`, seção I) | Vigência coerente nos dois documentos e dentro dos limites |
| Prorrogação sucessiva: condições (1.3) | INT-MINUTA (cl. 1, subitem 1.3); INT-EDITAL (seção 13, previsão de prorrogação) | EXT-LEI14133-ART107, EXT-AGU-CONTRATO-DEMO-2025 | Se o edital prevê a prorrogação, se a Minuta exige ateste de vantajosidade, manifestação expressa da contratada e os requisitos do modelo da AGU (relatório, interesse, habilitação, Cadin, custos não renováveis) e se admite a extinção sem ônus na negociação | Minuta que obriga a contratada a aceitar a prorrogação, ou prevê prorrogação além de 10 anos ou sem previsão no edital | Prorrogação prevista no edital, até 10 anos, com ateste e sem obrigação de aceitar |
| Extinção sem ônus na data de aniversário (1.4) | INT-MINUTA (cl. 1, subitem 1.4; cl. 8, subitem 8.4); INT-PLANILHA (Módulo 5, custos de mobilização) | EXT-LEI14133-ART106 (III e § 1º), EXT-LEI14133-ART105 | Se a Minuta limita a extinção sem ônus à data de aniversário, com 2 meses de aviso, e se a extinção antes disso gera indenização | Minuta que permite extinguir sem ônus a qualquer tempo ou com aviso menor que 2 meses | Regra do art. 106, III e § 1º |
| Prorrogação x planilha do 2º ano em diante | INT-MINUTA (cl. 1, subitem 1.3; cl. 3); INT-PLANILHA (Módulo 3; submódulo 3.1); INT-PLANILHA (Submódulos 2.1 e 4.1) | EXT-MGI-NT35883 (só União), EXT-TCU-AC1186-2017 (regra anterior), EXT-REG-ENTE, EXT-ADM-MEC-2024 | Regra da Minuta para o preço nas prorrogações (aviso prévio trabalhado reduzido nas prorrogações, 0,83% por prorrogação na União, e troca da provisão de férias depois do 1º ano) | Minuta que mantém nas prorrogações os custos que só existem no 1º ano, ou que manda reduzi-los sem a regra da planilha (volta de `planilha/fontes.md`, Módulo 3) | Regra das prorrogações coerente com a planilha |
| Vigência x meses de execução da planilha | INT-MINUTA (cl. 1); INT-PLANILHA (cabeçalho, meses de execução; Módulo 3, submódulo 3.1) | EXT-TCU-AC1186-2017, EXT-LEI14133-ART106 | Vigência inicial da Minuta ao lado dos meses de execução do cabeçalho da planilha e do percentual do aviso prévio trabalhado | Vigência inicial acima de 12 meses com o aviso trabalhado de 1,94% sem diluição (ver `planilha/fontes.md`, seção 3) | Vigência e meses coincidentes e aviso diluído |
| Condição de eficácia: divulgação no PNCP (1.1) | INT-MINUTA (cl. 1, subitem 1.1); INT-EDITAL (seção 11) | EXT-LEI14133-ART94, EXT-BASE-PNCP | Previsão de divulgação do contrato e dos aditivos no PNCP | — (ponto de execução, não de impugnação; volta de `edital/fontes.md`, seção 11) | Previsão coerente |
| Prazo de assinatura e validade da proposta | INT-MINUTA (cl. 1); INT-EDITAL (seções 5 e 11) | EXT-LEI14133-ART90, EXT-REG-ENTE | Prazo de convocação e assinatura e validade da proposta no edital e na Minuta | Divergência entre edital e Minuta, ou prazo de assinatura inexequível (volta de `edital/fontes.md`, seções 5 e 11) | Prazos coincidentes |
| Minuta publicada com o edital | INT-EDITAL (seção 13, rol de anexos); INT-MINUTA | EXT-LEI14133-ART25 (§ 3º), EXT-BASE-PNCP, EXT-BASE-COMPRASGOV | Minuta no rol de anexos ao lado do arquivo no PNCP, com data | Minuta ausente, publicada depois do edital ou só com cadastro (volta de `edital/fontes.md`, seção 13) | Publicada no mesmo dia, sem cadastro |

---

## 2. Cláusula de Condições de Pagamento e Liquidação da Despesa

Base: `minuta/analise.md`, focos 2 (prazos e condições de pagamento) e 5 (retenção); checklist, itens 3, 4 e 6.

Pergunta-chave: "O pagamento tem prazo certo, não depende de evento de terceiro, prevê encargos de mora e só retém a parcela controvertida, respeitadas as garantias trabalhistas da dedicação exclusiva?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Pagamento condicionado a repasse (checklist 3) | INT-MINUTA (cl. 2); INT-TR (seções VI e X); INT-DOTACAO | EXT-LEI14133-ART150, EXT-LEI14133-ART141, EXT-LEI14133-ART92 (V) | Cláusula que liga o pagamento à liberação de recursos de convênio ou ministério; dotação indicada no processo | Pagamento subordinado a evento incerto de terceiro, sem prazo certo (volta de `tr/fontes.md`, seções VI e X) | Dotação indicada e prazo de pagamento certo |
| Prazos de recebimento provisório e definitivo (2.1) | INT-MINUTA (cl. 2, subitem 2.1); INT-TR (seção VI) | EXT-LEI14133-ART140 (§ 3º), EXT-REG-ENTE | Prazos dos dois recebimentos no TR e na Minuta; regulamento do ente | Prazo aberto ou excessivo, ou divergência entre TR e Minuta (volta de `tr/fontes.md`, seção VI) | Prazos fixos, iguais nos dois documentos e dentro do regulamento |
| Prazo de pagamento (2.2) | INT-MINUTA (cl. 2, subitem 2.2); INT-TR (seção VI); INT-EDITAL (seção 11) | EXT-LEI14133-ART92 (V e VI), EXT-IN77-2022 (só União), EXT-REG-ENTE | Prazo de liquidação e de pagamento contado do recebimento definitivo ou da liquidação, no TR, no edital e na Minuta; prazo em branco na Minuta | Prazo aberto, prazo acima do regulamento do ente (na União, acima de 10 + 10 dias úteis de EXT-IN77-2022) ou divergente do TR | Prazo certo e dentro do regulamento |
| Ordem cronológica (2.3) | INT-MINUTA (cl. 2, subitem 2.3); INT-TR (seção VI) | EXT-LEI14133-ART141, EXT-IN77-2022 (só União), EXT-REG-ENTE | Previsão da ordem cronológica e das hipóteses de quebra | Cláusula que admite pagar fora da ordem sem as hipóteses justificadas (volta de `tr/fontes.md`, seção VI) | Ordem cronológica prevista |
| Encargos moratórios (2.4; checklist 4) | INT-MINUTA (cl. 2, subitem 2.4); INT-TR (seções VI e VII, obrigações do órgão) | EXT-LEI14133-ART92 (V), EXT-BASE-IBGE, EXT-CF88-ART37 (XXI) | Fórmula de atualização e juros pelo atraso da Administração; índice indicado | Minuta sem encargos moratórios pelo atraso do órgão (cláusula necessária) | Fórmula de atualização e juros prevista (o índice e a taxa são escolha do contrato; IPCA mais juros é parâmetro prático) |
| Liberação da parcela incontroversa (2.5) | INT-MINUTA (cl. 2, subitem 2.5); INT-TR (seção VI); INT-EDITAL (seção 11) | EXT-LEI14133-ART143, EXT-TCU-AC964-2012, EXT-TCU-AC1505-2026 | Regra da Minuta para a fatura com parte contestada; cláusula que suspende "qualquer pagamento" enquanto houver penalidade ou pendência | Minuta (ou edital) que suspende a fatura inteira enquanto houver controvérsia, penalidade ou pendência, mesmo quando outra cláusula manda liberar a parcela incontroversa | Parcela incontroversa paga no prazo |
| Retenção total por falha pontual (foco 5; checklist 6) | INT-MINUTA (cl. 2 e 7); INT-TR (seção VI, IMR); INT-PLANILHA (Módulo 6, preço do posto) | EXT-LEI14133-ART143, EXT-LEI14133-ART5, EXT-TCU-AC964-2012, EXT-TCU-AC1505-2026 | Cláusula que retém 100% da fatura por certidão vencida, documento acessório ou falta pontual; valor retido ao lado do valor da falha | Retenção da fatura inteira por falha pontual ou irregularidade fiscal, desvinculada das verbas trabalhistas do contrato (volta de `tr/fontes.md`, seção VI) | Retenção limitada à parcela controvertida ou ligada às verbas trabalhistas do contrato (linha abaixo) |
| Ressalva: garantias trabalhistas da dedicação exclusiva (2.6) | INT-MINUTA (cl. 2, subitem 2.6); INT-TR (seção V, fiscalização trabalhista); INT-PLANILHA (Módulos 2 e 3, provisões) | EXT-LEI14133-ART121 (§ 3º), EXT-IN5-2017, EXT-REG-ENTE | Previsão de conta vinculada, pagamento direto ou condicionamento do pagamento à quitação das verbas trabalhistas do contrato; rubricas provisionadas na planilha | Minuta que retém valores além das provisões da planilha ou por verbas alheias ao contrato (volta de `planilha/fontes.md`, Módulo 3, e `tr/fontes.md`, seção V) | Mecanismo de EXT-LEI14133-ART121 (§ 3º) ligado às verbas do próprio contrato: lícito, não impugnar |
| Glosa do IMR sobre a fatura | INT-MINUTA (cl. 2 e 7); INT-TR (seção VI) | EXT-LEI14133-ART143, EXT-LEI14133-ART5 | Faixas de glosa e base de cálculo (item falho x fatura total) | Glosa que supera a fração do preço correspondente à falha e não é sanção proporcional e motivada (volta de `tr/fontes.md`, seção VI) | Glosa restrita ao não executado |
| Obrigações do órgão e papéis da fiscalização | INT-MINUTA (cl. 2); INT-TR (seções V e VII) | EXT-LEI14133-ART117, EXT-AGU-MODELOS, EXT-REG-ENTE | Quem atesta, em que prazo, e obrigações da contratante coerentes com a cláusula de pagamento | — (omissão pede esclarecimento; volta de `tr/fontes.md`, seções V e VII) | Papéis e obrigações definidos |
| Remissão ao TR | INT-MINUTA (cl. 2, 3, 4 e 7); INT-TR (seções III e VI; sanções) | EXT-AGU-CONTRATO-DEMO-2025, EXT-LEI14133-ART89 (§ 2º) | Se a Minuta só remete ao TR e se o TR traz a regra completa; divergência entre o texto da Minuta e o do TR | Regra que não está em nenhum dos dois, ou que diverge entre eles sem prevalência definida | Regra completa no TR, com remissão clara |
| Pagamento antecipado (2.7) | INT-MINUTA (cl. 2, subitem 2.7); INT-EDITAL (seção 11) | EXT-LEI14133-ART145 | Se há antecipação, com justificativa no processo, previsão no edital e garantia adicional | — (antecipação irregular é risco da Administração; esclarecimento) | Sem antecipação, ou antecipação regular |

---

## 3. Cláusula de Preservação do Equilíbrio Econômico-Financeiro

Base: `minuta/analise.md`, foco 1 (reajuste); checklist, item 1.

Pergunta-chave: "A Minuta usa o instituto certo para o objeto (reajuste com índice e data-base do orçamento; repactuação com as datas-base da proposta e da CCT em dedicação exclusiva), sem condicioná-lo à vontade ou ao orçamento da Administração, e trata o reequilíbrio como direito a qualquer tempo?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Instituto certo para o objeto | INT-MINUTA (cl. 3); INT-TR (seções I e IV, dedicação exclusiva); INT-PLANILHA (Módulos 1 a 6) | EXT-LEI14133-ART25 (§ 8º, I e II), EXT-LEI14133-ART92 (V) | Se o objeto tem dedicação exclusiva ou predominância de mão de obra e qual instituto a Minuta prevê | Serviço com dedicação exclusiva só com reajuste por índice (sem repactuação), ou objeto sem mão de obra dedicada sem reajuste | Repactuação em dedicação exclusiva; reajuste nos demais |
| Omissão de reajuste ou repactuação | INT-MINUTA (cl. 3); INT-EDITAL (seção 13) | EXT-LEI14133-ART25 (§ 7º), EXT-LEI14133-ART92 (V), EXT-TCU-AC7184-2018 | Se edital e Minuta trazem cláusula de recomposição, inclusive em vigência de até 12 meses prorrogável | Minuta sem critério de reajuste ou repactuação: o critério é imposição, não discricionariedade (EXT-TCU-AC7184-2018) | Critério previsto |
| Reajuste: índice e data-base (3.1) | INT-MINUTA (cl. 3, subitem 3.1); INT-PLANILHA (data-base do orçamento); INT-PESQUISA (item 3, data do mapa de preços) | EXT-LEI14133-ART25 (§ 7º), EXT-LEI14133-ART92 (§ 3º), EXT-BASE-IBGE, EXT-BASE-FGV, EXT-BASE-SINAPI | Índice indicado e marco inicial da contagem de 12 meses ao lado da data do orçamento estimado | Data-base na assinatura do contrato ou na ordem de serviço (e não no orçamento), ou índice ausente | Índice oficial ou setorial e data-base no orçamento estimado |
| Repactuação: datas-base e procedimento (3.2) | INT-MINUTA (cl. 3, subitem 3.2); INT-PLANILHA (Módulo 1, CCT e data-base; Módulos 2 a 6, custos de mercado) | EXT-LEI14133-ART25 (§ 8º, II), EXT-LEI14133-ART135 (I e II e § 6º), EXT-LEI14133-ART92 (X), EXT-NORMA-CCT, EXT-BASE-MEDIADOR | Datas-base da Minuta (proposta para custos de mercado; acordo, convenção ou dissídio **ao qual a proposta esteja vinculada** para mão de obra), documentos exigidos e prazo de resposta ao pedido | Data-base única na assinatura, data-base da mão de obra ligada à CCT do orçamento e não à da proposta, ou falta de prazo de resposta (volta de `planilha/fontes.md`, Módulo 1) | Duas datas-base de EXT-LEI14133-ART135 e prazo de resposta previsto |
| Reajuste e repactuação na mesma minuta | INT-MINUTA (cl. 3, subitens 3.1 e 3.2); INT-TR (seção VI) | EXT-LEI14133-ART25 (§ 8º), EXT-LEI14133-ART92 (§ 4º) | Se a Minuta de serviço com dedicação exclusiva prevê, além da repactuação, reajuste do contrato inteiro por índice, e qual data-base cada um usa | Reajuste por índice do contrato inteiro ao lado da repactuação, ou cláusula que se contradiz sobre a data-base | Índice só para os custos de mercado, dentro da repactuação |
| Interregno da repactuação | INT-MINUTA (cl. 3, subitem 3.2); INT-EDITAL (seção 11); INT-TR (seção VI) | EXT-LEI14133-ART135 (§ 3º), EXT-AGU-TR-2026 | Marco do primeiro ano (CCT da proposta para mão de obra; proposta para custos de mercado; última repactuação nas seguintes) no edital, no TR e na Minuta | Interregno contado de marco diferente do art. 135, § 3º (por exemplo, da data do orçamento), ou marcos divergentes entre edital, TR e Minuta | Marcos da lei, iguais nos três documentos |
| Prazo de resposta e preclusão | INT-MINUTA (cl. 3, subitem 3.2) | EXT-LEI14133-ART92 (X e § 6º), EXT-LEI14133-ART123, EXT-AGU-TR-2026 | Prazo para decidir o pedido de repactuação; regra de preclusão do pedido não feito antes da prorrogação | Prazo bem acima de 1 mês sem motivo, ou preclusão sem ressalva no aditivo quando a CCT ainda não saiu | Prazo de cerca de 1 mês e ressalva da repactuação futura |
| Limites da CCT na repactuação | INT-MINUTA (cl. 3, subitem 3.2); INT-PLANILHA (Módulo 1 e submódulo 2.3) | EXT-LEI14133-ART135 (§§ 1º e 2º), EXT-NORMA-CCT | Cláusulas da CCT que a Minuta exclui da repactuação | Minuta que exclui cláusulas trabalhistas válidas da CCT, fora das exceções legais | Exclusão só das matérias dos §§ 1º e 2º |
| Recomposição condicionada | INT-MINUTA (cl. 3); INT-DOTACAO | EXT-CF88-ART37 (XXI), EXT-LEI14133-ART92 (V), EXT-LEI14133-ART5 | Frases como "a critério da Administração" ou "desde que haja disponibilidade orçamentária" | Reajuste ou repactuação sujeitos a juízo discricionário ou a sobra de orçamento | Recomposição como direito, com procedimento objetivo |
| Revisão por fato imprevisível (3.3) | INT-MINUTA (cl. 3, subitem 3.3; cl. 5) | EXT-LEI14133-ART124 (II, "d"), EXT-LEI14133-ART92 (XI), EXT-CC-ART393, EXT-CF88-ART37 (XXI) | Se a Minuta admite o reequilíbrio a qualquer tempo e fixa prazo de resposta | Minuta que veda o reequilíbrio, exige 12 meses para pedi-lo ou não fixa prazo de resposta | Reequilíbrio a qualquer tempo, com prazo de resposta |
| Troca de tributos na reforma tributária | INT-MINUTA (cl. 3); INT-PLANILHA (Módulo 6, submódulo 6.3; data-base) | EXT-LC214-ART348, EXT-LEI14133-ART124 (II, "d"), EXT-LEI14133-ART103 (§ 5º) | Regra da Minuta para a variação de tributos por lei posterior à data-base | Minuta que atribui à contratada a variação de tributos criada por lei superveniente (volta de `planilha/fontes.md`, Módulo 6) | Variação de tributos tratada como reequilíbrio |

---

## 4. Cláusula de Garantia Contratual de Execução

Base: `minuta/analise.md`, foco 3 (modalidade de garantia); checklist, item 2.

Pergunta-chave: "A Minuta deixa a contratada escolher entre as 4 modalidades, respeita o percentual máximo e devolve a garantia ao fim do contrato?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Escolha da modalidade (4.1) | INT-MINUTA (cl. 4, subitem 4.1); INT-EDITAL (seção 11) | EXT-LEI14133-ART96 (§ 1º), EXT-BASE-SUSEP | Modalidades admitidas no edital e na Minuta: caução em dinheiro ou títulos, seguro-garantia, fiança bancária, título de capitalização | Minuta ou edital que impõem uma só modalidade ou excluem alguma das 4, ou divergem entre si (volta de `edital/fontes.md`, seção 11) | As 4 modalidades à escolha da contratada |
| Percentual da garantia (4.2) | INT-MINUTA (cl. 4, subitem 4.2); INT-EDITAL (seção 11); INT-ETP (inciso X, riscos) | EXT-LEI14133-ART98, EXT-LEI14133-ART99, EXT-LEI14133-ART102 | Percentual exigido e justificativa de complexidade e risco quando acima de 5%; em contrato contínuo de mais de 1 ano, base anual | Percentual acima de 5% sem justificativa, acima de 10% fora de grande vulto de engenharia, ou calculado sobre o valor plurianual em contrato contínuo | Até 5%, ou até 10% justificado; grande vulto de engenharia nas regras de EXT-LEI14133-ART99 e EXT-LEI14133-ART102 |
| Liberação e restituição (4.3) [derivada da Estrutura] | INT-MINUTA (cl. 4, subitem 4.3; cl. 8, subitem 8.5) | EXT-LEI14133-ART96, EXT-LEI14133-ART100, EXT-LEI14133-ART138 (§ 2º), EXT-LEI14133-ART121 (§ 3º) | Momento e condição de devolução da garantia | Minuta sem prazo de devolução, ou que retém a garantia por obrigações alheias ao contrato | Devolução após o recebimento definitivo e a quitação das verbas do contrato |
| Prazos e suspensão da garantia (4.4) [derivada da Estrutura] | INT-MINUTA (cl. 4, subitem 4.4); INT-EDITAL (seção 11) | EXT-LEI14133-ART96 (§§ 2º e 3º) | Prazo para apresentar o seguro-garantia contado da homologação; regra da suspensão por culpa da Administração | Edital ou Minuta sem o prazo mínimo de 1 mês para o seguro-garantia antes da assinatura, ou que obriga a renovar a garantia durante suspensão causada pela Administração | Prazo de pelo menos 1 mês e desobrigação na suspensão |
| Cobertura trabalhista da garantia | INT-MINUTA (cl. 4, subitem 4.3); INT-TR (seção III, garantia) | EXT-LEI14133-ART121 (§ 3º, I), EXT-AGU-CONTRATO-DEMO-2025 | Se a garantia cobre verbas trabalhistas e rescisórias e quando é liberada | — (cobertura trabalhista é lícita em dedicação exclusiva; o vício é reter além das verbas do contrato) | Cobertura ligada às verbas do contrato |

---

## 5. Cláusula de Matriz de Alocação de Riscos

Base: `minuta/analise.md`, foco 6 (desequilíbrio na matriz).

Pergunta-chave: "Se há matriz (facultativa, salvo nas hipóteses obrigatórias), ela é equilibrada e não põe na contratada riscos que só a Administração controla? Se não há, a Minuta usa cláusula aberta para fazer o mesmo?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Matriz obrigatória ou facultativa | INT-MINUTA (cl. 5); INT-EDITAL (seção 2, objeto e regime); INT-ETP (análise de riscos, se constar dele ou de documento próprio) | EXT-LEI14133-ART22 (caput e § 3º) | Valor estimado e regime de execução (grande vulto; contratação integrada ou semi-integrada) | Objeto nas hipóteses obrigatórias sem matriz (volta de `etp/fontes.md`, inciso X) | Fora das hipóteses obrigatórias: a ausência de matriz não é vício |
| Riscos da Administração atribuídos à contratada (5.2) | INT-MINUTA (cl. 5, subitem 5.2); INT-TR (seção VII); INT-ETP (inciso X) | EXT-LEI14133-ART103, EXT-CC-ART393, EXT-LEI14133-ART124 (II, "d"), EXT-CF88-ART37 (XXI), EXT-MERC-VISTORIA | Riscos listados para a contratada (licenças, desapropriação, eventos climáticos extremos, greve geral) e quem os controla | Matriz ou cláusula aberta ("quaisquer eventos") que imputa à contratada risco sobre o qual ela não tem controle (volta de `tr/fontes.md`, seção VII, e `etp/fontes.md`, inciso X) | Alocação equilibrada, cada risco com quem pode geri-lo |
| Renúncia ao reequilíbrio (5.3) | INT-MINUTA (cl. 5, subitem 5.3; cl. 3) | EXT-LEI14133-ART103 (§ 5º), EXT-LEI14133-ART124 (I) | Se a renúncia preserva as exceções (alteração unilateral e tributos por lei superveniente) | Renúncia geral, sem as exceções legais | Exceções preservadas |
| Coerência com os riscos do planejamento | INT-MINUTA (cl. 5); INT-ETP (inciso X; análise de riscos); INT-TR (seções IV e VII) | EXT-LEI14133-ART18 (caput, X) | Riscos identificados na fase preparatória ao lado da alocação da matriz | Risco conhecido pela Administração e omitido no processo, mas lançado na contratada | Riscos do planejamento refletidos na matriz |
| Dedicação exclusiva sem matriz (5.4) [derivada da Estrutura] | INT-MINUTA (cl. 5, subitem 5.4; cl. 3) | EXT-LEI14133-ART92 (IX), EXT-AGU-CONTRATO-DEMO-2025, EXT-LEI14133-ART124 (II, "d") | Se a Minuta sem matriz transfere riscos à contratada em cláusula solta | Cláusula que põe na contratada riscos que só a Administração controla, sem matriz nem recomposição | Sem matriz e com repactuação e reequilíbrio preservados |

---

## 6. Cláusula de Alterações Contratuais e Limites de Aditivos [derivada da Estrutura]

Base: `minuta/estrutura.md`, cláusula 6 (subitens 6.1 a 6.3). A Análise não tem foco próprio para esta cláusula.

Pergunta-chave: "A Minuta respeita os limites de acréscimo e supressão e as hipóteses de alteração unilateral, sem obrigar a contratada a aceitar além deles?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Hipóteses de alteração unilateral (6.1) | INT-MINUTA (cl. 6, subitem 6.1) | EXT-LEI14133-ART124 (I) | Hipóteses previstas na Minuta | Minuta que cria hipótese de alteração unilateral fora da lei | Hipóteses legais |
| Limites de acréscimo e supressão (6.2) | INT-MINUTA (cl. 6, subitem 6.2); INT-TR (seção I, quantitativos) | EXT-LEI14133-ART125 | Percentual de acréscimo e supressão obrigatório na Minuta | Minuta que obriga a aceitar acréscimo ou supressão acima de 25% (ou acréscimo acima de 50% em reforma) | Limites legais; o que passar deles, só por acordo |
| Acréscimo consensual acima do limite (6.2) | INT-MINUTA (cl. 6, subitem 6.2) | EXT-LEI14133-ART125, EXT-AGU-CONTRATO-DEMO-2025 | Se a Minuta admite acréscimo acima de 25% por acordo, ou só a supressão consensual | — (a lei não prevê acréscimo consensual acima do limite; cláusula que o admite pede esclarecimento; posição do TCU a conferir) | Só supressão consensual acima de 25% |
| Formalização e objeto (6.3) [derivada da Estrutura] | INT-MINUTA (cl. 6, subitem 6.3) | EXT-LEI14133-ART126, EXT-LEI14133-ART130, EXT-LEI14133-ART132, EXT-LEI14133-ART136 | Se a alteração preserva o objeto, recompõe o equilíbrio no mesmo aditivo, exige aditivo prévio (ou formalização em 1 mês) e usa apostila só nos casos do art. 136 | Alteração que transfigura o objeto, aditivo de encargos sem recomposição, ou execução sem aditivo além de 1 mês | Regras dos arts. 126, 130, 132 e 136 |
| Alteração e reequilíbrio | INT-MINUTA (cl. 6; cl. 3, subitem 3.3) | EXT-LEI14133-ART124, EXT-CF88-ART37 (XXI) | Se a alteração unilateral vem com a recomposição do equilíbrio | Minuta que admite alterar encargos sem recompor o preço | Recomposição prevista |

---

## 7. Cláusula de Sanções Administrativas e Dosimetria

Base: `minuta/analise.md`, foco 4 (multas desproporcionais); checklist, item 5.

Pergunta-chave: "A multa de mora incide sobre a parcela em atraso, a multa sancionatória fica entre 0,5% e 30% do valor do contrato e a Minuta garante a defesa antes da sanção?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Multa de mora: base de cálculo | INT-MINUTA (cl. 7, subitem 7.1); INT-PLANILHA (valor da parcela ou do posto) | EXT-LEI14133-ART162, EXT-LEI14133-ART5 | Percentual diário e base (parcela em atraso x valor global); simulação com um atraso curto | Multa de mora sobre o valor global por atraso de parcela pequena, desproporcional ao dano | Multa sobre a parcela em atraso, em percentual proporcional (0,1% a 0,5% ao dia é parâmetro prático, não exigência legal) |
| Multa sancionatória: faixa legal | INT-MINUTA (cl. 7, subitem 7.1); INT-EDITAL (seção 12); INT-TR (sanções) | EXT-LEI14133-ART156 (§ 3º) | Percentuais da Minuta e do edital, lado a lado | Multa acima de 30% ou abaixo de 0,5% do valor do contrato, ou percentuais divergentes entre edital e Minuta (volta de `edital/fontes.md`, seção 12) | Percentuais na faixa e iguais nos dois documentos |
| Mora x teto: soma das multas | INT-MINUTA (cl. 7) | EXT-LEI14133-ART162, EXT-LEI14133-ART156 (§ 3º) | Se a Minuta limita o acúmulo da multa de mora ou permite que ela supere o teto da multa sancionatória | Mora sem limite, que na prática ultrapassa 30% do contrato | Mora limitada ou convertida em inexecução com multa dentro da faixa |
| Rol e prazos das sanções | INT-MINUTA (cl. 7, subitem 7.1); INT-EDITAL (seção 12) | EXT-LEI14133-ART156 (caput, §§ 4º e 5º) | Sanções previstas, prazo do impedimento e da inidoneidade e abrangência (ente ou todos os entes) | Sanção fora do rol, impedimento acima de 3 anos ou inidoneidade fora de 3 a 6 anos | Rol e prazos legais |
| Defesa prévia (7.2) [derivada da Estrutura] | INT-MINUTA (cl. 7, subitem 7.2); INT-EDITAL (seção 12) | EXT-LEI14133-ART157, EXT-LEI14133-ART158, EXT-CF88-ART5 | Prazo de defesa antes da multa e procedimento antes do impedimento e da inidoneidade | Minuta que aplica multa sem defesa de 15 dias úteis, ou impedimento e inidoneidade sem processo de responsabilização | Prazos e procedimento legais |
| Glosa do IMR usada como multa | INT-MINUTA (cl. 2 e 7); INT-TR (seção VI) | EXT-LEI14133-ART143, EXT-LEI14133-ART156 (§ 3º) | Se a glosa é desconto do não executado ou sanção disfarçada | Glosa sancionatória sem defesa e sem proporcionalidade (volta de `tr/fontes.md`, seção VI) | Glosa só do não executado; sanção pelo rito da cláusula 7 |
| Multa e glosa pelo mesmo fato | INT-MINUTA (cl. 2 e 7); INT-TR (seção VI, IMR) | EXT-LEI14133-ART156 (§ 3º), EXT-LEI14133-ART143, EXT-LEI14133-ART5 | Se a mesma avaliação do IMR gera multa e redução do pagamento | Multa e glosa somadas pelo mesmo fato, sem que a glosa seja só o desconto do não executado (a conferir caso a caso) | Glosa do não executado e multa por fato distinto |
| Infrações da licitação no contrato | INT-MINUTA (cl. 7); INT-EDITAL (seção 12) | EXT-LEI14133-ART155, EXT-LEI14133-ART156 | Se a Minuta lista infrações da fase de licitação (não manter a proposta, não assinar o contrato) ao lado das de execução | — (texto de modelo; esclarecimento formal) | Só infrações de execução |

---

## 8. Cláusula de Extinção Contratual e Direitos do Contratado

Base: `minuta/analise.md`, foco 7 (renúncia ao direito de suspensão); checklist, item 7.

Pergunta-chave: "A Minuta preserva o direito da contratada de suspender a execução ou pedir a extinção por atraso de pagamento superior a 2 meses e as demais hipóteses legais, e prevê a indenização na extinção por culpa da Administração?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Renúncia ao direito de suspensão (8.2) | INT-MINUTA (cl. 8, subitem 8.2) | EXT-LEI14133-ART137 (§ 2º, IV, e § 3º, II) | Cláusula do tipo "em nenhuma hipótese a contratada poderá suspender a execução" | Minuta que veda a suspensão ou a extinção por atraso de pagamento superior a 2 meses | Direitos de EXT-LEI14133-ART137 (§§ 2º e 3º) preservados ou não restringidos |
| Demais hipóteses a favor da contratada (8.2) [derivada da Estrutura] | INT-MINUTA (cl. 8, subitem 8.2; cl. 6) | EXT-LEI14133-ART137 (§ 2º, I, II, III e V), EXT-LEI14133-ART125 | Supressão além do limite, suspensão por ordem escrita por mais de 3 meses, suspensões repetidas, não liberação do local | Minuta que exclui alguma dessas hipóteses | Hipóteses preservadas |
| Extinção por culpa da contratada (8.1) [derivada da Estrutura] | INT-MINUTA (cl. 8, subitem 8.1); INT-TR (seção VII, obrigações) | EXT-LEI14133-ART137 | Motivos de extinção listados contra a contratada | Hipótese genérica ("a critério da Administração") que permite extinguir sem motivo legal | Motivos legais e objetivos |
| Indenização por culpa exclusiva da Administração (8.3) | INT-MINUTA (cl. 8, subitem 8.3; cl. 4, subitem 4.3) | EXT-LEI14133-ART138 (§ 2º) | Se a Minuta prevê ressarcimento dos prejuízos, devolução da garantia, pagamentos devidos e custo da desmobilização | Minuta que exclui a indenização ou a devolução da garantia nessa hipótese | Indenização prevista ou não restringida |
| Extinção sem ônus por falta de crédito ou vantagem (8.4) [derivada da Estrutura] | INT-MINUTA (cl. 8, subitem 8.4; cl. 1, subitem 1.4) | EXT-LEI14133-ART106 (III e § 1º), EXT-LEI14133-ART138 (§ 2º) | Data e aviso da extinção sem ônus e o que a Minuta paga se a extinção vier antes do aniversário | Extinção sem ônus fora da data de aniversário ou sem os 2 meses de aviso | Regra do art. 106 e ônus fora dela |
| Consequências e retenções na extinção (8.5) [derivada da Estrutura] | INT-MINUTA (cl. 8, subitem 8.5; cl. 4, subitem 4.3); INT-PLANILHA (Módulo 3) | EXT-LEI14133-ART139, EXT-LEI14133-ART121 (§ 3º), EXT-AGU-CONTRATO-DEMO-2025 | Retenção da garantia e das faturas até a prova das verbas rescisórias; pagamento direto aos empregados | Retenção total, sem relação com o inadimplemento trabalhista, ou retenção de créditos além dos prejuízos e das multas | Retenção proporcional ao inadimplemento, como no modelo da AGU |

---

## 9. Cláusula de Foro e Meios Alternativos de Resolução de Controvérsias [derivada da Estrutura]

Base: `minuta/estrutura.md`, cláusula 9 (subitens 9.1 e 9.2). A Análise não tem foco próprio para esta cláusula.

Pergunta-chave: "O foro da Minuta coincide com o do edital e, se há meio alternativo, ele está regulado de forma clara?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Foro (9.1) | INT-MINUTA (cl. 9, subitem 9.1); INT-EDITAL (seção 13) | EXT-LEI14133-ART151 | Foro no edital e na Minuta | Foro divergente entre edital e Minuta (volta de `edital/fontes.md`, seção 13) | Foro coincidente |
| Meios alternativos (9.2) | INT-MINUTA (cl. 9, subitem 9.2) | EXT-LEI14133-ART151 | Se há conciliação, mediação, comitê de disputas ou arbitragem e quem escolhe a câmara e paga os custos | — (cláusula facultativa; regra obscura pede esclarecimento) | Cláusula ausente ou clara |

---

## Seção complementar: Identificação e execução [derivada da Estrutura]

Base: `minuta/estrutura.md`, bloco "Cláusulas de identificação e execução"; tabela do art. 92 na introdução.

Pergunta-chave: "A Minuta tem as cláusulas necessárias do art. 92 e elas batem com o edital, o TR e a proposta?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Cláusulas necessárias do art. 92 | INT-MINUTA (todas); INT-TR | EXT-LEI14133-ART92, EXT-AGU-CONTRATO-DEMO-2025 | Lista dos incisos do art. 92 ao lado das cláusulas da Minuta (ou do TR, quando há remissão) | Cláusula necessária ausente na Minuta e no TR (por exemplo, prazo de pagamento, data-base, prazo de resposta à repactuação) | Todas presentes, na Minuta ou no TR |
| Preâmbulo, objeto e vinculação | INT-MINUTA (preâmbulo e cl. do objeto); INT-EDITAL (seções 1 e 2); INT-TR (seção I) | EXT-LEI14133-ART89, EXT-LEI14133-ART92 (I e II) | Número do pregão e do processo, objeto e documentos vinculados, ao lado do edital | Número de pregão ou de processo diferente do edital, ou objeto divergente do TR | Identificação igual à do edital |
| Legislação e casos omissos | INT-MINUTA (cl. da legislação) | EXT-LEI14133-ART92 (III), EXT-REG-ENTE | Normas citadas e regra dos casos omissos | — (omissão pede esclarecimento) | Cláusula presente |
| Preço e dotação | INT-MINUTA (cl. do preço e da dotação); INT-EDITAL (seção 3); INT-DOTACAO | EXT-LEI14133-ART92 (V e VIII), EXT-LEI14133-ART105, EXT-LEI14133-ART150 | Valor mensal e total, classificação da despesa e regra dos exercícios seguintes | Dotação ausente ou divergente da do edital (ver `edital/fontes.md`, seção 3) | Dotação indicada e coerente |
| Execução, gestão e subcontratação | INT-MINUTA (cl. de execução e gestão); INT-TR (seções IV e V) | EXT-LEI14133-ART92 (IV, VII e XVIII), EXT-LEI14133-ART117, EXT-LEI14133-ART122 | Regime, modelo de gestão, fiscal e regras de subcontratação, na Minuta e no TR | Minuta e TR divergentes sobre gestão ou subcontratação | Remissão ao TR, ou texto igual |
| Publicação e eficácia | INT-MINUTA (cl. da publicação) | EXT-LEI14133-ART91, EXT-LEI14133-ART94 | Divulgação no PNCP e no sítio oficial | — (ponto de execução) | Cláusula presente |
| Minuta que repete o TR | INT-MINUTA; INT-TR | EXT-LEI14133-ART89 (§ 2º) | Trechos do TR copiados na Minuta e erratas que mudaram só um dos dois | Divergência entre a cópia e o TR depois de errata, sem regra de prevalência | Cópia idêntica ou remissão |

---

## Seção complementar: Obrigações das partes [derivada da Estrutura]

Base: `minuta/estrutura.md`, bloco "Obrigações das partes"; volta de `tr/fontes.md`, seção VII.

Pergunta-chave: "As obrigações da Minuta são legais, cabem na planilha e não criam ingerência nem custo sem contrapartida?"

| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova (o que extrair ou demonstrar) | Gera impugnação se… | Descarta se… |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Obrigação sem custo na planilha | INT-MINUTA (obrigações da contratada); INT-PLANILHA (Módulo 5); INT-TR (seção VII) | EXT-LEI14133-ART92 (XIV), EXT-LEI14133-ART18 (caput, IV) | Obrigações de fazer ou de fornecer ao lado das linhas da planilha | Obrigação relevante sem custo na planilha estimada (ver `planilha/fontes.md`, Módulo 5) | Obrigação precificada |
| Ingerência na gestão da contratada | INT-MINUTA (obrigações do contratante e da contratada); INT-TR (seção V) | EXT-AGU-CONTRATO-DEMO-2025, EXT-LEI14133-ART121 | Cláusula que indica pessoas, fixa salário, subordina empregados ou paga só por reembolso de salários | Ingerência que desnatura a terceirização ou transfere a gestão de pessoal | Sem ingerência |
| Habilitação e reserva de cargos | INT-MINUTA (obrigações da contratada); INT-EDITAL (seção 8) | EXT-LEI14133-ART92 (XVI e XVII), EXT-LEI14133-ART116 | Dever de manter a habilitação e de cumprir e comprovar a reserva de cargos | Exigência de comprovação fora da lei ou sem prazo | Regras legais |
| Responsabilidade e encargos | INT-MINUTA (obrigações da contratada) | EXT-LEI14133-ART120, EXT-LEI14133-ART121 | Responsabilidade por danos e por encargos; responsabilidade da Administração por falha na fiscalização | Cláusula que exclui a responsabilidade legal da Administração na dedicação exclusiva (art. 121, § 2º) | Regra legal |
| Autorização para pagamento direto | INT-MINUTA (obrigações da contratada; cl. 2, subitem 2.6) | EXT-LEI14133-ART121 (§ 3º, IV) | Autorização, na assinatura, para descontar das faturas e pagar salários e encargos | — (medida lícita; o vício é usá-la além do inadimplemento) | Autorização ligada ao inadimplemento |
| Dever de decidir os pedidos | INT-MINUTA (obrigações do contratante) | EXT-LEI14133-ART123, EXT-LEI14133-ART92 (XI) | Prazo para decidir pedidos e para responder ao reequilíbrio | Prazo indefinido, ou bem acima de 1 mês sem motivo | Prazos fixados |
| Preposto | INT-MINUTA (obrigações da contratada); INT-TR (seção V) | EXT-LEI14133-ART118 | Exigência de preposto e se ele é posto exclusivo | Preposto exclusivo sem custo na planilha (ver `planilha/fontes.md`, Módulo 6) | Preposto previsto e precificado |
| Simples Nacional, capital social e cotas | INT-MINUTA (obrigações da contratada); INT-PLANILHA (Módulo 6) | EXT-LC123-ART17, EXT-LC123-ART18, EXT-LEI6019-ART4B, EXT-LEI14967-ART14, EXT-LEI14133-ART25 (§ 9º) | Vedação ao Simples na cessão de mão de obra e exceções; capital social exigido; cota de mulheres vítimas de violência | Vedação ao Simples que ignora as exceções do art. 18, § 5º-C (vigilância, limpeza e conservação), ou capital exigido acima do legal | Regra legal com as exceções |
| Jornada, férias e LGPD | INT-MINUTA (cláusulas complementares) | EXT-DEC12174-2024 (só União), EXT-LEI13709-GERAL, EXT-REG-ENTE | Cláusulas de compensação de jornada, férias previsíveis e proteção de dados | — (ausência é ponto de esclarecimento; fora da União, depende do regulamento) | Cláusulas presentes ou dispensadas pelo regulamento |

---

## Matriz resumo

✓ = cruzamento usado na seção. Na coluna `INT-EDITAL`, o número indica a seção do edital (numeração de `edital/estrutura.md`); na coluna `INT-TR`, o algarismo romano indica a seção do TR; na coluna `INT-ETP`, o inciso do ETP; na coluna `INT-PLANILHA`, o módulo; na coluna `INT-PESQUISA`, o item de `pesquisa/estrutura.md`; na coluna `INT-MINUTA`, outra cláusula da própria Minuta.

| Seção | INT-EDITAL | INT-TR | INT-ETP | INT-PLANILHA | INT-PESQUISA | INT-MINUTA | Externas principais |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1. Vigência e prorrogação [derivada] | 2, 5, 11, 13 | I | — | cabeçalho, 2, 3, 4, 5 | — | 3, 8 | EXT-LEI14133-ART106, EXT-LEI14133-ART107, EXT-LEI14133-ART94, EXT-AGU-CONTRATO-DEMO-2025 |
| 2. Pagamento e retenção | 11 | III, V, VI, VII, X, sanções | — | 2, 3, 6 | — | 3, 4, 7 | EXT-LEI14133-ART143, EXT-LEI14133-ART121, EXT-TCU-AC1505-2026, EXT-LEI14133-ART145 |
| 3. Equilíbrio (reajuste e repactuação) | 11, 13 | I, IV, VI | — | cabeçalho, 1 a 6 | 3 | 5 | EXT-LEI14133-ART25, EXT-LEI14133-ART135, EXT-LEI14133-ART92, EXT-AGU-TR-2026 |
| 4. Garantia | 11 | III | X | — | — | 8 | EXT-LEI14133-ART96, EXT-LEI14133-ART98, EXT-LEI14133-ART100, EXT-BASE-SUSEP |
| 5. Matriz de riscos | 2 | IV, VII | X | — | — | 3 | EXT-LEI14133-ART22, EXT-LEI14133-ART103, EXT-CC-ART393, EXT-AGU-CONTRATO-DEMO-2025 |
| 6. Alterações [derivada] | — | I | — | — | — | 3 | EXT-LEI14133-ART124, EXT-LEI14133-ART125, EXT-LEI14133-ART130, EXT-LEI14133-ART136 |
| 7. Sanções | 12 | VI, sanções | — | ✓ | — | 2 | EXT-LEI14133-ART156, EXT-LEI14133-ART162, EXT-LEI14133-ART157 |
| 8. Extinção | — | VII | — | 3, 5 | — | 1, 4, 6 | EXT-LEI14133-ART137, EXT-LEI14133-ART138, EXT-LEI14133-ART139, EXT-LEI14133-ART106 |
| 9. Foro [derivada] | 13 | — | — | — | — | — | EXT-LEI14133-ART151 |
| Identificação e execução [complementar] | 1, 2, 3, 13 | I, IV, V | — | — | — | todas | EXT-LEI14133-ART92, EXT-LEI14133-ART89, EXT-AGU-CONTRATO-DEMO-2025 |
| Obrigações das partes [complementar] | 8 | V, VII | — | 5, 6 | — | 2 | EXT-LEI14133-ART121, EXT-LEI14133-ART123, EXT-LC123-ART18 |
