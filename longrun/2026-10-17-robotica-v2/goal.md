# Goal — robot v2 (17/10/2026)

Refazer o curso "Robótica do Zero ao Expert" (inematds.github.io/robot) no formato-curso-v2, sem carga horária, conteúdo 2026, + módulo do professor (6-1), depois EN/ES. Publicar via git (master, Pages publica docs/), portal id 29.

## Pronto quando (comando → saída esperada)
1. `python3 scripts/validate.py pt` → `== 0 problema(s) [pt]` (38 páginas: landing + 6 índices + 31 módulos; tópicos = manifesto; ≥3 SVG/módulo; sem termos proibidos/horas)
2. `grep -rlE "ledcSetup|ledcAttachPin|gmapping|GMapping" docs/curso docs/index.html docs/en docs/es` → vazio
3. browser-check (HTTP local, 390 px e 1280 px) PT/EN/ES → 0 overflow, 0 erro JS, 0 recurso 404
4. `python3 scripts/validate.py en` e `es` → 0 problemas; mesma contagem de páginas
5. Sobras PT no EN/ES: varredura de textos longos idênticos ao PT → ≤ 1% dos segmentos
6. após push: HTTP 200 em /robot/, /robot/en/, /robot/es/, /robot/curso/trilha6/modulo-6-1.html
7. portal: entrada id 29 atualizada + EN/ES registrados, push feito

## Fora do escopo
Vídeo, capa nova paga, tradução de imagens raster (curso é SVG com texto).
