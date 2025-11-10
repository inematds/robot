# Módulo 1.8: Projeto Final - Robô Desviador de Obstáculos

## Bem-vindo ao Projeto Final do Nível 1!

Neste módulo culminante, você construirá um **robô desviador de obstáculos** - um robô móvel autônomo capaz de navegar em ambientes desconhecidos, detectando e evitando obstáculos em tempo real. Este é um dos projetos mais empolgantes da robótica, pois o robô precisa "pensar" e tomar decisões sozinho!

Robôs desviadores de obstáculos são usados em:

- **Aspiradores Robóticos**: Como o Roomba, que limpa casas autonomamente
- **Robôs de Exploração**: Rovers em Marte, robôs de resgate em áreas perigosas
- **Veículos Autônomos**: Carros que evitam colisões
- **Drones**: Para navegação em ambientes fechados

---

## O Que Você Vai Aprender

1. **Sensor Ultrassônico HC-SR04**: Medição precisa de distâncias
2. **Algoritmos de Navegação**: Como fazer o robô decidir para onde ir
3. **Servo Pan-Tilt**: Varredura do ambiente para melhor percepção
4. **Máquinas de Estado**: Organização de comportamentos complexos
5. **Navegação Autônoma em Labirintos**: Desafio final!

---

## Módulo 8.1: O Sensor Ultrassônico HC-SR04

### Revisão e Aprofundamento

Você já foi apresentado ao HC-SR04 no Módulo 3. Agora vamos dominar completamente este sensor e usá-lo para navegação real.

### Especificações Técnicas

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Parâmetro</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Valor</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Tensão de Operação</strong></td>
<td class="border border-gray-300 px-4 py-2">5V</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Corrente</strong></td>
<td class="border border-gray-300 px-4 py-2">15 mA</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Alcance</strong></td>
<td class="border border-gray-300 px-4 py-2">2 cm a 400 cm</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Precisão</strong></td>
<td class="border border-gray-300 px-4 py-2">±3 mm</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Ângulo de Medição</strong></td>
<td class="border border-gray-300 px-4 py-2">15° (cone)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Frequência do Ultrassom</strong></td>
<td class="border border-gray-300 px-4 py-2">40 kHz</td>
</tr>
</tbody>
</table>

### Código de Leitura Otimizado

Vamos criar uma função robusta para ler distâncias:

```cpp
const int TRIG_PIN = 26;
const int ECHO_PIN = 25;

// Constantes físicas
const float VELOCIDADE_SOM = 0.0343; // cm/µs (343 m/s = 0.0343 cm/µs)

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

float lerDistanciaUltrassonico() {
  // Garante que o pino TRIG está LOW
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Envia pulso de 10µs
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Lê o tempo do pulso de eco
  // Timeout de 30ms (equivale a aproximadamente 5m)
  long duracao = pulseIn(ECHO_PIN, HIGH, 30000);

  // Se timeout, retorna valor indicando erro
  if (duracao == 0) {
    return -1; // Nada detectado ou fora de alcance
  }

  // Calcula distância em cm
  // Distância = (Tempo * Velocidade do Som) / 2
  // Dividimos por 2 porque o som vai e volta
  float distancia = (duracao * VELOCIDADE_SOM) / 2.0;

  return distancia;
}

void loop() {
  float dist = lerDistanciaUltrassonico();

  if (dist > 0) {
    Serial.print("Distância: ");
    Serial.print(dist);
    Serial.println(" cm");
  } else {
    Serial.println("Erro na leitura ou sem obstáculo detectável");
  }

  delay(100); // Aguarda 100ms entre leituras
}
```

### Lidando com Leituras Ruidosas

Sensores ultrassônicos podem ter leituras instáveis. Vamos implementar um filtro de média móvel:

