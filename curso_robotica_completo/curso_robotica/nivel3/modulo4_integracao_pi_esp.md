# Módulo 3.4: Integração Raspberry Pi + Arduino/ESP32

## O Cérebro Dividido: A Arquitetura Híbrida

Até agora, tentamos fazer tudo em uma única placa, seja um ESP32 ou um Raspberry Pi. No entanto, na robótica avançada, uma das arquiteturas mais poderosas e eficientes é a **arquitetura híbrida** ou de **processamento distribuído**. A ideia é simples: usar o melhor de cada plataforma para a tarefa em que ela se destaca.

-   **Raspberry Pi (O Cérebro de Alto Nível)**: Como um computador Linux completo, o Raspberry Pi é perfeito para tarefas que exigem grande poder de processamento, como visão computacional com OpenCV, execução de modelos de IA complexos, planejamento de trajetória, tomada de decisões estratégicas e hospedagem de interfaces web avançadas.

-   **Arduino/ESP32 (O Cérebro de Baixo Nível ou Controlador de Tempo Real)**: Microcontroladores como o Arduino e o ESP32 são mestres no controle de hardware em **tempo real**. Eles são extremamente confiáveis para gerar sinais PWM precisos para motores, ler sensores com timing exato e garantir que as ações físicas do robô aconteçam sem atrasos ou falhas, tarefas nas quais um sistema operacional como o Linux pode ter dificuldades devido à sua natureza multitarefa.

Ao combinar os dois, criamos um robô onde o Raspberry Pi "pensa" e o ESP32 "age". O Pi analisa a imagem da câmera, decide "precisamos virar à direita" e envia um comando simples para o ESP32, que se encarrega de traduzir esse comando em sinais elétricos precisos para os motores das rodas.

![Arquitetura Híbrida](/home/ubuntu/curso_robotica/imagens/arquitetura_hibrida.png)
*Figura 1: Diagrama de uma arquitetura híbrida. O Raspberry Pi lida com a IA e a visão, enquanto o ESP32 controla diretamente os motores e sensores de baixo nível.*

---

## Comunicação Entre Placas: A Ponte Serial

A forma mais simples e robusta de fazer as duas placas conversarem é através da **comunicação serial (UART)**. Ambos os dispositivos possuem pinos de Transmissão (TX) e Recepção (RX).

**Conexão Física:**
-   O pino **TX** (Transmit) do Raspberry Pi é conectado ao pino **RX** (Receive) do ESP32.
-   O pino **RX** do Raspberry Pi é conectado ao pino **TX** do ESP32.
-   **GND Comum**: É **obrigatório** conectar um pino `GND` do Raspberry Pi a um pino `GND` do ESP32 para que ambos tenham uma referência de tensão comum.

**Atenção à Tensão:** O Raspberry Pi usa lógica de 3.3V em seus pinos GPIO, assim como o ESP32. Portanto, a conexão entre eles é direta e segura. Se você estivesse conectando um Raspberry Pi a um Arduino UNO (que usa lógica de 5V), seria necessário um conversor de nível lógico para evitar danificar o Pi.

### Protocolo de Comunicação

Simplesmente conectar os fios não é suficiente. Precisamos definir um **protocolo**, ou seja, um conjunto de regras para as mensagens. Um protocolo simples pode ser baseado em caracteres ou strings:

-   O Pi envia a string `"frente\n"` para o ESP32 se mover para frente.
-   O Pi envia `"parar\n"` para o robô parar.
-   O Pi envia `"angulo,90\n"` para comandar um servo a ir para 90 graus.

O caractere de nova linha (`\n`) é frequentemente usado para marcar o fim de um comando, facilitando a leitura no lado do receptor.

---

## Projeto Prático: Ponte de Comando Serial

Vamos criar um sistema onde um script Python rodando no Raspberry Pi envia comandos para controlar o LED e um servo conectado a um ESP32.

**Materiais:**
- 1x Raspberry Pi (qualquer modelo com GPIO)
- 1x ESP32 DevKit
- 1x Servo Motor (SG90)
- 1x LED e 1x Resistor de 220Ω
- Fios Jumper

**Montagem:**

