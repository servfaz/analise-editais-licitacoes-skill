---
name: gerar-minuta-impugnacao
description: Gera o arquivo .docx da minuta de impugnação (ou de pedido de esclarecimento) da Servfaz a partir de uma peça em Markdown, sobre o timbre da empresa (cabeçalho e rodapé, margens, fonte, numeração romana nas seções e alíneas a), b), c)). Use quando o analista já tem a impugnação escrita em .md e pede para gerar, converter ou exportar a minuta em .docx ou Word. Não escreve nem altera o texto da peça, não monta a peça a partir de minutas por ponto, não faz triagem de edital, não assina, não protocola e não envia.
---

# Gerar minuta de impugnação em .docx

Esta skill só converte. Entra uma impugnação em Markdown já pronta; sai o `.docx` com o timbre da Servfaz, ao lado do `.md`. O texto não é escrito, corrigido nem resumido aqui: o que está no Markdown é o que vai para o Word. Quem revisa, assina e protocola é o analista.

`<skill>` é a pasta desta skill (a "Base directory" informada quando ela carrega).

## Como usar

1. Confirme com o analista qual arquivo `.md` é a peça. Se ele ainda não tem a peça escrita, esta skill não serve: a peça sai da triagem (`impugnacoes-triagem`).
2. Rode:

   ```bash
   <python> <skill>/scripts/gerar_minuta.py ENTRADA.md [--saida MINUTA.docx] [--data AAAA-MM-DD]
   ```

   Sem `--saida`, o `.docx` fica ao lado do `.md`, com o mesmo nome. O script imprime o caminho gravado.
3. Informe o caminho ao analista. Se o script listou campos em branco, repita a lista (linha do `.md` e marcador) e diga que eles estão em destaque amarelo no `.docx`, para o analista preencher à mão no Word e tirar o destaque. Não invente o dado nem edite o `.docx` por conta própria. Lembre que a revisão, a assinatura e o protocolo são dele, e não diga que a peça foi assinada, protocolada ou enviada.

Precisa de Python 3.10+ e `python-docx` (`scripts/requirements.txt`). Se o script recusar, leia a mensagem ao analista em palavras simples: ela aponta a linha e o que corrigir no Markdown.

## O modelo: convenções do Markdown

O conversor entende o Markdown comum abaixo. O que não está na tabela ou não vira nada ou é recusado (ver "Recusas").

| No Markdown | No .docx |
| :-- | :-- |
| Bloco `---` no início (front matter) | Ignorado |
| Linha `---` no meio do texto | Ignorada |
| `# TÍTULO` ou `### TÍTULO` | Seção com numeração romana automática (I., II., III...), negrito e caixa alta. Um "I." digitado no início do título é descartado, para não duplicar o número |
| `## TÍTULO` | Título da peça: centralizado, em negrito, sem número |
| `#### Título` ou parágrafo todo em `**negrito**` | Subtítulo em negrito, sem número |
| Parágrafo comum (separado por linha em branco) | Parágrafo justificado, Times New Roman 12,5 pt |
| Linhas seguidas sem linha em branco | Uma por parágrafo, sem espaço entre elas (bloco de assinatura) |
| `> texto` | Citação recuada, em itálico |
| Lista `1.` | Alíneas com numeração automática a), b), c), recomeçando em a) a cada lista; o último item termina em ponto final, mesmo que traga ";" |
| `- ` recuado logo abaixo de um item `1.` | Sub-item, mais recuado, dentro da mesma lista (o item seguinte continua a numeração). Se o texto já traz "a)" ou "**a)**", ele é mantido; senão entra com "– " |
| Lista `- ` solta | Alíneas a), b), c); se todos os itens já trazem "a)" digitado, só o recuo |
| Tabela `\|` | Quadro com bordas; a primeira linha é o cabeçalho, em negrito |
| `**negrito**`, `*itálico*`, `_itálico_` | Negrito, itálico |
| `<!-- centralizado -->` … `<!-- /centralizado -->` | Parágrafos centralizados (local e data) |

