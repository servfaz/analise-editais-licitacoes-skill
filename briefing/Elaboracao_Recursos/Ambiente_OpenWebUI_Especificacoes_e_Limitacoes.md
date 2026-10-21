# Ambiente OpenWebUI: especificações e limitações para a skill de recursos

**Finalidade:** registrar as condições conhecidas do ambiente de execução e suas implicações para a futura skill de análise e elaboração de recursos em licitações. Este documento é uma referência de projeto, não uma configuração técnica do servidor.

**Status do levantamento:** 21/10/2026. Atualizar quando houver mudança de versão, modelo, ferramentas ou configuração.

## 1. Ambiente informado pela equipe

| Aspecto | Situação informada | Observação para o projeto |
|---|---|---|
| Plataforma | OpenWebUI v0.11.4, instalada por imagem Docker | A variante exata da imagem (padrão ou `:slim`) ainda precisa ser confirmada. |
| Provedor/modelos | Um proxy disponibiliza modelos OpenAI e Google | O nome/ID exato de cada modelo no proxy e a passagem de chamadas de ferramentas dependem da configuração do proxy. |
| Modelo em uso | Google Flash 3.8, conforme identificação usada pela equipe | A documentação do Google registra suporte a function calling para `gemini-3.8-flash`; confirmar se esse é o ID efetivamente roteado pelo proxy. |
| Entrada documental | Arquivos anexados à conversa; predominam PDFs pesquisáveis e planilhas | A skill deve começar pelos arquivos da conversa. Não presumir que uma Knowledge Base esteja disponível. |
| Planilhas | Não se exige auditoria de fórmulas e células | A análise pode usar os dados e quadros extraídos, mas deve indicar limitações quando a estrutura ou a extração impedir conferir um valor. |
| Knowledge Bases | Uso futuro, ainda não confirmado para a primeira versão | A skill deve ser modular: não exigir Knowledge Base e permitir incorporá-la depois. |
| Pesquisa na web | Web Search está habilitado | A versão inicial trabalhará com documentos fornecidos e poderá pesquisar fontes públicas quando isso for pertinente e permitido pelo fluxo. |
| Pesquisa no TCU | Está prevista uma ferramenta MCP própria, ainda a implementar | Projetar uma etapa opcional e substituível: usar a ferramenta quando estiver disponível; caso contrário, prosseguir apenas com fontes acessíveis e informar a limitação. |
| Dados externos | Não há requisito de execução exclusivamente local | Isso não equivale a uma garantia de confidencialidade local: prompts e trechos de arquivos enviados ao modelo podem ser processados pelo provedor configurado. |
| Saída | O analista escolherá entre resposta em Markdown no chat ou arquivo `.docx` | A skill deve produzir conteúdo estruturado e revisável; a geração do Word será feita por ferramenta separada, acionada opcionalmente. |
| Modelo Word | O modelo/timbre da empresa será elaborado posteriormente | Até a ferramenta e o modelo existirem e serem testados, não prometer nem simular a geração de um `.docx` final. |
| Configurações | A equipe informa que os recursos estão no modo padrão do OpenWebUI | É necessário validar no ambiente real quais extratores e opções de busca estão efetivamente ativos; “padrão” pode variar por imagem e configuração administrativa. |

## 2. Implicações para a arquitetura e as instruções da skill

### 2.1 Skill, ferramentas e referências são componentes diferentes

No OpenWebUI, uma Skill é um conjunto de instruções em Markdown; ela orienta o comportamento do modelo, mas não executa por si só extração de documentos, pesquisa web, chamadas MCP ou conversão para Word. Essas capacidades dependem de ferramentas e configurações disponíveis no ambiente.

Assim, a skill deve:

- conter o fluxo de análise, critérios de qualidade, limites e formato das respostas;
- verificar ou declarar quando a ferramenta necessária não estiver disponível, sem fingir que a utilizou;
- tratar a pesquisa TCU e a geração de `.docx` como módulos opcionais, que podem ser adicionados sem reescrever o processo central;
- manter o texto principal conciso e carregar instruções complementares sob demanda. A documentação do OpenWebUI indica limites padrão de leitura/prévia de Skill (20.000/5.000 caracteres, configuráveis), o que recomenda não concentrar todo o material em um único arquivo.

