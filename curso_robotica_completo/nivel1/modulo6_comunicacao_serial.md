# Módulo 1.6: Comunicação Serial

## O Que é Comunicação Serial?

Até agora, nossos robôs funcionavam de forma independente, sem nos informar o que estava acontecendo "dentro" deles. A **comunicação serial** é a ponte que permite que microcontroladores como o ESP32 conversem com computadores, outros dispositivos eletrônicos e até mesmo entre si.

A palavra "serial" significa que os dados são enviados **um bit por vez**, em sequência, através de um ou mais fios. Isso contrasta com a comunicação "paralela", onde múltiplos bits são enviados simultaneamente através de múltiplos fios.

Imagine a comunicação serial como um túnel estreito onde os carros (bits de dados) passam um de cada vez, enquanto a comunicação paralela seria como uma rodovia de várias pistas onde os carros podem passar lado a lado.

---

## Por Que a Comunicação Serial é Importante em Robótica?

A comunicação serial é fundamental para:

- **Depuração**: Ver o que o robô está "pensando" através do Serial Monitor
- **Telemetria**: Enviar dados de sensores para um computador para análise
- **Controle Remoto**: Receber comandos de um computador ou smartphone
- **Data Logging**: Armazenar dados de sensores em um cartão SD
- **Comunicação entre Dispositivos**: Conectar múltiplos microcontroladores ou sensores inteligentes

---

## Módulo 6.1: UART e o Serial Monitor

### O Que é UART?

**UART** (Universal Asynchronous Receiver-Transmitter) é o protocolo de comunicação serial mais básico e amplamente usado. "Asynchronous" significa que não há um sinal de clock compartilhado entre os dispositivos - eles devem concordar previamente sobre a velocidade de transmissão.

### Componentes da Comunicação UART

Uma comunicação UART usa, no mínimo, três fios:

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Fio</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Nome</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Função</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>TX</strong></td>
<td class="border border-gray-300 px-4 py-2">Transmit (Transmitir)</td>
<td class="border border-gray-300 px-4 py-2">Envia dados do dispositivo</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>RX</strong></td>
<td class="border border-gray-300 px-4 py-2">Receive (Receber)</td>
<td class="border border-gray-300 px-4 py-2">Recebe dados para o dispositivo</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>GND</strong></td>
<td class="border border-gray-300 px-4 py-2">Ground (Terra)</td>
<td class="border border-gray-300 px-4 py-2">Referência comum de tensão</td>
</tr>
</tbody>
</table>

**Regra de Ouro**: O TX de um dispositivo deve ser conectado ao RX do outro, e vice-versa. Pense nisso como uma conversa: quando você fala (TX), a outra pessoa escuta (RX).

### Baud Rate (Taxa de Transmissão)

O **Baud Rate** é a velocidade de comunicação, medida em bits por segundo (bps). Ambos os dispositivos devem usar o mesmo Baud Rate. Os valores mais comuns são:

- 9600 bps (padrão, confiável)
- 115200 bps (mais rápido, usado em projetos avançados)

### Usando o Serial Monitor

O Arduino IDE possui uma ferramenta chamada **Serial Monitor** que permite visualizar e enviar dados pela porta serial USB. Ela é acessada através do ícone de lupa no canto superior direito ou pelo atalho `Ctrl+Shift+M`.

---

## Projeto Prático 1: Hello World Serial

Vamos começar com o exemplo mais básico: fazer o ESP32 enviar uma mensagem para o computador.

**Código:**

```cpp
void setup() {
  // Inicializa a comunicação serial a 115200 bps
  Serial.begin(115200);

  // Aguarda a conexão serial (útil para algumas placas)
  delay(1000);

  Serial.println("=================================");
  Serial.println("   Bem-vindo ao ESP32!          ");
  Serial.println("   Sistema Iniciado com Sucesso ");
  Serial.println("=================================");
}

void loop() {
  Serial.print("Tempo desde o início (ms): ");
  Serial.println(millis()); // millis() retorna o tempo desde que a placa ligou

  delay(1000); // Aguarda 1 segundo entre as mensagens
}
```

