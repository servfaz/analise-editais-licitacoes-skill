<!-- Cópia gerada por scripts/sync_estudo.py a partir de briefing/Mapeamento_Analise/Planilha de Custos/Estrutura - Planilha de Custos.md. Não edite aqui: corrija a origem e rode o sync. -->

Este documento descreve a **anatomia de cada linha (rubrica)** da planilha de custos e formação de preços.

No serviço público brasileiro, o padrão mais rigoroso e utilizado pelos órgãos é o modelo federal instituído pela **IN SEGES/MPDG nº 05/2017**. A **IN SEGES/ME nº 98/2022** não alterou o modelo: ela autoriza a aplicação da IN 5/2017, no que couber, às contratações regidas pela Lei nº 14.133/2021. Esse padrão desdobra a planilha em **6 Módulos com submódulos matemáticos detalhados**.

> **Nota sobre a esfera:** a IN SEGES/MPDG nº 05/2017 e o seu modelo de planilha são normas **federais**. Estados e municípios podem ter modelo próprio ou adotar o federal; confira o regulamento do ente que publicou o edital.

> **Modelo adaptável:** o próprio Anexo VII-D diz que a tabela "poderá ser adaptada às características do serviço contratado, inclusive no que concerne às rubricas e suas respectivas provisões" (Nota 1 da identificação do serviço). Adaptar o modelo não é vício; o vício é a adaptação que **omite custo obrigatório** (lei, CCT, TR) ou que mistura modelos diferentes entre a planilha de referência e a exigida na proposta.

> **Numeração:** a numeração 1.1 a 1.6, 2.1 a 2.3, 3.1 a 3.3, 4.1, 4.2 e 5.1 a 6.3 abaixo é a usada nos mapas de fontes (`INT-PLANILHA (Módulo N; submódulo N.N)`). As alíneas do Anexo VII-D (A, B, C...) estão indicadas em cada item.

Abaixo está o detalhamento completo de cada bloco, suas subdivisões, fórmulas e segredos práticos:

---

### Cabeçalho e Dados da Mão de Obra (antes do Módulo 1)

O Anexo VII-D abre com dois quadros que identificam a planilha. São eles que mostram **qual CCT, qual data-base e qual vigência** o orçamento usou; sem eles não é possível conferir o Módulo 1 nem a repactuação.

- **Discriminação dos serviços (dados da contratação):** data de apresentação da proposta; município/UF de execução; ano e número de registro da CCT (acordo, convenção ou dissídio) no MTE; número de meses de execução contratual. A identificação do serviço traz o tipo, a unidade de medida e a quantidade total.
- **Mão de obra vinculada à execução contratual:** tipo de serviço, CBO, salário normativo da categoria, categoria profissional e data-base da categoria. O modelo manda fazer um quadro para cada tipo de serviço e calcular sobre o valor mensal do empregado.
- **O que conferir:** se a CCT do cabeçalho é a vigente na data-base do orçamento e a da categoria e do local do TR; se os meses de execução coincidem com a vigência do TR e da Minuta (eles influem no Módulo 3); e se o regime tributário declarado coincide com o do Módulo 6.

---

### Módulo 1: Composição da Remuneração Direta

Este módulo apura quanto custa a remuneração direta do trabalhador por mês. Ele é a **base de cálculo de quase todos os percentuais dos módulos seguintes**. Se errar aqui, todo o resto da planilha desmorona.

_Correspondência com o Anexo VII-D (Módulo 1, redação da IN 7/2018): A salário-base (1.1) · B adicional de periculosidade (1.2) · C adicional de insalubridade (1.3) · D adicional noturno e **E adicional de hora noturna reduzida**, que no modelo são linhas separadas (1.4) · F outros (1.5 e 1.6). O DSR sobre os adicionais (1.5) não é linha própria do modelo: quando devido, entra em "F – Outros", com memória de cálculo._

- **1.1. Salário-Base (alínea A):**
  - O que é: O piso salarial obrigatório da categoria.
  - Onde checar: **Convenção Coletiva de Trabalho (CCT)** registrada no Ministério do Trabalho e Emprego (MTE).
  - _Ponto crítico:_ Checar a **data-base**. Se a CCT venceu e já houve reajuste em mesa de negociação com efeito retroativo, e o órgão usou a tabela do ano anterior, o salário-base está defasado.
