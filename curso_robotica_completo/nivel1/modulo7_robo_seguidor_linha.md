# Módulo 1.7: Projeto Final - Robô Seguidor de Linha

## Bem-vindo ao Seu Primeiro Robô Autônomo!

Este é um dos momentos mais emocionantes do curso! Você irá construir um **robô seguidor de linha**, um dos projetos mais clássicos e educacionais da robótica. Este robô consegue seguir de forma autônoma uma linha preta (ou branca) desenhada no chão, usando sensores infravermelhos para "ver" o caminho.

Os robôs seguidores de linha são usados em:

- **Indústria**: Veículos guiados automaticamente (AGVs) em fábricas
- **Competições**: Eventos de robótica como a RoboCore e OBR (Olimpíada Brasileira de Robótica)
- **Educação**: Ensino de conceitos de sensores, controle e lógica

---

## O Que Você Vai Aprender

1. **Design Mecânico**: Como projetar um chassi eficiente para um robô móvel
2. **Sensores Infravermelhos**: Como funcionam e como usá-los para detectar linhas
3. **Controle Diferencial**: Como fazer o robô se mover e girar usando dois motores
4. **Algoritmos de Controle**: Lógica de decisão baseada em sensores
5. **Calibração**: Como ajustar o robô para diferentes superfícies e iluminações

---

## Módulo 7.1: Design Mecânico e Lista de Materiais

### Conceito do Robô Seguidor de Linha

O robô seguidor de linha usa um array de sensores infravermelhos posicionados na parte frontal inferior do chassi. Esses sensores detectam o contraste entre a linha e o fundo, permitindo que o robô determine sua posição relativa à linha.

**Princípio de Funcionamento:**
- Sensores sobre a superfície clara (fundo) → Detectam reflexão alta
- Sensores sobre a linha preta → Detectam reflexão baixa
- O robô ajusta continuamente sua direção para manter os sensores centrais sobre a linha

### Materiais Necessários

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Quantidade</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Componente</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Especificações</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Custo Aprox.</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>ESP32 DevKit</strong></td>
<td class="border border-gray-300 px-4 py-2">Microcontrolador principal</td>
<td class="border border-gray-300 px-4 py-2">R$ 35</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Módulo Sensor IR 5 canais</strong></td>
<td class="border border-gray-300 px-4 py-2">TCRT5000 ou similar</td>
<td class="border border-gray-300 px-4 py-2">R$ 15</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Ponte H L298N</strong></td>
<td class="border border-gray-300 px-4 py-2">Driver de motor duplo</td>
<td class="border border-gray-300 px-4 py-2">R$ 12</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">2x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Motor DC com Caixa de Redução</strong></td>
<td class="border border-gray-300 px-4 py-2">3-6V, 100-200 RPM</td>
<td class="border border-gray-300 px-4 py-2">R$ 20</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">2x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Rodas</strong></td>
<td class="border border-gray-300 px-4 py-2">65-70mm de diâmetro</td>
<td class="border border-gray-300 px-4 py-2">R$ 10</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Rodízio ou Roda Boba</strong></td>
<td class="border border-gray-300 px-4 py-2">Para suporte dianteiro/traseiro</td>
<td class="border border-gray-300 px-4 py-2">R$ 8</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Suporte de Baterias</strong></td>
<td class="border border-gray-300 px-4 py-2">4x pilhas AA (6V)</td>
<td class="border border-gray-300 px-4 py-2">R$ 5</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">1x</td>
<td class="border border-gray-300 px-4 py-2"><strong>Chassi Acrílico ou MDF</strong></td>
<td class="border border-gray-300 px-4 py-2">15x12cm, 3mm espessura</td>
<td class="border border-gray-300 px-4 py-2">R$ 8</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">-</td>
<td class="border border-gray-300 px-4 py-2"><strong>Fios Jumper e Parafusos</strong></td>
<td class="border border-gray-300 px-4 py-2">Para montagem</td>
<td class="border border-gray-300 px-4 py-2">R$ 15</td>
</tr>
</tbody>
</table>

