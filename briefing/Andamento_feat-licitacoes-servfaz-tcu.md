# Branch `feat/licitacoes-servfaz-tcu`: o que foi feito e o que falta

Atualizado em 05/11/2026. Branch criado a partir do `main` em 30/10/2026; 16 commits, publicado no `origin` até `9b130c2`.

## Objetivo

Fazer a skill `licitacoes-servfaz` fundamentar impugnações, esclarecimentos e recursos só com fontes abertas na conversa (texto da Lei 14.133 e jurisprudência do TCU), em vez de citar de memória, e versionar o preset "Licitações Servfaz" do Open WebUI que usa a skill.

## Dependências fora deste branch

| O quê | Onde | Estado |
| --- | --- | --- |
| Tool "Fontes oficiais Servfaz" (TCU e Lei 14.133), v0.2.4 | `tools/comercial`, `skills/openwebui-tcu-jurisprudencia/` | Instalada no Open WebUI local |
| Action "Exportar Minuta de Impugnacao Servfaz", v2.2.0 (Valves de empresa e representante; recusa marcadores `[1]` do chat) | `tools/comercial`, `skills/openwebui-gerar-minuta-impugnacao/` (commits `4900099` e `92d679f`) | Instalada no Open WebUI local; Valves de razão social, local e representante ainda vazias |
| Limite de leitura de skills (`SKILL_CONTENT_MAX_CHARS`) | Admin do Open WebUI | 32000 na instância local |

## O que foi feito

### Capacidades e regras gerais (30/10 a 03/11)
- `capacidades.md`: capacidades "Texto da Lei 14.133" e "Jurisprudência do TCU", com roteiros; plano B (busca na web quando a pesquisa do TCU falha), com níveis internos de fonte A a D.
- `regras-gerais.md` §4: transcrição só do que foi aberto; "conferido" só com consulta registrada; precedente só com fonte aberta; LexML só com URN do TCU; nada entre aspas vindo de trecho de busca; letras dos níveis nunca aparecem para o analista, só a confiança em palavras.
- Fases 2, 4 e 5 remetem aos roteiros de `capacidades.md`.
- `.gitignore`: `dist/` (zip gerado da skill).

Commits: `d3561a9`, `cfe6033`, `3eeb0e1`, `55b9fba`, `fd9a9b6`, `9707772`, `323b3e0`, `17f7f3f`, `101b0c9`, `da427fe`, `8672766`.

### Fase 3 (impugnação)
- Passo obrigatório antes de redigir: abrir cada dispositivo e precedente; registrar uma linha por fonte antes da minuta.
- Pesquisa no TCU só depois da seleção dos pontos pelo analista; contraponto com o dispositivo favorável à Administração.
- Categoria **Condicionado**: ponto que depende de documento ausente entra só como esclarecimento ou pedido de exibição (`ac00766`).
- Peça sem marcadores de citação do chat e com referências por extenso; pedidos sem qualificar o prazo ("tempestiva") (`ac00766`).
- Dispositivo citado tem que dizer o que a peça afirma dele; aspas com cópia exata; paráfrase sem conclusão nova; registro antes da minuta diz o que cada texto aberto sustenta (`6b1e64b`).

### Jurisprudência sem qualificativo
- Skill e prompt proíbem "pacífica", "consolidada", "firme" e "reiterada" na resposta e na peça, mesmo com o inteiro teor aberto (`6b1e64b`, `9ce8080`).

### Preset "Licitações Servfaz" (`deploy/openwebui/preset-licitacoes-servfaz.md`)
- Configuração do preset e prompt de sistema versionados (`542b6a1`).
- Prompt mesclado com o agente "Analista de Licitações": papel, ativação da skill pelos arquivos de fase, roteamento, quadro de documentos, continuidade entre fases, ferramentas, regras invioláveis e comunicação (`9ce8080`).
- Regras de fundamento pertinente e aspas exatas; leitura dos arquivos da skill com `max_chars: 32000` (`9b130c2`).

### Situação no Open WebUI local (05/11)
- Preset `licitacoes-servfaz` com o prompt do último commit (8.566 caracteres).
- Skill importada a partir de `dist/licitacoes-servfaz.zip` gerado deste branch.

## Testes feitos

Com o edital do MPU SP (Pregão Eletrônico 38/2026, limpeza e copeiragem, baixado do PNCP; arquivos de teste fora do git em `briefing/editais-teste/`):

