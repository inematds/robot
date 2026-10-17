# FATOS conferidos (17/10/2026) — use estes, não chute versões

Regra: se um fato NÃO está aqui, escreva sem número de versão e mande o aluno conferir no site oficial (link). Preço: só faixa aproximada com "out/2026" e "confira antes de comprar".

## ESP32 / Arduino
- Pacote "esp32" da Espressif para Arduino (arduino-esp32) **3.x** (base ESP-IDF 5). Migração 2.x → 3.0: https://docs.espressif.com/projects/arduino-esp32/en/latest/migration_guides/2.x_to_3.0.html
- PWM (LEDC) na 3.x: **`ledcAttach(pino, freq, resolucao_bits)`** (canal escolhido sozinho) e **`ledcWrite(pino, valor)`** (recebe o PINO). `ledcDetachPin` virou `ledcDetach(pino)`. **PROIBIDO** usar `ledcSetup` / `ledcAttachPin` (não compilam mais).
- Servo no ESP32: biblioteca **ESP32Servo** (Kevin Harrington / madhephaestus) ou LEDC direto a 50 Hz. `Servo.h` do AVR não serve.
- Arduino IDE 2.x. Simulador online sem hardware: **Wokwi** (wokwi.com) — ESP32, sensores, servos.
- Placas: ESP32 DevKit (WROOM-32) ainda comum; **ESP32-S3** (USB nativo, instruções vetoriais p/ IA, mais RAM/PSRAM) é a escolha p/ IA e câmera; ESP32-C3/C6 baratos (RISC-V). Placas novas costumam vir com **USB-C**.
- Ponte H: preferir **TB6612FNG** ou **DRV8833** (eficientes, 3,3 V lógicos) ao L298N (antigo, perde ~2 V em calor). Pode citar o L298N como "ainda vendido, mas ineficiente".
- Energia: servo/motor NUNCA pela bateria 9 V quadrada (pouca corrente). Usar 4×AA (NiMH) ou 2× 18650 com suporte/BMS; regulador buck p/ 5 V. GND comum entre tudo.

## Raspberry Pi
- **Raspberry Pi 5** (preferido; Pi 4 ainda serve p/ o básico). Sistema: **Raspberry Pi OS 64-bit (base Debian "Trixie")**.
- Câmera: Camera Module 3 (ou AI Camera com Sony IMX500). Biblioteca Python: **picamera2** (rpicam-apps p/ linha de comando; `raspistill` antigo NÃO existe mais).
- Acelerador: **AI HAT+** (Hailo-8/8L, 13/26 TOPS) e **AI HAT+ 2** (Hailo-10H, 40 TOPS INT4, 8 GB RAM, roda LLM/VLM pequenos). Só no Pi 5 (PCIe). O antigo "AI Kit" saiu de linha. Doc: https://www.raspberrypi.com/documentation/computers/ai.html — AI HAT+ 2 ≈ US$ 130 (varejo EUA, 2026).
- Python: usar ambiente virtual (`python3 -m venv`), o sistema bloqueia `pip install` global.

## Visão / IA
- **Ultralytics YOLO26** é o YOLO atual (sucessor do YOLO11; YOLOv5/v8 são antigos). No Pi 5, YOLO26n ≈ 128 ms/imagem em FP32 640 px; exportar p/ **NCNN** é o mais rápido em CPU ARM. Guia: https://docs.ultralytics.com/guides/raspberry-pi/
- `pip install ultralytics` ; `yolo export model=yolo26n.pt format=ncnn`.
- **LiteRT** = novo nome do TensorFlow Lite (Google, 2024). Em microcontrolador: **TensorFlow Lite Micro**; no ESP32 via componente **esp-tflite-micro** (ESP-IDF; exemplos hello_world, micro_speech, person_detection) e otimizações ESP-NN (S3). Alternativa sem código: **Edge Impulse** (gera biblioteca Arduino).
- MediaPipe (Google) p/ mãos/rosto/pose no Pi.
- **Jetson Orin Nano Super** dev kit: lançado a US$ 249 (dez/2024), **US$ 399 desde jul/2026** (NVIDIA subiu preços). Jetson Nano original: descontinuado. AGX Thor: topo (US$ 5.499). Citar como "opção mais forte que o Pi, mais cara".