**Custo Total Aproximado:** R$ 128

---

### Design do Chassi

O chassi é a base estrutural do robô. Para um seguidor de linha eficiente, considere:

**Dimensões Recomendadas:**
- Comprimento: 15-18 cm
- Largura: 12-15 cm
- Altura: 5-8 cm (com componentes)

**Distribuição de Peso:**
- **Parte Traseira**: Baterias (mais pesadas) sobre as rodas motoras para melhor tração
- **Parte Frontal**: Sensores próximos ao chão (2-5mm de altura)
- **Centro**: ESP32 e ponte H em posição acessível

**Pontos de Montagem:**
1. Suportes para motores (fixos nas laterais)
2. Área para sensores (parte frontal inferior)
3. Plataforma elevada para eletrônica
4. Suporte para baterias (traseiro)

---

## Módulo 7.2: Entendendo os Sensores Infravermelhos

### Como Funcionam os Sensores TCRT5000

O TCRT5000 é um sensor óptico reflexivo que consiste em:

1. **LED Infravermelho Emissor**: Emite luz infravermelha (invisível aos olhos humanos)
2. **Fototransistor Receptor**: Detecta a luz infravermelha refletida

**Princípio de Operação:**

```
Superfície Clara (Branco):        Superfície Escura (Preto):
LED IR → Alta Reflexão → Sensor   LED IR → Baixa Reflexão → Sensor
Saída: HIGH (1)                   Saída: LOW (0)
```

### Módulo Sensor de 5 Canais

Um módulo típico possui 5 sensores TCRT5000 em linha:

```
[S1] [S2] [S3] [S4] [S5]
 ←        ↑        →
Esq     Centro    Dir
```

**Saídas Digitais:**
- Cada sensor tem um comparador que gera saída digital (HIGH/LOW)
- Potenciômetros de ajuste permitem calibrar a sensibilidade

**Distância Ideal:**
- 2-5mm entre o sensor e o chão
- Distância maior: perde sensibilidade
- Distância menor: campo de visão muito estreito

### Pinagem do Módulo

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Pino</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Função</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Conexão ESP32</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>VCC</strong></td>
<td class="border border-gray-300 px-4 py-2">Alimentação (+5V)</td>
<td class="border border-gray-300 px-4 py-2">5V ou 3.3V</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>GND</strong></td>
<td class="border border-gray-300 px-4 py-2">Terra</td>
<td class="border border-gray-300 px-4 py-2">GND</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT1</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensor 1 (Esquerda)</td>
<td class="border border-gray-300 px-4 py-2">GPIO 32</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT2</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensor 2</td>
<td class="border border-gray-300 px-4 py-2">GPIO 33</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT3</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensor 3 (Centro)</td>
<td class="border border-gray-300 px-4 py-2">GPIO 25</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT4</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensor 4</td>
<td class="border border-gray-300 px-4 py-2">GPIO 26</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT5</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensor 5 (Direita)</td>
<td class="border border-gray-300 px-4 py-2">GPIO 27</td>
</tr>
</tbody>
</table>

---

## Módulo 7.3: Ponte H e Controle de Motores

### O Que é uma Ponte H?

Uma **Ponte H** (H-Bridge) é um circuito eletrônico que permite controlar a direção e velocidade de motores DC. O nome vem da configuração em forma de "H" dos transistores internos.

### Módulo L298N

O L298N é um driver de motor duplo muito popular que pode controlar:
- 2 motores DC simultaneamente
- Corrente: até 2A por canal
- Tensão: 5-35V

