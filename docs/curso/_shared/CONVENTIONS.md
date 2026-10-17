# CONVENTIONS — curso "Robótica do Zero ao Expert" v2 (courseId `robot`)

LEIA INTEIRO antes de construir qualquer página. Depois leia:
1. `~/.claude/skills/formato-curso-v2/SKILL.md` (erros críticos #1–#31) e as referências que ela manda (MASTER_COMPLETO, LEARN-LAYER, SVG-FUTURISTA, CHECKLIST_REVISAO).
2. `docs/curso/_shared/FATOS.md` — versões e fatos conferidos. Não invente versões.
3. A **foundation** (padrão-ouro, quando existir): `docs/index.html`, `docs/curso/trilha1/index.html`, `docs/curso/trilha1/modulo-1-1.html`. Copie a ESTRUTURA dela (head, nav, rodapé, scripts, componentes). Mesma cara em todas as páginas.

Molde técnico de referência (curso v2 já publicado, mesma camada de aprendizagem): `~/projetos/oscoach/` (index.html, curso/trilha1/*.html, curso/_shared/*). Use para ver como o markup `data-inema-*` funciona. NÃO copie o conteúdo nem as cores antigas dele.

## 0. Onde fica
- Tudo publicado fica em `~/projetos/robot/docs/` (GitHub Pages publica a pasta `docs/`). Landing = `docs/index.html`. Trilhas = `docs/curso/trilhaN/`. Assets = `docs/assets/learn.css` + `learn.js` (já copiados; não edite sem necessidade).
- `docs/v1/` = site antigo. Não mexa. Pode LER como fonte de conteúdo, junto com `~/projetos/robot/curso_robotica_completo/` (markdown antigo — conteúdo de 2025, desatualizado: use como base didática, corrija tudo pelo FATOS.md).

## 1. Decisões travadas pelo dono (Nei)
- **SEM carga horária.** O aluno aprende por demanda. Nunca escreva "X horas", "duração", "semanas", "180h", "40h". No lugar da duração, o lado direito dos cartões do Mapa da trilha (#12) mostra o **TIPO** do módulo: `Fundamento` · `Prática` · `Projeto` (mantém o `justify-between`). Na landing, os cartões de trilha mostram "6 módulos · o que você monta" em vez de horas.
- Landing deixa claro: **comece por onde precisar** (percursos sugeridos: "nunca mexi com eletrônica" → T1; "já sei Arduino" → T2/T3; "quero ROS" → T4; "quero IA e braço" → T5; "vou ensinar" → T6).
- Trilha 6 "Para o professor" tem **um único módulo** (6-1, 8 tópicos): como ministrar este curso.
- Conteúdo de 2026, atualizado (ver FATOS.md). Código ESP32 SEMPRE na API 3.x.

## 2. Tokens visuais (DESIGN.md INEMA vence o MASTER onde divergem)
- Fundo `#0c0c10`, superfície `#16161e`, borda `#272730`, texto `#e6e6e6`, secundário `#a8a8b3`. No `tailwind.config`: `dark: { 900:'#0c0c10', 800:'#16161e', 700:'#1c1c26', 600:'#272730' }`. Regra #15 (bordas suavizadas no dark) usa **`#272730`** (não `#374151`).
- Primária amarela `#FACC15` (logo, CTA, dica). No claro: amarelo NUNCA é letra (texto de acento `#a16207`/`#854d0e`; botão fundo `#FACC15` letra `#1a1206`).
- Fontes: títulos **Sora** (h1–h3, logo), corpo **Inter**, código **JetBrains Mono**. Google Fonts: `family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600`.
- Cores das trilhas: T1 emerald · T2 blue · T3 purple · T4 amber · T5 teal · T6 rose. SVG: cor da trilha primária + ciano `#38bdf8` secundária.
- Emoji só como ícone pequeno (logo, título de cartão). Nunca no meio do texto.
- Logo do nav: `🦾` + "Robótica" (Sora, text-yellow-400). Depois `|` INEMA.CLUB (sky) `-` PRO (`https://inema.pro`, `text-amber-700 dark:text-slate-300`).

## 3. Ordem do `<head>` (Erros #18/#28)
1. `<meta charset>` + viewport + `<meta name="inema-course" content="robot">` + `<html lang="pt-BR">`
2. Anti-FOUC (`_shared/head-antifouc.html`, só o `<script>`) — PRIMEIRO script.
3. Manifesto: `<script type="application/json" data-inema-manifest>` + conteúdo de `_shared/manifest.json` **verbatim** (idêntico em TODAS as páginas).
4. Tailwind CDN + `tailwind.config` (darkMode:'class', primary `#FACC15`, paleta dark acima, fontFamily sora/inter/mono).
5. Google Fonts (acima).
6. `<style>` CSS base + light mode completo (Sec. 1.5 do MASTER, 4 partes) + Parte 5 (bordas `#272730`) + `h1,h2,h3{font-family:Sora,...}`.
7. `<link rel="stylesheet" href="REL/assets/learn.css">`.

## 4. Fim do `<body>`
- Funções-núcleo v1 inline (`toggleTopic`, theme toggle, `openModal/closeModal`), depois `<script src="REL/assets/learn.js">` + `INEMA.init()` por último (módulo: `INEMA.init({ autoResume: true })`).
- REL: landing = `.` ; `curso/trilhaN/*` = `../..`.

## 5. Nav (idêntico em todas as páginas, #13)
Logo → INEMA.CLUB → PRO → 6 botões de trilha (rótulo curto em telas pequenas `T1`..`T6`; longo em `lg`: Primeiros passos · Autônomo · Visão e IA · ROS 2 · IA moderna · Professor) → Minha jornada → Aparência → tema. A foundation define o markup exato: copie de `docs/curso/trilha1/index.html` e só troque qual trilha está ativa. Em 390 px de largura NÃO pode haver rolagem horizontal.

## 6. `data-inema-*` (tokens NUMÉRICOS — ver oscoach CONVENTIONS §4)
- Módulo: `<main id="conteudo" data-inema-module="N-Y" data-inema-track="N">`.
- Cada tópico: `<section id="topico-T" data-inema-topic="modulo-N-Y#topico-T" style="scroll-margin-top:5rem">` com T = 1..K. **K = `topics` do manifesto** (6 em todos, 8 no 6-1). Script vai contar.
- Prosa anotável: `data-inema-block="mN-Y-tT-pP"`.
- Controles por tópico: marcar lido (`data-inema-read-toggle`, `aria-pressed`, 4 spans canônicos) e dúvida (`data-inema-doubt-toggle`). TOC: `<nav data-inema-toc>`. Medidores: `data-inema-meter="curso|trilha:N|modulo:N-Y"`.

## 7. Conteúdo de cada módulo (#14, #17, #29–#31)
- 500–800 linhas, 6 tópicos (o manifesto manda), com VARIEDADE: ≥2 grids ✓/✗ (faça/não faça), ≥1 timeline/passo-a-passo, ≥2 tip boxes, code box em todo módulo prático.
- **Visual-first:** cada conceito-chave ganha SVG inline (circuito, pinagem simplificada, fluxo, diagrama de blocos, gráfico PID, grafo de nós ROS…), cor da trilha + ciano, `role="img"` + `aria-label`, legenda que ENSINA. Mínimo 3 SVGs por módulo de conteúdo; animação só sob `prefers-reduced-motion`.
- **Copy-run:** código COMPLETO que compila/roda (sketch Arduino inteiro, script Python inteiro, comandos), com: objetivo · bloco copiável · como verificar (o que deve aparecer no Serial Monitor / tela). Partes variáveis como `<seu_wifi>`. Sugira testar no Wokwi quando der.
- **Fundamento define termos** na 1ª aparição ("Novo aqui?": tensão, PWM, GPIO, I2C, nó ROS, tópico, inferência…).
- Segurança onde couber (bateria, motor preso, braço robótico se mexendo).
- Voz: "você", verbo concreto, sem hype, sem "!!", sem "revolucionar". PT-BR.
- Cada módulo fecha com "Para ir além" (links oficiais) e botões Anterior/Próximo à esquerda (#1).

## 8. Índice de trilha
Hero SVG, "Mapa da trilha" (#12, lado direito = tipo), cards de módulo com tópicos expansíveis (#9, ≥6), "Ver Completo" (#10), anel de progresso da trilha, o que você monta nesta trilha, kit da trilha (lista de peças com faixa de preço aproximada "out/2026, confira").

## 9. Proibido (o validador procura)
`ledcSetup`, `ledcAttachPin`, `GMapping`/`gmapping`, `raspistill`, `YOLOv5`, `Jetson Nano` sem "Orin", `Gazebo Classic` como recomendação, `ROS2 Humble` como recomendação, "horas" de carga horária, `[TODO]`, `lorem`, colchetes de placeholder.

## 10. Antes de entregar
CHECKLIST_REVISAO (trilha ou módulo) + #18–#31. Conte `data-inema-topic` = manifesto. Abra por HTTP (`python3 -m http.server` na pasta `docs/`), nunca `file://`.

## 11. Decisões da foundation (17/10/2026)
Foundation pronta: `docs/index.html`, `docs/curso/trilha1/index.html`, `docs/curso/trilha1/modulo-1-1.html`, `_shared/nav.html`. **Copie o `<head>` inteiro (linhas 1–134 do `modulo-1-1.html`) e o nav literalmente**; só troque `<title>`, `<meta description>`, a trilha ativa do nav e o REL dos assets.

**Head**
- `<html lang="pt-BR" class="dark">` (lang PRIMEIRO — o validador procura essa string), `<meta name="inema-course" content="robot">` (name antes de content), `<script type="application/json" data-inema-manifest>` (type primeiro, sem `=""`).
- O anti-FOUC é a versão compacta do `modulo-1-1.html`; mantenha `localStorage.getItem('inema.prefs')` com aspas simples.
- O `<style>` é UM bloco idêntico em todas as páginas (já cobre as 6 cores de trilha no claro, partes 1–5). Não edite por trilha. Ele também: (a) sobrescreve os tokens do learn.css no escuro (`html.dark:not([data-theme]) { --bg:#0c0c10; --surface:#16161e; ... }`); (b) corrige um bug do learn.css em que o `::after` do anel cobria o "%" (`.inema-ring__value { z-index:1 }`); (c) escurece o trilho do anel no claro.
- Claro: texto de acento usa -700/-800 (emerald `#047857`, blue `#1d4ed8`, purple `#6d28d9`, amber `#92400e`, teal `#0f766e`, rose `#9f1239`); `text-neutral-500` vira `#6b7280`. Amarelo nunca é letra: `.text-yellow-400`/`.text-primary` viram `#854d0e`.
- Botão sólido da trilha: `bg-COR-700 hover:bg-COR-600 text-white` (o -600 com branco falha AA). CTA amarelo: classe `.btn-primary` (`#FACC15` + letra `#1a1206`).

**Nav (390 px)**
- Botões de trilha usam a classe `.nav-trail` (definida no `<style>`): ativo `nav-trail text-COR-400 bg-COR-500/10` + `aria-current="page"`; inativo `nav-trail text-neutral-400 hover:text-COR-400 hover:bg-COR-500/10`. Abaixo de `sm` somem "Robótica", INEMA.CLUB e PRO (continuam no rodapé); jornada/aparência viram ícones abaixo de `md`. Testado: 390 px sem rolagem.
- Comentário `<!-- i18n:seletor -->` antes do botão de tema (nav) e no rodapé da landing. Ainda sem links en/es.

**Índice de trilha**
- Cartão do Mapa: `<a class="group bg-dark-800 rounded-xl border border-dark-600 hover:border-COR-500/30 p-5 transition-all" href="#modulo-N-Y">` com `<div class="flex items-center justify-between mb-2"><span>N.Y</span><span class="text-xs text-neutral-500">Fundamento|Prática|Projeto</span></div>` + `<h3>emoji título</h3>` + subtítulo curto.
- Card de módulo: `<div class="module-card bg-dark-800 ..." id="modulo-N-Y" style="scroll-margin-top:5rem">` (a classe `module-card` é usada pelo `toggleTopic` para manter um tópico aberto por card). Header com tipo + anel `data-inema-meter="modulo:N-Y" style="--ring-size:2.4rem"`. Tópico: `<div class="topic-item"><button aria-controls="tNY-T" aria-expanded="false" ... onclick="toggleTopic(this)">` + painel `id="tNY-T"` com O que é / Por que aprender / Conceitos-chave. Rodapé do card: "Ver em Modal" + "Ver Completo" (`justify-start`).
- Modais: `<iframe data-src="modulo-N-Y.html">` (NÃO `src`); o `openModal` do índice copia `data-src` para `src` ao abrir. Evita carregar 6 módulos (e 404 dos que ainda não existem) no load. Copie o bloco de scripts do `trilha1/index.html`.
- Seções do índice: header (badge, h1, 4 stats sem horas, anel `trilha:N`) → hero SVG em `<figure class="fig">` + "Como ler" → "O que você monta" + dica → Mapa da trilha → Conteúdo detalhado → Kit da trilha (`id="kit"`, faixa total "out/2026, confira") → botões (início · começar pelo 1º módulo · próxima trilha).

**Módulo**
- Tópico: `<section class="mb-16" id="topico-T" data-inema-topic="modulo-N-Y#topico-T" style="scroll-margin-top:5rem">` → círculo numerado + `<h2>` com emoji → `<div class="ml-0 sm:ml-16">` → dúvida (1 linha) → prosa `data-inema-block="mN-Y-tT-pP"` → componentes → `<h3>Por que aprender</h3>` → `<h3>Conceitos-chave</h3>` (grid de 4) → marcar-lido (2 linhas, 4 spans canônicos).
- Figura: `<figure class="fig mb-3"><svg role="img" aria-label="..." class="w-full h-auto" viewBox="0 0 640 H">` + `<p class="text-xs text-neutral-400 mb-6 px-1"><strong class="text-COR-400">Como ler:</strong> ...</p>`. `.fig` é painel ESCURO nos dois temas (o neon continua legível no claro). viewBox com largura ≤ 720 e textos ≥ 14–15 px (em 390 px a escala é ~0,55). IDs internos do SVG prefixados por página (`m11-…`, `t1-…`, `ld-…`).
- Code box (sempre escuro, botão à esquerda, sem texto em JS — rótulos em 2 spans para i18n):
  `<div class="code-box mb-3"><div class="code-head"><button type="button" class="copy-btn" onclick="copyCode(this)"><span class="copy-label">Copiar</span><span class="copy-done">Copiado</span></button><span class="code-file">arquivo.ino</span></div><pre><code>...</code></pre></div>`. Realce opcional: `<span class="c">` comentário, `.k` palavra-chave, `.s` string. Escape `<` `>` como `&lt;` `&gt;`. `copyCode()` está no bloco de scripts do módulo. Antes do bloco: "**Objetivo:**"; depois: caixa "Como verificar".
- Tabelas sempre dentro de `<div class="overflow-x-auto mb-6 rounded-xl border border-dark-600">`.
- Fim: Resumo → "Para ir além" (links oficiais) → "Próximo módulo" → botões `flex flex-wrap justify-start gap-3` (largura natural, sem `flex-1`).
- Tamanho: o head + nav já ocupam ~180 linhas; para ficar em 600–800 escreva compacto (botões de dúvida/lido em 1–2 linhas, defs do SVG enxutas).

**Armadilhas do validador** (rodam no texto visível, INCLUSIVE dentro de `<pre>`): não escreva `ledcSetup`/`ledcAttachPin` nem como "evite" (diga "funções de PWM da API 2.x antiga"); nada de número colado em "h" (o ícone do sol do nav usa `2 h1` com espaço por isso); "Jetson Nano" só como "Jetson Orin Nano Super" ou seguido de "descontinuado".

**Verificação**: `python3 scripts/validate.py pt` e `BASE_URL=http://127.0.0.1:<porta> PAGES="…" node scripts/browser-check.cjs` (escuro/claro × 390/1280, overflow, erros de console, nº de tópicos/TOC, marcar-lido com % persistindo no reload e no índice, toggle de tema; `FIGS=1` salva cada figura/code box/tabela em 390 px para conferir legibilidade).