**Como Testar:**

1. Carregue o código no ESP32
2. Abra o Serial Monitor (`Ferramentas > Monitor Serial`)
3. Certifique-se de que o Baud Rate no canto inferior direito está configurado para **115200**
4. Você verá a mensagem de boas-vindas seguida de atualizações a cada segundo

**Diferença entre `print()` e `println()`:**

- `Serial.print()`: Imprime o texto na mesma linha
- `Serial.println()`: Imprime o texto e pula para a próxima linha (adiciona `\n`)

---

## Projeto Prático 2: Controle por Comandos Seriais

Agora vamos fazer o inverso: enviar comandos do computador para o ESP32 controlar um LED.

**Materiais:**
- 1x ESP32
- 1x LED
- 1x Resistor 220Ω
- Protoboard e jumpers

**Montagem:**
- Conecte o LED ao GPIO 25 através do resistor
- Catodo do LED ao GND

**Código:**

```cpp
const int pinoLED = 25;

void setup() {
  Serial.begin(115200);
  pinMode(pinoLED, OUTPUT);

  Serial.println("\n=== Sistema de Controle por Serial ===");
  Serial.println("Comandos disponíveis:");
  Serial.println("  ON  - Liga o LED");
  Serial.println("  OFF - Desliga o LED");
  Serial.println("  STATUS - Mostra o estado atual");
  Serial.println("=====================================\n");
}

void loop() {
  // Verifica se há dados disponíveis para leitura
  if (Serial.available() > 0) {
    // Lê a string enviada até encontrar '\n'
    String comando = Serial.readStringUntil('\n');

    // Remove espaços em branco no início e fim
    comando.trim();

    // Converte para maiúsculas para facilitar a comparação
    comando.toUpperCase();

    // Processa o comando
    if (comando == "ON") {
      digitalWrite(pinoLED, HIGH);
      Serial.println("✓ LED ligado!");
    }
    else if (comando == "OFF") {
      digitalWrite(pinoLED, LOW);
      Serial.println("✓ LED desligado!");
    }
    else if (comando == "STATUS") {
      if (digitalRead(pinoLED) == HIGH) {
        Serial.println("Estado: LED está LIGADO");
      } else {
        Serial.println("Estado: LED está DESLIGADO");
      }
    }
    else {
      Serial.println("✗ Comando não reconhecido: " + comando);
      Serial.println("Use: ON, OFF ou STATUS");
    }
  }
}
```

**Como Usar:**

1. Carregue o código e abra o Serial Monitor
2. No campo de entrada do Serial Monitor, digite `ON` e pressione Enter
3. O LED deve acender e você verá a confirmação
4. Experimente os comandos `OFF` e `STATUS`

**Conceitos Importantes:**

- `Serial.available()`: Retorna o número de bytes disponíveis para leitura
- `Serial.readStringUntil('\n')`: Lê caracteres até encontrar uma nova linha
- `String.trim()`: Remove espaços em branco
- `String.toUpperCase()`: Converte para maiúsculas

---

## Módulo 6.2: Protocolo I2C

### O Que é I2C?

**I2C** (Inter-Integrated Circuit), pronunciado "I-squared-C" ou "I-two-C", é um protocolo de comunicação que permite conectar **múltiplos dispositivos** usando apenas **dois fios** para dados.

### Como o I2C Funciona?

O I2C usa um sistema de **mestre-escravo** (master-slave):

- **Mestre** (Master): Geralmente o microcontrolador (ESP32), que inicia e controla a comunicação
- **Escravo** (Slave): Sensores, displays ou outros dispositivos que respondem às solicitações do mestre

**Fios do I2C:**

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Fio</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Nome Completo</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Função</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>SDA</strong></td>
<td class="border border-gray-300 px-4 py-2">Serial Data</td>
<td class="border border-gray-300 px-4 py-2">Linha de dados bidirecional</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>SCL</strong></td>
<td class="border border-gray-300 px-4 py-2">Serial Clock</td>
<td class="border border-gray-300 px-4 py-2">Linha de clock gerada pelo mestre</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>GND</strong></td>
<td class="border border-gray-300 px-4 py-2">Ground</td>
<td class="border border-gray-300 px-4 py-2">Terra comum</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>VCC</strong></td>
<td class="border border-gray-300 px-4 py-2">Power</td>
<td class="border border-gray-300 px-4 py-2">Alimentação (3.3V ou 5V)</td>
</tr>
</tbody>
</table>