```cpp
const int NUM_LEITURAS = 5;
float leituras[NUM_LEITURAS];
int indiceLeitura = 0;

float lerDistanciaFiltrada() {
  // Faz uma nova leitura
  float novaLeitura = lerDistanciaUltrassonico();

  // Armazena no array circular
  leituras[indiceLeitura] = novaLeitura;
  indiceLeitura = (indiceLeitura + 1) % NUM_LEITURAS;

  // Calcula a média (ignorando valores inválidos)
  float soma = 0;
  int contadorValidos = 0;

  for (int i = 0; i < NUM_LEITURAS; i++) {
    if (leituras[i] > 0) { // Ignora leituras com erro
      soma += leituras[i];
      contadorValidos++;
    }
  }

  if (contadorValidos > 0) {
    return soma / contadorValidos;
  } else {
    return -1; // Todas as leituras inválidas
  }
}
```

---

## Módulo 8.2: Algoritmo de Navegação Básico

### Máquina de Estados Finitos

Vamos organizar o comportamento do robô usando uma **Máquina de Estados Finitos (FSM - Finite State Machine)**. Este é um padrão de design fundamental em robótica.

**Estados do Robô:**

```
┌─────────────┐
│   AVANÇAR   │ ← Estado inicial
└──────┬──────┘
       │ Obstáculo detectado
       ↓
┌─────────────┐
│    PARAR    │
└──────┬──────┘
       │ Avalia situação
       ↓
┌─────────────┐
│   DECIDIR   │ ← Verifica direita/esquerda
└──────┬──────┘
       │ Escolhe direção
       ↓
┌─────────────┐
│    GIRAR    │
└──────┬──────┘
       │ Giro completo
       ↓
   (volta para AVANÇAR)
```

### Lista de Materiais

Use os mesmos componentes do Módulo 7 (seguidor de linha), mas:

**Substitua:**
- Módulo de 5 sensores IR → 1x Sensor Ultrassônico HC-SR04

**Adicione (Opcional):**
- 1x Servo Motor SG90 (para pan-tilt do sensor)
- 1x Suporte para servo (pode ser feito com papelão)

---

## Módulo 8.3: Montagem do Robô

### Configuração 1: Sensor Fixo (Simples)

O sensor ultrassônico fica fixo apontando para frente.

**Posicionamento:**
- Altura: 5-10 cm do chão
- Ângulo: Ligeiramente inclinado para baixo (10-15°)
- Posição: Centro da frente do chassi

**Conexões:**
- HC-SR04 VCC → ESP32 5V
- HC-SR04 GND → ESP32 GND
- HC-SR04 TRIG → GPIO 26
- HC-SR04 ECHO → GPIO 25

### Configuração 2: Sensor com Pan-Tilt (Avançado)

O sensor pode girar para "olhar" para os lados.

**Montagem:**
1. Fixe o servo SG90 na parte frontal do chassi
2. Crie um suporte pequeno para o HC-SR04
3. Cole o HC-SR04 no "horn" do servo
4. Ajuste para que o servo possa girar de 0° a 180°

**Conexões Adicionais:**
- Servo Sinal → GPIO 13
- Servo VCC → 5V
- Servo GND → GND

---

## Módulo 8.4: Código - Versão Básica (Sensor Fixo)

