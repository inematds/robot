_# Módulo 2.2: Comunicação Sem Fio e Interfaces Web

## Wi-Fi: O Coração da Conectividade

No projeto anterior, usamos o ESP32 no modo **Station (STA)**, onde ele se conecta a uma rede Wi-Fi existente, como um celular ou computador. No projeto do Nível 1 (Rover de Papel), usamos o modo **Access Point (AP)**, onde o ESP32 cria sua própria rede Wi-Fi.

Compreender a diferença é fundamental para a robótica conectada:

| Modo | Descrição | Vantagens | Desvantagens |
| :--- | :--- | :--- | :--- |
| **Station (STA)** | O ESP32 é um **cliente** em uma rede maior (seu roteador de casa). | Acesso à internet, comunicação com outros dispositivos na rede. | Depende de uma rede Wi-Fi existente. |
| **Access Point (AP)** | O ESP32 é o **roteador**, criando sua própria rede. | Autocontido, funciona em qualquer lugar sem infraestrutura externa. | Sem acesso à internet, apenas dispositivos conectados diretamente a ele podem se comunicar. |
| **AP + STA** | Modo híbrido onde o ESP32 cria sua rede e simultaneamente se conecta a outra. | O melhor dos dois mundos: oferece um ponto de acesso para configuração e ainda se conecta à internet. | Mais complexo de gerenciar. |

Para robôs móveis, o modo AP é excelente para controle direto em campo, enquanto o modo STA é ideal para robôs que precisam buscar informações da internet ou serem controlados de qualquer lugar do mundo.

---

## HTTP e a Web: Como Funciona a Comunicação

Quando você acessa uma página no seu navegador, seu dispositivo está fazendo uma **requisição HTTP** para um servidor. O servidor então envia de volta uma **resposta HTTP**, que contém o conteúdo da página (geralmente HTML, CSS e JavaScript).

-   **Requisição (Request)**: O cliente (navegador) pede um recurso. Ex: `GET /led/on`.
-   **Resposta (Response)**: O servidor (ESP32) envia o recurso ou uma confirmação. Ex: `HTTP/1.1 200 OK` seguido do código HTML.

Nosso ESP32 atua como um mini servidor web. Ele escuta por requisições e responde de acordo com a lógica que programamos.

### Criando Interfaces Web Melhores

No código anterior, o HTML e o CSS estavam misturados em uma única `String` no código C++, o que é difícil de manter. Uma abordagem muito mais limpa é armazenar o HTML em uma variável separada usando a notação `R"rawliteral(...)rawliteral"` do C++. Isso permite escrever HTML de forma muito mais natural.

![Robô com Interface Web](/home/ubuntu/curso_robotica/imagens/esp32cam_robot.jpg)
*Figura 1: Um robô com ESP32-CAM sendo controlado por uma interface web sofisticada em um smartphone.*

---

## Projeto Prático: Dashboard de Controle Avançado

Vamos evoluir nosso web server para um dashboard mais completo. Ele terá botões que mudam de cor para refletir o estado do LED e usará um pouco de JavaScript para enviar comandos sem recarregar a página (uma técnica conhecida como **AJAX**), tornando a experiência muito mais fluida.

**Materiais:**
- Os mesmos do projeto anterior (Módulo 2.1).

**Montagem:**
- A mesma do projeto anterior.

**Código do Projeto:**

Este código é mais longo, mas a maior parte é a página HTML e o JavaScript. A lógica no ESP32 continua simples.

```cpp
#include <WiFi.h>

// ===== Configurações de Rede =====
const char* ssid = "SEU_WIFI";
const char* password = "SUA_SENHA";
WiFiServer server(80);

// ===== Pinos e Estado =====
const int pinoLed = 26;
bool estadoLed = false;

// ===== Página HTML com CSS e JavaScript =====
const char* HTML_PAGE = R"rawliteral(
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>ESP32 Dashboard</title>
<style>
  body { font-family: system-ui, sans-serif; text-align:center; margin: 24px; background-color: #f0f0f0; }
  h1 { color: #333; }
  .card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; margin: 20px auto; }
  button { font-size: 18px; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; transition: background-color 0.3s; }
  .on { background-color: #2ecc71; color: white; }
  .off { background-color: #e74c3c; color: white; }
</style>
</head>
<body>
  <h1>Dashboard do Robô</h1>
  <div class="card">
    <h2>Controle do LED</h2>
    <p>O LED está atualmente: <b id="status">DESLIGADO</b></p>
    <button id="btnLigar" class="on" onclick="sendCommand('on')">LIGAR</button>
    <button id="btnDesligar" class="off" onclick="sendCommand('off')">DESLIGAR</button>
  </div>
<script>
function sendCommand(cmd) {
  fetch('/led/' + cmd)
    .then(response => response.text())
    .then(data => {
      document.getElementById('status').innerText = data;
    });
}
</script>
</body>
</html>
)rawliteral";

void setup() {
  pinMode(pinoLed, OUTPUT);
  digitalWrite(pinoLed, LOW);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  server.begin();
}

void handleRequest(WiFiClient& client, String req) {
  String response_content_type = "text/html";
  String response_body = "";

  if (req.startsWith("GET /led/on")) {
    estadoLed = true;
    digitalWrite(pinoLed, HIGH);
    response_content_type = "text/plain";
    response_body = "LIGADO";
  } else if (req.startsWith("GET /led/off")) {
    estadoLed = false;
    digitalWrite(pinoLed, LOW);
    response_content_type = "text/plain";
    response_body = "DESLIGADO";
  } else {
    response_body = HTML_PAGE;
  }

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: " + response_content_type + "; charset=utf-8");
  client.println("Connection: close\r\n");
  client.print(response_body);
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;
  String req = client.readStringUntil('\r');
  while (client.available()) client.read();
  handleRequest(client, req);
  delay(1);
}
```

**Como o Código Funciona:**

1.  **HTML/CSS**: A página agora tem um estilo mais agradável, com um "card" para organizar o conteúdo.
2.  **JavaScript (AJAX)**: A função `sendCommand(cmd)` usa a API `fetch()` do navegador. Quando um botão é clicado, o JavaScript envia a requisição (ex: `/led/on`) para o ESP32 em segundo plano. Ele não recarrega a página inteira.
3.  **Lógica do ESP32**: O servidor agora é mais inteligente. Se ele recebe um comando `/led/on` ou `/led/off`, ele muda o estado do LED e responde apenas com o novo status em texto puro (ex: "LIGADO"). Se ele recebe qualquer outra requisição, ele responde com a página HTML completa.
4.  **Atualização da Interface**: O JavaScript recebe a resposta de texto puro e atualiza apenas o `<span>` com o ID "status", mudando o texto na tela sem piscar.

**Resultado Esperado:**

Ao acessar o IP do seu ESP32, você verá um dashboard mais profissional. Clicar nos botões "LIGAR" e "DESLIGAR" mudará o estado do LED instantaneamente, e o texto de status na página será atualizado sem que a página inteira precise ser recarregada. Esta é a base para criar interfaces de controle de robôs muito mais responsivas e agradáveis de usar.

No próximo módulo, vamos adicionar mais "sentidos" ao nosso robô com sensores avançados.
