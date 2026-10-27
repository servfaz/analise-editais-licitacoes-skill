# 00 - Objetivos e Organização do Diretório

## 1. Objetivo

Este diretório organiza o estudo feito para mapear e correlacionar as seções do edital e de seus anexos, a fim de identificar possíveis impugnações em licitações regidas pela Lei nº 14.133/2021.

O conteúdo se divide em duas camadas:

- **Edital:** detalhamento de cada seção e mapeamento das relações entre as partes do edital e os anexos.
- **Anexos:** para cada anexo, as partes que o compõem, o detalhamento de suas seções e os pontos que podem gerar impugnação.

Em ambas as camadas, o material também relaciona os pontos encontrados para verificar se são impugnáveis e se a impugnação é sustentável. Os mapas de fontes (`Fontes - {Documento}.md`) e o catálogo único (`01 - Catalogo de Fontes.md`) dizem onde buscar a prova e o fundamento de cada ponto.

## 2. Estrutura do diretório

Cada documento do processo licitatório tem uma pasta própria. Dentro de cada pasta há três arquivos:

| Arquivo | Conteúdo |
| :-- | :-- |
| `Estrutura - {Documento}.md` | As partes do documento, a finalidade de cada seção e a base legal correspondente. |
| `Analise - {Documento}.md` | Os pontos do documento que podem gerar impugnação e os cruzamentos com outros documentos e fontes. |
| `Fontes - {Documento}.md` | O mapa de fontes: para cada seção da `Estrutura`, as fontes internas (outros documentos do processo, com a seção a abrir) e as externas (IDs do catálogo), a prova a extrair e o critério que gera ou descarta a impugnação; fecha com uma matriz resumo dos cruzamentos. |

```
Mapeamento_Analise/
├── 00 - Objetivos_Organizacao.md
├── 01 - Catalogo de Fontes.md
├── 02 - Plano do Mapeamento de Fontes.md
├── Minhas observacoes.md
├── Edital/
│   ├── Estrutura - Edital.md
│   ├── Analise - Edital.md
│   └── Fontes - Edital.md
├── Termo de Referência/
│   ├── Estrutura - Termo de Refencia.md
│   ├── Analise - Termo de Referencia.md
│   └── Fontes - Termo de Referencia.md
├── Estudo Técnico Preliminar/
│   ├── Estrutura - ETP.md
│   ├── Analise - Estudo tecnico Preliminar.md
│   └── Fontes - ETP.md
├── Planilha de Custos/
│   ├── Estrutura - Planilha de Custos.md
│   ├── Analise - Planilha de Custos.md
│   └── Fontes - Planilha de Custos.md
├── Pesquisa(Mapa) de Preços/
│   ├── Estrutura - Pesquisa de Precos.md
│   ├── Analise - Pesquisa de Precos.md
│   └── Fontes - Pesquisa de Precos.md
├── Minuta Contratual/
│   ├── Estrutura - Minuta Contratual.md
│   ├── Analise - Minuta Contratual.md
│   └── Fontes - Minuta Contratual.md
└── Retificações, Esclarecimentos e Respostas/
    ├── Estrutura - RERI.md
    ├── Analise - RERI.md
    └── Fontes - RERI.md
```
## 3. Mapa das pastas

