# Módulo 3.8: Projeto Final Nível 3 - Robô Assistente com IA

## A Grande Final: Unindo Todas as Peças

Parabéns por chegar ao projeto final de toda a sua jornada na robótica! Este é o momento de sintetizar o conhecimento dos três níveis – os fundamentos da eletrônica, a navegação autônoma e a inteligência artificial – para construir o projeto mais ambicioso de todos: um **robô assistente autônomo**.

**O Conceito:**

Nosso objetivo é criar um robô móvel que possa navegar de forma autônoma em um ambiente doméstico, responder a comandos de voz e usar sua visão para encontrar e interagir com objetos ou pessoas. Ele será a culminação de tudo o que aprendemos, desde o controle de um simples LED até a implementação de redes neurais.

![Robô Assistente](/home/ubuntu/curso_robotica/imagens/assistant_robot.png)
*Figura 1: Concepção artística do nosso robô assistente final – um agente inteligente que combina mobilidade, visão e interação por voz.*

---

## Arquitetura do Sistema: O Cérebro Híbrido em Ação

Para este projeto, a arquitetura híbrida (Módulo 3.4) não é apenas uma opção, é uma necessidade. Dividiremos as tarefas entre um Raspberry Pi e um ESP32 para máxima eficiência.

**Componentes do Robô:**

-   **Cérebro de Alto Nível**: **Raspberry Pi 4** (ou superior).
    -   **Responsabilidades**: Executar o ROS, processamento de visão computacional (OpenCV), reconhecimento de objetos (modelo TensorFlow Lite/YOLO), reconhecimento de voz (Vosk), tomada de decisões e navegação de alto nível (SLAM/Move Base).
-   **Controlador de Baixo Nível**: **ESP32**.
    -   **Responsabilidades**: Controle preciso dos motores das rodas (com PID), leitura de encoders para odometria, leitura de sensores de baixo nível (IMU, sensores de linha), e controle de atuadores secundários (LEDs, garras, etc.).
-   **Sensores Principais**:
    -   **Câmera**: Conectada ao Raspberry Pi para visão.
    -   **LIDAR (Opcional, mas recomendado)**: Conectado ao Raspberry Pi para SLAM e navegação robusta.
    -   **Microfone USB**: Conectado ao Raspberry Pi para captura de áudio.
-   **Base Móvel**: Um chassi robusto com motores DC e **encoders** nas rodas.

**Fluxo de Dados e Controle:**

```mermaid
graph TD
    subgraph "Usuário"
        ComandoVoz["Ok Robô, encontre a bola vermelha"]
    end

    subgraph "Cérebro de Alto Nível (Raspberry Pi)"
        Microfone -->|Áudio| ReconhecimentoVoz[Nó de Reconhecimento de Voz (Vosk)]
        ReconhecimentoVoz -->|Texto do Comando| CerebroPrincipal[Nó Principal de Decisão]
        CerebroPrincipal -->|Meta: "bola vermelha"| Navegacao[Nó de Navegação (Move Base)]
        
        Camera -->|Stream de Vídeo| DetectorObjetos[Nó de Detecção de Objetos (YOLO)]
        DetectorObjetos -->|Posição do Objeto| CerebroPrincipal
        
        LIDAR -->|Scan| SLAM[Nó de SLAM]
        SLAM -->|Mapa| Navegacao
        
        Navegacao -->|Comandos de Velocidade<br/>(/cmd_vel)| ComunicacaoSerial[Nó de Comunicação Serial]
    end

    subgraph "Controlador de Baixo Nível (ESP32)"
        ComunicacaoSerial -->|Comandos via Serial| ESP32
        ESP32 -->|PWM| Motores
        Encoders -->|Leituras| ESP32
        ESP32 -->|Odometria via Serial| ComunicacaoSerial
    end

    ComandoVoz --> Microfone

    style CerebroPrincipal fill:#e74c3c,stroke:#c0392b,color:#fff
```
*Figura 2: A complexa, mas poderosa, arquitetura de software do nosso robô final, orquestrada pelo ROS.*

---

## Fases do Projeto