### Endereçamento I2C

Cada dispositivo I2C tem um **endereço único** (geralmente de 7 bits), permitindo que o mestre especifique com qual dispositivo deseja falar. É como um sistema de apartamentos: você precisa saber o número do apartamento para tocar a campainha certa.

**Pinos I2C no ESP32:**
- SDA: GPIO 21
- SCL: GPIO 22

---

## Projeto Prático 3: Scanner I2C

Antes de usar um dispositivo I2C, é útil descobrir seu endereço. Vamos criar um scanner que detecta todos os dispositivos I2C conectados.

**Código:**

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA = GPIO 21, SCL = GPIO 22

  Serial.println("\n=== Scanner I2C ===");
  Serial.println("Procurando dispositivos I2C...\n");
}

void loop() {
  byte erro, endereco;
  int dispositivosEncontrados = 0;

  Serial.println("Escaneando...");

  // Testa endereços de 1 a 127
  for(endereco = 1; endereco < 127; endereco++) {
    Wire.beginTransmission(endereco);
    erro = Wire.endTransmission();

    if (erro == 0) {
      Serial.print("Dispositivo I2C encontrado no endereço 0x");
      if (endereco < 16) Serial.print("0");
      Serial.print(endereco, HEX);
      Serial.println("!");

      dispositivosEncontrados++;
    }
    else if (erro == 4) {
      Serial.print("Erro desconhecido no endereço 0x");
      if (endereco < 16) Serial.print("0");
      Serial.println(endereco, HEX);
    }
  }

  if (dispositivosEncontrados == 0) {
    Serial.println("Nenhum dispositivo I2C encontrado.");
    Serial.println("Verifique as conexões!");
  }
  else {
    Serial.print("\nTotal: ");
    Serial.print(dispositivosEncontrados);
    Serial.println(" dispositivo(s) encontrado(s).\n");
  }

  delay(5000); // Aguarda 5 segundos antes de escanear novamente
}
```

**Como Usar:**

1. Conecte um dispositivo I2C ao ESP32 (como um display OLED ou sensor)
2. Carregue o código
3. Abra o Serial Monitor
4. O scanner mostrará os endereços encontrados em formato hexadecimal (ex: 0x3C)

---

## Projeto Prático 4: Display OLED I2C

Vamos usar o que aprendemos para controlar um display OLED usando I2C.

**Materiais:**
- 1x ESP32
- 1x Display OLED 0.96" I2C (128x64 pixels, geralmente endereço 0x3C)
- Fios jumper

**Montagem:**
- OLED VCC → ESP32 3.3V
- OLED GND → ESP32 GND
- OLED SDA → GPIO 21
- OLED SCL → GPIO 22

**Instalação da Biblioteca:**
1. Vá em `Ferramentas > Gerenciar Bibliotecas`
2. Procure por "Adafruit SSD1306"
3. Instale a biblioteca "Adafruit SSD1306 by Adafruit"
4. Instale também a dependência "Adafruit GFX Library"

**Código:**

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Configuração do display
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1  // Reset pin (ou -1 se compartilhado com ESP32)
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);

  // Inicializa o display
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println("Falha ao inicializar o display OLED!");
    while(1); // Para o programa
  }

  // Limpa o buffer
  display.clearDisplay();

  // Configurações de texto
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);

  // Escreve no display
  display.println("Robo");
  display.println("Expert");
  display.setTextSize(1);
  display.println("");
  display.println("I2C Funcionando!");

  // Envia o buffer para o display
  display.display();
}

void loop() {
  // Exibe um contador
  static int contador = 0;

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Sistema Ativo");
  display.println("");

  display.setTextSize(2);
  display.print("Count: ");
  display.println(contador);

  display.display();

  contador++;
  delay(1000);
}
```

