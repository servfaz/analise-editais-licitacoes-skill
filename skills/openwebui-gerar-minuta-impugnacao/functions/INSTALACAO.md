# Instalação da Action — Exportar Minuta de Impugnação Servfaz

## Pré-requisitos

- Open WebUI `0.12.3`, com `ENABLE_FUNCTIONS=true` (padrão).
- Uma conta com perfil **Admin**. A página **Admin Panel > Functions** não aparece para usuários comuns.
- O arquivo [gerar_minuta_impugnacao_action.py](gerar_minuta_impugnacao_action.py), gerado e versionado junto deste guia.
- A Skill [../SKILL.md](../SKILL.md) instalada e associada ao modelo que redigirá as minutas. A Action pode funcionar sem a Skill, mas a Skill instrui o modelo a entregar o bloco aprovado no formato esperado.

> **Segurança:** Functions executam código Python no servidor do Open WebUI. Revise o código antes de salvar e mantenha as permissões de criação/edição de Functions somente para administradores confiáveis.

## Instalação no Open WebUI

1. Entre no Open WebUI como administrador e abra **Admin Panel > Functions**.
2. Selecione **Create** e use, por exemplo, o ID `exportar_minuta_impugnacao_servfaz`.
3. Copie todo o conteúdo de [gerar_minuta_impugnacao_action.py](gerar_minuta_impugnacao_action.py) para o editor e clique em **Save**.
4. O Open WebUI reconhece automaticamente a classe `Action`; não é necessário escolher o tipo manualmente.
5. Ative a Function. Para disponibilizá-la, marque-a como **Global** ou associe-a especificamente ao modelo de impugnações.
6. Abra as **Valves** (ícone de engrenagem) e, se desejar, preencha somente os dados corporativos `CNPJ` e `ENDERECO`.

A Function declara `python-docx==1.1.2` no seu cabeçalho. Em uma instância de homologação com uma única réplica, o Open WebUI instala essa dependência automaticamente ao salvar ou carregar a Function, desde que `ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS=true`.

Para produção, especialmente com múltiplos workers ou réplicas, prefira instalar a dependência na imagem e desligar a instalação dinâmica:

```dockerfile
FROM ghcr.io/open-webui/open-webui:v0.12.3

RUN pip install --no-cache-dir python-docx==1.1.2
```

```env
ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS=False
```

## Configuração e acesso

- Conceda aos analistas acesso ao modelo que possui a Action habilitada; eles não precisam, e não devem, receber permissão para editar Functions.
- A Action só aparece como botão abaixo de uma resposta do assistente. Ela não é disparada por um comando de texto e não é chamada automaticamente pelo modelo.
- O botão pede confirmação antes de criar o arquivo. A peça não é assinada, protocolada ou enviada a terceiros.
- CNPJ e endereço podem ser preenchidos nas Valves. Nome, RG, CPF, local e data não são guardados nas Valves; marcadores não preenchidos permanecem em amarelo no Word para revisão humana.

## Teste de homologação

1. Inicie um chat usando o modelo ao qual a Skill e a Action foram associadas.
2. Solicite uma minuta fictícia. A resposta precisa conter **exatamente um** bloco delimitado assim:

   ```html
   <!-- minuta-servfaz:inicio -->
   ... minuta em Markdown revisada ...
   <!-- minuta-servfaz:fim -->
   ```

   Não inclua comentários HTML adicionais, texto antes/depois do bloco nem blocos de código com três crases.

3. Revise o texto e clique em **Exportar Minuta de Impugnação Servfaz**, abaixo da resposta.
4. Leia o hash mostrado na confirmação e confirme somente se ele corresponde à versão revisada.
5. O Open WebUI cria um arquivo como `minuta-impugnacao-<hash>.docx` e o anexa à mesma resposta. O cartão do arquivo aparece no início da resposta, acima do conteúdo da minuta; clique nele para abrir ou baixar.
6. Confirme no Word que o timbre foi preservado e que campos como `[Inserir CPF]` ficaram amarelos. Não use dados pessoais reais na homologação.

Teste também o cancelamento da confirmação e uma resposta sem o marcador inicial: nos dois casos, nenhum arquivo deve ser gerado.

## Atualização e diagnóstico

O arquivo instalado no Open WebUI é uma cópia. Após mudar o conversor canônico em `../../gerar-minuta-impugnacao/scripts/gerar_minuta.py` ou o timbre, gere novamente a Action antes de substituí-la no painel administrativo:

```sh
cd skills/openwebui-gerar-minuta-impugnacao
python3 build/montar_acao.py
```

Valide o pacote localmente no ambiente virtual de desenvolvimento:

```sh
python3 -m venv .venv-minuta
. .venv-minuta/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Problemas comuns:

| Sintoma | Verificação |
| --- | --- |
| O botão não aparece | A Function está ativa e Global ou vinculada ao modelo usado pelo analista. |
| Erro `ModuleNotFoundError: docx` | Instale `python-docx==1.1.2` na imagem/ambiente do Open WebUI ou habilite a instalação de requisitos do cabeçalho. |
| A Action recusa a exportação | A resposta não contém um único par dos marcadores `minuta-servfaz:inicio` e `minuta-servfaz:fim`. |
| A mensagem confirma a geração, mas o arquivo não está visível | Atualize a página e reabra a conversa; o arquivo é associado à resposta que originou a Action. |
| O arquivo abre, mas há campos amarelos | Isso é esperado para marcadores que exigem preenchimento e revisão manual. |
