# Skill: elaborar recurso em licitação

Pacote de Skill para OpenWebUI, com instruções em português para analisar e apoiar a elaboração de recursos administrativos em licitações de serviços com dedicação exclusiva de mão de obra. O fluxo da Fase 5 aceita tanto a passagem de achados da Fase 4 (com validação nos documentos primários) quanto o acionamento direto por briefing e anexos. As regras gerais têm precedência explícita e cobrem rastreabilidade, literalidade, evidência, pertinência das fontes, decisão humana, privacidade e cobertura documental.

## Conteúdo

- `SKILL.md` — fluxo operacional e controles essenciais.
- `references/documentos-e-fundamentacao.md` — documentos por tipo de tese, regime jurídico e orientação para seleção de fontes.
- `references/catalogo-de-fontes.md` — catálogo amplo de fontes herdado da versão anterior, pesquisadas e com existência confirmada; selecione-as conforme a tese e o regime do certame.
- `references/estrutura-e-redacao.md` — estrutura da minuta e padrões de redação generalizados do estudo de peças anteriores.
- `references/ambiente-openwebui.md` — compatibilidade, recursos opcionais e validações técnicas.

Os documentos originais examinados em `files/recursos` não fazem parte deste pacote e não são necessários para executar a Skill.

## Importação por versão

### OpenWebUI 0.11.4

Use [elaborar-recurso-licitacao-openwebui-0.11.4.md](elaborar-recurso-licitacao-openwebui-0.11.4.md), que contém em um único Markdown as instruções e orientações que, no pacote modular, ficam em `references/`. Na versão 0.11.4, abra **Workspace > Skills > Import** e selecione o `.md`; confira nome e descrição, depois salve a Skill. A importação de Markdown é tratada no [código dessa versão](https://github.com/open-webui/open-webui/blob/v0.11.4/src/lib/components/workspace/Skills.svelte#L252-L309). Conceda acesso de leitura aos analistas que a utilizarão.

### OpenWebUI 0.12.0 ou posterior

O pacote ZIP modular pode ser usado a partir da primeira versão em que confirmei suporte no código, 0.12.0: essa versão inclui `.zip` no seletor de importação e interpreta os arquivos do pacote. Confira a [implementação de importação no código da versão 0.12.0](https://github.com/open-webui/open-webui/blob/v0.12.0/src/lib/components/workspace/Skills.svelte#L351-L367) e a [documentação oficial atual](https://docs.openwebui.com/features/workspace/skills/). Como sempre, valide na instalação concreta.

Para qualquer versão, selecione a Skill no chat usando `$` ou o menu de integrações. Para o modelo ler documentos de apoio de um pacote modular, habilite ferramentas nativas/Skills e function calling quando disponíveis. Confirme se Web Search funciona no modelo e chat efetivos; teste com PDF pesquisável e planilha representativos antes do uso operacional. A variante Docker (`standard` ou `:slim`) e os extratores ativos ainda precisam ser confirmados.

## Estado das integrações

- Web Search: habilitado segundo informação da equipe; verificar no modelo/chat efetivo.
- MCP do TCU: previsto, ainda não implementado; a Skill não depende dele.
- Geração de `.docx` com timbre: disponível no pacote complementar `skills/openwebui-gerar-minuta-impugnacao`. Em produção, use a Action **Exportar Minuta de Impugnacao Servfaz**, que exporta apenas o bloco Markdown revisado após confirmação humana; mantenha a ferramenta legada desabilitada no modelo.
- Modelo atual: Google Flash 3.8 via proxy; confirmar o identificador e testar o uso real de ferramentas nessa rota.
