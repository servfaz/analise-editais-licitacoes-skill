# Impugnação de editais para Open WebUI

Skill independente para analisar editais, apresentar achados para escolha do analista e redigir a minuta dos pontos selecionados. A entrada deve estar legível e identificada; use capacidades de leitura disponíveis no ambiente, mas o pacote não inclui Tool própria de extração, indexação, banco persistente ou protocolo.

## Conteúdo

- `SKILL.md`: instruções para importar como Skill no Open WebUI e associar ao modelo de análise de impugnações.
- `references/`: cópia estruturada do estudo de impugnação, com análise e estrutura do edital e dos anexos, mapas de cruzamento entre documentos, catálogo de fontes e índice de consulta.
- `references/regras-priorizacao-fontes.md`: orientação própria desta Skill para priorizar ETP, planilha estimada e normas, além de limitar conclusões quando o orçamento estiver sigiloso.

## Usar as referências

O `SKILL.md` começa por um portão de verificação documental: inventaria os documentos e componentes, registra a cobertura e pausa antes da triagem quando faltar material necessário, salvo autorização prévia para prosseguir parcialmente. Depois orienta a leitura progressiva dos mapas: identificar as seções em `estrutura.md`, localizar hipóteses em `analise.md`, seguir em `fontes.md` os documentos e seções a cruzar, extrair a prova indicada e então conferir os IDs de fundamento no catálogo e nas fontes oficiais. Antes de avaliar hipóteses de planejamento ou custos, consulte também `references/regras-priorizacao-fontes.md`; essa regra própria da Skill prevalece sobre recomendações conflitantes nos mapas. O índice serve para localizar fontes; o catálogo contém o nome, esfera, endereço e status. Os mapas orientam a investigação, mas não substituem a conferência da fonte oficial nem a análise do caso concreto.

As referências são uma cópia adaptada do estudo mantido em `skills/impugnacoes-triagem/references/estudo/`. O catálogo omite a coluna “Usado em”, que duplicava a relação já indicada pelos mapas. A coluna “Status” foi mantida porque distingue fontes conferidas, pendentes, históricas e não utilizáveis; “conferido” registra uma checagem anterior e não dispensa abrir a fonte oficial atual antes de citar. A priorização de fontes e o tratamento de orçamento sigiloso são uma orientação operacional específica deste pacote, registrada em `references/regras-priorizacao-fontes.md`; os mapas gerados e a skill original não foram alterados. Se o estudo de origem mudar, atualize esta cópia preservando essas adaptações antes de importar uma nova versão da skill no Open WebUI.

## Exportação da minuta

A resposta de minuta contém exatamente um bloco entre `<!-- minuta-servfaz:inicio -->` e `<!-- minuta-servfaz:fim -->`, no Markdown aceito pela Action existente **Exportar Minuta de Impugnacao Servfaz**. Habilite essa Action no modelo para que o analista possa revisar o texto, confirmar a versão pelo hash e gerar o DOCX timbrado. A Action é instalada separadamente conforme `skills/openwebui-gerar-minuta-impugnacao/functions/INSTALACAO.md`. Importe o pacote como pasta, ZIP ou `.skill` para que o Open WebUI preserve `SKILL.md` e seus arquivos de referência.

A Skill e a Action não assinam, protocolam nem enviam documentos. Campos pessoais ausentes permanecem marcados para preenchimento e revisão humana.

## Verificação de homologação

Faça a conferência em ambiente de teste, sem dados pessoais reais:

1. Com trechos de edital e TR que demonstrem divergência de prazo, a skill apresenta evidências e IDs estáveis, explica o efeito e aguarda seleção.
2. Se outro anexo justificar ou resolver uma exigência, a skill registra o contraponto e não mantém um falso positivo como impugnação sugerida.
3. Ao selecionar somente um de dois achados, a minuta inclui apenas o selecionado e usa as seis partes padronizadas.
4. Se não houver fundamento ou prova suficientes, a skill informa a limitação e não transforma a suspeita em fato na peça.
5. Se faltar documento necessário à cobertura integral, o portão devolve somente o inventário e pergunta se o analista enviará os documentos ou autoriza a triagem parcial; sem autorização prévia, não apresenta matriz de achados. Após autorização, registra os limites e não conclui sobre pontos dependentes do material faltante.
6. O portão classifica documentos e componentes internos por conteúdo e legibilidade, com páginas/seções ou aba/linha/célula; uma planilha em PDF único é reconhecida pelo conteúdo. Componente ausente vira pendência, não achado automático.
7. A matriz conserva valores e dados literais relevantes, marca inferências como `[inferência]` com sua base e usa “Não localizado no material recebido — confirmar na versão oficial” sem alegar omissão do edital.
8. Sem ferramenta de consulta documental, jurídica ou de CCT, a skill não afirma que pesquisou: solicita material legível ou registra a verificação pendente.
9. Com ETP e planilha disponíveis, a análise usa o ETP para planejamento e a planilha para composição, cruzando os dois quando pertinente.
10. Sem ETP, mas com planilha disponível, a skill limita a análise aos fatos demonstrados pela planilha e não presume que o ETP inexista no processo.
11. Sem ETP nem planilha, a skill só usa as INs 05/2017 e 07/2018 após confirmar aplicabilidade; as normas orientam o exame, mas não provam erro no orçamento específico.
12. Com orçamento sigiloso e planilha inacessível, a skill marca como não avaliáveis os pontos dependentes da planilha, não infere conteúdo oculto e só mantém achados sustentados por evidência pública independente; avalia a justificativa do sigilo separadamente.

Revise o DOCX gerado, confirme a preservação do timbre e verifique que os campos pendentes aparecem destacados em amarelo. O clique de confirmação da Action é necessário para gerar o arquivo.