O timbre (`assets/timbre-servfaz.docx`) traz o cabeçalho e o rodapé com as imagens e a marca d'água, as margens A4, os estilos `Peca ...` e as numerações. Não traz texto de peça.

## Dados padrão da Servfaz e de quem assina

O script preenche sozinho estes campos do Markdown, com os valores de `assets/dados-servfaz.json`:

| No Markdown | Chave do JSON |
| :-- | :-- |
| `[Inserir CNPJ]` | `cnpj` |
| `[Inserir Endereço Completo]` (ou `[Inserir Endereço]`) | `endereco` |
| `[Inserir Nome]` (ou `[Inserir Representante]`) | `nome` |
| `[Inserir RG]` | `rg` |
| `[Inserir CPF]` | `cpf` |
| `[Data do Protocolo]` | não vem do JSON: se o analista informar a data, use `--data AAAA-MM-DD` (sai "20 de outubro de 2026") |

O arquivo tem dado de pessoa física (nome, RG e CPF de quem assina), por isso **não vai para o git**: está no `.gitignore`. O modelo, com valores fictícios, é `assets/dados-servfaz.exemplo.json`. Ao copiar a skill para outra conta ou máquina, copie o `dados-servfaz.json` junto; sem ele, nada é preenchido e todos os campos saem em branco no `.docx`. Não repita CPF, RG nem outro dado do arquivo na conversa. A skill só preenche o que o Markdown marca com `[Inserir ...]`; não acrescenta nome nem dado em lugar nenhum do texto. A data da peça é do analista: não escolha uma. Sem `--data`, o campo da data fica em branco no `.docx`, para o analista preencher.

## Campos em branco: preenchimento manual no .docx

Dado que falta **não barra a geração**. O que os dados padrão e o `--data` não cobrem (por exemplo `[Inserir Telefone]`, `[Data do Protocolo]` sem `--data`, ou `{{CAMPO}}`) vai ao `.docx` exatamente como está no texto, **em destaque amarelo**, e o script lista no fim da saída cada pendência com a linha do `.md`. O analista preenche à mão no Word e remove o destaque. Colchete de preenchimento é o que começa com inserir, preencher, informar, data, nome, cnpj, cpf ou endereço.

## Recusas

O script não grava o `.docx` e informa a linha de cada achado se o Markdown tiver:

- referência interna da triagem: ID de fonte (`EXT-`, `INT-`, `NOVA-`), marcador `[ID · status]` ou menção a "catálogo de fontes" ou aos arquivos do estudo. "Catálogo" sozinho não conta, porque um edital pode citar o Catálogo de Serviços;
- marcação que o conversor não trata: bloco de código, imagem, link `[texto](url)`, tag HTML, `~~riscado~~` e título de nível 5 ou 6.

Remissões numéricas como `[1]` não são recusadas: vão ao `.docx` exatamente como estão no texto. Se o analista não as quer na peça, ele pede para tirá-las e só então elas saem.

A correção vai no Markdown de origem, nunca no `.docx`. Dado do certame que falta não se completa por conta própria: deixe em branco no `.docx` e liste para o analista. Ajuste só de marcação (por exemplo, trocar `- a)` por lista) só com o pedido do analista, sem mudar nenhuma palavra do texto.

## Para quem mantém a skill

`scripts/criar_timbre.py --origem PECA.docx` gera `assets/timbre-servfaz.docx` a partir de uma peça .docx da Servfaz (a de referência é a da FMS): fica o cabeçalho, o rodapé, as margens e os estilos; o corpo e os metadados de autoria saem, e entram os estilos e as numerações que o `gerar_minuta.py` usa. Para mudar fonte, recuo ou espaçamento, altere o `criar_timbre.py` e gere o timbre de novo; não edite o .docx à mão. A skill em uso nunca roda esse script.

Testes: `python -m unittest discover -s scripts/tests`.