- **1.2. Adicional de Periculosidade (alínea B):**
  - Regra legal: **30% fixo** calculado estritamente sobre o salário-base (art. 193 da CLT).
  - Quem recebe: Vigilantes armados, eletricistas de alta tensão, frentistas, motoboys.
- **1.3. Adicional de Insalubridade (alínea C):**
  - Regra legal: Percentuais de **10% (grau mínimo), 20% (grau médio) ou 40% (grau máximo)**.
  - _Base de cálculo:_ Pelo art. 192 da CLT e Súmula Vinculante nº 4 do STF, a base é o **Salário Mínimo Nacional**, a menos que a CCT da categoria estipule expressamente o cálculo sobre o piso da categoria.
- **1.4. Adicional Noturno e Hora Noturna Reduzida (alíneas D e E do modelo):**
  - Horário: Trabalho executado entre as **22h00 e as 05h00**.
  - Percentual: **20%** sobre o valor da hora normal (para trabalhadores urbanos).
  - _O Detalhe Oculto (Hora Ficta):_ A hora noturna não tem 60 minutos, mas **52 minutos e 30 segundos** (art. 73, § 1º da CLT). Isso exige aplicar um fator multiplicador de **1,1428** sobre o cálculo da hora normal.
- **1.5. Descanso Semanal Remunerado (DSR) sobre os Adicionais (no modelo, em "F – Outros"):**
  - Adicionais noturnos e horas extras habituais geram reflexo no pagamento dos domingos e feriados (DSR). A Súmula nº 172 do TST trata das horas extras habituais no DSR; a integração do adicional noturno pago com habitualidade é da Súmula nº 60 do TST (item I; o item II estende o adicional às horas prorrogadas após a jornada noturna).
- **1.6. Gratificações e Adicionais Convencionais (alínea F – Outros):**
  - Previsões específicas da CCT, como: adicional de função (líder de equipe), triênio, biênio, assiduidade.

---

### Módulo 2: Encargos e Benefícios Anuais, Mensais e Diários

_Correspondência com o modelo da IN 5/2017, alterada pela IN 7/2018 (Anexo VII-D, conferido no Portal de Compras): o Módulo 2 tem os mesmos três submódulos — 2.1 (13º Salário, Férias e Adicional de Férias), 2.2 (GPS, FGTS e outras contribuições: INSS 20%, Salário-Educação 2,5%, SAT, SESC ou SESI 1,5%, SENAI ou SENAC 1,0%, SEBRAE 0,6%, INCRA 0,2% e FGTS 8%) e 2.3 (Benefícios Mensais e Diários: transporte, auxílio-refeição/alimentação, assistência médica e familiar e outros). O seguro de vida da CCT entra em "outros" do 2.3. Pela Nota 3 do 2.2, esses percentuais incidem sobre o Módulo 1 e o Submódulo 2.1._

Este módulo divide-se em três vertentes: as provisões anuais do trabalhador (13º e férias), o que vai para o Governo (tributos sobre a folha) e o que vai direto para o trabalhador no dia a dia (benefícios).

#### Submódulo 2.1: 13º Salário, Férias e Adicional de Férias

