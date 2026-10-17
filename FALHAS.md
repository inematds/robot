# FALHAS — robot

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-17 | Launch do 4-6 não subia o nó `odometria` do 4-3 (sem /odom no robô real) e lia `meu_robo.urdf.xacro`, que o 4-2 não cria; pinos da T2 divergiam entre 2-1/2-3 e 2-6 | Node odometria no launch + URDF do meu_robo_description; mapa de pinos único no índice T2. Agentes paralelos precisam de contrato de nomes/pinos no CONVENTIONS antes de escrever | prompt |
| 2026-10-17 | `receptor-pi.ino` (3-5) não compilava: `RX2`/`TX2` são macros do core esp32 3.x; e pinos do motor (18/19) colidiam com TRIG/ECHO do rover | renomear p/ PINO_RX/PINO_TX, mapa de pinos canônico no canal + `scripts/compile-check.py` compila todo .ino antes do push | prompt |