## ROS 2
- **ROS 2 Lyrical Luth** — LTS lançada em 22/05/2026, suporte até maio/2031, Ubuntu **26.04**. **Jazzy Jalisco** — LTS anterior (Ubuntu 24.04, até 2029), ainda muito usada e com mais pacotes/tutoriais. Humble: fim em maio/2027 — não recomendar para começar. Doc: https://docs.ros.org/en/lyrical/
- Recomendar: "Jazzy se seu tutorial/robô pede; Lyrical para começar do zero hoje". Exemplos de comando funcionam igual nas duas (`source /opt/ros/<distro>/setup.bash`).
- Simulador: **Gazebo** (o "Gazebo Classic" acabou em jan/2025). Par oficial: Jazzy ↔ **Gazebo Harmonic**; Lyrical ↔ **Gazebo Jetty**. Pacote ponte: `ros_gz`.
- SLAM no ROS 2: **slam_toolbox** (padrão). GMapping é do ROS 1 — NÃO usar. Cartographer existe mas menos mantido.
- Navegação: **Nav2** (`nav2_bringup`). Modelo didático: TurtleBot 3/4 simulados.
- **micro-ROS** no ESP32: componente ESP-IDF `micro_ros_espidf_component` (Jazzy = 24.x, Kilted = 25.x, Lyrical = 26.x) ou biblioteca `micro_ros_arduino` (conferir branch da distro). Precisa do **micro-ROS Agent** rodando no PC/Pi.
- LiDAR barato: RPLIDAR A1/C1 (Slamtec), LD19/LD06 (LDRobot).

## IA moderna
- **LeRobot** (Hugging Face, open-source, PyTorch). Braço **SO-101** (impresso 3D, servos Feetech STS3215; par líder/seguidor p/ teleoperação). Comandos: `lerobot-record` (gravar demonstrações), `lerobot-rollout` (avaliar a política no robô — na 0.6.x o record não aceita mais política; versões antigas avaliavam pelo record), `lerobot-train --policy.type=act` (treinar). Políticas: **ACT** (pequena, treina rápido), **SmolVLA** (visão-linguagem-ação pequena, base `lerobot/smolvla_base`, extra `[smolvla]`), família **pi0 / pi0.5** (Physical Intelligence, mais pesadas). Flags mudam entre versões: SEMPRE "confira na doc atual: https://huggingface.co/docs/lerobot".
- **VLA** = modelo Visão-Linguagem-Ação: recebe imagem + instrução em texto, devolve movimento.
- **VLM/LLM** como planejador de alto nível: o modelo escolhe entre AÇÕES PERMITIDAS (lista fechada, JSON); o microcontrolador mantém limites e parada de emergência. Nunca dar controle direto de motor ao LLM. Rodar local: Ollama no Pi 5/Jetson (modelos pequenos) ou AI HAT+ 2.
- Voz local: **Whisper** (whisper.cpp / faster-whisper) p/ ouvir; **Piper** p/ falar (TTS offline).
- Simulação: **MuJoCo** (leve, aberto), **NVIDIA Isaac Sim/Isaac Lab** (pesado, GPU NVIDIA). Projetos INEMA relacionados (citar como "veja também"): robotica-so101 (gêmeo do SO-101 na simulação) https://inematds.github.io/robotica-so101/guia/ e robotica-real2sim (foto da mesa vira simulação que treina o robô) https://inematds.github.io/robotica-real2sim/guia/

## Educação (módulo do professor)
- Competições no Brasil: **OBR** (Olimpíada Brasileira de Robótica), **FIRST LEGO League**, Torneio Juvenil de Robótica, RoboCup Brasil/LARC. Não citar datas de edição.
- BNCC: computação na educação básica (norma CNE de 2022) — citar só "a BNCC de Computação", sem números de artigo.
- Segurança: LiPo (carregar em saco anti-chamas, nunca perfurar, nunca deixar carregando sozinho), ferro de solda (suporte, ventilação, óculos), corte com estilete.