**Pinagem do L298N:**

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Pino</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Função</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Conexão</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>IN1, IN2</strong></td>
<td class="border border-gray-300 px-4 py-2">Controle do Motor A</td>
<td class="border border-gray-300 px-4 py-2">GPIOs do ESP32</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>IN3, IN4</strong></td>
<td class="border border-gray-300 px-4 py-2">Controle do Motor B</td>
<td class="border border-gray-300 px-4 py-2">GPIOs do ESP32</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>ENA, ENB</strong></td>
<td class="border border-gray-300 px-4 py-2">Enable (PWM para velocidade)</td>
<td class="border border-gray-300 px-4 py-2">GPIOs do ESP32 ou jumper</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT1, OUT2</strong></td>
<td class="border border-gray-300 px-4 py-2">Saída para Motor A</td>
<td class="border border-gray-300 px-4 py-2">Motor Esquerdo</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>OUT3, OUT4</strong></td>
<td class="border border-gray-300 px-4 py-2">Saída para Motor B</td>
<td class="border border-gray-300 px-4 py-2">Motor Direito</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>+12V</strong></td>
<td class="border border-gray-300 px-4 py-2">Alimentação dos motores</td>
<td class="border border-gray-300 px-4 py-2">Bateria 6V (4xAA)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>GND</strong></td>
<td class="border border-gray-300 px-4 py-2">Terra</td>
<td class="border border-gray-300 px-4 py-2">GND comum</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>+5V</strong></td>
<td class="border border-gray-300 px-4 py-2">Saída regulada 5V</td>
<td class="border border-gray-300 px-4 py-2">Pode alimentar ESP32</td>
</tr>
</tbody>
</table>

### Controle de Direção

A direção do motor é controlada pelos pinos IN1 e IN2:

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">IN1</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">IN2</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Resultado</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2">LOW</td>
<td class="border border-gray-300 px-4 py-2">LOW</td>
<td class="border border-gray-300 px-4 py-2">Motor PARADO</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">HIGH</td>
<td class="border border-gray-300 px-4 py-2">LOW</td>
<td class="border border-gray-300 px-4 py-2">Motor FRENTE</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">LOW</td>
<td class="border border-gray-300 px-4 py-2">HIGH</td>
<td class="border border-gray-300 px-4 py-2">Motor TRÁS</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2">HIGH</td>
<td class="border border-gray-300 px-4 py-2">HIGH</td>
<td class="border border-gray-300 px-4 py-2">Motor FREIO</td>
</tr>
</tbody>
</table>

---

## Módulo 7.4: Montagem Eletrônica Completa

### Diagrama de Conexões

**ESP32 → L298N:**
- GPIO 18 → IN1 (Motor Esquerdo)
- GPIO 19 → IN2 (Motor Esquerdo)
- GPIO 22 → IN3 (Motor Direito)
- GPIO 23 → IN4 (Motor Direito)
- GPIO 21 → ENA (PWM Motor Esquerdo)
- GPIO 12 → ENB (PWM Motor Direito)

**L298N → Motores:**
- OUT1, OUT2 → Motor Esquerdo
- OUT3, OUT4 → Motor Direito

**L298N → Bateria:**
- +12V → Positivo da bateria (6V)
- GND → Negativo da bateria

**Sensores → ESP32:**
- VCC → 3.3V
- GND → GND
- OUT1-5 → GPIOs 32, 33, 25, 26, 27

**Importante - GND Comum:**
Conecte o GND do ESP32, L298N e sensores juntos. Isto é crítico!

---

## Módulo 7.5: Código Base - Teste dos Motores

Antes de implementar o seguidor de linha, vamos testar os motores.