**Resultado Esperado:**

O display OLED mostrará o texto "Robo Expert" e um contador que aumenta a cada segundo. Você acabou de dominar a comunicação I2C!

---

## Módulo 6.3: Protocolo SPI

### O Que é SPI?

**SPI** (Serial Peripheral Interface) é um protocolo de comunicação serial **síncrono** de alta velocidade. Ele é mais rápido que o I2C, mas requer mais fios.

### Como o SPI Funciona?

O SPI também usa um sistema mestre-escravo, mas com mais linhas de comunicação:

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Fio</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Nome Completo</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Função</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>MOSI</strong></td>
<td class="border border-gray-300 px-4 py-2">Master Out Slave In</td>
<td class="border border-gray-300 px-4 py-2">Dados do mestre para o escravo</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>MISO</strong></td>
<td class="border border-gray-300 px-4 py-2">Master In Slave Out</td>
<td class="border border-gray-300 px-4 py-2">Dados do escravo para o mestre</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>SCK</strong></td>
<td class="border border-gray-300 px-4 py-2">Serial Clock</td>
<td class="border border-gray-300 px-4 py-2">Clock gerado pelo mestre</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>CS/SS</strong></td>
<td class="border border-gray-300 px-4 py-2">Chip Select / Slave Select</td>
<td class="border border-gray-300 px-4 py-2">Seleciona qual escravo está ativo</td>
</tr>
</tbody>
</table>

**Pinos SPI no ESP32:**
- MOSI: GPIO 23
- MISO: GPIO 19
- SCK: GPIO 18
- CS: Qualquer GPIO digital (você escolhe)

### SPI vs I2C: Quando Usar Cada Um?

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Característica</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">I2C</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">SPI</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Velocidade</strong></td>
<td class="border border-gray-300 px-4 py-2">Até 400 kHz (padrão)</td>
<td class="border border-gray-300 px-4 py-2">Até 80 MHz no ESP32</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Fios Necessários</strong></td>
<td class="border border-gray-300 px-4 py-2">2 (SDA, SCL)</td>
<td class="border border-gray-300 px-4 py-2">4+ (MOSI, MISO, SCK, CS)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Dispositivos</strong></td>
<td class="border border-gray-300 px-4 py-2">Muitos no mesmo barramento</td>
<td class="border border-gray-300 px-4 py-2">1 CS por dispositivo</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Melhor Para</strong></td>
<td class="border border-gray-300 px-4 py-2">Sensores, displays simples</td>
<td class="border border-gray-300 px-4 py-2">Cartões SD, displays TFT, módulos RF</td>
</tr>
</tbody>
</table>

---

## Projeto Prático 5: Data Logger com Cartão SD (SPI)

Vamos criar um sistema que grava dados de sensores em um arquivo de texto no cartão SD.

**Materiais:**
- 1x ESP32
- 1x Módulo Leitor de Cartão SD
- 1x Cartão microSD (formatado em FAT32)
- 1x Sensor de temperatura DHT22 (opcional, usaremos dados simulados)

**Montagem:**
- SD VCC → ESP32 5V
- SD GND → ESP32 GND
- SD MISO → GPIO 19
- SD MOSI → GPIO 23
- SD SCK → GPIO 18
- SD CS → GPIO 5

**Código:**