```cpp
// ===== Pinos dos Motores =====
const int MOTOR_ESQ_IN1 = 18;
const int MOTOR_ESQ_IN2 = 19;
const int MOTOR_ESQ_EN = 21;

const int MOTOR_DIR_IN3 = 22;
const int MOTOR_DIR_IN4 = 23;
const int MOTOR_DIR_EN = 12;

// ===== Pinos do Sensor Ultrassônico =====
const int TRIG_PIN = 26;
const int ECHO_PIN = 25;

// ===== Configurações PWM =====
const int PWM_FREQ = 1000;
const int PWM_RESOLUTION = 8;
const int PWM_CHANNEL_ESQ = 0;
const int PWM_CHANNEL_DIR = 1;

// ===== Parâmetros de Navegação =====
const int DISTANCIA_SEGURA = 30;        // cm - distância mínima antes de desviar
const int VELOCIDADE_NORMAL = 180;      // Velocidade de cruzeiro
const int VELOCIDADE_LENTA = 120;       // Velocidade ao se aproximar de obstáculos
const int TEMPO_GIRO_90_GRAUS = 500;    // ms - ajuste conforme seu robô

// ===== Estados da Máquina de Estados =====
enum Estado {
  AVANCAR,
  PARAR,
  GIRAR_DIREITA,
  GIRAR_ESQUERDA,
  RE
};

Estado estadoAtual = AVANCAR;

void setup() {
  Serial.begin(115200);
  Serial.println("=== Robô Desviador de Obstáculos ===");

  // Configura motores
  pinMode(MOTOR_ESQ_IN1, OUTPUT);
  pinMode(MOTOR_ESQ_IN2, OUTPUT);
  pinMode(MOTOR_DIR_IN3, OUTPUT);
  pinMode(MOTOR_DIR_IN4, OUTPUT);

  ledcSetup(PWM_CHANNEL_ESQ, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_DIR, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(MOTOR_ESQ_EN, PWM_CHANNEL_ESQ);
  ledcAttachPin(MOTOR_DIR_EN, PWM_CHANNEL_DIR);

  // Configura sensor
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.println("Robô pronto!");
  delay(2000);
}

void loop() {
  // Lê a distância
  float distancia = lerDistancia();

  // Exibe no Serial Monitor
  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print(" cm | Estado: ");

  // ===== MÁQUINA DE ESTADOS =====
  switch(estadoAtual) {

    case AVANCAR:
      Serial.println("AVANÇAR");

      if (distancia > 0 && distancia < DISTANCIA_SEGURA) {
        // Obstáculo próximo - parar e decidir
        estadoAtual = PARAR;
      } else if (distancia > DISTANCIA_SEGURA && distancia < DISTANCIA_SEGURA * 2) {
        // Obstáculo à distância média - reduzir velocidade
        frente(VELOCIDADE_LENTA);
      } else {
        // Caminho livre - velocidade normal
        frente(VELOCIDADE_NORMAL);
      }
      break;

    case PARAR:
      Serial.println("PARAR");
      parar();
      delay(300);

      // Decide para qual lado girar (aleatório nesta versão simples)
      if (random(0, 2) == 0) {
        estadoAtual = GIRAR_DIREITA;
      } else {
        estadoAtual = GIRAR_ESQUERDA;
      }
      break;

    case GIRAR_DIREITA:
      Serial.println("GIRAR DIREITA");
      girarDireita(200);
      delay(TEMPO_GIRO_90_GRAUS);
      estadoAtual = AVANCAR;
      break;

    case GIRAR_ESQUERDA:
      Serial.println("GIRAR ESQUERDA");
      girarEsquerda(200);
      delay(TEMPO_GIRO_90_GRAUS);
      estadoAtual = AVANCAR;
      break;

    case RE:
      Serial.println("RÉ");
      tras(180);
      delay(500);
      estadoAtual = GIRAR_DIREITA; // Depois de dar ré, gira
      break;
  }

  delay(50); // Pequeno delay para estabilidade
}

// ===== FUNÇÃO DE LEITURA DO SENSOR =====
float lerDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duracao == 0) {
    return 400; // Retorna valor alto se não detectar nada
  }

  float distancia = (duracao * 0.0343) / 2.0;
  return distancia;
}

// ===== FUNÇÕES DE MOVIMENTO =====
void frente(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void tras(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarDireita(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarEsquerda(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void parar() {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, 0);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, 0);
}
```

---

## Módulo 8.5: Código - Versão Avançada (com Pan-Tilt)

Agora vamos fazer o robô "olhar" para os lados antes de decidir para onde girar!

