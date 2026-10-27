# 03 - Plano de Fechamento do Estudo

## 1. Objetivo

Fechar o estudo de `briefing/Mapeamento_Analise/` depois do mapeamento de fontes (plano `02`). Ficaram três frentes:

1. **Marcas "a conferir" nos arquivos de estudo:** 31 marcas em 7 arquivos `Estrutura`/`Analise`, muitas sobre fontes que o catálogo já conferiu.
2. **Redação fora da auditoria:** três trechos que o README de `Contexto_Sessao/` registrou como pendentes.
3. **Push:** a `main` está à frente do remoto; sem push, o outro computador não recebe as correções.

Levantamento feito em 2026-10-15, com o catálogo (`01 - Catalogo de Fontes.md`) como referência de status.

## 2. Regras

- O catálogo é a fonte de verdade do status. Marca sobre fonte `conferido` no catálogo sai do texto; se o texto afirmar algo diferente do Nome no catálogo, o texto é corrigido, não só desmarcado.
- Conferência nova só na fonte oficial (Planalto, Pesquisa de Jurisprudência do TCU, Portal de Compras). A fonte conferida entra ou é atualizada no catálogo no mesmo commit.
- O que depende do edital (regulamento do ente, CCT, tabela FPAS da atividade) não é pendência do estudo: a marca vira "conferir no regulamento do ente" ou "conferir na CCT", sem "a conferir" solto.
- Os mapas `Fontes - *.md` só mudam se a correção mudar o que eles afirmam; nesse caso, manter a simetria e o "Usado em" do catálogo.
- Sem dados pessoais; grafia "Servfaz".

## 3. Frente 1 — marcas "a conferir"

### 3.1 Grupo A: fonte já conferida no catálogo (retirar a marca e alinhar o texto)

| Arquivo | Linha | Trecho | Fonte no catálogo |
| :-- | :-- | :-- | :-- |
| Estrutura - Edital | 47 | Exceções da LC 123 e limites do art. 4º | `EXT-LC123-ART48`, `ART49`, `EXT-LEI14133-ART4` |
| Analise - Edital | 18 | Idem | Idem |
| Analise - Edital | 19 | Recuperação judicial, Acórdão 1.201/2020 | `EXT-TCU-AC1201-2020` |
| Analise - Edital | 67 | Súmula 275 | `EXT-TCU-SUM275` |
| Analise - Edital | 68 | Somatório de atestados, Acórdão 1.101/2020 | `EXT-TCU-AC1101-2020` |
| Analise - Edital | 85 | Lei 9.784, prazos contínuos (art. 66) | `EXT-LEI9784-ART66` (§ 2º) |
| Estrutura - Pesquisa de Precos | 21 | IN 65, art. 5º, § 1º | `EXT-IN65-ART5` |
| Estrutura - Pesquisa de Precos | 63 | IN 65, art. 6º (métodos e descarte) | `EXT-IN65-ART6` |
| Analise - Termo de Referencia | 98 | Art. 6º, XXIII, "i" | `EXT-LEI14133-ART6` |
| Analise - Termo de Referencia | 114 | Súmula 263 | `EXT-TCU-SUM263` |
| Estrutura - Termo de Refencia | 16 (2 marcas), 90, 110, 122 | Alíneas "a" a "j" do art. 6º, XXIII e correspondência das seções | `EXT-LEI14133-ART6` (conferir no Planalto a correspondência de cada seção, ver 3.2) |
| Estrutura - Termo de Refencia | 26 | Vigência de até 5 anos e prorrogação até 10 | `EXT-LEI14133-ART106`, `ART107` |
| Estrutura - Termo de Refencia | 82 | IN 77/2022 (prazo de pagamento federal) | `EXT-IN77-2022` (10 + 10 dias úteis) |
| Estrutura - Planilha de Custos | 30 | Súmula 60 do TST | `EXT-TST-SUM60` |
| Estrutura - Planilha de Custos | 160 | CBS substitui PIS/Cofins em 2027 | `EXT-LC214-ART348` (conferir no Planalto o artigo da extinção do PIS/Cofins; ver 3.2) |

### 3.2 Grupo B: conferência nova na fonte oficial

