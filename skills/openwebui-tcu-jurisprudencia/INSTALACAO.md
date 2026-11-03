# Instalação da Tool — Fontes oficiais Servfaz

Tool do Open WebUI que consulta a Pesquisa de Jurisprudência do TCU (`pesquisa.apps.tcu.gov.br`) e o texto vigente da Lei 14.133/2021 no normas.leg.br (Congresso Nacional), para a skill `licitacoes-servfaz` fundamentar impugnações, esclarecimentos e recursos sem citar de memória.

## O que a Tool expõe

**Jurisprudência do TCU**

| Função | Para que serve |
| --- | --- |
| `buscar_jurisprudencia_selecionada(tema, pagina)` | Primeiro passo: enunciados curados pelo TCU, cada um com o acórdão de origem |
| `buscar_sumulas_tcu(termo)` | Súmula por número ("254") ou por assunto, com vigência e fundamento |
| `buscar_acordaos_tcu(consulta, ano_minimo, colegiado, pagina)` | Busca livre de acórdãos (frases entre aspas funcionam melhor) |
| `obter_acordao_tcu(numero, ano, colegiado)` | Inteiro teor: sumário, deliberação, voto e trecho do relatório |

**Lei 14.133/2021**

| Função | Para que serve |
| --- | --- |
| `buscar_na_lei(lei, termos)` | Acha os dispositivos sobre um assunto quando não se sabe o número do artigo (ex.: "conta vinculada" → art. 121, § 3º, III) |
| `obter_dispositivo_lei(lei, artigo, paragrafo, inciso, alinea)` | Texto vigente do artigo (inteiro, sem parágrafo) ou do parágrafo, inciso ou alínea, com a citação pronta, a localização e a fonte |

Nomes de advogados, interessados e quórum não são devolvidos ao modelo. Todo resultado traz o aviso de que é candidato (TCU) ou de que o texto não tem valor oficial (lei: o oficial é o publicado no DOU) e precisa ser lido por inteiro antes de citar.

### Como o texto da lei é montado

- A API do normas.leg.br devolve a lei inteira (cerca de 1,5 MB) com o histórico de versões de cada dispositivo. A Tool usa a versão mais recente que não está marcada como fora de vigor e anota a origem: veto derrubado, redação dada por outra lei, inclusão, decisão judicial, supressão de aplicabilidade.
- A lei fica em cache por `cache_horas`: só a primeira consulta depois desse prazo baixa a lei de novo (cerca de 1 s); a busca roda sobre a lei em cache.
- Só a Lei 14.133 está disponível: em 03/11/2026, a API trazia LC 123, CLT e Leis 8.666, 9.784 e 13.303 sem texto estruturado. Para essas, a Tool responde que a citação fica "a conferir".

## Pré-requisitos

- Open WebUI `0.12.3` com acesso de saída a `https://pesquisa.apps.tcu.gov.br` e `https://normas.leg.br` a partir do contêiner.
- Conta com perfil **Admin**.
- Nenhuma dependência extra: a Tool usa só a biblioteca padrão do Python.

## Instalação

1. **Workspace > Tools > + (Create)**; ID sugerido: `jurisprudencia_tcu_servfaz` (mantenha o ID se já estiver instalada, para não desligar a Tool dos presets).
2. Cole todo o conteúdo de [tools/tcu_jurisprudencia.py](tools/tcu_jurisprudencia.py) e salve.
3. Abra as **Valves** (engrenagem) e revise:
   - `user_agent`: identificação honesta do cliente (nome, versão e contato). O firewall do TCU barra identificadores genéricos, como o padrão do `curl`; não disfarce a Tool de navegador.
   - `timeout_s` (20), `max_resultados` (10) e `max_chars_texto` (12000): ajuste se as respostas ficarem lentas ou longas demais para o modelo. O art. 6º da Lei 14.133 passa de 12 mil caracteres e sai cortado, com orientação para pedir o inciso.
   - `cache_horas` (6): tempo que a lei fica em memória.
   - `base_url` e `normas_url`: mantenha o padrão.
4. Em **Workspace > Models**, edite o preset de licitações (o que usa a skill `licitacoes-servfaz`):
   - marque a Tool em **Tools**;
   - em **Advanced Params**, deixe **Function Calling = Native**.
   Sem preset salvo, a Tool fica como opção por conversa (ícone de ferramentas no campo de mensagem).

## Teste rápido no chat

1. "Qual o texto da Súmula 254 do TCU?" → chama `buscar_sumulas_tcu` e traz a súmula vigente.
2. "Abra o Acórdão 2924/2026 do Plenário do TCU" → chama `obter_acordao_tcu`.
3. "Há jurisprudência do TCU sobre retenção de pagamento por irregularidade fiscal?" → começa por `buscar_jurisprudencia_selecionada` e cita o acórdão de origem.
4. "Transcreva o art. 143 da Lei 14.133" → chama `obter_dispositivo_lei` e traz o texto literal.
5. "O que a Lei 14.133 diz sobre conta vinculada?" → chama `buscar_na_lei`, chega ao art. 121, § 3º, III, e abre o artigo antes de responder.
6. Altere `base_url` (ou `normas_url`) para um endereço inválido e repita o teste 1 (ou 4): a resposta deve dizer que a consulta falhou (erro técnico), não que não há resultado, e não deve transcrever de memória. Volte a Valve ao padrão.

## Cuidados

- Uso moderado: não rode varreduras nem laços de consulta; um IP bloqueado afeta toda a rede da Servfaz.
- As consultas vão ao TCU e ao normas.leg.br: o modelo deve enviar só termos jurídicos, nunca dados do cliente ou do edital.
- As duas APIs não têm contrato de serviço publicado: podem mudar sem aviso. Se as respostas vierem como "formato inesperado" ou "texto estruturado" ausente, confira o esquema atual antes de ajustar o código.
- O texto da lei vem do registro do Congresso, não do Planalto nem do DOU. Antes de protocolar, confira no Planalto os dispositivos citados na peça.

## Testes do pacote

```bash
.venv/bin/python -m unittest discover -s skills/openwebui-tcu-jurisprudencia/tests
```