```cpp
#include <ESP32Servo.h>

// ===== Pinos dos Motores =====
const int MOTOR_ESQ_IN1 = 18;
const int MOTOR_ESQ_IN2 = 19;
const int MOTOR_ESQ_EN = 21;

const int MOTOR_DIR_IN3 = 22;
const int MOTOR_DIR_IN4 = 23;
const int MOTOR_DIR_EN = 12;

// ===== Pinos do Sensor Ultrassônico =====
const int TRIG_PIN = 26;
const int ECHO_PIN = 25;

// ===== Pino do Servo =====
const int SERVO_PIN = 13;
Servo servoSensor;

// ===== Ângulos do Servo =====
const int ANGULO_CENTRO = 90;
const int ANGULO_DIREITA = 30;
const int ANGULO_ESQUERDA = 150;

// ===== Configurações PWM =====
const int PWM_FREQ = 1000;
const int PWM_RESOLUTION = 8;
const int PWM_CHANNEL_ESQ = 0;
const int PWM_CHANNEL_DIR = 1;

// ===== Parâmetros de Navegação =====
const int DISTANCIA_SEGURA = 35;
const int VELOCIDADE_NORMAL = 180;
const int TEMPO_GIRO_90_GRAUS = 500;

// ===== Estados =====
enum Estado {
  AVANCAR,
  ESCANEAR,
  GIRAR_DIREITA,
  GIRAR_ESQUERDA,
  RE
};

Estado estadoAtual = AVANCAR;

void setup() {
  Serial.begin(115200);
  Serial.println("=== Robô Inteligente com Pan-Tilt ===");

  // Motores
  pinMode(MOTOR_ESQ_IN1, OUTPUT);
  pinMode(MOTOR_ESQ_IN2, OUTPUT);
  pinMode(MOTOR_DIR_IN3, OUTPUT);
  pinMode(MOTOR_DIR_IN4, OUTPUT);

  ledcSetup(PWM_CHANNEL_ESQ, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_DIR, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(MOTOR_ESQ_EN, PWM_CHANNEL_ESQ);
  ledcAttachPin(MOTOR_DIR_EN, PWM_CHANNEL_DIR);

  // Sensor
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Servo
  servoSensor.attach(SERVO_PIN);
  servoSensor.write(ANGULO_CENTRO);

  Serial.println("Sistema pronto!");
  delay(2000);
}

void loop() {
  // Sensor olha para frente
  servoSensor.write(ANGULO_CENTRO);
  delay(100);

  float distanciaFrente = lerDistancia();

  Serial.print("Frente: ");
  Serial.print(distanciaFrente);
  Serial.print(" cm | Estado: ");

  // ===== MÁQUINA DE ESTADOS =====
  switch(estadoAtual) {

    case AVANCAR:
      Serial.println("AVANÇAR");

      if (distanciaFrente > 0 && distanciaFrente < DISTANCIA_SEGURA) {
        estadoAtual = ESCANEAR;
      } else {
        frente(VELOCIDADE_NORMAL);
      }
      break;

    case ESCANEAR:
      Serial.println("ESCANEAR");
      parar();
      delay(200);

      // Olha para a direita
      servoSensor.write(ANGULO_DIREITA);
      delay(500); // Aguarda o servo se posicionar
      float distanciaDireita = lerDistancia();
      Serial.print("  → Direita: ");
      Serial.print(distanciaDireita);
      Serial.println(" cm");

      // Olha para a esquerda
      servoSensor.write(ANGULO_ESQUERDA);
      delay(500);
      float distanciaEsquerda = lerDistancia();
      Serial.print("  → Esquerda: ");
      Serial.print(distanciaEsquerda);
      Serial.println(" cm");

      // Volta para o centro
      servoSensor.write(ANGULO_CENTRO);
      delay(300);

      // DECISÃO INTELIGENTE
      if (distanciaDireita < 15 && distanciaEsquerda < 15) {
        // Ambos os lados bloqueados - dar ré
        Serial.println("  → Decisão: DAR RÉ");
        estadoAtual = RE;
      }
      else if (distanciaDireita > distanciaEsquerda) {
        // Direita está mais livre
        Serial.println("  → Decisão: GIRAR DIREITA");
        estadoAtual = GIRAR_DIREITA;
      }
      else {
        // Esquerda está mais livre
        Serial.println("  → Decisão: GIRAR ESQUERDA");
        estadoAtual = GIRAR_ESQUERDA;
      }
      break;

    case GIRAR_DIREITA:
      Serial.println("GIRAR DIREITA");
      girarDireita(200);
      delay(TEMPO_GIRO_90_GRAUS);
      parar();
      estadoAtual = AVANCAR;
      break;

    case GIRAR_ESQUERDA:
      Serial.println("GIRAR ESQUERDA");
      girarEsquerda(200);
      delay(TEMPO_GIRO_90_GRAUS);
      parar();
      estadoAtual = AVANCAR;
      break;

    case RE:
      Serial.println("RÉ");
      tras(180);
      delay(800);
      parar();
      // Após dar ré, gira 180 graus
      girarDireita(200);
      delay(TEMPO_GIRO_90_GRAUS * 2);
      parar();
      estadoAtual = AVANCAR;
      break;
  }

  delay(50);
}

// ===== FUNÇÃO DE LEITURA =====
float lerDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duracao == 0) {
    return 400;
  }

  return (duracao * 0.0343) / 2.0;
}

// ===== FUNÇÕES DE MOVIMENTO =====
void frente(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void tras(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarDireita(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarEsquerda(int velocidade) {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void parar() {
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, 0);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, 0);
}
```

