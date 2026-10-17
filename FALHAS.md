# FALHAS — robot

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-17 | `receptor-pi.ino` (3-5) não compilava: `RX2`/`TX2` são macros do core esp32 3.x; e pinos do motor (18/19) colidiam com TRIG/ECHO do rover | renomear p/ PINO_RX/PINO_TX, mapa de pinos canônico no canal + `scripts/compile-check.py` compila todo .ino antes do push | prompt |
