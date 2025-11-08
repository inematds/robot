# Módulo 3.3: Processamento de Voz e Áudio

## Dando Ouvidos e Voz ao Robô

Um robô que pode ver e entender o mundo é incrível, mas um robô com o qual podemos **conversar** atinge um novo patamar de interação. Neste módulo, vamos explorar como dar ao nosso robô a capacidade de ouvir comandos (Reconhecimento de Voz) e de responder com sua própria voz (Síntese de Voz).

---

## Captura de Áudio: O Microfone

O primeiro passo para o processamento de voz é capturar o som do ambiente. Para isso, usamos um microfone. O ESP32 é particularmente bom para isso, pois possui ADCs (Conversores Analógico-Digitais) de boa qualidade e suporte para o protocolo **I2S (Inter-IC Sound)**, que é uma interface padrão para lidar com dados de áudio digital de alta qualidade.

-   **Microfones Analógicos**: Módulos simples com um microfone de eletreto. Eles emitem um sinal de tensão analógico que varia com a amplitude do som. Podem ser lidos por um pino ADC do ESP32.
-   **Microfones Digitais I2S**: Módulos mais avançados (como o INMP441 ou o SPH0645) que já digitalizam o som e o enviam via protocolo I2S. Eles oferecem uma qualidade de áudio muito superior e liberam os ADCs para outras tarefas.

![Diagrama de Voz](/home/ubuntu/curso_robotica/imagens/diagrama_voz.png)
*Figura 1: Fluxo de um sistema de interação por voz: o microfone captura o áudio, que é processado para reconhecimento de fala. A resposta é gerada como texto e convertida em áudio por um sintetizador de voz.*

---

## Reconhecimento de Voz (Speech-to-Text)

Converter o áudio capturado em texto é uma tarefa complexa de IA. Existem duas abordagens principais:

### 1. Reconhecimento Baseado em Nuvem

Serviços como **Google Cloud Speech-to-Text** ou **Azure Cognitive Services** oferecem APIs extremamente precisas para transcrição de áudio. 

-   **Como funciona**: O ESP32 captura um trecho de áudio, envia-o para o servidor da API via internet e recebe de volta o texto transcrito.
-   **Vantagens**: Altíssima precisão, suporte a múltiplos idiomas, não exige poder de processamento local.
-   **Desvantagens**: Requer conexão constante com a internet, pode ter custos associados e introduz latência (atraso).

### 2. Reconhecimento Offline (Edge)

Para robôs que precisam operar sem internet, podemos usar motores de reconhecimento de voz que rodam localmente. 

-   **Reconhecimento por Palavra-Chave (Keyword Spotting)**: Modelos de IA muito pequenos e eficientes (como os treinados com TensorFlow Lite) podem ser executados diretamente no ESP32 para reconhecer um conjunto limitado de comandos, como "Ligar", "Desligar", "Frente". É ideal para comandos simples e rápidos.
-   **Reconhecimento Contínuo Offline**: Frameworks como o **Vosk** ou o **Picovoice** podem ser executados em plataformas mais poderosas como o Raspberry Pi para transcrever a fala completa sem depender da nuvem.

---

## Síntese de Voz (Text-to-Speech - TTS)

Depois que o robô entende um comando e decide uma resposta, ele pode comunicá-la de volta usando a síntese de voz.

-   **Como funciona**: Um software de TTS converte uma string de texto (ex: "Ok, ligando o motor") em dados de áudio (um arquivo .wav ou .mp3).
-   **Abordagens**:
    -   **APIs na Nuvem**: Serviços como Google Text-to-Speech ou Amazon Polly geram áudio de altíssima qualidade. O robô envia o texto e recebe o arquivo de áudio para tocar.
    -   **TTS Local**: Em um Raspberry Pi, podemos usar softwares como o `espeak` ou o `pico2wave` para gerar uma voz sintetizada localmente. A qualidade é mais robótica, mas funciona offline.
    -   **ESP32**: Embora mais limitado, o ESP32 pode tocar arquivos de áudio pré-gravados de um cartão SD ou até mesmo usar bibliotecas mais simples de TTS para gerar uma fala básica.