```cpp
// ===== Definição dos Pinos =====
// Motor Esquerdo
const int MOTOR_ESQ_IN1 = 18;
const int MOTOR_ESQ_IN2 = 19;
const int MOTOR_ESQ_EN = 21;

// Motor Direito
const int MOTOR_DIR_IN3 = 22;
const int MOTOR_DIR_IN4 = 23;
const int MOTOR_DIR_EN = 12;

// Configuração PWM
const int PWM_FREQ = 1000;  // 1 kHz
const int PWM_RESOLUTION = 8; // 8 bits (0-255)
const int PWM_CHANNEL_ESQ = 0;
const int PWM_CHANNEL_DIR = 1;

void setup() {
  Serial.begin(115200);
  Serial.println("=== Teste de Motores ===");

  // Configura pinos como saída
  pinMode(MOTOR_ESQ_IN1, OUTPUT);
  pinMode(MOTOR_ESQ_IN2, OUTPUT);
  pinMode(MOTOR_DIR_IN3, OUTPUT);
  pinMode(MOTOR_DIR_IN4, OUTPUT);

  // Configura PWM
  ledcSetup(PWM_CHANNEL_ESQ, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_DIR, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(MOTOR_ESQ_EN, PWM_CHANNEL_ESQ);
  ledcAttachPin(MOTOR_DIR_EN, PWM_CHANNEL_DIR);
}

void loop() {
  Serial.println("Teste: FRENTE");
  frente(200);
  delay(2000);

  Serial.println("Teste: PARAR");
  parar();
  delay(1000);

  Serial.println("Teste: TRÁS");
  tras(200);
  delay(2000);

  Serial.println("Teste: PARAR");
  parar();
  delay(1000);

  Serial.println("Teste: GIRAR DIREITA");
  girarDireita(180);
  delay(2000);

  Serial.println("Teste: PARAR");
  parar();
  delay(1000);

  Serial.println("Teste: GIRAR ESQUERDA");
  girarEsquerda(180);
  delay(2000);

  Serial.println("Teste: PARAR");
  parar();
  delay(2000);
}

// ===== Funções de Movimento =====

void frente(int velocidade) {
  // Motor Esquerdo: Frente
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  // Motor Direito: Frente
  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void tras(int velocidade) {
  // Motor Esquerdo: Trás
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  // Motor Direito: Trás
  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarDireita(int velocidade) {
  // Motor Esquerdo: Frente
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  // Motor Direito: Trás
  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, velocidade);
}

void girarEsquerda(int velocidade) {
  // Motor Esquerdo: Trás
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, velocidade);

  // Motor Direito: Frente
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

**Teste este código antes de prosseguir!** Certifique-se de que o robô se move corretamente em todas as direções.

---

## Módulo 7.6: Código do Seguidor de Linha

Agora vamos implementar o algoritmo de seguimento de linha!

```cpp
// ===== Pinos dos Motores =====
const int MOTOR_ESQ_IN1 = 18;
const int MOTOR_ESQ_IN2 = 19;
const int MOTOR_ESQ_EN = 21;

const int MOTOR_DIR_IN3 = 22;
const int MOTOR_DIR_IN4 = 23;
const int MOTOR_DIR_EN = 12;

// ===== Pinos dos Sensores IR =====
const int SENSOR_1 = 32; // Esquerda extrema
const int SENSOR_2 = 33; // Esquerda
const int SENSOR_3 = 25; // Centro
const int SENSOR_4 = 26; // Direita
const int SENSOR_5 = 27; // Direita extrema

// ===== Configurações PWM =====
const int PWM_FREQ = 1000;
const int PWM_RESOLUTION = 8;
const int PWM_CHANNEL_ESQ = 0;
const int PWM_CHANNEL_DIR = 1;

// ===== Parâmetros de Velocidade =====
const int VELOCIDADE_BASE = 150;    // Velocidade quando na linha reta
const int VELOCIDADE_CURVA = 100;   // Velocidade ao fazer curvas
const int VELOCIDADE_CORRECAO = 180; // Velocidade para correções rápidas

// ===== Variáveis dos Sensores =====
int s1, s2, s3, s4, s5;

