# Capacidades externas (contrato agnóstico de ferramenta)

A skill descreve **o que** precisa, nunca o nome de uma ferramenta específica. Em cada ambiente (Claude, Open WebUI ou outro), use a ferramenta disponível que cumpra a capacidade. Se nenhuma cumprir, siga o comportamento sem ferramenta, sem fingir que a consulta foi feita.

| Capacidade | Para que serve | Fases | Sem ferramenta disponível |
| --- | --- | --- | --- |
| **Consulta de CCT** | Buscar a CCT vigente por sindicato, categoria, UF ou nº de registro MTE: pisos, adicionais, benefícios, vigência, data-base | 2, 4 | Usar a CCT enviada pelo analista ou citada no edital e marcar "dados de CCT a validar na fonte oficial" |
| **Leitura de documentos** | Extrair texto e tabelas de PDF, DOCX e XLSX enviados, preservando página, aba e célula | Todas | Pedir o texto ou o arquivo em formato legível; não concluir sobre o que não foi lido |
| **Busca no conjunto documental** | Localizar trechos em editais longos já indexados | 1, 2, 3 | Ler o documento integralmente |
| **Texto da Lei 14.133** | Achar os dispositivos da Lei 14.133/2021 por assunto e trazer o texto vigente do artigo, parágrafo, inciso ou alínea | 2, 3, 4, 5 | Citar sem aspas, marcar `a conferir` e sinalizar validação jurídica humana; não transcrever de memória |
| **Legislação oficial** | Conferir as demais normas (LC 123, CLT, decretos, instruções normativas, normas do ente) no texto oficial (Planalto, Portal de Compras, diário do ente) | 2, 3, 4, 5 | Manter a fonte como `a conferir` e sinalizar validação jurídica humana |
| **Jurisprudência do TCU** | Buscar jurisprudência selecionada, súmulas e acórdãos do TCU e abrir o inteiro teor do acórdão | 2, 3, 4, 5 | Plano B (busca na web com níveis de confiança, seção abaixo); sem busca na web, manter o precedente `a conferir` e sinalizar validação jurídica humana; nunca citar acórdão de memória |
| **Exportação da minuta de impugnação em .docx** | Gerar o Word timbrado da Servfaz a partir do bloco `minuta-servfaz` aprovado | 3 | Entregar o Markdown delimitado para o analista formatar |

## Como usar a consulta de CCT

1. Monte a consulta com os dados literais do edital: nome do sindicato, nº de registro MTE (ex.: `DF000042/2025`), categoria/cargo e UF.
2. Confira na resposta: nº de registro, vigência e data-base. CCT vencida ou de outra categoria não serve como parâmetro; registre a divergência.
3. Cite a fonte como `(CCT nº <registro>, cláusula X)`, indicando que veio da base de CCTs.
4. Resultado da base é candidato, não prova: se houver aditivo mais recente citado no edital e ausente na base, aponte a diferença.

## Como usar o texto da Lei 14.133

Toda citação ou transcrição da Lei 14.133/2021 passa por aqui.

1. Ache o número do dispositivo no estudo: mapa de fontes do documento (`references/estudo/<documento>/fontes.md`) ou catálogo (`EXT-LEI14133-ARTn`). Só se o ponto não estiver lá, use a busca por assunto na lei, com as palavras do vício (ex.: `conta vinculada`, `retenção pagamento obrigações trabalhistas`); frases exatas entre aspas. Número lembrado de memória é só palpite: confirme pela busca.
2. Abra o artigo pela consulta ao texto da lei antes de citar. Sem parágrafo, a consulta devolve o artigo inteiro; leia todos os parágrafos e incisos, não só o que pretende citar.
3. Transcreva só o trecho devolvido pela consulta, com a citação que ela traz (ex.: `Lei 14.133/2021, art. 121, § 3º, inciso II`). Registre: "conferido nesta execução (texto do normas.leg.br, registro de dd/mm/aaaa)".
4. Use as notas da consulta: "redação dada por", "veto derrubado", "decisão judicial", "aplicação afastada em hipótese específica". Uma nota de decisão judicial ou de aplicação afastada exige dizer isso ao analista antes de usar o dispositivo como fundamento.
5. No contraponto, procure no mesmo artigo o dispositivo que favorece a Administração (ex.: o inciso que autoriza outra forma da medida contestada) e enfrente-o.
6. Falha técnica, lei fora da consulta ou dispositivo não encontrado: cite sem aspas e marque `a conferir`. A busca é por palavras: "nenhum resultado" não prova que a lei não trata do assunto.
7. O texto vem do registro do Congresso Nacional, sem valor oficial (o oficial é o do DOU). Na pendência final, peça ao analista que confira no Planalto os dispositivos transcritos antes de protocolar.

## Como usar a pesquisa de jurisprudência do TCU

Só quando a tese depender de precedente; lei clara basta por si.