---

## Projeto Prático: Controle de LED por Voz com ESP32 e IFTTT

Vamos criar um projeto que usa serviços na nuvem para um resultado impressionante com hardware simples. Usaremos o **Google Assistente** no seu celular para enviar comandos de voz para o ESP32 através de um serviço gratuito chamado **IFTTT (If This Then That)**.

**Como vai funcionar:**
1.  Você diz: "Ok Google, ligar o LED do robô".
2.  O Google Assistente reconhece o comando.
3.  O IFTTT detecta a frase e faz uma requisição web (um *webhook*) para um serviço chamado **Adafruit IO**.
4.  O Adafruit IO (uma plataforma de IoT gratuita) atualiza o estado de um "feed" (uma variável na nuvem).
5.  Nosso ESP32 estará constantemente monitorando esse feed. Quando ele vê a mudança, ele executa a ação correspondente (ligar o LED).

**Materiais:**
- 1x ESP32 DevKit
- 1x LED e 1x Resistor de 220Ω

**Configuração dos Serviços (Passos Resumidos):**

1.  **Crie uma conta no Adafruit IO**: Vá para [io.adafruit.com](https://io.adafruit.com), crie uma conta e um novo "Feed" chamado `led-status`.
2.  **Crie uma conta no IFTTT**: Vá para [ifttt.com](https://ifttt.com) e crie uma nova "Applet".
    -   **If This (Se Isso)**: Escolha o serviço "Google Assistant" e a opção "Say a simple phrase". Configure a frase, como "Ligar o LED do robô".
    -   **Then That (Então Aquilo)**: Escolha o serviço "Adafruit" e a opção "Send data to Adafruit IO". Selecione o feed `led-status` e o dado a ser enviado (ex: a palavra `ON`).
    -   Crie uma segunda applet para o comando de desligar, enviando a palavra `OFF`.

**Código do Projeto:**

Você precisará instalar a biblioteca **"Adafruit MQTT Library"** no Arduino IDE.

```cpp
#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// --- Configuração Wi-Fi ---
#define WLAN_SSID       "SEU_WIFI"
#define WLAN_PASS       "SUA_SENHA"

// --- Configuração Adafruit IO ---
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "SEU_USUARIO_ADAFRUIT"
#define AIO_KEY         "SUA_CHAVE_ADAFRUIT"

// --- Pinos ---
const int pinoLed = 26;

// --- Objetos MQTT ---
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
Adafruit_MQTT_Subscribe ledStatus = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/led-status");

void setup() {
  pinMode(pinoLed, OUTPUT);
  Serial.begin(115200);

  // Conecta ao Wi-Fi
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }

  // Assina o feed do Adafruit IO
  mqtt.subscribe(&ledStatus);
}

void loop() {
  // Conecta/mantém conexão com o servidor MQTT
  MQTT_connect();

  // Espera por novas mensagens
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &ledStatus) {
      Serial.print("Recebido: ");
      Serial.println((char *)ledStatus.lastread);

      if (strcmp((char *)ledStatus.lastread, "ON") == 0) {
        digitalWrite(pinoLed, HIGH);
      }
      if (strcmp((char *)ledStatus.lastread, "OFF") == 0) {
        digitalWrite(pinoLed, LOW);
      }
    }
  }
}

void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) { return; }
  while ((ret = mqtt.connect()) != 0) {
       mqtt.disconnect();
       delay(5000);
  }
}
```

**Resultado Esperado:**

Após carregar o código (com suas credenciais de Wi-Fi e Adafruit IO), o ESP32 se conectará à internet. Agora, pegue seu celular e diga: **"Ok Google, ligar o LED do robô"**. Após alguns segundos, o LED conectado ao seu ESP32 deverá acender! Diga o comando de desligar, e ele apagará.

Você acabou de controlar um hardware no mundo físico usando sua voz, através de uma cadeia de serviços na nuvem. Este é um exemplo poderoso de como a IoT e a IA se unem na robótica moderna. No próximo módulo, veremos como combinar plataformas para tarefas ainda mais complexas.