- **13º Salário:** provisão mensal de 1/12 da remuneração = **8,33%** (Anexo VII-D, Submódulo 2.1, Nota 1; o mesmo 8,33% aparece na tabela da conta vinculada, Anexo XII, item 14).
- **Férias e Adicional de Férias (1/3 constitucional):** provisão mensal de 1/12 das férias (8,33%) mais 1/12 do terço (2,78%) = **11,11%** no 1º ano (Anexo VII-D, Submódulo 2.1, Notas 1 e 2). Pela Nota 3, a rubrica férias vira **custo não renovável** na prorrogação; a partir dela, o Esclarecimento 09 do MEC no Pregão 90011/2024 mantém só o terço (2,78%) no 2.1 e passa o substituto de férias (8,33%) para o Módulo 4. A tabela da conta vinculada (Anexo XII, item 14) usa 12,10% para "férias e 1/3"; esse percentual é o da retenção na conta, não a rubrica da planilha.
  - _Atenção:_ esta provisão e o substituto de férias do Submódulo 4.1-A **não devem ser somados quando cobrem o mesmo custo** (ver a Análise, item 4).
  - **Dois modos de provisionar as férias, ambos usados pelos órgãos:**
    - _Modo 1 — adicional no 2.1 e substituto no 4.1-A:_ o 2.1 traz só o 13º (8,33%) e o terço de férias (2,78%), e o substituto das férias entra inteiro no 4.1-A (cerca de 8,33%). Exemplo: CBM-DF, PE 90099/2025 (servente: 2.1 = 11,11%; 4.1-A = 8,33%).
    - _Modo 2 — férias completas no 2.1 e substituto residual no 4.1-A:_ o 2.1 traz o 13º (8,33%) e férias com o terço (11,11%), total de 19,44%, e o 4.1-A fica com um percentual pequeno. Exemplo: SEMED São Luís, SRP 90.099/2025 (servente: 2.1 = 19,44%; 4.1-A = 0,69%).
    - _O que conferir:_ qual modo a planilha adotou e se o outro bloco foi ajustado de acordo. O vício é usar o Modo 2 no 2.1 **e** o substituto inteiro no 4.1-A, o que cobra as férias duas vezes.

#### Submódulo 2.2: GPS, FGTS e Outras Contribuições

São as alíquotas incidentes sobre a folha de pagamento:

- **INSS Patronal:** **20,00%** (contribuição previdenciária da cota patronal). Se a empresa estiver na desoneração (CPRB), veja a transição da Lei nº 14.973/2024 no Módulo 6;
- **FGTS:** **8,00%**;
- **Salário-Educação:** **2,50%**;
- **INCRA:** **0,20%**;
- **Sistema "S" (SESI/SENAI, SESC/SENAC, SEST/SENAT):** o Anexo VII-D traz as linhas separadas — **SESC ou SESI 1,50%**, **SENAI ou SENAC 1,00%** e **SEBRAE 0,60%** (total de 3,10%). Desdobrar por entidade conforme o código FPAS da atividade. SESC+SENAC (FPAS 515, limpeza e conservação) ou SESI+SENAI (FPAS 507) somam **2,5%**; o percentual usual de **3,10%** já inclui o SEBRAE (0,6%), conforme a tabela FPAS (IN RFB 2.110/2022, Anexo III; Tabela 04 do eSocial). Conferir o código FPAS da atividade;
- **SEBRAE:** **0,60%** (não somar de novo se já estiver incluído no percentual do Sistema "S");
- **RAT/SAT ajustado pelo FAP:**
  - RAT (Risco Ambiental do Trabalho): alíquota base de **1%, 2% ou 3%** conforme o risco da atividade.
  - FAP (Fator Acidentário de Prevenção): multiplicador que varia de **0,5 a 2,0**.
  - _O RAT Final:_ Pode variar de **0,5% até 6,0%**. A planilha do órgão normalmente adota FAP neutro (1,0).

#### Submódulo 2.3: Benefícios Mensais e Diários (Custo Direto do Trabalhador)

- **Vale-Transporte (VT):**
  - Cálculo: $(Tarifa \times 2 \text{ viagens} \times Dias Trabalhados) - Desconto Legal$.
  - _O Detalhe Oculto:_ O empregador tem o direito por lei (Lei nº 7.418/85) de descontar até **6% do salário-base** do empregado. O que entra na planilha é apenas a diferença que a empresa paga do próprio bolso.
- **Vale-Alimentação / Vale-Refeição (VA/VR):**
  - Valor fixado na CCT por dia trabalhado (ex.: R$ 25,00/dia).
- **Assistência Médica e Odontológica:**
  - Valor mensal per capita, caso seja cláusula obrigatória da CCT da categoria.
- **Seguro de Vida em Grupo:**
  - Apólice obrigatória exigida na quase totalidade das CCTs de vigilância e limpeza (parâmetro prático, sem fonte: geralmente entre R$ 5,00 e R$ 15,00 por funcionário/mês).