### 2.2 Anexos, PDFs e planilhas

O fluxo inicial deve considerar os arquivos anexados diretamente ao chat. O conteúdo efetivamente disponível ao modelo depende do mecanismo de extração configurado, não apenas do fato de o arquivo estar anexado.

- PDFs pesquisáveis são a entrada preferencial, mas a skill deve conferir se o texto extraído contém as páginas e os trechos necessários. Se houver arquivo escaneado, página ausente, tabela desordenada ou texto ilegível, registrar a limitação e pedir OCR, versão pesquisável ou validação humana quando isso for material.
- Para planilhas, considerar leitura dos dados extraídos e dos quadros pertinentes; não reconstruir fórmulas nem declarar que conferiu fórmulas/células, pois isso está fora do escopo definido.
- A variante Docker é uma dependência importante: na versão 0.11.4, o caminho padrão documentado usa carregador de PDF e, para `.xlsx`, carregadores que podem recorrer a representação textual da planilha. A variante `:slim` tem limitações de carregamento de PDF e XLSX com o extrator interno e pode exigir um extrator externo. Confirmar a variante antes de validar a skill com esses formatos.
- Mesmo no caminho padrão, tabelas e planilhas podem perder relações entre cabeçalhos, linhas e valores ao virarem texto. Uma afirmação relevante deve ser rastreável ao arquivo e à localização; em caso de extração ambígua, não inferir silenciosamente.

### 2.3 Modelos e chamadas de ferramentas

O modelo informado como atual é Google Flash 3.8. A documentação oficial do Google registra function calling para `gemini-3.8-flash`, mas isso não garante que o proxy encaminhe corretamente esquemas de ferramentas, chamadas e resultados até o OpenWebUI.

Antes de habilitar uso operacional de ferramentas, testar no caminho real (OpenWebUI → proxy → modelo):

- se a Skill é carregada e seguida no modelo selecionado;
- se o modelo consegue invocar as ferramentas disponibilizadas e interpretar seus resultados;
- se Web Search está habilitado para o modelo/rota e pode ser acionado na conversa;
- se, quando os modelos OpenAI forem usados, seus respectivos IDs e capacidades também foram validados.

A skill não deve concluir que houve pesquisa só porque Web Search aparece habilitado na plataforma. A pesquisa precisa ter sido realmente executada e suas fontes identificadas.

### 2.4 Web Search e futura ferramenta MCP do TCU

Web Search e a integração MCP são recursos separados. A configuração de pesquisa pode depender de provedor global, suporte da rota/modelo e ativação na conversa. O MCP do TCU ainda não existe no fluxo informado e, por isso, não pode ser pressuposto pela primeira versão.

Para preservar a modularidade:

1. O núcleo da skill deve aceitar documentos fornecidos e fontes públicas efetivamente consultadas.
2. A etapa de jurisprudência deve preferir a ferramenta MCP do TCU depois que ela estiver implementada e validada.
3. Sem a ferramenta, deve sinalizar a limitação e não inventar resultados, números de acórdãos, enunciados ou trechos.
4. A integração precisa ser registrada no OpenWebUI por administrador. A documentação da versão indica suporte nativo a MCP via Streamable HTTP; endpoints em outros transportes podem exigir uma ponte compatível. Em Docker, o endereço do servidor MCP deve ser alcançável a partir do contêiner — não presumir que `localhost` do contêiner seja o host ou outro serviço.
5. Uma conexão MCP estabelecida não comprova que o modelo fará chamadas corretas; é necessário testar invocação, parâmetros, resposta e tratamento de erros.

### 2.5 Saída Markdown e geração de `.docx`

Markdown no chat é a saída nativa e deve servir de conteúdo-base revisável. A geração de Word será um módulo independente e opcional:

- só converter após escolha do analista;
- usar o modelo/timbre que será definido pela empresa;
- preservar o conteúdo jurídico aprovado, sem a ferramenta de formatação alterar teses, fatos, citações ou pedidos;
- identificar campos pendentes em vez de completar lacunas com dados presumidos;
- validar o arquivo gerado e a ferramenta no ambiente antes de oferecer o `.docx` como saída operacional.

### 2.6 Privacidade e uso de provedores externos

Foi informado que não há exigência de execução local exclusiva. Ainda assim, o desenho deve considerar que, quando um provedor externo é usado, o prompt e o contexto necessário para a resposta podem ser encaminhados a esse provedor. A skill deve evitar incluir dados sem relação com a análise e não deve afirmar que o processamento é local ou confidencial sem confirmação da configuração e das condições aplicáveis ao serviço.

## 3. Validações técnicas pendentes antes da implantação

- [ ] Confirmar se a imagem Docker é a padrão ou `:slim` e qual extrator de documentos está ativo.
- [ ] Testar um PDF pesquisável representativo e verificar se páginas, citações e tabelas são recuperadas corretamente.
- [ ] Testar uma planilha representativa, observando legibilidade dos dados extraídos sem ampliar o escopo para auditoria de fórmulas/células.
- [ ] Testar no proxy o modelo Google Flash 3.8 e confirmar seu identificador, carregamento de Skills e uso de ferramentas.
- [ ] Confirmar como Web Search é habilitado na rota/modelo e na conversa real.
- [ ] Definir se a compatibilidade com os modelos OpenAI também será requisito de lançamento ou apenas posterior.
- [ ] Ao implementar o MCP do TCU, definir transporte, autenticação, endereço acessível pelo contêiner, administração/registro e casos de teste de pesquisa.
- [ ] Desenvolver e testar separadamente a ferramenta de conversão `.docx` e o modelo/timbre da empresa.

## 4. Fontes técnicas

| Tema | Fonte oficial | Uso neste levantamento |
|---|---|---|
| Skills no OpenWebUI | [Skills — OpenWebUI Documentation](https://docs.openwebui.com/features/workspace/skills/) | Natureza das Skills, carregamento, limites padrão e uso de referências. |
| Knowledge Bases | [Knowledge — OpenWebUI Documentation](https://docs.openwebui.com/features/workspace/knowledge/) | Diferença entre anexos/conhecimento e modos de recuperação. |
| Web Search | [Agentic Web Search — OpenWebUI Documentation](https://docs.openwebui.com/features/chat-conversations/web-search/agentic-search/) | Condições de disponibilidade e dependência do modelo/ferramenta. |
| MCP | [MCP — OpenWebUI Documentation](https://docs.openwebui.com/features/extensibility/mcp/) | Suporte, transporte, registro administrativo e cuidados de conectividade. |
| Extração documental | [Document Extraction — OpenWebUI Documentation](https://docs.openwebui.com/features/chat-conversations/rag/document-extraction/) | Variação dos extratores e limites de processamento. |
| Carregadores na versão 0.11.4 | [Código oficial dos carregadores (tag v0.11.4)](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/retrieval/loaders/main.py) | Diferença relevante entre caminhos padrão e `:slim` para PDF/XLSX. |
| Function calling | [Gemini 3.8 Flash — Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) | Capacidade documentada do modelo; não substitui teste do proxy real. |
| Privacidade | [Chat Data Privacy and Encryption — OpenWebUI Documentation](https://docs.openwebui.com/security/chat-data-privacy-and-encryption/) | Considerações sobre processamento e envio de contexto aos provedores. |

## 5. Referências internas

- [Fluxo operacional da Skill de elaboração de recurso](Fluxo_Operacional_Skill_Elaboracao_Recurso.md) — etapas e critérios de passagem da análise até a minuta.
- [Documentos e fundamentação do recurso](Documentos_e_Fundamentacao_do_Recurso.md) — fontes documentais e jurídicas previstas para a análise.
- [Briefing mínimo](Briefing_Minimo.md) — informações direcionadoras fornecidas pelo analista.
