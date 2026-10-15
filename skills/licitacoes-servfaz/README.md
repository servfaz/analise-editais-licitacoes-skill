# licitacoes-servfaz

Skill única do processo comercial de licitações da Servfaz, do edital ao recurso. Fonte única para Claude e Open WebUI: o conteúdo fica aqui e `scripts/build_skill.py` gera o pacote de cada ambiente.

## Estrutura

| Arquivo | Conteúdo | Origem |
| --- | --- | --- |
| `SKILL.md` | Orquestrador: identifica a fase, abre com o quadro de documentos, passa o resultado adiante | novo |
| `references/regras-gerais.md` | Regras comuns a todas as fases | consolidado de `SKILL.md`, `SKILL_triagem.md` e da skill de impugnação |
| `references/capacidades.md` | Contrato de ferramentas por capacidade (CCT, leitura, pesquisa jurídica) | novo |
| `references/fase-1-triagem.md` | Triagem (seguir/descartar) | `SKILL_triagem.md` |
| `references/fase-2-analise-edital.md` | Levantamento para composição de preços e parecer | `SKILL.md` |
| `references/fase-3-impugnacao.md` e `fase-3-temas-e-exemplos.md` | Hipóteses de impugnação e esclarecimento | `skills/impugnacao-editais-tcu` |
| `references/fase-4-pcfp.md` e `fase-4-pcfp-regras.md` | PCFP da concorrente e carta ao pregoeiro | skill `analise-pcfp` |
| `references/fase-5-recurso.md` | Recurso administrativo (versão inicial) | novo |
| `references/catalogo-de-fontes.md` | Status das fontes legais | `briefing/Mapeamento_Analise/01 - Catalogo de Fontes.md` |
| `evals/roteamento.json` | Casos de teste do roteamento | novo |

## Ajustes em relação às skills de origem

- **Ferramenta de CCT:** a referência à ferramenta `Conhecimento Servfaz` foi substituída pela capacidade "consulta de CCT", atendida pelo RAG de CCTs via MCP em qualquer ambiente.
- **RAT ajustado pelo FAP:** a regra da PCFP passou a comparar o RAT ajustado (0,5% a 6%), não o FAP (multiplicador de 0,5 a 2,0).
- **Estrutura da PCFP:** a saída sem inconsistências voltou para o passo 4 da etapa 2.
- **Regras de tributos e encargos:** a PCFP ganhou as regras do briefing de planilha de custos.
- **Carta da PCFP:** passou a exigir a fonte de cada critério e o status da fonte no catálogo.
- **Pontos marcados `[a validar]` em `fase-4-pcfp-regras.md`:** faixa da conta vinculada (qual rubrica) e plano de saúde no DF. Dependem do time comercial.

As skills de origem continuam no repositório e devem ser retiradas depois que esta for validada, para que o modelo não escolha entre versões concorrentes.

## Gerar os pacotes

```bash
python3 scripts/build_skill.py
python3 -m unittest scripts/test_build_skill.py
```

Saída em `dist/` (não versionado):

| Arquivo | Uso |
| --- | --- |
| `dist/claude/licitacoes-servfaz.zip` | Claude: pasta com `SKILL.md` e `references/`, carregadas sob demanda |
| `dist/openwebui/licitacoes-servfaz.md` | Open WebUI: arquivo único com todas as fases (~143 KB, todo injetado no contexto) |
| `dist/openwebui/licitacoes-servfaz-fase-N-*.md` | Open WebUI: uma skill por fase (50 a 80 KB), mais leve |

No Open WebUI a skill é importada como um único Markdown, sem `references/`. O build converte cada `references/x.md` em "a seção «Título» deste documento" ou, no pacote por fase, em "a skill `licitacoes-servfaz-fase-N`".

## Instalar

**Claude:** envie o `.zip` em Configurações > Capacidades > Skills para teste individual. Para o time, o administrador da organização publica a skill para todos. A consulta de CCT exige o conector MCP do RAG de CCTs adicionado nos conectores da conta.

**Open WebUI:** em Workspace > Skills, importe o `.md` desejado (ver `skills/openwebui-impugnacao-editais-tcu/README.md`, seção 3). Cadastre o servidor MCP do RAG de CCTs como ferramenta externa e habilite-o no modelo. Use um modelo com chamada de ferramentas em modo Native.

## Manutenção

Edite apenas os arquivos desta pasta. Todo arquivo de `references/` precisa começar com um título `# ` único, que o build usa como nome da seção. Nova referência citada no `SKILL.md` deve existir em `references/`; o build falha se não existir.
