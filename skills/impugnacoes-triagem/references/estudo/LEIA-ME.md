<!-- Gerado por scripts/sync_estudo.py. Não edite aqui. -->

# Estudo de impugnação (cópia de referência)

Cópia do estudo de `briefing/Mapeamento_Analise`. Não edite estes arquivos: corrija a origem e rode `scripts/sync_estudo.py`. Os caminhos citados dentro dos arquivos são relativos a esta pasta.

| Pasta | Documento |
| :-- | :-- |
| `edital/` | Edital |
| `tr/` | Termo de Referência |
| `etp/` | Estudo Técnico Preliminar |
| `planilha/` | Planilha de Custos |
| `pesquisa/` | Pesquisa de Preços |
| `minuta/` | Minuta Contratual |

Cada pasta tem três arquivos:

- `estrutura.md`: as seções do documento, a finalidade de cada uma e a base legal. A numeração das seções é a chave usada nos mapas (por exemplo, `INT-TR (seção III)`).
- `analise.md`: onde o vício costuma se esconder, como cruzar com outros documentos e o fundamento.
- `fontes.md`: o mapa de fontes. Para cada seção: ponto a verificar, fontes internas (`INT-*` com a seção a abrir), fontes externas (IDs do catálogo), prova a extrair, "gera impugnação se" e "descarta se". Fecha com uma matriz resumo.

Na raiz:

- `catalogo-fontes.md`: fonte de verdade do nome, da esfera, de onde consultar e do status de cada ID.
- `indice-fontes.md`: resumo do catálogo (ID, nome abreviado, esfera, status, se pode ser citado).
- `MANIFEST.json`: hash da origem e da cópia, para saber que versão do estudo foi usada.

Regras de uso:

- Fontes externas são citadas pelo ID. Antes de citar em minuta, confira a linha completa no catálogo.
- `a conferir` nunca aparece como certo. `EXT-PEND-*` e as fontes marcadas "não usar" não são citados.
- Esfera `federal (União)`: o ente do edital pode ter regulamento próprio (`EXT-REG-ENTE`).
- A RERI (retificações, esclarecimentos e respostas) é um processo à parte, depois do lançamento do edital, e fica fora desta cópia. Para a triagem, os mapas foram ajustados: saíram a instrução "confira também `INT-RERI`", a coluna e a legenda `INT-RERI` das matrizes, o `INT-RERI` das fontes internas e as linhas cujo assunto é um ato da RERI. O que saiu de cada mapa está em `MANIFEST.json` (`escopo_triagem`). O catálogo continua inteiro.