| Pasta | Documento | O que os arquivos descrevem |
| :-- | :-- | :-- |
| `Edital/` | Edital (instrumento convocatório) | **Estrutura:** as 13 seções do edital, do preâmbulo ao rol de anexos. **Análise:** o mapa de cruzamentos entre as seções do edital (condições de participação, sessão pública e disputa, julgamento, habilitação, recursos e impugnações) e os anexos. **Fontes:** as 13 seções, com as seções 1–5 da Análise como base e as demais derivadas da Estrutura. |
| `Termo de Referência/` | Termo de Referência (TR) / Projeto Básico | **Estrutura:** objetivo do TR e finalidade de cada seção. **Análise:** pontos impugnáveis por seção (objeto, requisitos técnicos, execução, gestão e fiscalização, medição e pagamento, obrigações, habilitação). **Fontes:** as 10 seções do TR. |
| `Estudo Técnico Preliminar/` | ETP (art. 18, § 1º) | **Estrutura:** conteúdo formal do ETP. **Análise:** pontos impugnáveis em levantamento de mercado, quantidades, parcelamento, valor estimado e matriz de riscos. **Fontes:** os 13 incisos do art. 18, § 1º (obrigatórios marcados), e o checklist de existência e publicidade. |
| `Planilha de Custos/` | Planilha de custos e formação de preços | **Estrutura:** os 6 módulos da planilha. **Análise:** erros e omissões por módulo, incluindo remuneração, encargos, rescisão, insumos e tributos. **Fontes:** os 6 módulos e a planilha como um todo. |
| `Pesquisa(Mapa) de Preços/` | Pesquisa de preços (art. 23) | **Estrutura:** estrutura formal da pesquisa. **Análise:** vícios típicos do mapa de cotações. **Fontes:** os 5 parâmetros do art. 23, § 1º, a validade, o tratamento dos dados e os 5 vícios da Análise. |
| `Minuta Contratual/` | Minuta de contrato / ata de registro de preços | **Estrutura:** as 9 cláusulas principais e seus artigos. **Análise:** pontos impugnáveis em reajuste, pagamento, garantia, multas, retenções, riscos e rescisão. **Fontes:** as 9 cláusulas. |
| `Retificações, Esclarecimentos e Respostas/` | Atos publicados após o edital (RERI) | **Estrutura:** natureza jurídica dos três tipos de ato. **Análise:** o ciclo de triagem aplicado a cada nova publicação. **Fontes:** os três atos, os 5 checkpoints e o modelo de tabela de controle. |

**RERI como processo à parte.** Os atos da RERI só existem dias depois do lançamento do edital. Por isso, a pasta `Retificações, Esclarecimentos e Respostas/` é a base de um processo à parte e não entra na skill de triagem (`skills/impugnacoes-triagem/`). A cópia do estudo usada pela skill deixa de fora essa pasta, as linhas dos mapas cujo assunto é um ato da RERI e as menções a `INT-RERI`; o que sai de cada mapa fica registrado no `MANIFEST.json` da cópia. Os arquivos desta pasta e as menções a `INT-RERI` nos outros mapas continuam valendo para o processo da RERI.

## 4. Arquivos na raiz

| Arquivo | Conteúdo |
| :-- | :-- |
| `00 - Objetivos_Organizacao.md` | Este arquivo: objetivo, estrutura e mapa do diretório. |
| `01 - Catalogo de Fontes.md` | Catálogo único das fontes internas (`INT-*`) e externas (`EXT-*`): nome, tipo, esfera, onde consultar, arquivos que a usam e status (`conferido` ou `a conferir`). Os mapas citam as fontes externas só pelo ID; quando a lei ou a jurisprudência mudar, atualize o catálogo. |
| `02 - Plano do Mapeamento de Fontes.md` | Plano do mapeamento de fontes em 6 fases, com os formatos, o andamento e as pendências resolvidas na consolidação. |
| `Minhas observacoes.md` | Anotações pessoais do autor, mantidas à parte e não fazem parte do mapeamento. |

## 5. Ordem de leitura sugerida

1. `Edital/Estrutura - Edital.md` e `Edital/Analise - Edital.md`, que são o ponto de partida e indicam quais anexos se relacionam com cada seção.
2. Para cada anexo, o par `Estrutura` e depois `Analise`: a estrutura define as seções citadas na análise.
3. `Retificações, Esclarecimentos e Respostas/`, por tratar de documentos publicados depois do edital.
4. Na análise de um edital concreto, o `Fontes - {Documento}.md` da pasta, com o `01 - Catalogo de Fontes.md` aberto ao lado para o texto e o status de cada ID. Comece pelo mapa do Edital; a matriz resumo de cada mapa indica que seção dos outros documentos abrir, e o mapa de destino traz a volta.
5. `02 - Plano do Mapeamento de Fontes.md` só para entender como os mapas foram feitos ou para estendê-los.