---

### Módulo 3: Provisão para Rescisão Contratual

A Administração retém ou provisiona esses valores todo mês para garantir que, quando o contrato terminar (após 1, 2 ou 5 anos), a empresa tenha fundos para demitir a equipe sem dar calote trabalhista.

_Correspondência com o Anexo VII-D (Módulo 3, redação da IN 7/2018, conferido no Portal de Compras):_

| Alínea do modelo | Rubrica | Item desta Estrutura |
| :-- | :-- | :-- |
| A | Aviso prévio indenizado | 3.2 |
| B | Incidência do FGTS sobre o aviso prévio indenizado | 3.2 |
| C | Multa do FGTS e contribuição social sobre o aviso prévio indenizado | 3.3 |
| D | Aviso prévio trabalhado | 3.1 |
| E | Incidência de GPS, FGTS e outras contribuições (Submódulo 2.2) sobre o aviso prévio trabalhado | 3.1 |
| F | Multa do FGTS e contribuição social sobre o aviso prévio trabalhado | 3.3 |

Há planilhas que juntam as alíneas C e F numa linha só ("multa do FGTS nas rescisões sem justa causa"). Não é vício por si, mas dificulta conferir o percentual: peça a memória de cálculo.

- **3.1. Aviso Prévio Trabalhado (alíneas D e E):**
  - Percentual mensal guardado para pagar o salário do último mês em que o trabalhador cumpre o aviso.
  - _Incidência dos encargos (alínea E):_ sobre o aviso trabalhado incidem os percentuais do Submódulo 2.2; a linha deve existir.
  - _Vigência inicial acima de 12 meses:_ o 1,94% vem da fórmula [(100% / 30) × 7] / 12, isto é, 7 dias de aviso diluídos em 12 meses (Acórdão 1186/2017-Plenário). Em contrato com vigência inicial maior, manter 1,94% em todos os meses provisiona mais do que o custo; a diluição deve considerar o número de meses de execução do cabeçalho (ex.: 30 meses → cerca de 0,78% ao mês). Conferir a regra do ente e calcular o efeito antes de alegar sobrepreço.
  - _Parâmetros:_ o Acórdão 1186/2017-Plenário fixa até **1,94%** no 1º ano de contrato e até **0,194%** a cada ano de prorrogação. Na esfera federal, a Nota Técnica SEI 35883/2026/MGI (Orientação 46 do Portal de Compras, agosto de 2026), a partir do Acórdão 58/2026-Plenário, recomenda **1,94%** no 1º ano e **0,83%** a cada prorrogação em que o empregado permanecer alocado, avaliados os custos não renováveis já amortizados. Em estados e municípios, conferir se o ente segue a nota técnica, o acórdão de 2017 ou regra própria.
- **3.2. Aviso Prévio Indenizado e Aviso Prévio Proporcional (alíneas A e B):**
  - _Indenizado:_ o trabalhador é dispensado de cumprir o período e a empresa paga o valor correspondente.
  - _Proporcional (Lei nº 12.506/2011):_ para contratos que duram mais de 1 ano, o trabalhador ganha **3 dias a mais por ano de serviço** até o teto de 90 dias. A planilha precisa conter uma fração atuarial para esse acréscimo.
- **3.3. Multa Rescisória do FGTS (40%) (alíneas C e F):**
  - Cálculo da indenização compensatória de 40% sobre todos os depósitos de FGTS feitos durante a vigência contratual.
  - _Ponto crítico histórico:_ A Lei Complementar nº 110/2001 previa mais 10% (totalizando 50%). A Lei nº 13.932/2019 **extinguiu os 10% adicionais**. Se a planilha do órgão ainda cobrar 50%, há erro de cálculo a ser impugnado.
- _Nota — reflexos do aviso no 13º e nas férias:_ o período do aviso prévio (mesmo indenizado) projeta 1 mês a mais no cálculo do 13º salário e das férias proporcionais com 1/3. **Não é linha do Anexo VII-D**: quando o órgão o considera, o reflexo entra no cálculo das alíneas A e D, com memória de cálculo. (Até esta revisão, era o item "3.4" desta Estrutura.)

---

