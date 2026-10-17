# Canal — robotica-v2 (só acrescentar; nunca reescrever)

Conhecimento do projeto que a compactação perde: fatos descobertos, aprendizados, glossário, armadilhas, onde estão as coisas.
Não é estado da tarefa (isso vai em state/plan/progress). Preencha cedo — o hook avisa na faixa 1 (~50% do contexto).

Formato: `- AAAA-MM-DD HH:MM · fato|aprendizado|glossário|armadilha · texto`


## 17/10/2026 — início
- Pages = workflow publicando `docs/` no branch `master`. Site antigo movido p/ docs/v1/ (git mv).
- Decisões do Nei: sem carga horária; v2; depois EN/ES; +1 módulo "como o professor ministra" (trilha 6, módulo 6-1, 8 tópicos).
- Mapa da trilha: lado direito = tipo (Fundamento/Prática/Projeto) no lugar da duração.
- Tokens DESIGN.md (#0c0c10/#16161e/#272730, Sora) vencem o MASTER/oscoach.
- Fatos conferidos em docs/curso/_shared/FATOS.md (ROS 2 Lyrical LTS 22/05/2026, Gazebo Jetty/Harmonic, YOLO26, AI HAT+ 2, Orin Nano Super US$ 399 jul/2026, ledcAttach/ledcWrite(pino)).
- i18n: scripts/localization.py → translate.py (Codex gpt-6-luna, lotes paralelos, checagem do esqueleto de código em <pre>) → render-locales.py. <code> inline não traduz.
- Validador: scripts/validate.py [pt|en|es].
- Armadilha: render-locales regrava o PT via BeautifulSoup (diff grande) — só rodar com PT final.
- Teste i18n (17/10): 788 segmentos EN da foundation traduzidos e cacheados em i18n/en.json; 1 lote falhou 3x por instabilidade e passou na reexecução (retries 3→4). Render EN ok (código idêntico, só comentários/strings).
- T6 pronta (index 351 l, 6-1 1026 l, 7 SVG). PENDENTE: alinhar faixas de preço por trilha citadas no 6-1 com os kits dos índices T2–T5. browser-check: PAGES separado por VÍRGULA.
- T4 4-4..4-6 prontos. PENDENTE: conferir coerência meu_robo (ament_python, urdf/meu_robo.urdf.xacro) e ESP32 publicando /odom + TF odom→base_link entre 4-2/4-3 e 4-6.
- T3 3-4..3-6 prontos. PENDENTE coerência: pinos TB6612 (3-5/3-6: 25/26/27/18/32/33, STBY 19; UART2 16/17) x pinos do rover 1-5/1-6 e 2-x; venv ~/robo-venv (3-1/3-5).
- 1-5/1-6 prontos. MAPA DE PINOS CANÔNICO (1-6): PWMA 25, AIN1 26, AIN2 27, PWMB 33, BIN1 32, BIN2 4, STBY 13, TRIG 18, ECHO 19 (divisor 1k/2k), servo 23, BOOT 0, I2C 21/22. CONFLITO: 3-5/3-6 usam 18/19 p/ motor/STBY → corrigir p/ o canônico; UART2 16/17 ok. Conferir 1-4, 2-x, 4-3 também. Ideia: compilar todos os sketches com arduino-cli + esp32 3.x no fim.
- 5-4..5-6 prontos e testados (MuJoCo, assistente --simular; flags LeRobot 0.6.1). FATOS: avaliação = lerobot-rollout. Conferir 5-3/índice T5 se citam lerobot-record p/ avaliar.
- 2-4..2-6 prontos. DECISÃO pinos: mapa por trilha, coerente dentro da trilha. T2 (2-6): PWMB 14, BIN1 16, BIN2 17 (IR no ADC1 36/39/34/35/32; SD 18/19/23). 2-1/2-3 usam PWMB 13/BIN1 33/BIN2 32 → alinhar ao 2-6 e explicar a mudança no índice T2/2-6.

## 17/10/2026 — fechamento (sessão robot-v2 retomada)
- armadilha · translate.py: o modelo às vezes devolve {"source": "<tradução>", "kind": ...} em vez de string → lote inteiro rejeitado. Corrigido (normaliza dict→source); 2.011 recuperados das rejeições sem nova chamada.
- armadilha · render-locales (BeautifulSoup) reordena atributos → validate.py com regex de ordem fixa acusava 114 falsos problemas. validate.py agora usa lookahead.
- fato · learn.js tinha ~55 mensagens PT (contador "0 de 36", Minha jornada, notas). Dicionário __INEMA_D en/es no topo + __INEMA_T('...') pelo lang do <html>. Script: scratchpad learn-i18n.py (idempotente pelo marcador __INEMA_T).
- armadilha · tradução de string Python em aspas simples com apóstrofo ("couldn't") quebra o código; o code_skeleton pega, mas aceitar à mão exige olhar.
- fato · T4: launch 4-6 agora sobe Node(meu_robo/odometria) e lê meu_robo_description/urdf/robo.urdf.xacro. T2: mapa único (PWMB 14, BIN1 16, BIN2 17, STBY 3V3) + tabela #pinos no índice.
