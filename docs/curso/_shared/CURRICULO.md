# CURRÍCULO TRAVADO — tópicos por módulo (títulos dos 6 tópicos; o índice da trilha e o módulo usam ESTES títulos)

Tipo do módulo entre colchetes (vai no lado direito do Mapa da trilha). Pode ajustar a redação do título do tópico levemente, mas não a ordem nem o assunto.

## T1 Primeiros passos (emerald) — já definido em docs/curso/trilha1/index.html
- 1-1 [Fundamento] O que é um robô: sentir, pensar, agir · Robôs no mundo real em 2026 · O caminho do curso e como estudar por demanda · Microcontrolador x computador · O kit inicial peça por peça · Começar sem hardware: Wokwi e segurança
- 1-2 [Fundamento] Tensão, corrente e resistência · Lei de Ohm e o resistor do LED · Protoboard: como as trilhas se ligam · Multímetro: medir antes de ligar · Digital, analógico e lógica de 3,3 V · Divisor de tensão e resistor de pull-up
- 1-3 [Prática] Arduino IDE 2.x e o pacote esp32 3.x · Placa, porta e primeiro upload · setup, loop, variáveis e funções · Serial Monitor para depurar · Entradas: botão e leitura analógica · PWM na API 3.x: brilho e som
- 1-4 [Prática] Como um sensor "fala" com a placa · HC-SR04: distância por eco · Infravermelho: linha e obstáculo · Ruído e filtro de média · Sensores I2C: dois fios, vários sensores · Ler vários sensores sem travar
- 1-5 [Prática] Motor DC, servo ou passo: qual usar · Ponte H: TB6612FNG e DRV8833 · Velocidade e sentido com PWM · Servo no ESP32 com ESP32Servo · Baterias: NiMH, 18650, LiPo e BMS · Regulador, GND comum e ruído do motor
- 1-6 [Projeto] Planejar o rover no papel · Montar chassi e fiação · Testar cada parte isolada · Lógica de desvio com máquina de estados · Ajuste fino e problemas comuns · Próximos passos: linha, buzina e Wi-Fi

## T2 Robô autônomo (blue)
Kit extra: MPU-6050 ou ICM-20948 (IMU), 2 motores com encoder (N20 ou TT com disco), barra de 5 sensores IR (TCRT5000/QTR), módulo cartão microSD, opcional display OLED SSD1306.
- 2-1 [Prática] Wi-Fi: modo estação e ponto de acesso · Servidor web no ESP32 (página com botões) · WebSocket: controle sem atraso · BLE: controlar pelo app do celular · Segurança: senha, parada se perder conexão (watchdog de comando) · Joystick no navegador para o rover
- 2-2 [Fundamento] O que uma IMU mede (acelerômetro e giroscópio) · Ler a MPU-6050 por I2C · Ângulo com filtro complementar · Encoders: contar giros da roda · Odometria: de pulsos a posição (x, y, θ) · Erros que se acumulam e como conviver com eles
- 2-3 [Fundamento] Por que liga/desliga não basta · P, I e D explicados com o carro na pista · PID em código (loop de tempo fixo) · Sintonia passo a passo (Ziegler-Nichols simplificado e na mão) · Windup, saturação e filtro na derivada · Velocidade igual nas duas rodas com PID
- 2-4 [Prática] Por que delay() trava o robô · millis() e tarefas sem bloqueio · Máquina de estados de verdade · FreeRTOS no ESP32: tarefas e núcleos · Filas e semáforos: tarefas conversando · Organizar o código em arquivos e classes
- 2-5 [Prática] O que medir e com que frequência · Gráfico ao vivo pelo Serial Plotter · Gravar em cartão microSD (CSV) · MQTT: publicar telemetria na rede · Painel no navegador ou no Node-RED/Grafana · Analisar o log em Python (pandas + gráfico)
- 2-6 [Projeto] A pista e a barra de sensores · Calcular o erro da linha (média ponderada) · PID de direção somado à velocidade base · Calibração automática dos sensores · Ajuste por telemetria (antes/depois) · Desafios: curvas fechadas, cruzamentos, cronômetro

## T3 Visão e IA embarcada (purple)
Kit extra: Raspberry Pi 5 (4 ou 8 GB) + fonte oficial 27 W + cartão 32 GB+ + cooler ativo, Camera Module 3, opcional AI HAT+/AI HAT+ 2, opcional ESP32-S3 com câmera (ex.: XIAO ESP32-S3 Sense).
- 3-1 [Fundamento] Por que um computador no robô · Preparar o Pi 5 (Raspberry Pi Imager, OS 64-bit Trixie, SSH) · Terminal Linux essencial · Python com ambiente virtual · GPIO no Pi (gpiozero) e cuidados com 3,3 V · Energia e calor no Pi 5 dentro do robô
- 3-2 [Prática] Como o computador vê uma imagem (pixels, canais) · Camera Module 3 com picamera2 · OpenCV: cores, HSV e máscaras · Contornos e centro do objeto · Medir FPS e reduzir resolução · Transmitir o vídeo para o navegador
- 3-3 [Prática] O que é detecção de objetos · YOLO26 no Pi 5 com Ultralytics · Exportar para NCNN e medir velocidade · Acelerar com AI HAT+ (Hailo) · Treinar com suas próprias imagens (rotular, treinar no PC/Colab) · Limites: luz, distância, falsos positivos
- 3-4 [Fundamento] Por que IA dentro do microcontrolador · TinyML: modelo pequeno, quantizado em int8 · Edge Impulse: do dado ao sketch Arduino · TensorFlow Lite Micro / LiteRT no ESP32-S3 · Exemplo: reconhecer um gesto com a IMU · Exemplo: palavra-chave por voz ou pessoa na câmera
- 3-5 [Prática] Divisão de trabalho: Pi pensa, ESP32 age · UART entre Pi e ESP32 (níveis 3,3 V) · Protocolo simples de mensagens (linhas de texto ou JSON curto, checagem) · Lado ESP32: receber comandos com segurança · Lado Pi: Python com pyserial · Falhas: perda de link, reset, parada segura
- 3-6 [Projeto] O plano: câmera → detecção → erro → motores · Montagem do Pi + ESP32 no chassi · Seguir um objeto colorido (OpenCV) · Seguir uma pessoa ou objeto (YOLO26) · PID de giro e de distância · Testes, segurança e melhorias

