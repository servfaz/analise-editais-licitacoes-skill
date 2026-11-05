# Branch `tools/comercial`: o que foi feito e o que falta

Atualizado em 05/11/2026. Commits de 21/10 a 05/11/2026 sobre o `main`, enviados ao `origin`.

## Objetivo

Reunir as ferramentas do Open WebUI que o time comercial usa junto com as skills de licitação:

- a Action que exporta a minuta de impugnação aprovada para `.docx` timbrado da Servfaz;
- a Tool "Fontes oficiais Servfaz", que consulta a jurisprudência do TCU e o texto vigente da Lei 14.133 para o modelo não citar de memória.

As regras de uso dessas ferramentas na skill `licitacoes-servfaz` e o preset do Open WebUI estão no branch `feat/licitacoes-servfaz-tcu` (ver `briefing/Andamento_feat-licitacoes-servfaz-tcu.md` naquele branch).

## O que foi feito

### Elaboração de recurso (21/10 a 22/10)
- Levantamento do processo de recurso, modelagem da minuta, fluxo operacional e especificações e limites do Open WebUI: `briefing/Elaboracao_Recursos/` e `briefing/Fluxo - Analise e Recurso em Licitacao.md`.
- Pacote `skills/openwebui-elaborar-recurso-licitacao/` e seu zip (removidos em 05/11, ver abaixo).
- Passagem da Fase 4 (PCFP) para a elaboração do recurso.

Commits: `9dfca8a`, `1313e70`, `42c64c1`, `f104328`, `ddb113a`, `e77a19b`, `5890bca`, `728b811`.

### Impugnação no Open WebUI (22/10 a 23/10)
- Pacote `skills/openwebui-impugnacao/` (`licitacoes-servfaz-fase-3-impugnacao`, versão 1.0.0), removido em 05/11.
- Pacote `skills/openwebui-gerar-minuta-impugnacao/`: Action de exportação da minuta para `.docx` (caminho de produção), com confirmação humana e hash da versão, e a Tool legada de conversão. Os dois arquivos colados no Open WebUI são gerados por `build/montar_acao.py` e `build/montar_tool.py` a partir do núcleo `skills/gerar-minuta-impugnacao/scripts/gerar_minuta.py`.

Commits: `17b5a8d`, `f05948b`.

### Tool "Fontes oficiais Servfaz" (30/10 a 03/11, versão 0.2.4)
Pacote `skills/openwebui-tcu-jurisprudencia/` (tool, 44 testes e `INSTALACAO.md`; ID no Open WebUI: `jurisprudencia_tcu_servfaz`).

- **Jurisprudência do TCU** (API pública da Pesquisa do TCU): `buscar_jurisprudencia_selecionada`, `buscar_sumulas_tcu`, `buscar_acordaos_tcu` e `obter_acordao_tcu` (inteiro teor). Não devolve nomes de partes, advogados e interessados.
- **Lei 14.133** (normas.leg.br): `obter_dispositivo_lei` traz o texto vigente do artigo, parágrafo, inciso ou alínea, com as notas de alteração; `buscar_na_lei` acha o dispositivo por assunto. Só a 14.133 tem texto estruturado na API.
- **Falhas:** mensagens distintas para "nenhum resultado" e "falha técnica"; nova tentativa automática (3 tentativas de até 15 s) porque a API do TCU às vezes trava; na falha, a mensagem manda seguir o plano B (busca na web com página aberta, LexML só com URN do TCU, confiança em palavras, sem as letras internas A a D).

Commits: `b86aea8`, `f904d51`, `6261ee2`, `2ac2b46`, `ff4488a`, `b1c8352`, `074994b`, `2fa15aa`, `a94b41d`.

### Action de minuta (04/11, versão 2.2.0)
- Valves de razão social, CNPJ, endereço, local e nome, cargo, RG e CPF do representante; o núcleo reconhece os rótulos que a Fase 3 usa (ex.: "Representante Legal"). A data do protocolo continua como campo em amarelo (`4900099`).
- Recusa os marcadores de citação do chat (`[1]`, `[1, 2]`, `[1][2]`), que chegavam ao Word sem sentido (`92d679f`).

### Limpeza e documentação (05/11)
- Removidos os pacotes `skills/openwebui-impugnacao/` e `skills/openwebui-elaborar-recurso-licitacao/`: no `main`, a impugnação e o recurso passaram a ser fases da skill única `licitacoes-servfaz` (`a68af20`) (`c843766`).
- O zip `skills/elaborar-recurso-licitacao-openwebui.zip` saiu do git (o arquivo continua na pasta) e o `.gitignore` passou a ignorar `*.zip` (`6e70d95`).
- `INSTALACAO.md` da Tool do TCU com as Valves `timeout_s` (15) e `tentativas` (3) da versão 0.2.4 (`f58e1c0`).

## Estado em 05/11/2026

| Item | Situação |
| --- | --- |
| Testes | Tool do TCU: 44 OK. Action e Tool de minuta: 15 OK |
| Open WebUI local | Tool 0.2.4 e Action 2.2.0 instaladas (Function `gerar_minuta`); Valves da Action com CNPJ e endereço, as demais vazias |
| `main` não incorporado | 5 commits, entre eles `a68af20` (skills de todas as fases reunidas em `licitacoes-servfaz`) |
| Arquivos fora do git, de propósito | `skills/gerar-minuta-impugnacao/assets/dados-servfaz.json` e as pastas `*-workspace/` das skills |

## Pendente para análise

1. **Valves da Action:** preencher razão social, local e nome, cargo, RG e CPF do representante. RG e CPF ficam visíveis a quem administra Functions; restringir esse acesso.
2. **Tool do TCU, evoluções opcionais:** consulta direta ao LexML quando a pesquisa do TCU falhar; outras leis federais (LC 123, CLT, 8.666, 9.784), que hoje não têm texto estruturado no normas.leg.br.
3. **Decisão pendente:** manter a Tool no Open WebUI ou levá-la para um servidor MCP dedicado no `servfaz-rag`.
4. **Entrega:** PR para o `main` (incorporando os 5 commits do `main`) e instalação da Tool e da Action na VPS.