1.  **Conexão Serial**: 
    -   Conecte o `GND` do Pi ao `GND` do ESP32.
    -   Conecte o **TXD** do Pi (GPIO 14) ao **RX2** do ESP32 (GPIO 16).
    -   Conecte o **RXD** do Pi (GPIO 15) ao **TX2** do ESP32 (GPIO 17).
    *(Usamos a `Serial2` no ESP32 para deixar a `Serial` principal livre para depuração no computador.)*
2.  **Hardware no ESP32**:
    -   Conecte o LED (com resistor) ao **GPIO 26**.
    -   Conecte o servo ao **GPIO 18** (lembre-se de alimentá-lo com uma fonte de 5V externa, compartilhando o GND).

**Parte 1: Código do ESP32 (O Receptor e Atuador)**

Carregue este código no seu ESP32.

```cpp
#include <ESP32Servo.h>

// Pinos de Hardware
const int pinoLed = 26;
Servo meuServo;
const int pinoServo = 18;

void setup() {
  // Serial para depuração no PC
  Serial.begin(115200);
  // Serial2 para comunicação com o Raspberry Pi
  Serial2.begin(9600, SERIAL_8N1, 16, 17); // RX, TX

  pinMode(pinoLed, OUTPUT);
  meuServo.attach(pinoServo);
  Serial.println("Receptor pronto para receber comandos do Pi.");
}

void loop() {
  if (Serial2.available()) {
    String comando = Serial2.readStringUntil(\'\n\');
    comando.trim(); // Remove espaços em branco

    Serial.print("Comando recebido: ");
    Serial.println(comando);

    if (comando == "led_on") {
      digitalWrite(pinoLed, HIGH);
    } else if (comando == "led_off") {
      digitalWrite(pinoLed, LOW);
    } else if (comando.startsWith("servo")) {
      // Exemplo de comando: "servo,90"
      int virgulaIndex = comando.indexOf(",");
      if (virgulaIndex > 0) {
        String valorStr = comando.substring(virgulaIndex + 1);
        int angulo = valorStr.toInt();
        meuServo.write(angulo);
      }
    }
  }
}
```

**Parte 2: Código do Raspberry Pi (O Cérebro)**

No seu Raspberry Pi, salve este código como um arquivo Python (ex: `controlador.py`).

```python
import serial
import time

# Configura a porta serial. No Raspberry Pi 3/4, geralmente é /dev/ttyS0 ou /dev/serial0
# É preciso habilitar a porta serial em raspi-config e desabilitar o console serial
ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
time.sleep(2) # Espera a conexão serial estabilizar

def enviar_comando(comando):
    print(f"Enviando comando: {comando}")
    ser.write((comando + "\n").encode("utf-8"))

if __name__ == "__main__":
    try:
        while True:
            print("\n--- Menu de Comandos ---")
            print("1: Ligar LED")
            print("2: Desligar LED")
            print("3: Mover servo para 0 graus")
            print("4: Mover servo para 90 graus")
            print("5: Mover servo para 180 graus")
            
            escolha = input("Digite sua escolha (1-5): ")

            if escolha == "1":
                enviar_comando("led_on")
            elif escolha == "2":
                enviar_comando("led_off")
            elif escolha == "3":
                enviar_comando("servo,0")
            elif escolha == "4":
                enviar_comando("servo,90")
            elif escolha == "5":
                enviar_comando("servo,180")
            else:
                print("Escolha inválida.")

    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
    finally:
        ser.close()

```

**Resultado Esperado:**

1.  Execute o script Python no seu Raspberry Pi com `python3 controlador.py`.
2.  Um menu aparecerá no terminal do Pi.
3.  Digite `1` e pressione Enter. O script enviará o comando `"led_on\n"` pela porta serial.
4.  O ESP32 receberá o comando, o imprimirá em seu Monitor Serial (se conectado ao PC) e acenderá o LED.
5.  Teste os outros comandos para controlar o servo em diferentes ângulos.

Você acabou de criar uma ponte de comando entre um cérebro de alto nível e um controlador de baixo nível. Esta arquitetura é a base para os robôs mais avançados, onde o script Python no Pi poderia estar executando um complexo algoritmo de visão computacional e enviando comandos de movimento para o ESP32. No próximo módulo, vamos explorar o SLAM, a tecnologia que permite a um robô mapear seu ambiente.
