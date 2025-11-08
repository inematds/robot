# Módulo 3.1: Introdução à Visão Computacional

## Bem-vindo ao Nível Expert: Dando Olhos aos Robôs

Você chegou ao nível final e mais emocionante do curso! Nos níveis anteriores, construímos robôs que podiam navegar usando sensores de toque e de proximidade. Agora, vamos dar um salto quântico e equipar nossos robôs com o sentido mais poderoso de todos: a **visão**. 

A **Visão Computacional** é um campo da Inteligência Artificial que treina computadores para interpretar e entender o mundo visual. Usando imagens digitais de câmeras e vídeos, os robôs podem identificar objetos, navegar em ambientes complexos e interagir com o mundo de uma forma muito mais humana.

![Ilustração de Visão Computacional](/home/ubuntu/curso_robotica/imagens/ilustracao_visao_computacional.png)
*Figura 1: Um robô usando visão computacional para identificar e categorizar objetos em seu ambiente.*

---

## Hardware para Visão Robótica

Para que um robô possa "ver", ele precisa de uma câmera. A escolha da câmera depende do poder de processamento disponível e da complexidade da tarefa.

### ESP32-CAM

O **ESP32-CAM** é uma placa de desenvolvimento incrivelmente barata e compacta que combina um microcontrolador ESP32-S com uma câmera (geralmente o modelo OV2640). É a porta de entrada perfeita para projetos de visão computacional em robótica.

-   **Vantagens**: Baixo custo, tamanho reduzido, baixo consumo de energia, Wi-Fi integrado para streaming de vídeo.
-   **Limitações**: Poder de processamento limitado, não é ideal para algoritmos de IA complexos diretamente na placa (embora possa executar modelos mais simples).

### Câmera para Raspberry Pi

O **Raspberry Pi** é um computador de placa única muito mais poderoso que o ESP32. Quando combinado com seu módulo de câmera oficial, ele se torna uma plataforma de visão computacional formidável, capaz de executar análises de vídeo em tempo real e rodar bibliotecas como o OpenCV com muito mais fluidez.

-   **Vantagens**: Alto poder de processamento, suporte completo a sistemas operacionais (Linux), grande comunidade e compatibilidade com frameworks de IA avançados.
-   **Limitações**: Maior custo, maior consumo de energia e tamanho maior em comparação com o ESP32-CAM.

![Robô com Câmera](/home/ubuntu/curso_robotica/imagens/raspberry_robot.jpg)
*Figura 2: Um robô mais avançado utilizando um Raspberry Pi e uma câmera para tarefas de visão computacional.*

---

## Conceitos Fundamentais de Visão Computacional

Uma imagem, para um computador, é apenas uma grande matriz de números. Cada número representa um **pixel** (o menor ponto de uma imagem). O trabalho da visão computacional é encontrar padrões significativos nesses números.

-   **Espaços de Cor**: A forma como a cor de um pixel é representada. O mais comum é o **RGB** (Vermelho, Verde, Azul). Para muitas tarefas de processamento, as imagens são convertidas para **escala de cinza (Grayscale)**, pois isso simplifica os cálculos (usando apenas um valor de intensidade por pixel em vez de três).
-   **Processamento de Imagem**: Antes de qualquer análise complexa, as imagens geralmente passam por um pré-processamento para realçar características importantes. Isso inclui técnicas como:
    -   **Thresholding (Limiarização)**: Converter uma imagem em escala de cinza para uma imagem puramente preta e branca, separando o objeto de interesse do fundo.
    -   **Filtros (Blur/Suavização)**: Reduzir o ruído e os detalhes irrelevantes da imagem.
    -   **Detecção de Bordas**: Identificar os contornos dos objetos na imagem.

### OpenCV: A Biblioteca Padrão

**OpenCV (Open Source Computer Vision Library)** é a biblioteca mais popular e poderosa para visão computacional. Ela fornece milhares de algoritmos otimizados para análise de imagem e vídeo em tempo real. É a ferramenta que usaremos para implementar a maioria das nossas funcionalidades de visão.

---

## Projeto Prático: "Olá, Mundo!" da Visão - Streaming de Vídeo com ESP32-CAM

Nosso primeiro projeto será configurar um ESP32-CAM para capturar vídeo e transmiti-lo (fazer *streaming*) via Wi-Fi para um navegador web. Este é o passo fundamental para qualquer projeto de visão remota.

**Materiais Necessários:**
- 1x Placa ESP32-CAM com câmera OV2640
- 1x Conversor FTDI (ou um Arduino UNO) para programar o ESP32-CAM, pois ele não tem uma porta USB nativa para programação.
- Fios Jumper

**Montagem para Programação:**

1.  **Conecte o Conversor FTDI ao ESP32-CAM**: 
    -   `5V` do FTDI -> `5V` do ESP32-CAM
    -   `GND` do FTDI -> `GND` do ESP32-CAM
    -   `TX` do FTDI -> `U0R` (RX) do ESP32-CAM
    -   `RX` do FTDI -> `U0T` (TX) do ESP32-CAM
2.  **Modo de Flash**: Para carregar o código, o pino **GPIO 0** deve ser conectado ao **GND**. Coloque um jumper entre `GPIO0` e `GND`.

**Código do Projeto:**

1.  **Configure o Arduino IDE**: Vá em `Arquivo > Exemplos > ESP32 > Camera` e abra o exemplo `CameraWebServer`.
2.  **Selecione o Modelo da Placa**: No código, descomente a linha `#define CAMERA_MODEL_AI_THINKER` (ou o modelo correspondente à sua placa).
3.  **Insira suas Credenciais de Wi-Fi**: Preencha os campos `ssid` e `password` com os dados da sua rede.
4.  **Carregue o Código**: Selecione a placa "AI Thinker ESP32-CAM" em `Ferramentas > Placa`. Compile e carregue o código.
5.  **Remova o Jumper**: Após o carregamento, **remova o jumper entre GPIO 0 e GND** e pressione o botão de reset na placa.

**Resultado Esperado:**

1.  Abra o Monitor Serial na velocidade `115200`.
2.  O ESP32-CAM se conectará à sua rede Wi-Fi e imprimirá o endereço de IP onde o servidor de vídeo está rodando.
3.  Digite esse endereço de IP no seu navegador web.
4.  Você verá uma página com várias configurações da câmera. Clique no botão **"Start Stream"**.

Pronto! Você estará vendo o vídeo ao vivo da sua câmera ESP32-CAM diretamente no seu navegador. Você agora tem um robô com um olho funcional. No próximo módulo, vamos ensinar esse olho a reconhecer objetos usando Inteligência Artificial.
