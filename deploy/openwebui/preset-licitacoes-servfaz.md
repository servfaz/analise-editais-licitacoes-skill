# Preset "Licitações Servfaz" no Open WebUI

Preset do Workspace > Models que usa a skill `licitacoes-servfaz` com a Tool "Fontes oficiais Servfaz" (jurisprudência do TCU e texto da Lei 14.133, pacote `skills/openwebui-tcu-jurisprudencia/` no branch `tools/comercial`). Exportado da instância local (Open WebUI 0.13.0) em 03/11/2026, depois do teste que o validou.

O preset existe só no banco do Open WebUI: este arquivo é a referência para recriá-lo em outra instância (por exemplo, na VPS).

## Por que o prompt de sistema tem estas regras

Nos testes de 03/11/2026, com a pesquisa do TCU fora do ar, a skill e a mensagem da Tool já descreviam o plano B (busca na web com níveis de confiança), mas o modelo nem sempre lia o arquivo da skill e, mesmo recebendo a mensagem da Tool, ignorava a parte de apresentação: não informava a confiança, dizia "jurisprudência pacífica" e mostrava as letras internas dos níveis. As regras no prompt de sistema valem em toda mensagem e resolveram isso no teste:

- aviso de que a pesquisa do TCU falhou, no início da resposta;
- confiança em palavras (alta, média, baixa) e motivo ao lado de cada precedente, e uma linha final "Confiança da resposta";
- sem letras internas (A a D) e sem "pacífica", "consolidada" ou "firme" quando o inteiro teor não foi aberto;
- nenhum precedente citado sem fonte aberta na conversa;
- nada entre aspas vindo de trecho de resultado de busca, e o LexML só como fonte oficial com URN do TCU (regra 7, de 03/11/2026: num teste completo, o resumo de um artigo de revista catalogado no LexML entrou na minuta como "ementa oficial" do Acórdão 964/2012).

As letras A a D continuam na skill (`references/capacidades.md` e `references/regras-gerais.md`) e na Tool, só para o modelo classificar as fontes.

## Configuração

| Campo | Valor |
| --- | --- |
| ID | `licitacoes-servfaz` |
| Nome | Licitações Servfaz |
| Modelo base | `gemini/gemini-3.6-flash` |
| Descrição | Licitações da Servfaz (Lei 14.133): skill licitacoes-servfaz, fontes oficiais (TCU e Lei 14.133) e busca na web com confiança. |
| Tools | `jurisprudencia_tcu_servfaz` (Tool "Fontes oficiais Servfaz", 0.2.4 ou posterior) |
| Skills | `licitacoes-servfaz` |
| Recursos ligados por padrão | Pesquisa na Web (`web_search`) |
| Function Calling | Native |
| Acesso | Privado ao criador; compartilhe em Workspace > Models quando for liberar ao time |

```json
{
  "id": "licitacoes-servfaz",
  "name": "Licitações Servfaz",
  "base_model_id": "gemini/gemini-3.6-flash",
  "meta": {
    "description": "Licitações da Servfaz (Lei 14.133): skill licitacoes-servfaz, fontes oficiais (TCU e Lei 14.133) e busca na web com confiança.",
    "capabilities": {
      "file_context": true, "vision": true, "file_upload": true, "web_search": true,
      "image_generation": false, "code_interpreter": false, "terminal": false,
      "citations": true, "status_updates": true, "memory": false, "builtin_tools": true
    },
    "toolIds": ["jurisprudencia_tcu_servfaz"],
    "skillIds": ["licitacoes-servfaz"],
    "defaultFeatureIds": ["web_search"]
  },
  "params": { "function_calling": "native" }
}
```

A Pesquisa na Web precisa estar habilitada na instância (Admin > Settings > Web Search). Na instância local o provedor é o Tavily. Com ela, o modelo recebe as ferramentas nativas `search_web` e `fetch_url`; o plano B depende das duas, porque o trecho do resultado de busca não conta como fonte aberta.

## Prompt de sistema

```text
Você apoia o time comercial da Servfaz em licitações regidas pela Lei 14.133/2021, seguindo a skill licitacoes-servfaz.

Regras de fundamentação, válidas em toda resposta:
1. Não cite lei, súmula, acórdão ou julgado de nenhum tribunal de memória: só o que veio de uma ferramenta ou de uma página aberta nesta conversa.
2. Se a pesquisa do TCU falhar, diga isso ao usuário no início da resposta e siga o plano B indicado pela ferramenta.
3. Ao lado de cada precedente que não veio do inteiro teor aberto na pesquisa oficial do TCU, escreva a confiança em palavras e o motivo, por exemplo: "confiança média: confirmado em publicação oficial do TCU; texto integral do acórdão a conferir". Termine a resposta com a linha "Confiança da resposta: alta, média ou baixa — motivo".
4. Não mostre códigos internos de classificação das fontes, como "nível A" ou "nível B".
5. Sem o inteiro teor do acórdão aberto na pesquisa oficial do TCU, não use "pacífica", "consolidada", "firme" nem "confirmada na base oficial".
6. Só atribua uma tese a um acórdão se o texto aberto a ligar a esse acórdão.
7. Texto entre aspas (lei, ementa, enunciado ou trecho de acórdão) só pode vir do resultado de uma ferramenta ou de uma página aberta com fetch_url, nunca do trecho de um resultado de busca. No LexML, só é fonte oficial a página com URN do TCU (urn:lex:br:tribunal.contas.uniao); registro de biblioteca, revista ou livro é doutrina e não vale como ementa.
```

## Como recriar

1. Instale a Tool (`skills/openwebui-tcu-jurisprudencia/INSTALACAO.md`, branch `tools/comercial`) e importe a skill (`dist/licitacoes-servfaz.zip`, gerado a partir de `skills/licitacoes-servfaz/`).
2. Em **Workspace > Models > + (Create)**, preencha os campos da tabela acima e cole o prompt de sistema.
3. Em **Advanced Params**, deixe **Function Calling = Native**.
4. Teste com o TCU simulado fora do ar: troque a Valve `base_url` da Tool por um endereço inválido, pergunte "há jurisprudência do TCU sobre retenção de pagamento por irregularidade fiscal?" e confira o aviso de falha, a confiança de cada acórdão, a linha final de confiança e a ausência de letras e de "pacífica". Depois, volte a Valve para `https://pesquisa.apps.tcu.gov.br/rest/publico`.

## Limites conhecidos

- Na paráfrase da tese de cada acórdão, o modelo ainda pode juntar frases de enunciados vizinhos ou acrescentar inferências (visto em 2 de 4 acórdãos no teste). A confiança "média; texto integral a conferir" sinaliza isso, mas a tese precisa de revisão do analista antes de ir para uma peça.
- O branch `origin/claude/gifted-albattani-zk6oog` tem outro prompt de agente para a mesma skill (`deploy/openwebui/agente-analista-licitacoes.md`), com roteamento da skill e ferramentas de CCT e de exportação. Se for integrado, junte as regras de fundamentação acima àquele prompt.
