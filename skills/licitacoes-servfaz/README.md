# licitacoes-servfaz

Skill única do processo comercial de licitações da Servfaz, do edital ao recurso. A mesma pasta serve ao Claude e ao Open WebUI (0.12 ou posterior, que importa pacotes com `references/`).

## Estrutura

| Caminho | Conteúdo | Origem |
| --- | --- | --- |
| `SKILL.md` | Orquestrador: identifica a fase, abre com o quadro de documentos, passa o resultado adiante | novo |
| `references/regras-gerais.md` | Regras comuns a todas as fases | consolidado das skills de origem |
| `references/capacidades.md` | Contrato de ferramentas por capacidade (CCT, leitura, pesquisa jurídica, exportação .docx) | novo |
| `references/fase-1-triagem/` | Triagem (seguir ou descartar) | `SKILL_triagem.md` |
| `references/fase-2-analise-edital/` | Levantamento para composição de preços e parecer | `SKILL.md` da raiz |
| `references/fase-3-impugnacao/` | Triagem de impugnação, seleção de pontos e minuta para a Action de .docx | `skills/openwebui-impugnacao` (branch `tools/comercial`, commit `f05948b`) |
| `references/fase-4-pcfp/` | PCFP da concorrente e carta ao pregoeiro | skill `analise-pcfp` |
| `references/fase-5-recurso/` | Análise e minuta de recurso | `skills/openwebui-elaborar-recurso-licitacao` (mesmo commit) |
| `references/estudo/` | Estrutura, análise e mapa de fontes de cada documento, catálogo e índice de fontes, compartilhados por todas as fases | `skills/openwebui-impugnacao/references` |
| `evals/roteamento.json` | Casos de teste do roteamento | novo |

## Decisões da unificação

- **Catálogo único:** `references/estudo/catalogo-fontes.md`, a versão conferida nas fontes oficiais. A Fase 5 deixou de usar o catálogo próprio, que era uma versão anterior sem status. Saíram dele `EXT-BASE-PAINELPRECOS` (retirado do estudo), `EXT-IN5-2014` (só histórica) e `EXT-TCU-INFO2026-INDICES` (substituído na revisão do catálogo).
- **Status das fontes:** `conferido` fundamenta peça depois de reaberta a fonte oficial; `a conferir` só como pendência (ver `references/regras-gerais.md`).
- **Fase 3:** a versão de impugnação para Open WebUI substituiu a antiga `impugnacao-editais-tcu`. A versão de Claude Code com scripts (`skills/impugnacoes-triagem`) continua separada, porque depende de pasta local e de Python.
- **Pontos `[a validar]`** em `references/fase-4-pcfp/regras-conteudo.md`: faixa da conta vinculada e plano de saúde no DF.

As skills de origem continuam no repositório. Depois de validar esta, retire-as dos modelos e das contas para que não concorram com ela.

## Validar e empacotar

```bash
python3 scripts/build_skill.py
python3 -m unittest scripts/test_build_skill.py
```

O script falha se algum `references/...` citado não existir e avisa sobre arquivos acima de 20.000 caracteres, o limite padrão de leitura de Skills no Open WebUI. Gera `dist/licitacoes-servfaz.zip` com `SKILL.md` e `references/`; README e evals ficam fora do pacote.

## Instalar

- **Claude:** Configurações > Capacidades > Skills > enviar o `.zip`.
- **Open WebUI:** Workspace > Skills > importar o `.zip` ou importar por link. Se o repositório for privado, o servidor do Open WebUI precisa de acesso ao link. Configuração do agente em `deploy/openwebui/agente-analista-licitacoes.md`.

## Manutenção

Edite só esta pasta. Ao trazer novas versões das skills do time, copie para a pasta da fase e ajuste os caminhos para `references/fase-N-*/` ou `references/estudo/`; o script acusa caminho quebrado.
