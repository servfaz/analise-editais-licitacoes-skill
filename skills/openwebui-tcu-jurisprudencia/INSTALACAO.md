# Instalação da Tool — Jurisprudência TCU Servfaz

Tool do Open WebUI que pesquisa a Pesquisa de Jurisprudência do TCU (`pesquisa.apps.tcu.gov.br`) para a skill `licitacoes-servfaz` fundamentar impugnações, esclarecimentos e recursos.

## O que a Tool expõe

| Função | Para que serve |
| --- | --- |
| `buscar_jurisprudencia_selecionada(tema, pagina)` | Primeiro passo: enunciados curados pelo TCU, cada um com o acórdão de origem |
| `buscar_sumulas_tcu(termo)` | Súmula por número ("254") ou por assunto, com vigência e fundamento |
| `buscar_acordaos_tcu(consulta, ano_minimo, colegiado, pagina)` | Busca livre de acórdãos (frases entre aspas funcionam melhor) |
| `obter_acordao_tcu(numero, ano, colegiado)` | Inteiro teor: sumário, deliberação, voto e trecho do relatório |

Nomes de advogados, interessados e quórum não são devolvidos ao modelo. Todo resultado traz o aviso de que é candidato e precisa de conferência do inteiro teor.

## Pré-requisitos

- Open WebUI `0.12.3` com acesso de saída a `https://pesquisa.apps.tcu.gov.br` a partir do contêiner.
- Conta com perfil **Admin**.
- Nenhuma dependência extra: a Tool usa só a biblioteca padrão do Python.

## Instalação

1. **Workspace > Tools > + (Create)**; ID sugerido: `jurisprudencia_tcu_servfaz`.
2. Cole todo o conteúdo de [tools/tcu_jurisprudencia.py](tools/tcu_jurisprudencia.py) e salve.
3. Abra as **Valves** (engrenagem) e revise:
   - `user_agent`: identificação honesta do cliente (nome, versão e contato). O firewall do TCU barra identificadores genéricos, como o padrão do `curl`; não disfarce a Tool de navegador.
   - `timeout_s` (20), `max_resultados` (10) e `max_chars_texto` (12000): ajuste se as respostas ficarem lentas ou longas demais para o modelo.
   - `base_url`: mantenha o padrão.
4. Em **Workspace > Models**, edite o preset de licitações (o que usa a skill `licitacoes-servfaz`):
   - marque a Tool em **Tools**;
   - em **Advanced Params**, deixe **Function Calling = Native**.
   Sem preset salvo, a Tool fica como opção por conversa (ícone de ferramentas no campo de mensagem).

## Teste rápido no chat

1. "Qual o texto da Súmula 254 do TCU?" → chama `buscar_sumulas_tcu` e traz a súmula vigente.
2. "Abra o Acórdão 2924/2026 do Plenário do TCU" → chama `obter_acordao_tcu`.
3. "Há jurisprudência do TCU sobre retenção de pagamento por irregularidade fiscal?" → começa por `buscar_jurisprudencia_selecionada` e cita o acórdão de origem.
4. Altere `base_url` para um endereço inválido e repita o teste 1: a resposta deve dizer que a consulta falhou (erro técnico), não que não há resultado. Volte a Valve ao padrão.

## Cuidados

- Uso moderado: não rode varreduras nem laços de consulta; um IP bloqueado afeta toda a rede da Servfaz.
- A consulta vai ao TCU: o modelo deve enviar só termos jurídicos, nunca dados do cliente ou do edital.
- A API é a que o portal usa, sem contrato de serviço publicado: pode mudar sem aviso. Se as respostas vierem como "formato inesperado", confira o esquema atual antes de ajustar o código.

## Testes do pacote

```bash
.venv/bin/python -m unittest discover -s skills/openwebui-tcu-jurisprudencia/tests
```