void setup() {
  Serial.begin(115200);
  Serial.println("=== Robô Seguidor de Linha ===");

  // Configura pinos dos motores
  pinMode(MOTOR_ESQ_IN1, OUTPUT);
  pinMode(MOTOR_ESQ_IN2, OUTPUT);
  pinMode(MOTOR_DIR_IN3, OUTPUT);
  pinMode(MOTOR_DIR_IN4, OUTPUT);

  // Configura PWM
  ledcSetup(PWM_CHANNEL_ESQ, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_DIR, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(MOTOR_ESQ_EN, PWM_CHANNEL_ESQ);
  ledcAttachPin(MOTOR_DIR_EN, PWM_CHANNEL_DIR);

  // Configura pinos dos sensores
  pinMode(SENSOR_1, INPUT);
  pinMode(SENSOR_2, INPUT);
  pinMode(SENSOR_3, INPUT);
  pinMode(SENSOR_4, INPUT);
  pinMode(SENSOR_5, INPUT);

  Serial.println("Aguardando 3 segundos...");
  delay(3000);
  Serial.println("INICIANDO!");
}

void loop() {
  // Lê os sensores (0 = preto/linha, 1 = branco/fundo)
  s1 = digitalRead(SENSOR_1);
  s2 = digitalRead(SENSOR_2);
  s3 = digitalRead(SENSOR_3);
  s4 = digitalRead(SENSOR_4);
  s5 = digitalRead(SENSOR_5);

  // Debug (envie para Serial Monitor)
  Serial.print(s1); Serial.print(" ");
  Serial.print(s2); Serial.print(" ");
  Serial.print(s3); Serial.print(" ");
  Serial.print(s4); Serial.print(" ");
  Serial.println(s5);

  // ===== LÓGICA DE DECISÃO =====

  // Caso 1: Sensor central na linha - SEGUIR RETO
  if (s3 == 0) {
    frente(VELOCIDADE_BASE);
    Serial.println("Ação: RETO");
  }

  // Caso 2: Sensores centrais e à direita na linha - LEVE CURVA À DIREITA
  else if (s3 == 0 && s4 == 0) {
    curvaLeveDireita();
    Serial.println("Ação: CURVA LEVE DIREITA");
  }

  // Caso 3: Sensores centrais e à esquerda na linha - LEVE CURVA À ESQUERDA
  else if (s2 == 0 && s3 == 0) {
    curvaLeveEsquerda();
    Serial.println("Ação: CURVA LEVE ESQUERDA");
  }

  // Caso 4: Apenas sensor direito na linha - CURVA FORTE DIREITA
  else if (s4 == 0 || s5 == 0) {
    curvaForteDireita();
    Serial.println("Ação: CURVA FORTE DIREITA");
  }

  // Caso 5: Apenas sensor esquerdo na linha - CURVA FORTE ESQUERDA
  else if (s1 == 0 || s2 == 0) {
    curvaForteEsquerda();
    Serial.println("Ação: CURVA FORTE ESQUERDA");
  }

  // Caso 6: Todos os sensores no branco - PERDEU A LINHA
  else if (s1 == 1 && s2 == 1 && s3 == 1 && s4 == 1 && s5 == 1) {
    frente(VELOCIDADE_CURVA);
    Serial.println("Ação: PROCURANDO LINHA...");
  }

  // Caso 7: Todos os sensores no preto - CRUZAMENTO OU LINHA GROSSA
  else if (s1 == 0 && s2 == 0 && s3 == 0 && s4 == 0 && s5 == 0) {
    frente(VELOCIDADE_BASE);
    Serial.println("Ação: CRUZAMENTO - SEGUIR RETO");
  }

  // Pequeno delay para estabilidade
  delay(10);
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

void curvaLeveDireita() {
  // Reduz velocidade do motor direito
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, VELOCIDADE_BASE);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, VELOCIDADE_CURVA);
}

void curvaLeveEsquerda() {
  // Reduz velocidade do motor esquerdo
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, VELOCIDADE_CURVA);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, VELOCIDADE_BASE);
}

void curvaForteDireita() {
  // Motor esquerdo frente, direito parado ou trás
  digitalWrite(MOTOR_ESQ_IN1, HIGH);
  digitalWrite(MOTOR_ESQ_IN2, LOW);
  ledcWrite(PWM_CHANNEL_ESQ, VELOCIDADE_CORRECAO);

  digitalWrite(MOTOR_DIR_IN3, LOW);
  digitalWrite(MOTOR_DIR_IN4, HIGH);
  ledcWrite(PWM_CHANNEL_DIR, VELOCIDADE_CURVA);
}