### Módulo 4: Custo de Reposição do Profissional Ausente

A Administração Pública não contrata um "indivíduo"; ela contrata um **"posto de serviço ininterrupto"** (ex.: a portaria não pode ficar vazia nenhum dia útil do ano). Quando o titular falta, tira férias ou adoece, a empresa precisa colocar um substituto. Este módulo precifica esse substituto.

_Correspondência com o modelo (Anexo VII-D da IN 5/2017, na redação da IN 7/2018, conferido no Portal de Compras): Submódulo 4.1, "Substituto nas Ausências Legais", com as mesmas alíneas A a F (substituto na cobertura de férias, ausências legais, licença-paternidade, ausência por acidente de trabalho, afastamento maternidade e outras ausências), e Submódulo 4.2, "Substituto na Intrajornada" (alínea A, intervalo para repouso ou alimentação). Pela Nota 1 do Módulo 4, os itens são o custo dos dias trabalhados pelo substituto quando o empregado alocado estiver ausente, conforme a legislação. A nota que mandava incidir o Submódulo 2.2 sobre o Módulo 4 foi revogada pela IN 7/2018._

- **4.1. Substituto nas Ausências Legais:**
  - **A. Férias:**
    - Todo trabalhador tem direito a 30 dias de férias após 12 meses.
    - O substituto trabalhará esses 30 dias e receberá salário + encargos + benefícios.
    - Fração atuarial (parâmetro prático, sem fonte normativa): aproximadamente **8,33%** a **11%** (dependendo da escala de trabalho: 44h semanais vs. escala 12x36).
    - _Atenção:_ não somar com a provisão de férias do Submódulo 2.1 quando ambas cobrem o mesmo custo. Ver os dois modos de provisionar as férias no Submódulo 2.1.
  - **B. Ausências Legais (Art. 473 da CLT):**
    - Dias remunerados em que o titular falta por direito da lei: casamento (3 dias), falecimento de parente próximo (2 dias), doação de sangue (1 dia), convocação da Justiça Eleitoral.
    - Parâmetro prático (sem fonte normativa): o percentual varia de **0,28% a 0,56%** da remuneração.
  - **C. Licença-Paternidade:**
    - Nascimento de filho (licença-paternidade de 5 a 20 dias).
  - **D. Ausência por Acidente de Trabalho:**
    - A empresa paga o salário dos primeiros **15 dias** de afastamento antes de o empregado entrar no benefício previdenciário do INSS (Lei nº 8.213/1991, art. 60, § 3º).
  - **E. Afastamento Maternidade:**
    - Cobertura do posto durante a licença-maternidade de 120 dias da titular (CLT, art. 392); o custo na planilha é o do substituto. O modelo do Anexo VII-D só nomeia a rubrica (4.1, alínea E) e não traz fórmula nem percentual: a memória de cálculo vem do órgão e deve constar da planilha do edital.
  - **F. Outras Ausências:**
    - Demais ausências previstas no modelo ou na CCT (conferir no modelo da IN 5/2017 e na CCT da categoria).
- **4.2. Substituto na Intrajornada:**
  - Cobertura do intervalo para repouso e alimentação do titular quando o posto não pode ficar vazio. O modelo do Anexo VII-D só nomeia a rubrica (4.2, alínea A) e não traz fórmula: o custo depende da escala e da duração do intervalo e deve vir com memória de cálculo na planilha do edital.

---

### Módulo 5: Insumos Diversos (Materiais, Uniformes e Equipamentos)

É onde se quantifica tudo o que é físico e perecível.

- **5.1. Uniformes e EPIs (Equipamentos de Proteção Individual):**
  - Não se joga um valor arbitrário. A fórmula usual é a **depreciação mensal por vida útil**:
    $$\text{Custo Mensal} = \frac{\text{Quantidade de Peças} \times \text{Preço Unitário de Mercado}}{\text{Vida Útil em Meses}}$$
  - _Exemplo:_ Se o trabalhador precisa de 2 pares de botas por ano (vida útil de 6 meses cada par) a R$ 120,00 o par: $\frac{1 \times 120}{6} = \text{R\$ 20,00/mês}$.