---

## Módulo 8.6: Calibração e Otimizações

### Calibração do Tempo de Giro

Para que o robô gire exatamente 90°:

1. Execute este código de teste:

```cpp
void setup() {
  // Configurações de motor aqui
}

void loop() {
  Serial.println("Girando 90° para direita...");
  girarDireita(200);
  delay(500); // Ajuste este valor
  parar();
  delay(5000); // Espera 5 segundos

  Serial.println("Girando 90° para esquerda...");
  girarEsquerda(200);
  delay(500); // Ajuste este valor
  parar();
  delay(5000);
}
```

2. Use uma fita no chão como referência
3. Ajuste o valor do `delay()` até o giro ser preciso

### Ajuste de Distância Segura

Se o robô estiver:

**Batendo em obstáculos:**
- Aumente `DISTANCIA_SEGURA` (ex: de 30 para 40 cm)

**Parando longe demais:**
- Diminua `DISTANCIA_SEGURA` (ex: de 30 para 20 cm)

### Otimização: Evitando Loops Infinitos

Adicione um contador para detectar quando o robô está preso:

```cpp
int tentativasGiro = 0;
const int MAX_TENTATIVAS = 3;

// No estado ESCANEAR, adicione:
if (estadoAtual == ESCANEAR) {
  tentativasGiro++;

  if (tentativasGiro >= MAX_TENTATIVAS) {
    // Está preso - estratégia de escape!
    Serial.println("ROBÔ PRESO - MODO ESCAPE");
    tras(200);
    delay(1000);
    girarDireita(200);
    delay(TEMPO_GIRO_90_GRAUS * 3); // Gira 270°
    tentativasGiro = 0;
    estadoAtual = AVANCAR;
  }
}

// No estado AVANCAR, resete o contador:
if (estadoAtual == AVANCAR && distanciaFrente > DISTANCIA_SEGURA) {
  tentativasGiro = 0;
}
```

---

## Módulo 8.7: Desafio Final - Navegação em Labirinto

### Algoritmo de Seguir Parede (Wall Following)

Este é um algoritmo clássico que sempre mantém uma parede à direita (ou esquerda) do robô:

**Regra de Ouro:** "Sempre mantém a mão direita na parede"

```cpp
void navegarLabirinto() {
  servoSensor.write(ANGULO_DIREITA);
  delay(200);
  float distDireita = lerDistancia();

  servoSensor.write(ANGULO_CENTRO);
  delay(200);
  float distFrente = lerDistancia();

  const int DIST_PAREDE = 25; // Distância ideal da parede

  // Lógica de seguir parede direita
  if (distFrente < 30) {
    // Obstáculo à frente - girar esquerda
    parar();
    girarEsquerda(180);
    delay(TEMPO_GIRO_90_GRAUS);
  }
  else if (distDireita > DIST_PAREDE + 10) {
    // Muito longe da parede - corrigir para direita
    digitalWrite(MOTOR_ESQ_IN1, HIGH);
    digitalWrite(MOTOR_ESQ_IN2, LOW);
    ledcWrite(PWM_CHANNEL_ESQ, 200);

    digitalWrite(MOTOR_DIR_IN3, HIGH);
    digitalWrite(MOTOR_DIR_IN4, LOW);
    ledcWrite(PWM_CHANNEL_DIR, 150); // Motor direito mais lento
  }
  else if (distDireita < DIST_PAREDE - 10) {
    // Muito perto da parede - corrigir para esquerda
    digitalWrite(MOTOR_ESQ_IN1, HIGH);
    digitalWrite(MOTOR_ESQ_IN2, LOW);
    ledcWrite(PWM_CHANNEL_ESQ, 150); // Motor esquerdo mais lento

    digitalWrite(MOTOR_DIR_IN3, HIGH);
    digitalWrite(MOTOR_DIR_IN4, LOW);
    ledcWrite(PWM_CHANNEL_DIR, 200);
  }
  else {
    // Distância ideal - seguir reto
    frente(180);
  }
}
```

