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