- **5.2. Materiais de Consumo:**
  - Itens que se gastam na operação: sacos de lixo, panos de chão, desinfetantes, bobinas de crachá, combustível de roçadeira.
  - Devem ser orçados por quantidade consumida estimada por posto ou por metro quadrado ($m^2$).
- **5.3. Máquinas e Equipamentos:**
  - Itens de longa duração: lavadoras de alta pressão, andaimes, computadores.
  - Podem entrar pelo **custo de locação mensal de mercado** ou pelo cálculo de **depreciação contábil do bem** $+$ **taxa mensal de manutenção preventiva**.

---

### Módulo 6: Custos Indiretos, Lucro e Tributos (O BDI do Serviço)

É a conclusão da planilha, onde as despesas corporativas e os impostos são adicionados sobre o custo da operação.

- **6.1. Custos Indiretos (Administração Central):**
  - Rateio das despesas da sede da empresa para manter aquele contrato funcionando (salário do departamento financeiro, advogados, contadores, sistemas de TI, aluguel da sede).
  - Parâmetro prático (sem fonte normativa): varia geralmente entre **1,5% e 5,0%** sobre o custo total da operação.
- **6.2. Lucro da Empresa:**
  - A remuneração líquida do empresário pelo risco da operação (parâmetro prático, sem fonte normativa: geralmente entre **4% e 10%**).
- **6.3. Tributos Incidentes sobre o Faturamento (Impostos Diretos):**
  - **ISS:** Imposto Sobre Serviços (Municipal, entre **2,00% e 5,00%** conforme o local da prestação);
  - **PIS:** Alíquota federal (**0,65%** no lucro presumido/cumulativo ou **1,65%** no lucro real/não cumulativo);
  - **COFINS:** Alíquota federal (**3,00%** no lucro presumido ou **7,60%** no lucro real);
  - _Nota sobre o regime não cumulativo:_ 1,65% e 7,60% são alíquotas nominais. Como o regime não cumulativo gera créditos, na planilha usa-se a **alíquota efetiva** de PIS/Cofins (média recolhida após os créditos), e não a nominal. A IN 5/2017 não trata do tema (o Módulo 6 do Anexo VII-D só manda aplicar o percentual dos tributos sobre o faturamento); o fundamento é o Acórdão 2.622/2013-Plenário do TCU, item 9.3.2.4, que manda exigir nos editais, das empresas no regime não cumulativo, demonstrativo de que os percentuais de PIS e Cofins adotados correspondem à média dos percentuais efetivos recolhidos (o acórdão trata do BDI de obras).
  - _CPRB (Desoneração da Folha - Lei nº 12.546/2011) — situação em outubro de 2026:_ A desoneração está em transição pela **Lei nº 14.973/2024** (texto conferido no Planalto):
    - **2025:** CPRB a 80% da alíquota + 5% de INSS sobre a folha;
    - **2026:** CPRB a 60% da alíquota + 10% de INSS sobre a folha;
    - **2027:** CPRB a 40% da alíquota + 15% de INSS sobre a folha;
    - **2028:** fim da CPRB; INSS Patronal integral de 20% sobre a folha.
    - Portanto, o INSS Patronal do Submódulo 2.2 **não desaparece**: em 2026 a planilha deve trazer a CPRB reduzida aqui no Módulo 6 (alíquota base de **1,0% a 4,5% sobre a receita bruta**) e a parcela de 10% sobre a folha no Módulo 2.
  - _Transição da Reforma Tributária (LC nº 214/2025) — situação em outubro de 2026:_ 2026 é ano-teste, com **CBS de 0,9%** e **IBS de 0,1%**, compensáveis com PIS/Cofins ou dispensados para quem cumpre as obrigações acessórias (art. 348, §1º). Em 2027 a CBS substitui o PIS e a Cofins: o art. 542 da LC 214/2025 revoga, a partir de 1º/01/2027, os dispositivos que instituem as duas contribuições (entre eles, LC 7/1970, LC 70/1991, Lei 9.718/1998, Lei 10.637/2002 e Lei 10.833/2003), e em 2027 e 2028 a CBS é cobrada pela alíquota de referência reduzida em 0,1 ponto percentual (art. 347).
