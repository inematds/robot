# Módulo 3.5: SLAM e Navegação Avançada

## Onde Estou? Para Onde Vou? O Santo Graal da Robótica Autônoma

Até agora, nossos robôs navegavam de forma reativa, seguindo uma linha ou evitando um obstáculo imediato. Eles não tinham memória de onde estiveram nem um mapa do ambiente. Para alcançar o nível mais alto de autonomia, um robô precisa responder a duas perguntas fundamentais: "Onde estou?" e "Como chego ao meu destino?". A tecnologia que resolve a primeira pergunta é o **SLAM**.

### SLAM: Mapeamento e Localização Simultâneos

**SLAM (Simultaneous Localization and Mapping)** é um dos problemas mais desafiadores e importantes da robótica. É um algoritmo computacional que permite a um robô, em um ambiente desconhecido, fazer duas coisas ao mesmo tempo:

1.  **Mapeamento (Mapping)**: Construir um mapa do ambiente ao seu redor.
2.  **Localização (Localization)**: Usar esse mapa para descobrir sua própria posição e orientação dentro dele.

É um problema de "ovo e galinha": para construir um mapa preciso, o robô precisa saber onde ele está. Mas para saber onde ele está, ele precisa de um mapa. O SLAM resolve esse ciclo de dependência usando técnicas estatísticas complexas (como Filtros de Kalman e Filtros de Partículas) para estimar simultaneamente tanto o mapa quanto a pose (posição e orientação) do robô.

![Ilustração de SLAM](/home/ubuntu/curso_robotica/imagens/slam_illustration.png)
*Figura 1: Visualização do processo de SLAM. O robô (centro) usa um sensor (como um LIDAR) para detectar pontos do ambiente (paredes) e, ao mesmo tempo, calcula sua trajetória e posição dentro do mapa que está construindo.*

---

## Hardware para SLAM: O Sensor LIDAR

Embora seja teoricamente possível fazer SLAM com uma câmera (Visual SLAM ou V-SLAM), o método mais comum e robusto usa um sensor **LIDAR (Light Detection and Ranging)**.

Um LIDAR funciona de forma semelhante a um radar, mas usa pulsos de luz laser em vez de ondas de rádio. Ele gira rapidamente (geralmente 360 graus) e mede a distância até os objetos em centenas ou milhares de pontos ao seu redor, criando uma "nuvem de pontos" 2D ou 3D do ambiente em tempo real. A precisão e a densidade de dados de um LIDAR são ideais para algoritmos de SLAM.

-   **RPLIDAR A1**: Um dos LIDARs 2D de baixo custo mais populares para hobbistas e pesquisadores. Ele fornece 360 graus de medições de distância, várias vezes por segundo, e é perfeito para mapear um andar de uma casa.

---

## ROS: O Sistema Operacional para Robôs

Implementar SLAM do zero é uma tarefa monumental. Felizmente, a comunidade de robótica tem uma ferramenta padrão para isso: **ROS (Robot Operating System)**.

ROS não é um sistema operacional no sentido tradicional (como Windows ou Linux), mas sim um **framework de software** ou um *middleware*. Ele fornece um conjunto de bibliotecas, ferramentas e convenções para ajudar a construir software de robô complexo de forma modular.

**Conceitos Chave do ROS:**

-   **Nós (Nodes)**: Um nó é um programa executável que realiza uma tarefa específica (ex: um nó para ler os dados do LIDAR, um nó para controlar os motores, um nó para executar o algoritmo de SLAM).
-   **Tópicos (Topics)**: Os nós se comunicam publicando e assinando mensagens em "tópicos". Por exemplo, o nó do LIDAR publica as leituras da nuvem de pontos em um tópico chamado `/scan`. O nó de SLAM assina esse tópico para receber os dados e construir o mapa.
-   **Mensagens (Messages)**: Estruturas de dados com um formato definido para a comunicação entre os nós (ex: a mensagem do tipo `sensor_msgs/LaserScan`).

O ROS já possui pacotes de SLAM incrivelmente poderosos e prontos para usar, como o **GMapping**, **Cartographer** e **Hector SLAM**. Nós podemos simplesmente configurar nosso robô para publicar os dados do LIDAR e a odometria (estimativa de movimento a partir dos motores) nos tópicos corretos, e o pacote de SLAM cuidará de todo o trabalho pesado de construir o mapa.

---

## Projeto Teórico: Arquitetura de um Robô com SLAM e ROS

Construir e configurar um robô com ROS e SLAM é um curso inteiro por si só. Portanto, este projeto será teórico, descrevendo a arquitetura e os passos necessários. A plataforma ideal para este projeto é um **Raspberry Pi 4** (devido à sua capacidade de processamento e portas USB) executando **Ubuntu com ROS**.

**Arquitetura do Robô:**

1.  **Base Móvel**: Um chassi com motores e encoders nas rodas. Os encoders são cruciais para fornecer a **odometria** – uma estimativa de quanto o robô se moveu com base na rotação das rodas.
2.  **Controlador de Baixo Nível (ESP32)**: Conectado ao Raspberry Pi via serial. Ele recebe comandos de velocidade (ex: `velocidade_linear, velocidade_angular`) do Pi e os traduz em sinais PWM para os motores. Ele também lê os encoders das rodas e publica os dados de odometria de volta para o Pi.
3.  **Sensor Principal (LIDAR)**: Conectado a uma porta USB do Raspberry Pi.
4.  **Cérebro Principal (Raspberry Pi)**: Executa o Ubuntu e o ROS.

**Fluxo de Trabalho no ROS:**

1.  **Nó do Driver do Robô**: Um nó Python ou C++ no Pi se comunica com o ESP32. Ele assina um tópico de comando de velocidade (chamado `/cmd_vel`) e envia os comandos recebidos para o ESP32. Ele também recebe os dados dos encoders do ESP32 e os publica como mensagens de odometria no tópico `/odom`.
2.  **Nó do Driver do LIDAR**: O ROS possui um nó pronto para o RPLIDAR que publica as varreduras do laser no tópico `/scan`.
3.  **Nó de SLAM (ex: GMapping)**: Este nó assina os tópicos `/scan` e `/odom`. Usando esses dois fluxos de informação, ele gera o mapa e o publica em um tópico chamado `/map`. Ele também calcula a pose mais provável do robô no mapa.
4.  **Nó de Navegação (Move Base)**: Uma vez que o mapa está pronto, podemos usar outro pacote do ROS, o `move_base`. Ele permite que você clique em um ponto no mapa (usando uma ferramenta de visualização chamada **RViz**), e o `move_base` planejará uma trajetória livre de obstáculos e publicará os comandos de velocidade necessários no tópico `/cmd_vel` para levar o robô até lá.

**Resultado:**

O resultado é um robô verdadeiramente autônomo. Você pode teleoperá-lo por um ambiente para que ele construa um mapa. Depois, você pode simplesmente dar a ele um objetivo no mapa, e ele navegará de forma inteligente até o destino, desviando de obstáculos que não estavam no mapa original. Este é o estado da arte em navegação de robôs móveis internos, usado em tudo, desde aspiradores de pó robóticos a robôs de armazém.

No próximo módulo, vamos explorar como o Machine Learning pode ser usado para ensinar um robô a aprender comportamentos em vez de programá-los explicitamente.