| Teste | Resultado |
| --- | --- |
| Quadro de documentos (Fase 1) | Planilha marcada "citado e não enviado", embora estivesse no PDF e na base: o modelo só viu os trechos recuperados |
| Minuta 1 (Fase 3) | Tese do ETP sem o ETP, "pacífica", "inequívoca tempestividade", marcadores `[1]` no Word. Corrigido em `ac00766` e na Action |
| Minuta 2 (Fase 3) | Problemas anteriores resolvidos; novos: vigência errada, arts. 56 e 121 sem pertinência, parêntese dentro das aspas, paráfrase além do acórdão, "consolidada", páginas inventadas, art. 55 citado sem abrir. Itens 2, 3, 4 e 5 corrigidos em `6b1e64b` e `9b130c2` |
| Leitura da skill | O modelo leu a Fase 3 inteira em três partes de 10 mil caracteres; a falha dos itens 3 e 7 não foi de leitura |

Não houve teste depois dos commits de 05/11.

## Pendente para análise

### Skill
1. **Fase 2 levanta impugnações.** O Tópico 6 do MODO 2 manda buscar "TODOS" os pontos de impugnação, com fundamento, antes da Fase 3. Decidir entre só sinalizar candidatos para a Fase 3 ou remover o tópico. Os exemplos do tópico usam itens e e-mail de um edital real de outro órgão e devem virar genéricos.
2. **Fase 1 com menos rigor que a Fase 3.** Propostos: portão documental leve, "não localizado no material examinado" em vez de "não enviado", destinação "não sustentado" e contraponto na Etapa 4, prazo de impugnação conferido no edital.
3. **Quadro de documentos com base de conhecimento.** Quando o material vem de busca por trechos, registrar "não localizado nos trechos recuperados" e listar os arquivos de origem.
4. **Item 1 (dado errado no argumento).** As regras de transcrição literal cobrem a cláusula alegada; falta dizer que todo dado usado na Fundamentação também precisa de fonte.
5. **Item 7 (art. 55 nos Pedidos).** O Passo obrigatório fala em "para cada ponto escolhido… antes da Fundamentação"; incluir os dispositivos citados nos Pedidos e no fecho.
6. **Item 6 (páginas inventadas).** Mandar omitir a página quando ela não aparece no trecho lido.
7. **Item 8 (esclarecimento mal formulado)** e **item 10 (razão social escrita em vez do marcador)**: rever a orientação da Fase 3 sobre perguntas de esclarecimento e campos da qualificação.
8. **Arquivos acima de 32 mil caracteres.** Fase 2 (30.067) e Fase 3 (29.346) cabem no novo limite; os arquivos de `references/estudo/` passam de 32 mil (o catálogo tem 88.630) e devem ser pesquisados por trecho. Avaliar dividir Fase 2 e Fase 3.
9. **Paráfrase de teses no plano B** e **status falso de "conferido"**: limites anteriores, não retestados.

### Avaliação do comportamento do modelo
10. Repetir a minuta do MPU SP com o preset atual (3 execuções) e contar: qualificativos de jurisprudência, dispositivos citados sem chamada à ferramenta, páginas sem fonte, leituras com `max_chars: 32000`.
11. Opcional: script que cruza os artigos e acórdãos citados no bloco da minuta com as chamadas de ferramenta da conversa; a mesma checagem pode virar aviso na Action.

### Ambiente (Open WebUI e `servfaz-rag`)
12. Preencher as Valves da Action (razão social, local, nome, cargo, RG e CPF do representante); RG e CPF ficam visíveis a quem administra Functions.
13. Embeddings: 10 coleções antigas do Chroma estão com 3072 dimensões, e o embedding atual (`gemini-embedding-001` no LiteLLM, `dimensions: 1536`) gera 1536. Reindexar ou reenviar esses arquivos.
14. MinerU: o Open WebUI espera 300 s (`MINERU_API_TIMEOUT`); o edital de 275 páginas passa disso em CPU. Proposto 1800 s. O contêiner do MinerU reiniciou uma vez no meio de um PDF grande (suspeita de memória, limite de 6 GiB).
15. Fase 4 com o MPU SP (etapa 1, planilha `.ods` convertida para `.xlsx`): não testada.

### Entrega
16. PR deste branch; push e PR do `tools/comercial` (11 commits à frente do `origin` em 05/11).
17. Recriar o preset e a skill na VPS a partir de `deploy/openwebui/preset-licitacoes-servfaz.md` e do zip deste branch.
18. Se o branch `origin/claude/gifted-albattani-zk6oog` for integrado, manter um só prompt de agente (o deste branch já tem o conteúdo daquele).