### Construindo um Labirinto de Teste

**Materiais:**
- Caixas de papelão
- Livros
- Garrafas PET
- Blocos de madeira

**Dicas de Design:**
- Corredores de pelo menos 30cm de largura
- Paredes de pelo menos 15cm de altura
- Evite superfícies muito reflexivas (espelhos, metal brilhante)
- Use paredes opacas para melhor detecção

**Exemplo de Labirinto Simples:**

```
┌─────────────────┐
│  START          │
│    │            │
│    │    ┌───────┤
│    │    │       │
│    └────┤       │
│         │   ┌───┤
│         │   │   │
│         └───┤ E │
│             │ N │
│             │ D │
└─────────────┴───┘
```

---

## Módulo 8.8: Funcionalidades Avançadas

### 1. Modo de Operação Selecionável

Adicione um botão para alternar entre modos:

```cpp
const int BOTAO_PIN = 14;

enum Modo {
  EXPLORADOR,      // Navegação livre
  SEGUIR_PAREDE,   // Algoritmo de parede
  RETORNAR_BASE    // Volta para o ponto inicial
};

Modo modoAtual = EXPLORADOR;

void setup() {
  pinMode(BOTAO_PIN, INPUT_PULLUP);
  // ... resto do setup
}

void loop() {
  // Verifica se o botão foi pressionado
  if (digitalRead(BOTAO_PIN) == LOW) {
    modoAtual = (Modo)((modoAtual + 1) % 3);
    Serial.print("Modo alterado para: ");
    Serial.println(modoAtual);
    delay(500); // Debounce
  }

  switch(modoAtual) {
    case EXPLORADOR:
      navegarLivremente();
      break;
    case SEGUIR_PAREDE:
      navegarLabirinto();
      break;
    case RETORNAR_BASE:
      retornarBase();
      break;
  }
}
```

### 2. Mapeamento Simples

Mantenha registro dos movimentos para criar um "mapa mental":

```cpp
const int MAX_MOVIMENTOS = 100;
char historico[MAX_MOVIMENTOS];
int indiceHistorico = 0;

void registrarMovimento(char movimento) {
  // 'F' = Frente, 'D' = Direita, 'E' = Esquerda, 'R' = Ré
  if (indiceHistorico < MAX_MOVIMENTOS) {
    historico[indiceHistorico] = movimento;
    indiceHistorico++;
  }
}

void imprimirMapa() {
  Serial.println("=== Mapa de Movimentos ===");
  for (int i = 0; i < indiceHistorico; i++) {
    Serial.print(historico[i]);
    if ((i + 1) % 20 == 0) Serial.println(); // Quebra de linha a cada 20
  }
  Serial.println();
}
```

### 3. Telemetria via Wi-Fi

Envie dados do robô para um dashboard web:

```cpp
#include <WiFi.h>

const char* ssid = "ROBO_EXPLORER";
WiFiServer server(80);

void enviarTelemetria() {
  WiFiClient client = server.available();
  if (client) {
    String dados = "Distancia:" + String(lerDistancia()) +
                   ",Estado:" + String(estadoAtual) +
                   ",Velocidade:" + String(VELOCIDADE_NORMAL);

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println();
    client.println("{\"" + dados + "\"}");
    client.stop();
  }
}
```

### 4. Detecção de Bordas (para mesas)

Adicione sensores IR apontando para baixo para detectar quedas:

```cpp
const int SENSOR_BORDA_ESQ = 34;
const int SENSOR_BORDA_DIR = 35;

void verificarBordas() {
  if (digitalRead(SENSOR_BORDA_ESQ) == HIGH ||
      digitalRead(SENSOR_BORDA_DIR) == HIGH) {
    // Borda detectada!
    Serial.println("ALERTA: BORDA DETECTADA!");
    parar();
    tras(200);
    delay(500);
    girarDireita(200);
    delay(TEMPO_GIRO_90_GRAUS * 2); // 180°
  }
}
```

