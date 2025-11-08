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