| Arquivo | Linha | O que conferir | Onde |
| :-- | :-- | :-- | :-- |
| Estrutura - Termo de Refencia | 16, 90, 110, 122 | Correspondência de cada seção do TR com as alíneas "a" a "j" do art. 6º, XXIII; se a seção VII (obrigações) de fato não é alínea | Planalto (Lei 14.133) |
| Estrutura - Planilha de Custos | 38, 99 | Correspondência dos Módulos 2 e 4 com o Anexo VII-D da IN 5/2017 (IN 7/2018) | Portal de Compras |
| Estrutura - Planilha de Custos | 44, 45 | 13º (8,33%) e férias + 1/3 no Submódulo 2.1 (o catálogo registra 11,11% no 1º ano, `EXT-ADM-MEC-2024`) | Anexo VII-D da IN 5/2017; `EXT-ADM-MEC-2024` |
| Estrutura - Planilha de Custos | 115, 119 | Fórmula do substituto na licença-maternidade (4.1-E) e na intrajornada (4.2) | Anexo VII-D da IN 5/2017 |
| Estrutura - Planilha de Custos | 153 | Alíquota efetiva de PIS/Cofins no regime não cumulativo | IN 5/2017 (Anexo VII-D, notas do Módulo 6) e jurisprudência do TCU |
| Estrutura - Planilha de Custos | 160 | Artigo da LC 214/2025 que extingue PIS/Cofins em 2027 | Planalto (LC 214/2025) |
| Estrutura - Minuta Contratual | 141 | Indenização na extinção por interesse público (art. 137, VIII, e art. 138, § 2º ou outro) | Planalto (Lei 14.133) |

Se a fonte não confirmar o que o texto diz, corrigir o texto. Se não for possível abrir a fonte, manter a marca e registrar o motivo na seção 9.2 do catálogo.

### 3.3 Grupo C: depende do ente ou da categoria (trocar a marca por orientação)

| Arquivo | Linha | Troca |
| :-- | :-- | :-- |
| Estrutura - Minuta Contratual | 34 | Prazos de recebimento: "conferir no regulamento do ente; na União, IN 77/2022" |
| Estrutura - Minuta Contratual | 36 | Prazo de pagamento: "na União, até 10 + 10 dias úteis (IN 77/2022); nos demais entes, conferir o regulamento" |
| Estrutura - Planilha de Custos | 56 | Sistema S: "conferir as alíquotas pelo código FPAS da atividade (`EXT-BASE-FPAS`)"; se a tabela confirmar que 3,1% já inclui o SEBRAE, dizer isso sem marca |
| Estrutura - Planilha de Custos | 117 | Demais ausências: "conferir no modelo da IN 5/2017 e na CCT da categoria" |

### 3.4 Verificação da frente 1

- `grep -rn "a conferir"` nos `Estrutura`/`Analise` só pode achar marcas do Grupo B que não puderam ser conferidas, cada uma registrada na seção 9.2 do catálogo.
- Toda fonte nova ou atualizada tem status e "Usado em" no catálogo.

## 4. Frente 2 — redação fora da auditoria

| Arquivo | Linha | Trecho | Ajuste |
| :-- | :-- | :-- | :-- |
| Analise - Minuta Contratual | 22 | "jurisprudência pacífica do TCU", sem acórdão | Citar o acórdão que sustenta a tese, se o catálogo tiver (ex.: `EXT-TCU-AC7184-2018` sobre o critério de reajuste), ou retirar a expressão |
| Analise - Estudo tecnico Preliminar | 103 | "ou anular a fase preparatória" | Alinhar à tese de saneamento: nulidade só pelo regime dos arts. 147 a 150, com ponderação do interesse público |
| Analise - Minuta Contratual | 126 | "tese perfeita de impugnação" | Fecho neutro (ex.: "há base para impugnação da cláusula") |
| Analise - RERI | 127 | "um passo à frente do pregoeiro e dos concorrentes" | Fecho neutro sobre o registro de controle |

Verificação: `grep` pelas quatro expressões não acha nada.

## 5. Frente 3 — push

1. Depois das frentes 1 e 2, conferir `git status` (só arquivos do `briefing/` no commit) e `git log origin/main..main`.
2. Atualizar `briefing/Contexto_Sessao/README.md`: estudo fechado e o que segue (levar a estrutura para a skill).
3. Fazer `git push origin main`, com confirmação da usuária.

## 6. Ordem e commits

| Etapa | Entrega | Commit |
| :-- | :-- | :-- |
| 1 | Frente 1, Grupos A e C (só texto, sem conferência nova) | um commit |
| 2 | Frente 1, Grupo B (conferência nova; catálogo atualizado) | um commit |
| 3 | Frente 2 | um commit (pode ir junto da etapa 1) |
| 4 | README e push | um commit + push |

## 7. Andamento

| Etapa | Status | Commit |
| :-- | :-- | :-- |
| 1. Grupos A e C | concluída (marcas do TR sobre o art. 6º, XXIII, e da CBS 2027 ficam para a etapa 2) | este commit |
| 2. Grupo B | concluída (todas as fontes abriram: Planalto, Portal de Compras e Pesquisa do TCU; nenhuma marca ficou na seção 9.2 do catálogo; prazo de recebimento da Minuta passou a citar o art. 140, § 3º) | este commit |
| 3. Redação | concluída (Acórdão 7.184/2018-Segunda Câmara citado na Análise da Minuta) | junto da etapa 1 |
| 4. README e push | README concluído (este commit); push aguardando confirmação da usuária | — |