```cpp
#include <SPI.h>
#include <SD.h>

// Pino CS do módulo SD
const int CS_PIN = 5;

File arquivoDados;

void setup() {
  Serial.begin(115200);

  Serial.println("=== Sistema de Data Logger ===");

  // Inicializa o cartão SD
  if (!SD.begin(CS_PIN)) {
    Serial.println("ERRO: Falha ao inicializar o cartão SD!");
    Serial.println("Verifique se o cartão está inserido.");
    while (1);
  }

  Serial.println("✓ Cartão SD inicializado com sucesso!");

  // Verifica o tipo do cartão
  uint8_t tipoCartao = SD.cardType();
  if (tipoCartao == CARD_NONE) {
    Serial.println("Nenhum cartão SD detectado!");
    return;
  }

  Serial.print("Tipo do Cartão: ");
  if (tipoCartao == CARD_MMC) Serial.println("MMC");
  else if (tipoCartao == CARD_SD) Serial.println("SD");
  else if (tipoCartao == CARD_SDHC) Serial.println("SDHC");

  // Mostra o tamanho do cartão
  uint64_t tamanhoCartao = SD.cardSize() / (1024 * 1024);
  Serial.print("Tamanho do Cartão: ");
  Serial.print(tamanhoCartao);
  Serial.println(" MB");

  Serial.println("\nIniciando gravação de dados...\n");
}

void loop() {
  // Simula leituras de sensores
  float temperatura = 20.0 + random(-50, 50) / 10.0; // Temperatura entre 15°C e 25°C
  float umidade = 60.0 + random(-100, 100) / 10.0;   // Umidade entre 50% e 70%

  // Obtém o timestamp
  unsigned long timestamp = millis();

  // Cria string com os dados
  String linha = String(timestamp) + "," +
                 String(temperatura, 2) + "," +
                 String(umidade, 2);

  // Abre o arquivo para adicionar dados (append)
  arquivoDados = SD.open("/dados.txt", FILE_APPEND);

  if (arquivoDados) {
    arquivoDados.println(linha);
    arquivoDados.close();

    Serial.println("✓ Dados gravados: " + linha);
  } else {
    Serial.println("✗ Erro ao abrir o arquivo!");
  }

  delay(5000); // Grava a cada 5 segundos
}
```

**Como Usar:**

1. Insira um cartão microSD formatado (FAT32) no módulo
2. Carregue o código
3. Abra o Serial Monitor
4. O sistema gravará dados simulados de temperatura e umidade a cada 5 segundos
5. Após alguns minutos, desligue o ESP32 e insira o cartão SD no computador
6. Abra o arquivo `dados.txt` - você verá um log CSV dos dados!

**Formato dos Dados (CSV):**
```
1234,22.34,65.12
6234,21.98,64.87
11234,22.15,65.34
```

Você pode abrir este arquivo no Excel ou Google Sheets para análise!

---

## Módulo 6.4: Comparação de Protocolos

### Tabela Resumo

<table class="w-full border-collapse border border-gray-300">
<thead class="bg-gray-100"><tr>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">Protocolo</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">UART</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">I2C</th>
<th class="border border-gray-300 px-4 py-2 text-left font-semibold">SPI</th>
</tr></thead>
<tbody>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Fios</strong></td>
<td class="border border-gray-300 px-4 py-2">2 (TX, RX)</td>
<td class="border border-gray-300 px-4 py-2">2 (SDA, SCL)</td>
<td class="border border-gray-300 px-4 py-2">4+ (MOSI, MISO, SCK, CS)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Velocidade</strong></td>
<td class="border border-gray-300 px-4 py-2">9600 - 115200 bps</td>
<td class="border border-gray-300 px-4 py-2">100 - 400 kHz</td>
<td class="border border-gray-300 px-4 py-2">Até 80 MHz</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Distância</strong></td>
<td class="border border-gray-300 px-4 py-2">Longa (até 15m)</td>
<td class="border border-gray-300 px-4 py-2">Curta (< 1m)</td>
<td class="border border-gray-300 px-4 py-2">Muito curta (< 50cm)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Dispositivos</strong></td>
<td class="border border-gray-300 px-4 py-2">1-para-1</td>
<td class="border border-gray-300 px-4 py-2">Múltiplos (127 max)</td>
<td class="border border-gray-300 px-4 py-2">Múltiplos (1 CS cada)</td>
</tr>
<tr>
<td class="border border-gray-300 px-4 py-2"><strong>Uso Típico</strong></td>
<td class="border border-gray-300 px-4 py-2">Debug, GPS, Bluetooth</td>
<td class="border border-gray-300 px-4 py-2">Sensores, OLED, RTC</td>
<td class="border border-gray-300 px-4 py-2">SD, TFT, RF, ADC rápidos</td>
</tr>
</tbody>
</table>

---

## Projeto Final: Sistema de Telemetria Completo

