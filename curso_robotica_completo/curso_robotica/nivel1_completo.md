# Módulo 1.1: Introdução à Robótica e Eletrônica Básica

## O Que é um Robô?

Bem-vindo ao início da sua jornada no fascinante mundo da robótica! Um **robô** é, em sua essência, uma máquina programável capaz de realizar uma série de ações de forma autônoma ou semi-autônoma. A palavra "robô" foi popularizada pelo escritor tcheco Karel Čapek em sua peça de 1920, "R.U.R." (Rossum's Universal Robots), derivando da palavra tcheca *robota*, que significa "trabalho forçado".

Os robôs modernos são compostos por três pilares fundamentais:

1.  **Mecânica**: O corpo físico do robô, incluindo seu chassi, rodas, braços e garras.
2.  **Eletrônica**: O sistema nervoso do robô, composto por sensores, atuadores e a unidade de controle (o "cérebro").
3.  **Programação**: A inteligência do robô, o conjunto de instruções que define seu comportamento.

Neste curso, exploraremos todos os três pilares, começando com os blocos de construção da eletrônica.

![Componentes Eletrônicos](/home/ubuntu/curso_robotica/imagens/componentes_eletronicos.png)
*Figura 1: Diversos componentes eletrônicos que formam a base da robótica.*

---

## Conceitos Fundamentais de Eletrônica

Para construir robôs, é crucial entender três conceitos básicos da eletricidade: Tensão, Corrente e Resistência.

| Conceito | Unidade | Analogia com Água |
| :--- | :--- | :--- |
| **Tensão (V)** | Volt (V) | A **pressão** da água em uma mangueira. É a "força" que impulsiona os elétrons. |
| **Corrente (I)** | Ampere (A) | O **fluxo** de água que passa pela mangueira. É a quantidade de elétrons em movimento. |
| **Resistência (R)** | Ohm (Ω) | Um **estreitamento** na mangueira que limita o fluxo de água. Controla a quantidade de corrente. |

A **Lei de Ohm** relaciona esses três conceitos: **V = I * R**. Esta é a lei mais fundamental da eletrônica e nos ajuda a calcular como os componentes se comportarão em um circuito.

---

## Componentes Eletrônicos Essenciais

Vamos conhecer alguns dos componentes mais comuns que você usará.

### Protoboard (Matriz de Contatos)

A protoboard é uma ferramenta que permite montar e testar circuitos eletrônicos sem a necessidade de solda. Suas conexões internas facilitam a prototipagem rápida.

![Protoboard](/home/ubuntu/curso_robotica/imagens/ilustracao_protoboard.png)
*Figura 2: Diagrama de uma protoboard mostrando as conexões internas das fileiras e colunas.*

-   **Linhas de Alimentação**: As colunas nas laterais (geralmente marcadas com `+` e `-`) são conectadas verticalmente. São usadas para distribuir a tensão (VCC) e o terra (GND) por todo o circuito.
-   **Área de Componentes**: As fileiras na área central são conectadas horizontalmente. Cada fileira é um nó elétrico, permitindo conectar os terminais dos componentes.

### LED (Diodo Emissor de Luz)

O LED é um componente que emite luz quando a corrente elétrica passa por ele. Ele é um **diodo**, o que significa que a corrente só pode fluir em uma direção. O terminal mais longo é o **anodo (+)** e o mais curto é o **catodo (-)**.

### Resistor

O resistor é um componente que limita a passagem de corrente. Ele é crucial para proteger componentes sensíveis, como os LEDs, de receberem corrente excessiva e queimarem. O valor de um resistor é medido em Ohms (Ω).

![Circuito de LED](/home/ubuntu/curso_robotica/imagens/led_circuit.png)
*Figura 3: Esquema de um circuito simples para acender um LED, mostrando a necessidade de um resistor para limitar a corrente.*

---

## Projeto Prático: Acendendo seu Primeiro LED

Vamos aplicar o que aprendemos montando um circuito físico simples. Este projeto não requer programação, apenas uma fonte de energia.

**Materiais Necessários:**
- 1x Protoboard
- 1x LED (qualquer cor)
- 1x Resistor de 220Ω a 330Ω
- Fios Jumper
- 1x Fonte de alimentação de 5V (pode ser um power bank ou a saída 5V de uma placa Arduino/ESP32)

**Passos da Montagem:**

1.  **Conecte a Alimentação**: Use fios jumper para conectar a saída de 5V da sua fonte à linha de alimentação positiva (`+`) da protoboard e o GND à linha negativa (`-`).
2.  **Posicione o LED**: Espete o LED na área central da protoboard, com cada terminal em uma fileira diferente.
3.  **Conecte o Resistor**: Conecte uma perna do resistor na mesma fileira do terminal **anodo (+)** do LED.
4.  **Feche o Circuito**:
    -   Use um fio para conectar a outra perna do resistor à linha de alimentação positiva (`+`).
    -   Use outro fio para conectar a fileira do terminal **catodo (-)** do LED à linha de alimentação negativa (`-`).

**Resultado Esperado:**

Ao ligar a fonte de alimentação, o LED deve acender! Se não acender, verifique as conexões, a polaridade do LED (anodo/catodo) e se a fonte está funcionando.

Parabéns! Você montou seu primeiro circuito eletrônico. No próximo módulo, aprenderemos a controlar componentes como este usando programação.
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
_# Módulo 1.3: Sensores Básicos

## O Que São Sensores?

Se os atuadores são as "mãos" de um robô, os **sensores** são seus "sentidos". Sensores são componentes eletrônicos que permitem a um robô perceber o ambiente ao seu redor. Eles convertem uma propriedade física (como luz, distância ou temperatura) em um sinal elétrico que o microcontrolador pode ler e interpretar.

Neste módulo, vamos explorar um dos sensores mais populares e úteis para robôs iniciantes: o sensor de distância ultrassônico.

---

## Sensor de Distância Ultrassônico (HC-SR04)

O HC-SR04 é um sensor que mede distâncias usando ondas sonoras de alta frequência (ultrassom), de forma semelhante a como um morcego ou um sonar de submarino funciona.

![Sensor Ultrassônico HC-SR04](/home/ubuntu/curso_robotica/imagens/hcsr04_sensor.jpg)
*Figura 1: O sensor ultrassônico HC-SR04, com seus dois transdutores (emissor e receptor).*

**Como Funciona:**
1.  O pino **Trig** (Trigger/Gatilho) recebe um pulso do microcontrolador.
2.  Em resposta, o sensor emite um breve pulso de som ultrassônico.
3.  O som viaja, bate em um objeto e retorna como um eco.
4.  O pino **Echo** (Eco) detecta o eco e envia um sinal de volta ao microcontrolador. A duração desse sinal é proporcional ao tempo que o som levou para ir e voltar.

Conhecendo a velocidade do som no ar (aproximadamente 343 metros por segundo), podemos calcular a distância até o objeto.

### Pinos do HC-SR04

![Pinagem do HC-SR04](/home/ubuntu/curso_robotica/imagens/hcsr04_pinout.png)
*Figura 2: Diagrama de pinagem do sensor HC-SR04.*

-   **VCC**: Alimentação de 5V.
-   **Trig**: Pino de entrada do gatilho.
-   **Echo**: Pino de saída do eco.
-   **GND**: Terra (0V).

**Atenção com o ESP32:** O ESP32 opera com 3.3V em seus pinos de GPIO. O pino Echo do HC-SR04 envia um sinal de 5V. Para conectar o Echo a um pino do ESP32 de forma segura, precisamos de um **divisor de tensão** para reduzir o sinal de 5V para aproximadamente 3.3V. Um divisor de tensão simples pode ser feito com dois resistores (ex: 1kΩ e 2kΩ).

---

## Projeto Prático: Sistema de Alarme de Distância

Vamos construir um "alarme de ré" que acende um LED e emite um som (usando o LED da própria placa) quando um objeto se aproxima demais do sensor.

**Materiais Necessários:**
- 1x ESP32 DevKit
- 1x Sensor Ultrassônico HC-SR04
- 1x Protoboard
- 1x Resistor de 1kΩ
- 1x Resistor de 2kΩ
- Fios Jumper

**Montagem do Circuito:**

![Esquema de Ligação do HC-SR04](/home/ubuntu/curso_robotica/imagens/hcsr04_wiring.jpg)
*Figura 3: Exemplo de como conectar o sensor HC-SR04 a uma placa Arduino. A lógica para o ESP32 é similar, mas requer o divisor de tensão.*

1.  Conecte os pinos `VCC` e `GND` do sensor às saídas `5V` e `GND` do ESP32, respectivamente.
2.  Conecte o pino `Trig` do sensor ao **GPIO 12** do ESP32.
3.  **Crie o Divisor de Tensão:**
    -   Conecte o pino `Echo` do sensor a um ponto na protoboard.
    -   Nesse mesmo ponto, conecte o resistor de 1kΩ.
    -   Conecte a outra ponta do resistor de 1kΩ ao **GPIO 13** do ESP32.
    -   No pino GPIO 13, conecte também o resistor de 2kΩ. A outra ponta do resistor de 2kΩ deve ser conectada ao `GND`.

**Código do Projeto:**

```cpp
// Define os pinos para o sensor ultrassônico
const int pinoTrig = 12;
const int pinoEcho = 13;

// Define o pino do LED embutido na placa (geralmente é o 2)
const int ledEmbutido = 2;

// Variáveis para armazenar a duração do pulso e a distância
long duracao;
int distanciaCm;

void setup() {
  Serial.begin(115200); // Inicia a comunicação serial para vermos os resultados
  pinMode(pinoTrig, OUTPUT);
  pinMode(pinoEcho, INPUT);
  pinMode(ledEmbutido, OUTPUT);
}

void loop() {
  // Limpa o pino Trig
  digitalWrite(pinoTrig, LOW);
  delayMicroseconds(2);

  // Envia um pulso de 10 microssegundos no pino Trig
  digitalWrite(pinoTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinoTrig, LOW);

  // Lê o tempo de retorno do pulso no pino Echo
  duracao = pulseIn(pinoEcho, HIGH);

  // Calcula a distância em centímetros
  // Velocidade do som (343 m/s) = 0.0343 cm/µs
  // A distância é o tempo / 2 (ida e volta) * velocidade
  distanciaCm = duracao * 0.0343 / 2;

  // Imprime a distância no Monitor Serial
  Serial.print("Distância: ");
  Serial.print(distanciaCm);
  Serial.println(" cm");

  // Lógica do alarme
  if (distanciaCm < 10) {
    // Se o objeto estiver a menos de 10 cm, acende o LED
    digitalWrite(ledEmbutido, HIGH);
  } else {
    // Caso contrário, apaga o LED
    digitalWrite(ledEmbutido, LOW);
  }

  delay(100); // Pequena pausa antes da próxima leitura
}
```

**Resultado Esperado:**

Abra o **Monitor Serial** (`Ferramentas > Monitor Serial`) com a velocidade de `115200`. Você verá as leituras de distância sendo impressas. Aproxime sua mão do sensor. Quando a distância for menor que 10 cm, o LED azul embutido na sua placa ESP32 deverá acender.

Você acabou de dar "olhos" ao seu projeto! No próximo módulo, vamos aprender a fazer nosso robô se mover usando servomotores.
_# Módulo 1.4: Atuadores - Servomotores

## O Que São Atuadores?

**Atuadores** são os componentes que permitem a um robô interagir fisicamente com o mundo. Eles convertem energia (geralmente elétrica) em movimento. Enquanto os sensores coletam informações, os atuadores executam as ações. Os motores são o tipo mais comum de atuador em robótica móvel.

Neste módulo, focaremos nos **servomotores**, que são essenciais para a robótica de precisão.

---

## Tipos de Servomotores

Um servomotor (ou simplesmente "servo") é um motor especial que permite o controle preciso de sua posição angular ou velocidade. Existem dois tipos principais que usaremos:

### 1. Servo Padrão (ex: SG90)

Este servo é projetado para girar para uma posição específica dentro de um alcance limitado, geralmente de 0 a 180 graus. Ele é ideal para aplicações que exigem controle de ângulo, como:

-   Braços robóticos
-   Timões de direção
-   Pernas de robôs
-   Controle de câmeras (pan/tilt)

### 2. Servo de Rotação Contínua (ex: FS90R)

Visualmente idêntico ao servo padrão, este tipo é modificado para girar continuamente em 360 graus, sem um limite de posição. Em vez de controlar o ângulo, controlamos a **velocidade e a direção** da rotação. É a escolha perfeita para as rodas de um robô móvel.

![Servo FS90R](/home/ubuntu/curso_robotica/imagens/fs90r_servo.jpg)
*Figura 1: O servo de rotação contínua FS90R, ideal para as rodas do nosso robô.*

---

## Como Controlar um Servo: PWM

Servos são controlados por um sinal de **PWM (Pulse Width Modulation)**, ou Modulação por Largura de Pulso. Em vez de um sinal digital simples (ligado/desligado), o PWM é um pulso que se repete em uma frequência constante (geralmente 50 Hz para servos), mas cuja **largura** (duração) pode ser variada.

![Diagrama de PWM](/home/ubuntu/curso_robotica/imagens/ilustracao_pwm.png)
*Figura 2: Um sinal PWM com diferentes larguras de pulso (duty cycles). É essa largura que o servo interpreta.*

-   **Para Servos Padrão (SG90)**:
    -   Um pulso de ~1000 µs (microssegundos) corresponde a 0 graus.
    -   Um pulso de ~1500 µs corresponde a 90 graus (centro).
    -   Um pulso de ~2000 µs corresponde a 180 graus.

-   **Para Servos de Rotação Contínua (FS90R)**:
    -   Um pulso de ~1300 µs corresponde à velocidade máxima em um sentido (ex: anti-horário).
    -   Um pulso de ~1500 µs corresponde a **parado**.
    -   Um pulso de ~1700 µs corresponde à velocidade máxima no outro sentido (ex: horário).

O ESP32 possui hardware dedicado (LEDC) para gerar sinais PWM precisos, o que o torna excelente para controlar múltiplos servos.

![Pinagem de um Servo](/home/ubuntu/curso_robotica/imagens/sg90_pinout.png)
*Figura 3: A pinagem típica de um servo, com fios para alimentação (VCC), terra (GND) e sinal (PWM).*

---

## Projeto Prático: Controlando um Servo de Rotação Contínua

Vamos testar um servo FS90R, fazendo-o girar para frente, para trás e parar, usando a biblioteca `ESP32Servo`.

**Materiais Necessários:**
- 1x ESP32 DevKit
- 1x Servo de Rotação Contínua FS90R
- 1x Protoboard
- Fios Jumper
- Fonte de alimentação externa de 5V (um power bank é ideal, pois o USB do computador pode não fornecer corrente suficiente)

**Montagem do Circuito:**

**Importante:** Nunca alimente servos diretamente dos pinos 5V/3.3V do microcontrolador enquanto ele estiver conectado ao USB do seu computador. Servos podem consumir muita corrente e danificar a porta USB ou o próprio computador. Use sempre uma fonte externa para os servos.

1.  **GND Comum**: Conecte o `GND` da sua fonte de 5V, o `GND` do ESP32 e o fio **marrom/preto** do servo todos juntos na linha negativa (`-`) da protoboard. Este é o passo mais importante.
2.  **Alimentação do Servo**: Conecte o fio **vermelho** do servo à saída de `5V` da sua fonte externa.
3.  **Alimentação do ESP32**: Conecte o pino `5V` do ESP32 à saída de `5V` da fonte externa.
4.  **Sinal de Controle**: Conecte o fio de sinal **amarelo/laranja** do servo ao **GPIO 18** do ESP32.

**Código do Projeto:**

Primeiro, instale a biblioteca `ESP32Servo`: vá em `Ferramentas > Gerenciar Bibliotecas`, procure por "ESP32Servo" e instale-a.

```cpp
#include <ESP32Servo.h>

// Cria um objeto Servo
Servo meuServo;

// Define o pino onde o servo está conectado
const int pinoServo = 18;

void setup() {
  // Associa o objeto Servo ao pino e define os parâmetros de PWM
  // (500 µs = pulso mínimo, 2500 µs = pulso máximo)
  meuServo.attach(pinoServo, 500, 2500);
}

void loop() {
  Serial.println("Girando para frente (velocidade máxima)");
  meuServo.writeMicroseconds(1300); // Valor para girar em um sentido
  delay(3000); // Gira por 3 segundos

  Serial.println("Parando");
  meuServo.writeMicroseconds(1500); // Valor para parar
  delay(3000); // Fica parado por 3 segundos

  Serial.println("Girando para trás (velocidade máxima)");
  meuServo.writeMicroseconds(1700); // Valor para girar no outro sentido
  delay(3000); // Gira por 3 segundos

  Serial.println("Parando");
  meuServo.writeMicroseconds(1500); // Valor para parar
  delay(3000); // Fica parado por 3 segundos
}
```

**Calibração:**

O valor exato para parar um servo de rotação contínua pode variar ligeiramente (ex: 1480, 1510). Se o seu servo não parar completamente com `1500`, ajuste este valor no código até encontrar o ponto de repouso perfeito.

**Resultado Esperado:**

O servo irá girar em um sentido por 3 segundos, parar por 3 segundos, girar no sentido oposto por 3 segundos e parar novamente, repetindo o ciclo. Você agora tem o conhecimento para dar movimento ao seu robô!

No próximo módulo, vamos juntar tudo o que aprendemos para construir nosso primeiro robô completo: o Rover de Papel!
# Módulo 1.5: Projeto Final Nível 1 - Robô Rover de Papel

## Chegou a Hora de Construir!

Parabéns por chegar ao projeto final do Nível 1! Neste módulo, vamos integrar tudo o que aprendemos sobre eletrônica, programação e atuadores para construir nosso primeiro robô funcional: um **Rover de Papel controlado por Wi-Fi**.

Este projeto é fantástico para iniciantes porque utiliza materiais simples e acessíveis (como papelão) para o chassi, combinado com a potência do ESP32 para criar uma interface de controle web que funciona em qualquer smartphone. Vamos colocar a mão na massa!

![Robô Rover](/home/ubuntu/curso_robotica/imagens/robot_rover_1.jpg)
*Figura 1: Exemplo de um robô rover similar ao que vamos construir, controlado por um aplicativo web.*

---

## 1. Materiais Necessários

| Quantidade | Componente | Descrição | Módulo Relacionado |
| :--- | :--- | :--- | :--- |
| 1x | **ESP32 DevKit** | O cérebro do nosso robô. | 1.2 |
| 2x | **Servo de Rotação Contínua FS90R** | Os motores que moverão as rodas. | 1.4 |
| 2x | **Rodas para Servo** | Podem ser compradas ou feitas de papelão. | 1.4 |
| 1x | **Rodízio ou Roda Boba** | Para dar um terceiro ponto de apoio. | 1.1 |
| 1x | **Power Bank 5V (≥ 2A)** | Fonte de alimentação para o robô. | 1.1 |
| 1x | **Protoboard Mini** | Para organizar as conexões. | 1.1 |
| - | **Fios Jumper Macho-Fêmea** | Para conectar os componentes. | 1.1 |
| - | **Papelão ou Cartolina Rígida** | Para construir o chassi. | - |
| - | **Ferramentas** | Fita dupla-face, cola quente, tesoura, régua. | - |

---

## 2. Montagem Mecânica: O Chassi

Vamos criar o corpo do nosso robô. A simplicidade é a chave aqui.

![Diagrama do Chassi](/home/ubuntu/curso_robotica/imagens/ilustracao_chassi_papel.png)
*Figura 2: Um gabarito técnico para o design do chassi, mostrando a posição dos servos e rodas.*

1.  **Corte o Chassi**: Desenhe e corte um retângulo de papelão com aproximadamente **15 cm de comprimento por 9 cm de largura**.
2.  **Fixe os Servos**: Prenda os dois servos FS90R nas laterais do chassi, um de cada lado. Os eixos dos servos devem ficar para fora. Você pode usar fita dupla-face forte ou cola quente.
3.  **Prepare as Rodas**: Se você não tiver rodas prontas, corte dois discos de papelão com cerca de 6-7 cm de diâmetro. Cole duas camadas de papelão para maior rigidez. Em seguida, parafuse o *horn* (acessório plástico) do servo no centro da roda.
4.  **Encaixe as Rodas**: Encaixe as rodas nos eixos dos servos.
5.  **Adicione o Rodízio**: Cole o rodízio na parte traseira e central do chassi. Isso servirá como o terceiro ponto de apoio, permitindo que o robô gire facilmente.

---

## 3. Ligações Elétricas: O Sistema Nervoso

Agora, vamos conectar os componentes eletrônicos. Preste muita atenção ao **GND comum**, que é essencial para o funcionamento do circuito.

![Diagrama de Arquitetura](/home/ubuntu/curso_robotica/imagens/diagrama_arquitetura_rover.png)
*Figura 3: A arquitetura do nosso robô, mostrando como a energia e os sinais fluem entre os componentes.*

1.  **Distribua a Alimentação**: Conecte a saída do Power Bank a uma protoboard mini. Isso facilitará a distribuição de 5V e GND.
2.  **Alimente o ESP32**: Conecte o pino **5V** do ESP32 na linha positiva da protoboard e o pino **GND** na linha negativa.
3.  **Alimente os Servos**: Conecte os fios **vermelhos** de AMBOS os servos na linha positiva (5V) e os fios **marrons/pretos** na linha negativa (GND).
4.  **Conecte os Sinais dos Servos**:
    -   Conecte o fio de sinal (amarelo/laranja) do **servo esquerdo** ao **GPIO 18** do ESP32.
    -   Conecte o fio de sinal do **servo direito** ao **GPIO 19** do ESP32.

![Esquema de Ligação](/home/ubuntu/curso_robotica/imagens/servo_wiring.jpg)
*Figura 4: Exemplo de ligação de um servo. Lembre-se de que o GND deve ser comum a todos os componentes.*

---

## 4. Programação: A Inteligência do Robô

Este código transformará seu ESP32 em um ponto de acesso Wi-Fi (Access Point). Ao se conectar a ele com seu celular, você poderá acessar uma página web com botões para controlar o robô.

Copie o código abaixo, cole no seu Arduino IDE e carregue-o para o ESP32.

```cpp
#include <WiFi.h>
#include <ESP32Servo.h>

// ===== Configuração do Wi-Fi AP =====
const char* ssid = "ROBO_PAPEL";
const char* password = "12345678";
WiFiServer server(80);

// ===== Configuração dos Servos =====
Servo servoEsquerdo;
Servo servoDireito;

const int pinoServoEsquerdo = 18;
const int pinoServoDireito = 19;

// ===== Calibração e Velocidade =====
// Ajuste estes valores se os servos não pararem completamente
int paradoEsquerdo = 1500;
int paradoDireito = 1500;
int velocidade = 200; // Quão rápido o robô se move (100-400)

// ===== Funções de Movimento =====
void parar() {
  servoEsquerdo.writeMicroseconds(paradoEsquerdo);
  servoDireito.writeMicroseconds(paradoDireito);
}

void frente() {
  servoEsquerdo.writeMicroseconds(paradoEsquerdo + velocidade);
  servoDireito.writeMicroseconds(paradoDireito - velocidade);
}

void tras() {
  servoEsquerdo.writeMicroseconds(paradoEsquerdo - velocidade);
  servoDireito.writeMicroseconds(paradoDireito + velocidade);
}

void esquerda() {
  servoEsquerdo.writeMicroseconds(paradoEsquerdo - velocidade);
  servoDireito.writeMicroseconds(paradoDireito - velocidade);
}

void direita() {
  servoEsquerdo.writeMicroseconds(paradoEsquerdo + velocidade);
  servoDireito.writeMicroseconds(paradoDireito + velocidade);
}

// ===== Página HTML de Controle =====
String html = "<!DOCTYPE html><html><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><style>" \
             "body{text-align:center; font-family:sans-serif;} button{font-size:24px; padding:20px; margin:10px;}" \
             ".dir{display:flex; justify-content:center;} #stop{background-color:red; color:white;}" \
             "</style></head><body><h1>Controle do Robô</h1>" \
             "<div class=\"dir\"><button onmousedown=\"fetch(\"/frente\")\" ontouchstart=\"fetch(\"/frente\")\">▲</button></div>" \
             "<div class=\"dir\"><button onmousedown=\"fetch(\"/esquerda\")\" ontouchstart=\"fetch(\"/esquerda\")\">◄</button>" \
             "<button id=\"stop\" onmousedown=\"fetch(\"/parar\")\" ontouchstart=\"fetch(\"/parar\")\">■</button>" \
             "<button onmousedown=\"fetch(\"/direita\")\" ontouchstart=\"fetch(\"/direita\")\">►</button></div>" \
             "<div class=\"dir\"><button onmousedown=\"fetch(\"/tras\")\" ontouchstart=\"fetch(\"/tras\")\">▼</button></div>" \
             "</body></html>";

void setup() {
  servoEsquerdo.attach(pinoServoEsquerdo);
  servoDireito.attach(pinoServoDireito);
  parar();

  WiFi.softAP(ssid, password);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String req = client.readStringUntil(\'\r\');
    if (req.indexOf("/frente") != -1) frente();
    else if (req.indexOf("/tras") != -1) tras();
    else if (req.indexOf("/esquerda") != -1) esquerda();
    else if (req.indexOf("/direita") != -1) direita();
    else if (req.indexOf("/parar") != -1) parar();
    
    client.print(html);
    delay(1);
  }
}
```

---

## 5. Teste e Calibração

1.  **Ligue o Robô**: Conecte o Power Bank.
2.  **Conecte-se ao Wi-Fi**: No seu celular, procure a rede Wi-Fi chamada `ROBO_PAPEL` e conecte-se a ela usando a senha `12345678`.
3.  **Acesse a Página de Controle**: Abra o navegador do seu celular e digite o endereço `192.168.4.1`.
4.  **Controle o Robô**: A página com os botões de controle deve aparecer. Teste cada um dos botões.

**Calibração Fina**: Se o robô se mover lentamente quando deveria estar parado, ajuste os valores das variáveis `paradoEsquerdo` e `paradoDireito` no código. Aumente ou diminua os valores em pequenos incrementos (ex: de 1500 para 1505, ou 1495) até que as rodas fiquem perfeitamente imóveis ao pressionar o botão de parar.

---

## Próximos Passos e Upgrades

Você construiu seu primeiro robô! Agora, as possibilidades são infinitas. Aqui estão algumas ideias para evoluir seu projeto, que serão a base para o Nível 2 do nosso curso:

-   **Adicione Sensores**: Integre o sensor ultrassônico (HC-SR04) do Módulo 1.3 para criar um modo autônomo que evita obstáculos.
-   **Melhore o Chassi**: Projete e imprima em 3D um chassi mais robusto e personalizado.
-   **Gestão de Energia**: Troque o power bank por uma bateria de Li-Ion com um circuito de gerenciamento para um robô mais compacto.
-   **Sensores de Linha**: Adicione sensores de infravermelho para que o robô possa seguir uma linha preta no chão.

**Parabéns por concluir o Nível 1! Você agora tem uma base sólida em robótica e está pronto para explorar os desafios mais avançados do Nível 2.**