1. Formule o vício em uma frase e identifique o dispositivo da Lei 14.133/2021 envolvido.
2. Comece pela jurisprudência selecionada e pelas súmulas, com frases curtas entre aspas (ex.: `"retenção de pagamento" "regularidade fiscal"`). Palavras soltas trazem resultado ruidoso. Só depois busque acórdãos, filtrando a partir de 2021 quando a tese for sobre a Lei 14.133.
3. Antes de citar, abra o inteiro teor do acórdão de origem e confira: número, ano, colegiado, item da deliberação que sustenta a tese, lei aplicada (8.666/1993 ou 14.133/2021), data e se há entendimento posterior em sentido contrário. Enunciado, sumário e trecho de busca são resumos, não o inteiro teor.
4. Cite como `Acórdão N/AAAA-Colegiado, item X` e registre na matriz ou pendência: "conferido na Pesquisa do TCU nesta execução". Súmula: número e vigência.
5. Resultado de busca é candidato. Falha técnica não prova que não há jurisprudência. Se a pesquisa falhar ou não trouxer resultado pertinente, siga o plano B abaixo para o analista não ficar sem resposta.
6. Na consulta, envie só termos jurídicos: nunca nome do órgão, do cliente, da Servfaz ou dados do edital.
7. Consulte com moderação: poucas buscas por ponto, sem varreduras.

## Plano B: busca na web quando a pesquisa do TCU falhar

Use só depois de a pesquisa do TCU falhar (erro técnico) ou não trazer resultado pertinente, e diga ao analista que está no plano B.

1. Busque primeiro nas fontes oficiais, restringindo o domínio: `site:tcu.gov.br`, `site:lexml.gov.br` (ex.: `site:lexml.gov.br acórdão 964/2012 TCU`). Só depois, se preciso, faça a busca aberta, apenas para achar o número do precedente.
2. Abra a página de cada resultado que for usar (no Open WebUI, `fetch_url`). O trecho do resultado de busca não é fonte aberta: sem abrir, vale no máximo C. Classifique cada fonte pelo nível de confiança da tabela abaixo, pelo domínio da página aberta, não pelo título do resultado. Atribua uma tese a um acórdão só se o texto aberto a ligar a ele.
3. Confirme número, ano, colegiado e data em fonte de nível A ou B antes de usar o precedente. Divergência entre fontes (ex.: colegiado diferente) é sinal de erro: prevalece a fonte de nível mais alto.
4. Apresente ao analista cada precedente com a confiança em palavras e o motivo em linguagem simples, sem as letras dos níveis: `Acórdão N/AAAA-Colegiado (confiança média: ementa oficial no LexML; texto integral do acórdão a conferir)`.
5. Na consulta, valem as mesmas regras da pesquisa do TCU: só termos jurídicos, poucas buscas.

### Níveis de confiança das fontes

As letras A a D são só para classificação interna: não aparecem na resposta ao analista nem na minuta. Na resposta, use apenas a confiança (alta, média, baixa) e o motivo.

| Nível | Confiança | Fontes | O que pode ser feito |
| --- | --- | --- | --- |
| **A** | Alta | O próprio acórdão ou súmula, no TCU: `pesquisa.apps.tcu.gov.br`, `contas.tcu.gov.br` (PDF/RTF do acórdão), `sites.tcu.gov.br` (dados abertos) | Citar e transcrever o que foi aberto: `conferido nesta execução` |
| **B** | Média | Oficial, mas derivada: `lexml.gov.br` (ementa oficial com número, ano, colegiado e data), `licitacoesecontratos.tcu.gov.br` (manual do TCU), outras páginas do `tcu.gov.br` que citam o acórdão (boletins, atas, publicações), outros órgãos públicos que reproduzem o precedente (`.gov.br`, `.jus.br`, `.leg.br`, tribunais de contas estaduais) | Confirmar a existência e citar número e ementa transcrita da página aberta, identificada como ementa; o conteúdo da deliberação fica `a conferir` |
| **C** | Baixa | Repositórios e editoras jurídicas: `jusbrasil.com.br`, `zenite.blog.br`, `sollicita.com.br`, `jmlgrupo.com.br`, `conlicitacao.com.br` e similares | Só pista para achar o número; confirmar em A ou B; nunca transcrever nem citar como fonte |
| **D** | Sem garantia | Blogs de escritórios e consultorias, sites gerados por IA, aplicativos, `scribd`, redes sociais, vídeos | Não usar como fonte; no máximo pista de busca. Já houve erro de colegiado em site desse tipo |

Domínio fora da lista: classifique pelo tipo (órgão público oficial = B; editora ou repositório jurídico = C; demais = D). Na dúvida, use o nível mais baixo.

## Referência por ambiente

| Ambiente | Consulta de CCT | Exportação .docx (impugnação) | Pesquisa jurídica |
| --- | --- | --- | --- |
| Claude (claude.ai / Claude Code) | Conector MCP do RAG de CCTs da Servfaz | Skill de documentos Word, quando disponível | Busca web, quando habilitada |
| Open WebUI | Servidor MCP `servfaz-rag` | Action **Exportar Minuta de Impugnacao Servfaz** | Tool **Fontes oficiais Servfaz**: jurisprudência do TCU (`buscar_jurisprudencia_selecionada`, `buscar_sumulas_tcu`, `buscar_acordaos_tcu`, `obter_acordao_tcu`) e texto da Lei 14.133 (`buscar_na_lei`, `obter_dispositivo_lei`); Web Search para as demais normas e para o plano B da jurisprudência |

A exportação nunca altera o texto aprovado e só ocorre por decisão do analista. Recurso ainda não tem exportação própria: entregue Markdown e não use o conversor de impugnação.

Esta tabela é informativa. A skill não depende dela: o modelo escolhe a ferramenta pela capacidade descrita acima.