Vamos integrar tudo em um projeto final que combina UART, I2C e conceitos de data logging.

**Objetivo:** Criar um sistema que lê dados de sensores, exibe em um display OLED (I2C) e envia telemetria para o Serial Monitor (UART).

**Materiais:**
- 1x ESP32
- 1x Display OLED I2C
- 1x Sensor ultrassônico HC-SR04
- 1x LED
- 1x Resistor 220Ω

**Código:**

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Configuração do OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Configuração do sensor ultrassônico
const int trigPin = 26;
const int echoPin = 25;

// LED de alerta
const int ledPin = 27;

// Variáveis
float distancia = 0;
unsigned long ultimaLeitura = 0;
const int intervaloLeitura = 500; // 500ms entre leituras

void setup() {
  // Inicializa Serial
  Serial.begin(115200);
  Serial.println("\n=== Sistema de Telemetria ===");
  Serial.println("Timestamp(ms), Distancia(cm), Status");

  // Inicializa pinos
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  // Inicializa OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println("ERRO: Display OLED não encontrado!");
    while(1);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Sistema Ativo");
  display.display();
}

void loop() {
  unsigned long tempoAtual = millis();

  // Realiza leitura periódica
  if (tempoAtual - ultimaLeitura >= intervaloLeitura) {
    ultimaLeitura = tempoAtual;

    // Lê o sensor ultrassônico
    distancia = lerDistancia();

    // Determina o status
    String status;
    if (distancia < 10) {
      status = "CRITICO";
      digitalWrite(ledPin, HIGH);
    } else if (distancia < 30) {
      status = "ALERTA";
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
    } else {
      status = "NORMAL";
      digitalWrite(ledPin, LOW);
    }

    // Envia telemetria via Serial (UART)
    Serial.print(tempoAtual);
    Serial.print(", ");
    Serial.print(distancia, 2);
    Serial.print(", ");
    Serial.println(status);

    // Atualiza o display (I2C)
    atualizarDisplay(distancia, status);
  }
}

float lerDistancia() {
  // Envia pulso
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Lê o eco
  long duracao = pulseIn(echoPin, HIGH, 30000); // Timeout de 30ms

  // Calcula a distância em cm
  float dist = duracao * 0.034 / 2;

  // Se o timeout foi atingido
  if (duracao == 0) {
    return 999; // Indica erro ou distância muito grande
  }

  return dist;
}

void atualizarDisplay(float dist, String status) {
  display.clearDisplay();

  // Título
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Telemetria v1.0");
  display.drawLine(0, 10, 127, 10, SSD1306_WHITE);

  // Distância
  display.setCursor(0, 16);
  display.print("Distancia:");
  display.setTextSize(2);
  display.setCursor(0, 28);
  if (dist < 999) {
    display.print(dist, 1);
    display.println(" cm");
  } else {
    display.println("---");
  }

  // Status
  display.setTextSize(1);
  display.setCursor(0, 50);
  display.print("Status: ");
  display.println(status);

  display.display();
}
```

**Resultado Esperado:**

- O display OLED mostra a distância medida e o status
- O Serial Monitor exibe os dados em formato CSV para análise
- O LED acende quando objetos estão próximos
- Você tem um sistema completo de telemetria!

**Desafios de Extensão:**

1. Adicione um botão para pausar/retomar as leituras
2. Calcule a média das últimas 10 leituras para suavizar os dados
3. Implemente logging em cartão SD
4. Crie gráficos em tempo real usando Processing ou Python

---

## Conclusão do Módulo 6

Parabéns! Você dominou os três principais protocolos de comunicação serial:

- **UART**: Para comunicação simples ponto-a-ponto (debug, GPS, Bluetooth)
- **I2C**: Para conectar múltiplos sensores e displays com apenas 2 fios
- **SPI**: Para comunicação de alta velocidade (SD, displays TFT)

Estes protocolos são a base de praticamente todos os projetos de robótica e IoT. No próximo módulo, usaremos todas essas habilidades para construir nosso primeiro robô autônomo completo: o Robô Seguidor de Linha!
