---
name: gerar-minuta-impugnacao-openwebui
description: Prepara uma minuta de impugnação aprovada para exportação em .docx timbrado da Servfaz, com confirmação humana obrigatória.
version: 2.0.0
---

# Exportar minuta de impugnação em `.docx`

Esta skill controla somente a passagem de uma minuta **já revisada** para o Word timbrado da Servfaz. Ela não analisa edital, pesquisa fundamento jurídico, completa fatos, corrige redação, assina, protocola nem envia documentos. A exportação de produção é feita pela Action **Exportar Minuta de Impugnacao Servfaz**, por clique do analista e confirmação explícita.

## Quando usar

Use depois que o analista revisou o conteúdo resultante da triagem e da redação. Não use se ainda houver ponto jurídico, documento, dado do certame, data, qualificação ou pedido a decidir.

## Fluxo obrigatório

1. Mostre a minuta integral no formato Markdown aceito pelo conversor, dentro de **um único** bloco abaixo. Não reescreva, resuma ou corrija o texto depois da aprovação do analista. As crases da ilustração não entram na resposta real: ela deve trazer apenas os comentários delimitadores e o Markdown, nunca um bloco de código.

   ```markdown
   <!-- minuta-servfaz:inicio -->
   ## IMPUGNAÇÃO AO EDITAL

   ... texto integral aprovado ...
   <!-- minuta-servfaz:fim -->
   ```

   Os comentários delimitadores são apenas o contrato com a Action e não entram no `.docx`.

2. Informe que o analista deve revisar a resposta e clicar em **Exportar Minuta de Impugnacao Servfaz** nessa mesma resposta. Não chame a Tool legada `gerar_minuta_impugnacao` no fluxo normal.

3. A Action exibe o hash abreviado do Markdown e pede confirmação. Somente após a confirmação ela gera o `.docx` do bloco exatamente como revisado e anexa o arquivo ao chat. O arquivo é guardado no Open WebUI sob o usuário que o gerou; a Action não o envia a terceiros.

4. Diga o nome do arquivo e os campos pendentes, se houver. Campos como `[Inserir Nome]`, `[Inserir RG]`, `[Inserir CPF]`, `[Data do Protocolo]` e `{{CAMPO}}` permanecem destacados em amarelo para preenchimento e conferência manual. Não invente dados de pessoa física nem tente removê-los sem instrução explícita.

5. Reforce que o analista continua responsável por revisão final, assinatura e protocolo. Nunca declare que a peça foi assinada, protocolada ou enviada.

## Convenções do Markdown

| No Markdown | No `.docx` |
| :-- | :-- |
| `# TÍTULO` ou `### TÍTULO` | Seção romana automática, em negrito e caixa alta. Um `I.` já digitado é descartado. |
| `## TÍTULO` | Título centralizado da peça. |
| `#### Título` ou parágrafo inteiro em `**negrito**` | Subtítulo em negrito. |
| Parágrafo comum | Texto justificado em Times New Roman 12,5 pt. |
| `> texto` | Citação recuada e em itálico. |
| Lista `1.` | Alíneas automáticas a), b), c), reiniciadas a cada lista. |
| `- ` sob um item numerado | Subitem recuado. |
| Tabela Markdown `\|` | Quadro com bordas; primeira linha em negrito. |
| `**negrito**`, `*itálico*`, `_itálico_` | Formatação de trecho. |
| `<!-- centralizado -->` … `<!-- /centralizado -->` | Local e data centralizados. |

Remissões como `[1]` são preservadas. O conversor recusa referências internas de triagem (`EXT-`, `INT-`, `NOVA-`, catálogo de fontes), blocos de código, imagens, links Markdown, tags HTML, texto riscado e títulos de níveis 5 ou 6.

## Dados corporativos e pendências

Nas Valves da Action, o administrador pode configurar apenas `CNPJ` e `ENDERECO` da Servfaz. Elas preenchem exclusivamente `[Inserir CNPJ]`, `[Inserir Endereço]` e `[Inserir Endereço Completo]` quando esses marcadores existirem.

Nome, RG, CPF e outros dados do signatário não são armazenados nas Valves da Action ou da Tool legada. Se estiverem no texto como marcadores, ficam destacados para o analista autorizado completar no Word. O mesmo vale para a data, salvo se ela já constar de modo aprovado no Markdown.

## Instalação no Open WebUI 0.12.3

1. Em **Admin Panel > Functions**, crie a Action e cole todo o conteúdo de `functions/gerar_minuta_impugnacao_action.py`. Salve-a como **Exportar Minuta de Impugnacao Servfaz**. O backend precisa ter `python-docx==1.1.2` disponível.
2. Nas Valves da Action, configure apenas o CNPJ e o endereço corporativos, se desejado.
3. Em **Workspace > Skills**, importe esta pasta ou um ZIP que contenha este `SKILL.md`. Anexe a Skill ao modelo especializado de impugnações.
4. Restrinja a Function, a Skill e o modelo ao grupo comercial/jurídico. Não conceda a analistas permissão para criar ou editar Tools/Functions.
5. Gere uma minuta de teste contendo `[Inserir CPF]`; revise a resposta, clique na Action, confirme e confira que o `.docx` chegou como arquivo do chat e que o campo segue amarelo.

A Tool em `tools/gerar_minuta_impugnacao.py` permanece somente como compatibilidade para instalações antigas. Ela entrega um Rich UI e não deve ser vinculada ao modelo de produção.

## Manutenção e teste

`scripts/gerar_minuta.py` é a fonte canônica do conversor. Depois de alterar esse arquivo ou `assets/timbre-servfaz.docx`, gere novamente os artefatos:

```sh
# A partir da raiz do repositório.
python3 -m venv .venv-minuta
. .venv-minuta/bin/activate
python -m pip install --upgrade pip
python -m pip install -r skills/openwebui-gerar-minuta-impugnacao/requirements-dev.txt

python skills/openwebui-gerar-minuta-impugnacao/build/montar_tool.py
python skills/openwebui-gerar-minuta-impugnacao/build/montar_acao.py
python -m unittest discover -s skills/openwebui-gerar-minuta-impugnacao/tests -v
```

Se o teste falhar em `from docx import Document`, o ambiente ativo não tem o pacote **python-docx**. Não instale `docx` (é outro pacote): execute o comando `python -m pip install -r .../requirements-dev.txt` no mesmo interpretador que executará o `unittest`. Confirme com `python -c "from docx import Document; print('python-docx OK')"`.

Os montadores incorporam o timbre original sem alterá-lo, para que o pacote seja reproduzível independentemente do ambiente que o gerou. A homologação de produção deve confirmar a Action em uma instância Open WebUI v0.12.3, incluindo controle de acesso e download do arquivo pelo analista comum.