---

## Módulo 8.9: Troubleshooting (Resolução de Problemas)

### Problema 1: Sensor não detecta obstáculos próximos

**Causas possíveis:**
- Objeto muito pequeno ou fino
- Superfície absorve ultrassom (tecido, espuma)
- Ângulo de incidência muito oblíquo

**Solução:**
- Use múltiplos sensores
- Adicione sensores IR para objetos próximos
- Teste com diferentes materiais

### Problema 2: Robô oscila muito

**Causas possíveis:**
- Leituras do sensor muito ruidosas
- Reações muito bruscas

**Solução:**
- Implemente filtro de média móvel
- Adicione "zona morta" (hysteresis)
- Reduza velocidades

### Problema 3: Baterias descarregam rápido

**Causas possíveis:**
- Motores consumindo muita corrente
- Curto-circuito
- Baterias fracas

**Solução:**
- Use baterias de maior capacidade (2500mAh+)
- Adicione um display de nível de bateria
- Implemente modo de economia de energia

```cpp
float lerTensaoBateria() {
  // ESP32 ADC no pino 36 (VP)
  int leitura = analogRead(36);
  float tensao = (leitura / 4095.0) * 3.3 * 2; // Divisor de tensão 1:1
  return tensao;
}

void verificarBateria() {
  float tensao = lerTensaoBateria();
  if (tensao < 5.5) { // Bateria fraca (< 5.5V)
    Serial.println("BATERIA FRACA!");
    VELOCIDADE_NORMAL = 120; // Reduz velocidade
  }
}
```

---

## Conclusão do Nível 1

**PARABÉNS!** Você completou o Nível 1 do curso de Robótica!

### O Que Você Conquistou:

✓ Domínio de eletrônica básica (lei de Ohm, componentes)
✓ Programação em C/C++ para microcontroladores
✓ Uso de sensores (ultrassônico, IR, temperatura)
✓ Controle de atuadores (LEDs, motores DC, servos)
✓ Comunicação serial (UART, I2C, SPI)
✓ Construção de dois robôs autônomos completos
✓ Algoritmos de navegação e controle

### Projetos Construídos:

1. Circuitos eletrônicos básicos
2. Semáforo inteligente
3. Sistema de telemetria
4. Robô rover controlado por Wi-Fi
5. **Robô seguidor de linha**
6. **Robô desviador de obstáculos**

### Próximos Passos - Nível 2: Robótica Autônoma

No Nível 2, você aprenderá:

- Visão computacional com câmeras
- Sensores IMU e odometria
- SLAM (Localização e Mapeamento Simultâneos)
- ROS (Robot Operating System)
- Inteligência artificial para robôs
- Robôs com braços manipuladores

### Desafios Finais para Consolidar o Conhecimento:

1. **Combine os dois robôs**: Crie um robô que segue linha MAS desvia se houver obstáculo na frente

2. **Competição**: Faça uma corrida de robôs seguidores de linha com amigos

3. **Labirinto Complexo**: Construa um labirinto com múltiplos caminhos e faça o robô encontrar a saída

4. **Controle por Voz**: Adicione um módulo de reconhecimento de voz

5. **Robô Social**: Faça o robô seguir pessoas usando o sensor ultrassônico

---

## Recursos Adicionais

**Fóruns e Comunidades:**
- Arduino Forum
- ESP32.com
- Reddit: r/robotics, r/arduino

**Competições:**
- OBR - Olimpíada Brasileira de Robótica
- RoboCore Competition
- FIRST Robotics

**Livros Recomendados:**
- "Programming Robots with ROS" - Morgan Quigley
- "Make: Electronics" - Charles Platt
- "Robot Builder's Bonanza" - Gordon McComb

**Canais do YouTube (em português):**
- Brincando com Ideias
- Manual do Mundo
- Laboratório de Garagem

---

Você agora tem as fundações sólidas para construir praticamente qualquer projeto de robótica! Continue experimentando, quebrando coisas (literalmente, às vezes), aprendendo e, acima de tudo, se divertindo.

**Bem-vindo à comunidade de criadores de robôs!** 🤖