- **O Segredo do Cálculo Matemático ("Preço por Dentro / Gross-Up"):**
  - Os impostos incidem sobre a própria Nota Fiscal emitida. Por isso, a fórmula matemática não é simplesmente somar a porcentagem, mas aplicar a fórmula de divisão:
    $$\text{Preço Final} = \frac{\text{Custo Total} + \text{Custos Indiretos} + \text{Lucro}}{1 - (\text{ISS} + \text{PIS} + \text{COFINS})}$$
- **IRPJ e CSLL no orçamento-base (Súmula nº 254 do TCU):**
  - Pela Súmula 254, o **IRPJ** (Imposto de Renda da Pessoa Jurídica) e a **CSLL** (Contribuição Social sobre o Lucro Líquido) não são despesas indiretas passíveis de inclusão no BDI do orçamento-base, por serem tributos diretos e personalísticos (paráfrase do enunciado oficial, conferido).
  - A súmula trata do **orçamento-base** do órgão: não fala em nulidade nem proíbe o licitante de cobrir esses tributos com o seu lucro. Se o órgão incluir IRPJ e CSLL no BDI da planilha de referência, o pedido cabível é a retificação.

---

### Quadros Finais e Complementos (depois do Módulo 6)

É aqui que a planilha vira o **valor estimado do edital**. Sem esses quadros não dá para conferir o teto.

- **2. Quadro-resumo do custo por empregado:** Módulos 1 a 5 (subtotal) + Módulo 6 = valor total por empregado.
- **3. Quadro-resumo do valor mensal dos serviços:** para cada tipo de serviço, valor por empregado × empregados por posto = valor por posto; × número de postos = valor total do serviço.
- **4. Quadro demonstrativo do valor global:** valor por unidade de medida, valor mensal e valor global (mensal × meses do contrato).
- **5. Complemento dos serviços de vigilância:** preço mensal por tipo de posto (44 h diurno; 12x36 diurno e noturno, com 2 vigilantes), número de postos e subtotal.
- **6. Complemento dos serviços de limpeza:** preço mensal por m² por tipo de área (interna, externa, esquadria, fachada envidraçada, área hospitalar), a partir da produtividade de referência do Anexo VI-B e do preço do homem-mês do servente e do encarregado.
- **O que conferir:** se o valor mensal e o global dos quadros batem com o edital, o TR, o ETP e o PNCP; se os postos e as áreas coincidem com os quantitativos do TR; e se a produtividade usada é a de referência ou foi justificada.

---

### Resumo dos 6 Módulos em um Fluxograma Lógico

```
[CABEÇALHO] CCT (ano e registro), data-base, meses de execução, CBO, salário normativo
    │
    ▼
[MÓDULO 1] Remuneração Direta (Salário CCT + Periculosidade + Insalubridade + Noturno)
    │
    ▼ (Gera a base de cálculo para)
[MÓDULO 2] 13º/Férias + Encargos de Folha (INSS, FGTS, RAT/FAP) + Benefícios (VT, VR, Saúde)
    │
    ▼ (Acrescenta-se o risco de saída)
[MÓDULO 3] Provisão para Demissão (Aviso Prévio + Multa 40% FGTS)
    │
    ▼ (Acrescenta-se a reposição de ausências)
[MÓDULO 4] Cobertura de Faltas e Férias (Substituto do Titular)
    │
    ▼ (Soma-se os insumos de trabalho)
[MÓDULO 5] Uniformes + EPIs + Materiais de Limpeza + Depreciação de Máquinas
    │
    ▼ (TOTAL DO CUSTO DIRETO OPERACIONAL)
    │
[MÓDULO 6] Aplica-se: Administração Central (%) + Lucro (%) + Impostos "por dentro" (ISS + PIS + COFINS)
    │
    ▼
=========================================
 PREÇO FINAL UNITÁRIO DO POSTO / SERVIÇO
=========================================
    │
    ▼
[QUADROS FINAIS] Custo por empregado → valor mensal (empregados por posto × postos) → valor global (× meses)
                 + complemento de vigilância (por posto) ou de limpeza (por m²)
```