A construção deste robô é um projeto de integração em larga escala. Deve ser abordado em fases.

### Fase 1: Construção da Base e Controle de Baixo Nível

1.  **Montagem Física**: Construa o chassi, monte os motores com encoders, o sistema de bateria, o ESP32 e o Raspberry Pi.
2.  **Controlador do ESP32**: Programe o ESP32 para:
    -   Receber comandos de velocidade (velocidade linear e angular) via serial.
    -   Implementar um controle PID para manter a velocidade dos motores precisa.
    -   Ler os pulsos dos encoders.
    -   Calcular a odometria (quanto o robô se moveu) e enviá-la de volta para o Pi via serial.

### Fase 2: Configuração do ROS e Navegação Básica

1.  **Instalação**: Instale o Ubuntu e o ROS no Raspberry Pi.
2.  **Nó de Comunicação**: Crie o nó ROS no Pi que conversa com o ESP32, traduzindo mensagens do tópico `/cmd_vel` para comandos seriais e publicando os dados de odometria do ESP32 no tópico `/odom`.
3.  **Teleoperação**: Use um nó de teleoperação do ROS (`teleop_twist_keyboard`) para controlar o robô manualmente usando o teclado do seu computador. Isso confirma que toda a cadeia de controle (ROS -> Serial -> ESP32 -> Motores) está funcionando.

### Fase 3: Mapeamento e Navegação Autônoma (SLAM)

1.  **Integração do LIDAR**: Configure o driver do LIDAR no ROS para publicar os dados de varredura.
2.  **Executar o SLAM**: Lance um pacote de SLAM como o `gmapping`. Teleopere o robô pelo seu quarto ou casa para construir um mapa 2D do ambiente.
3.  **Salvar o Mapa**: Salve o mapa gerado.
4.  **Navegação (Move Base)**: Lance o pacote de navegação `move_base`, carregando o mapa salvo. Agora, usando a ferramenta RViz, você pode dar ao robô um destino no mapa, e ele navegará autonomamente até lá, desviando de obstáculos.

### Fase 4: Integração da IA (Visão e Voz)

1.  **Nó de Visão**: Crie um nó ROS que captura imagens da câmera e usa um modelo de detecção de objetos (como YOLOv5) para encontrar e publicar a localização de objetos de interesse (ex: "bola", "pessoa") em um tópico.
2.  **Nó de Voz**: Crie um nó que usa o microfone e o framework Vosk para ouvir continuamente. Quando ele transcreve um comando, ele o publica em um tópico de texto.
3.  **Nó de Decisão Principal**: Este é o cérebro que une tudo. Ele assina os tópicos de comando de voz e de detecção de objetos. Ele mantém o estado do robô (ex: "procurando", "indo até o objeto", "esperando comando").

**Exemplo de Lógica do Nó Principal:**
-   Ouve o tópico de voz. Recebe o comando: "encontre a bola".
-   Muda o estado para "procurando a bola".
-   Começa a girar lentamente no lugar, enquanto monitora o tópico de detecção de objetos.
-   O nó de visão publica: "Objeto 'bola' detectado na coordenada X, Y".
-   O nó principal recebe essa informação, para de girar e envia a coordenada (X, Y) como um novo objetivo para o nó de navegação `move_base`.
-   O `move_base` assume, planejando uma rota e movendo o robô até a bola.
-   Ao chegar, o nó principal pode usar a síntese de voz para anunciar: "Encontrei a bola".

---

## Conclusão da Sua Jornada

Construir este robô assistente é um projeto desafiador que pode levar semanas ou meses. No entanto, ao completá-lo, você terá dominado uma vasta gama de habilidades que definem a robótica moderna. Você terá construído um sistema complexo, integrado hardware e software, e implementado algoritmos de ponta em inteligência artificial.

O campo da robótica está em constante evolução. As ferramentas e técnicas que você aprendeu neste curso são a base sobre a qual as próximas gerações de robôs serão construídas. Continue explorando, continue aprendendo e, acima de tudo, continue construindo.

**Parabéns, Engenheiro(a) de Robótica!**
