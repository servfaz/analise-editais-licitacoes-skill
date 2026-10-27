"""Pacote da máquina de estados da triagem; o ponto de entrada é scripts/estado.py.

Mapa regra → módulo:
  portões e fase derivada (fila, minuta em revisão, próxima ação, alertas, status) → fases.py
  caminhos fixos do estudo (MANIFEST.json) e dos modelos da peça (assets/, só modelo-<tipo>.<ext> não vazio e sem
    cópia de editor), sem opção na linha de comando → fases.py
  frases do analista em formato fixo (prosseguir, decidir, minuta, reabrir, peça, aceite): normalização, conferência,
    mensagens com o formato esperado e exemplo com os dados da triagem; nenhuma interpretação de texto livre
    → formatos.py
  gravação e trava (leitura de entrada, gravação atômica, .estado.lock, forma do estado.json) → persistencia.py
  integridade do estado.json (.estado.sha256, cópia .estado.gravado.json, recusa de gravar sobre edição à mão, pasta
    de formato 2 que não volta a ser "anterior ao controle") → persistencia.py
  invariantes do validar (formato 2: evento de cada decisão e frase gravada no formato do comando) → invariantes.py
  aceite de edição à mão (só campos descritivos alterados) → aceite.py
  registro.md → registro.py
  arquivos das minutas (sha256, histórico, restauração) → arquivos.py
  comandos: slug, iniciar, status, documentos, prosseguir, prazo, itens, decidir, reabrir → comandos.py;
  minuta → minutas.py; peca → peca.py; validar → invariantes.py; aceitar-edicao → aceite.py
  base (recusa, relógio, texto, listas, hash, datas, IDs, slug) → comum.py
"""