void curvaForteEsquerda() {
  // Motor direito frente, esquerdo parado ou trás
  digitalWrite(MOTOR_ESQ_IN1, LOW);
  digitalWrite(MOTOR_ESQ_IN2, HIGH);
  ledcWrite(PWM_CHANNEL_ESQ, VELOCIDADE_CURVA);

  digitalWrite(MOTOR_DIR_IN3, HIGH);
  digitalWrite(MOTOR_DIR_IN4, LOW);
  ledcWrite(PWM_CHANNEL_DIR, VELOCIDADE_CORRECAO);
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

## Módulo 7.7: Calibração e Ajustes

### Calibração dos Sensores

1. **Ajuste de Altura**: Mantenha os sensores entre 2-5mm do chão
2. **Potenciômetros**: Gire os potenciômetros no módulo até que:
   - LED acenda quando sobre a linha preta
   - LED apague quando sobre o fundo branco
3. **Teste Manual**: Use o Serial Monitor para ver os valores dos sensores

### Ajuste de Velocidades

Se o robô estiver:

**Muito Lento:**
- Aumente `VELOCIDADE_BASE` (máximo 255)

**Oscilando Muito:**
- Diminua `VELOCIDADE_CORRECAO`
- Aumente `VELOCIDADE_CURVA`

**Saindo da Linha em Curvas:**
- Diminua `VELOCIDADE_BASE`
- Aumente `VELOCIDADE_CORRECAO`

### Pista de Teste

Crie uma pista simples usando:
- **Fita isolante preta** (18-25mm de largura) sobre fundo branco
- **Cartolina branca** com linha desenhada com marcador preto
- **Impressão** de uma pista em papel

**Dicas de Design da Pista:**
- Comece com linhas retas e curvas suaves
- Largura da linha: 18-25mm (ideal para 5 sensores)
- Evite curvas de 90° no início
- Adicione curvas fechadas depois que o robô estiver funcionando bem

---

## Módulo 7.8: Desafios e Melhorias

### Desafio 1: Detecção de Marcações Especiais

Adicione detecção de quando todos os sensores detectam preto (cruzamento) e faça o robô:
- Piscar um LED
- Enviar telemetria via Serial
- Contar quantos cruzamentos passou

### Desafio 2: Controle PID

Implemente um controlador PID (Proporcional-Integral-Derivativo) para um seguimento mais suave:

```cpp
float kP = 25;  // Ganho proporcional
float kD = 15;  // Ganho derivativo

int erroAnterior = 0;

void seguirLinhaPID() {
  // Calcula o erro de posição
  int erro = calcularErro();

  // Termo Proporcional
  float P = erro * kP;

  // Termo Derivativo
  float D = (erro - erroAnterior) * kD;
  erroAnterior = erro;

  // Ajuste de velocidade
  int ajuste = P + D;

  int velEsq = constrain(VELOCIDADE_BASE + ajuste, 0, 255);
  int velDir = constrain(VELOCIDADE_BASE - ajuste, 0, 255);

  moverMotores(velEsq, velDir);
}

int calcularErro() {
  // -2: muito à esquerda, 0: centralizado, +2: muito à direita
  if (s1 == 0) return -2;
  if (s2 == 0) return -1;
  if (s3 == 0) return 0;
  if (s4 == 0) return 1;
  if (s5 == 0) return 2;
  return 0;
}
```

### Desafio 3: Interface de Calibração

Adicione um botão que permite alternar entre:
- Modo de calibração (mostra valores dos sensores)
- Modo de operação (segue a linha)

### Desafio 4: Display de Status

Adicione um display OLED que mostra:
- Estado atual (qual sensor está na linha)
- Velocidade
- Número de curvas feitas

---

## Conclusão do Módulo 7

Parabéns! Você construiu um robô autônomo completo que:
- Navega de forma independente seguindo uma linha
- Usa sensores para perceber o ambiente
- Toma decisões em tempo real
- Ajusta seu comportamento com base no feedback dos sensores

Este projeto ensinou conceitos fundamentais de:
- Controle diferencial de motores
- Lógica de decisão baseada em sensores
- Calibração de hardware
- Debugging de sistemas robóticos

No próximo módulo, vamos elevar o nível construindo um **Robô Desviador de Obstáculos** que navega livremente evitando colisões!
