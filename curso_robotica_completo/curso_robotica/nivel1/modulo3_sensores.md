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
