_# Módulo 2.1: Aprofundando no ESP32

## Bem-vindo ao Nível Intermediário!

No Nível 1, você construiu um robô funcional e aprendeu os fundamentos da programação e eletrônica. Agora, no Nível 2, vamos mergulhar em conceitos mais avançados para tornar nossos robôs mais inteligentes e autônomos. Começaremos explorando todo o potencial do **ESP32**, o cérebro poderoso que já estamos usando.

Enquanto o Arduino UNO é fantástico para começar, o ESP32 é uma plataforma muito mais robusta, projetada para a era da **Internet das Coisas (IoT)**. Suas principais vantagens são o processamento dual-core e, mais importante, a conectividade sem fio integrada.

![Pinagem do ESP32](/home/ubuntu/curso_robotica/imagens/esp32_pinout_1.png)
*Figura 1: Diagrama de pinagem detalhado de um ESP32 DevKit, mostrando a vasta quantidade de periféricos disponíveis.*

---

## Arquitetura e Vantagens do ESP32

| Característica | Arduino UNO (ATmega328P) | ESP32 (Xtensa LX6) |
| :--- | :--- | :--- |
| **Processador** | Single-Core 8-bit @ 16 MHz | **Dual-Core 32-bit @ 240 MHz** |
| **Memória RAM** | 2 KB | **520 KB** |
| **Memória Flash** | 32 KB | **4 MB** (ou mais) |
| **Conectividade** | Nenhuma (requer shields) | **Wi-Fi 802.11 b/g/n e Bluetooth 4.2/BLE** |
| **Pinos GPIO** | 14 Digitais, 6 Analógicos | **Até 34**, com múltiplas funções (ADC, DAC, Touch, etc.) |
| **Tensão de Operação** | 5V | **3.3V** |

Essa superioridade em hardware permite que o ESP32 execute tarefas muito mais complexas, como:

-   Hospedar servidores web completos.
-   Processar dados de múltiplos sensores em tempo real.
-   Comunicar-se com outros dispositivos e serviços na nuvem.
-   Executar algoritmos de machine learning (no Nível 3).

### O Sistema Dual-Core

O ESP32 possui dois núcleos de processamento que podem executar tarefas de forma independente. Isso é extremamente útil em robótica. Podemos, por exemplo, dedicar um núcleo para tarefas críticas de tempo real (como o controle dos motores e a leitura de sensores), enquanto o outro núcleo cuida da comunicação Wi-Fi e da interface do usuário. Essa divisão evita que a conexão de rede interfira na estabilidade do robô.

---

## Pinos e Periféricos Especiais

Além dos pinos digitais e analógicos, o ESP32 oferece uma gama de periféricos avançados:

-   **ADC (Conversor Analógico-Digital)**: Múltiplos pinos para ler sensores analógicos com maior precisão.
-   **DAC (Conversor Digital-Analógico)**: Dois pinos que podem gerar um sinal de tensão analógico real, útil para áudio.
-   **Sensores de Toque**: Pinos que podem detectar o toque capacitivo, permitindo criar interfaces sem botões físicos.
-   **LEDC (PWM Avançado)**: O sistema de PWM do ESP32 é muito mais flexível que o do Arduino, permitindo configurar frequência e resolução para até 16 canais, ideal para controlar muitos servos ou LEDs com precisão.
-   **Comunicação**: Além do Serial (`UART`), o ESP32 suporta `I2C` e `SPI`, protocolos para se comunicar com centenas de sensores e outros chips usando poucos fios.

---

## Projeto Prático: Monitor de Status com Web Server

Vamos criar um projeto que demonstra o poder do ESP32. Construiremos um servidor web que não apenas controla um LED, mas também exibe o status de um pino (como um botão) e o tempo que o ESP32 está ligado (`uptime`).

**Materiais Necessários:**
- 1x ESP32 DevKit
- 1x LED
- 1x Resistor de 220Ω
- 1x Botão (Push-button)
- 1x Resistor de 10kΩ (pull-down)
- Protoboard e Fios Jumper

**Montagem do Circuito:**

1.  **LED**: Conecte o anodo (+) do LED ao **GPIO 26** através do resistor de 220Ω. Conecte o catodo (-) ao `GND`.
2.  **Botão**: Conecte um terminal do botão ao **GPIO 25**. No mesmo terminal, conecte o resistor de 10kΩ, e a outra ponta do resistor ao `GND`. Conecte o outro terminal do botão ao `3.3V` do ESP32.

**Código do Projeto:**

```cpp
#include <WiFi.h>

// Configurações de Rede
const char* ssid = "SEU_WIFI"; // <<< COLOQUE O NOME DA SUA REDE
const char* password = "SUA_SENHA"; // <<< COLOQUE A SENHA DA SUA REDE

WiFiServer server(80);

// Pinos dos componentes
const int pinoLed = 26;
const int pinoBotao = 25;

void setup() {
  Serial.begin(115200);
  pinMode(pinoLed, OUTPUT);
  pinMode(pinoBotao, INPUT);

  // Conecta ao Wi-Fi
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String req = client.readStringUntil('\r');

    // Controle do LED
    if (req.indexOf("/led/on") != -1) {
      digitalWrite(pinoLed, HIGH);
    } else if (req.indexOf("/led/off") != -1) {
      digitalWrite(pinoLed, LOW);
    }

    // Monta a página HTML
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.println("<!DOCTYPE html><html><head><title>ESP32 Web Server</title>");
    client.println("<meta http-equiv=\"refresh\" content=\"5\">"); // Atualiza a página a cada 5s
    client.println("</head><body><h1>Status do ESP32</h1>");
    client.print("<p>Uptime: ");
    client.print(millis() / 1000);
    client.println(" segundos</p>");
    client.print("<p>Status do Botão: ");
    client.print(digitalRead(pinoBotao) == HIGH ? "Pressionado" : "Solto");
    client.println("</p>");
    client.println("<p>Controle do LED:</p>");
    client.println("<a href=\"/led/on\"><button>Ligar</button></a>");
    client.println("<a href=\"/led/off\"><button>Desligar</button></a>");
    client.println("</body></html>");
  }
}
```

**Resultado Esperado:**

1.  **Atualize o SSID e a Senha**: Mude `"SEU_WIFI"` e `"SUA_SENHA"` para os dados da sua rede Wi-Fi.
2.  **Carregue o Código**: Envie o código para o ESP32.
3.  **Encontre o IP**: Abra o Monitor Serial. Ele mostrará o endereço de IP que o ESP32 recebeu do seu roteador.
4.  **Acesse o Servidor**: Digite esse endereço de IP no navegador de qualquer dispositivo (computador, celular) conectado à mesma rede Wi-Fi.

Você verá uma página que mostra há quanto tempo o ESP32 está ligado e o estado do botão. A página se atualizará automaticamente a cada 5 segundos. Os botões na página permitirão que você ligue e desligue o LED remotamente.

Este projeto demonstra como o ESP32 pode atuar como um dispositivo de IoT completo, servindo uma interface de usuário e interagindo com o hardware simultaneamente. No próximo módulo, vamos aprofundar na criação de interfaces web mais ricas e na comunicação sem fio.
