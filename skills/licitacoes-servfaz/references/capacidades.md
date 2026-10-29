# Capacidades externas (contrato agnóstico de ferramenta)

A skill descreve **o que** precisa, nunca o nome de uma ferramenta específica. Em cada ambiente (Claude, Open WebUI ou outro), use a ferramenta disponível que cumpra a capacidade. Se nenhuma cumprir, siga o comportamento sem ferramenta, sem fingir que a consulta foi feita.

| Capacidade | Para que serve | Fases | Sem ferramenta disponível |
| --- | --- | --- | --- |
| **Consulta de CCT** | Buscar a CCT vigente por sindicato, categoria, UF ou nº de registro MTE: pisos, adicionais, benefícios, vigência, data-base | 2, 4 | Usar a CCT enviada pelo analista ou citada no edital e marcar "dados de CCT a validar na fonte oficial" |
| **Leitura de documentos** | Extrair texto e tabelas de PDF, DOCX e XLSX enviados, preservando página, aba e célula | Todas | Pedir o texto ou o arquivo em formato legível; não concluir sobre o que não foi lido |
| **Busca no conjunto documental** | Localizar trechos em editais longos já indexados | 1, 2, 3 | Ler o documento integralmente |
| **Pesquisa jurídica oficial** | Conferir lei no Planalto e jurisprudência no portal do TCU | 3, 4, 5 | Manter a fonte como `a conferir` e sinalizar validação jurídica humana |
| **Exportação da minuta de impugnação em .docx** | Gerar o Word timbrado da Servfaz a partir do bloco `minuta-servfaz` aprovado | 3 | Entregar o Markdown delimitado para o analista formatar |

## Como usar a consulta de CCT

1. Monte a consulta com os dados literais do edital: nome do sindicato, nº de registro MTE (ex.: `DF000042/2025`), categoria/cargo e UF.
2. Confira na resposta: nº de registro, vigência e data-base. CCT vencida ou de outra categoria não serve como parâmetro; registre a divergência.
3. Cite a fonte como `(CCT nº <registro>, cláusula X)`, indicando que veio da base de CCTs.
4. Resultado da base é candidato, não prova: se houver aditivo mais recente citado no edital e ausente na base, aponte a diferença.

## Referência por ambiente

| Ambiente | Consulta de CCT | Exportação .docx (impugnação) | Pesquisa jurídica |
| --- | --- | --- | --- |
| Claude (claude.ai / Claude Code) | Conector MCP do RAG de CCTs da Servfaz | Skill de documentos Word, quando disponível | Busca web, quando habilitada |
| Open WebUI | Servidor MCP `servfaz-rag` | Action **Exportar Minuta de Impugnacao Servfaz** | Web Search; MCP do TCU quando implantado |

A exportação nunca altera o texto aprovado e só ocorre por decisão do analista. Recurso ainda não tem exportação própria: entregue Markdown e não use o conversor de impugnação.

Esta tabela é informativa. A skill não depende dela: o modelo escolhe a ferramenta pela capacidade descrita acima.
