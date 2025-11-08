_# Módulo 1.2: Introdução ao Arduino e Programação

## O Que é Arduino?

No módulo anterior, montamos um circuito estático. Agora, vamos dar vida aos nossos projetos com o **Arduino**. O Arduino não é um único componente, mas uma **plataforma de prototipagem eletrônica de código aberto** que combina hardware e software para criar projetos interativos.

-   **Hardware**: Uma placa de microcontrolador que pode ser programada para ler entradas (como a luz em um sensor) e transformá-las em saídas (como acender um LED ou mover um motor).
-   **Software**: O Arduino IDE (Ambiente de Desenvolvimento Integrado), um programa de computador onde você escreve e envia o código para a placa.

Existem muitas placas na família Arduino, mas a mais icônica é o **Arduino UNO**. Para este curso, focaremos no **ESP32**, uma placa mais poderosa com Wi-Fi e Bluetooth integrados, mas que pode ser programada da mesma forma que um Arduino.

![Placa ESP32](/home/ubuntu/curso_robotica/imagens/esp32_board.jpg)
*Figura 1: Um ESP32 DevKit, uma placa poderosa e versátil que usaremos em nossos projetos.*

---

## Instalação do Arduino IDE e ESP32

Para programar o ESP32, usaremos o Arduino IDE. Siga estes passos para configurar seu ambiente:

1.  **Baixe e Instale o Arduino IDE**: Acesse o site oficial do [Arduino](https://www.arduino.cc/en/software) e baixe a versão mais recente para o seu sistema operacional.

2.  **Adicione o Suporte ao ESP32**:
    -   Abra o Arduino IDE, vá em `Arquivo > Preferências`.
    -   No campo "URLs de Gerenciadores de Placas Adicionais", cole o seguinte link:
        ```
        https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
        ```

3.  **Instale as Placas ESP32**:
    -   Vá em `Ferramentas > Placa > Gerenciador de Placas`.
    -   Pesquise por "esp32" e instale o pacote "esp32 by Espressif Systems".

4.  **Selecione a Placa e a Porta**:
    -   Conecte seu ESP32 ao computador via cabo USB.
    -   Em `Ferramentas > Placa`, navegue até "ESP32 Arduino" e selecione "ESP32 Dev Module".
    -   Em `Ferramentas > Porta`, selecione a porta serial correspondente ao seu ESP32 (ex: `COM3` no Windows ou `/dev/ttyUSB0` no Linux).

---

## Estrutura Básica de um Programa Arduino

Todo programa (chamado de *sketch*) para Arduino possui duas funções principais:

```cpp
void setup() {
  // Código de configuração, executado uma vez quando a placa liga ou é resetada.
}

void loop() {
  // Código principal, executado repetidamente em um loop infinito.
}
```

-   `setup()`: Usada para inicializar configurações, como definir se um pino será de entrada ou saída.
-   `loop()`: Onde a lógica principal do robô acontece. Ele lê sensores, toma decisões e controla atuadores, repetidamente.

### Variáveis e Tipos de Dados

Variáveis são "caixas" na memória onde guardamos informações. Cada variável tem um tipo:

-   `int`: para números inteiros (ex: `int idade = 30;`)
-   `float`: para números com casas decimais (ex: `float pi = 3.14;`)
-   `bool`: para valores verdadeiro ou falso (ex: `bool ledAceso = true;`)
-   `String`: para texto (ex: `String nome = "Robô";`)

### Entrada e Saída Digital

Os pinos de um microcontrolador podem ser configurados como **entrada** (para ler dados, como um botão) ou **saída** (para enviar sinais, como acender um LED).

-   `pinMode(pino, MODO)`: Configura um pino como `INPUT` ou `OUTPUT`.
-   `digitalWrite(pino, VALOR)`: Escreve um valor `HIGH` (ligado, 5V/3.3V) ou `LOW` (desligado, 0V) em um pino de saída.
-   `digitalRead(pino)`: Lê o valor de um pino de entrada, que será `HIGH` ou `LOW`.

---

## Projeto Prático: Semáforo com LEDs

Vamos criar um semáforo simples com três LEDs (vermelho, amarelo e verde) que acendem em sequência.

**Materiais Necessários:**
- 1x ESP32 DevKit
- 1x Protoboard
- 3x LEDs (1 vermelho, 1 amarelo, 1 verde)
- 3x Resistores de 220Ω
- Fios Jumper

**Montagem do Circuito:**

1.  Conecte o pino `GND` do ESP32 à linha de alimentação negativa (`-`) da protoboard.
2.  Conecte os LEDs na protoboard, cada um com seu resistor em série no terminal anodo (+).
3.  Conecte o catodo (-) de todos os LEDs à linha negativa (`-`) da protoboard.
4.  Conecte os resistores dos LEDs aos pinos do ESP32:
    -   LED Verde: **GPIO 25**
    -   LED Amarelo: **GPIO 26**
    -   LED Vermelho: **GPIO 27**

**Código do Projeto:**

Copie e cole este código no seu Arduino IDE, e clique no botão "Carregar" (seta para a direita).

```cpp
// Define os pinos para cada LED
const int pinoLedVerde = 25;
const int pinoLedAmarelo = 26;
const int pinoLedVermelho = 27;

void setup() {
  // Configura todos os pinos dos LEDs como saída
  pinMode(pinoLedVerde, OUTPUT);
  pinMode(pinoLedAmarelo, OUTPUT);
  pinMode(pinoLedVermelho, OUTPUT);
}

void loop() {
  // Sequência do semáforo

  // 1. Verde aceso por 5 segundos
  digitalWrite(pinoLedVerde, HIGH);
  delay(5000); // Espera 5000 milissegundos (5 segundos)
  digitalWrite(pinoLedVerde, LOW);

  // 2. Amarelo aceso por 2 segundos
  digitalWrite(pinoLedAmarelo, HIGH);
  delay(2000);
  digitalWrite(pinoLedAmarelo, LOW);

  // 3. Vermelho aceso por 5 segundos
  digitalWrite(pinoLedVermelho, HIGH);
  delay(5000);
  digitalWrite(pinoLedVermelho, LOW);
}
```

**Resultado Esperado:**

Após carregar o código, seu circuito se comportará como um semáforo, alternando entre os LEDs verde, amarelo e vermelho. A função `delay()` pausa o programa, permitindo que cada luz fique acesa por um tempo.

Você acaba de dar o primeiro passo na programação de hardware! No próximo módulo, aprenderemos a interagir com o mundo exterior usando sensores.