## T4 ROS 2 e navegação (amber)
Kit extra: o robô da T3 + LiDAR 2D (RPLIDAR C1/A1 ou LD19), encoders da T2. Tudo pode ser feito primeiro só em simulação (PC com Ubuntu ou máquina virtual / Docker).
- 4-1 [Fundamento] O que é o ROS 2 e por que usar · Qual distro: Lyrical ou Jazzy · Instalar (Ubuntu, Docker ou Pi) · Nós, tópicos, mensagens · Serviços, ações e parâmetros · Seu primeiro nó em Python (rclpy) publicando e ouvindo
- 4-2 [Prática] Workspace, pacotes e colcon · URDF/xacro: descrever o robô · TF2: quadros de coordenadas · RViz2: ver o robô e os sensores · Gazebo (Harmonic/Jetty) e ros_gz · Dirigir o robô simulado com teleop
- 4-3 [Prática] O que é o micro-ROS · Instalar o micro-ROS Agent · ESP32 publicando dados (encoders, IMU) · ESP32 ouvindo /cmd_vel e girando os motores · Odometria do robô real no ROS 2 · Problemas comuns (Wi-Fi x serial, sincronizar tempo)
- 4-4 [Fundamento] O que um LiDAR enxerga (LaserScan) · Ligar o LiDAR no ROS 2 · SLAM explicado: mapa e posição ao mesmo tempo · slam_toolbox na simulação · Mapear sua casa ou sala de aula · Salvar e carregar mapas
- 4-5 [Prática] Nav2: a pilha de navegação · Localização com AMCL no mapa salvo · Mapas de custo e planejadores · Mandar o robô até um ponto (RViz e Python) · Recuperação quando o robô trava · Waypoints: uma ronda pela casa
- 4-6 [Projeto] Arquitetura do robô real com ROS 2 · Launch files que sobem tudo · Do simulado ao real: o que muda · Mapear o ambiente · Navegar entre cômodos · Checklist de segurança e próximos passos

## T5 IA moderna e braço robótico (teal)
Kit extra: braço SO-101 (par líder/seguidor, servos Feetech STS3215, peças impressas em 3D) + 1–2 câmeras USB; PC com GPU NVIDIA ou Colab para treinar; opcional Pi 5 + AI HAT+ 2 ou Jetson Orin Nano Super para rodar modelos locais.
- 5-1 [Fundamento] LLM, VLM e VLA: o que cada um faz no robô · Arquitetura segura: o modelo escolhe, o robô executa · Lista fechada de ações em JSON (function calling) · Rodar um modelo local (Ollama no Pi 5/PC) · VLM: "o que você vê?" pela câmera · Travas: limites, confirmação e parada de emergência
- 5-2 [Prática] Pipeline de voz: ouvir, entender, falar · Whisper local (faster-whisper / whisper.cpp) · Palavra de ativação e microfone no robô · Do texto ao comando (com o 5-1) · Piper: voz offline em português · Latência e privacidade
- 5-3 [Prática] O braço SO-101 e o projeto LeRobot · Montar, configurar IDs e calibrar servos · Instalar o LeRobot (Python) · Teleoperação líder/seguidor · Câmeras e espaço de trabalho · Segurança com braço em movimento
- 5-4 [Prática] Aprender por demonstração (imitação) · Gravar episódios com lerobot-record · Dataset no Hugging Face Hub · Treinar ACT com lerobot-train · Avaliar a política no braço real · SmolVLA e pi0: políticas com linguagem
- 5-5 [Fundamento] Por que simular antes · MuJoCo e o gêmeo do SO-101 · Isaac Sim/Isaac Lab: quando vale · Real2sim: foto da mesa vira cena · Sim2real: a distância entre simulado e real · Gerar dados sintéticos para treinar
- 5-6 [Projeto] O robô assistente: escopo e regras · Voz → plano (LLM) → ações · Ver e pegar um objeto (visão + braço) · Base móvel + braço: integração · Testes e métricas de sucesso · Apresentar, documentar e compartilhar

## T6 Para o professor (rose) — 1 módulo, 8 tópicos
- 6-1 [Fundamento] Como ministrar este curso: 1 Perfis de turma e percursos por demanda (escola, técnico, universidade, maker space, clube) · 2 Formatos: oficina de 1 dia, projeto bimestral, disciplina semestral, clube contínuo (sem carga horária fixa: blocos de encontro) · 3 Kits por grupo, orçamento e onde comprar (por trilha, com faixa de preço out/2026) · 4 Plano de encontro modelo (abertura, demonstração, mão na massa, desafio, registro) com exemplos para T1 e T3 · 5 Laboratório seguro (baterias LiPo, solda, ferramentas, braço robótico, regras da bancada) · 6 Avaliação por projeto: rubricas, diário de bordo, portfólio, apresentação · 7 Inclusão e diferenciação: simulação (Wokwi/Gazebo) para quem não tem kit, papéis no grupo, desafios extra · 8 Competições (OBR, FLL e outras), BNCC de Computação e comunidade; como usar a "Minha jornada" e o export/import para acompanhar alunos
