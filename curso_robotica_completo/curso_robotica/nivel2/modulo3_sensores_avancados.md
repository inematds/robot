_# Módulo 2.3: Sensores Avançados

## Dando Mais Sentidos ao Robô

No Nível 1, usamos o sensor ultrassônico para dar ao nosso robô uma percepção básica de distância. Agora, vamos equipá-lo com sentidos mais aguçados que permitem tarefas de navegação complexas, como seguir uma linha ou saber sua própria orientação no espaço.

### Sensor de Linha Infravermelho (TCRT5000)

O TCRT5000 é um sensor de refletância. Ele consiste em um LED infravermelho (emissor) e um fototransistor (receptor). O LED emite luz IR, que é refletida pela superfície abaixo do sensor e captada pelo fototransistor.

-   **Superfícies Claras (Branco)**: Refletem muita luz IR. O fototransistor recebe um sinal forte.
-   **Superfícies Escuras (Preto)**: Absorvem a maior parte da luz IR. O fototransistor recebe um sinal fraco.

Ao ler a intensidade do sinal refletido, o robô pode distinguir entre uma linha preta e um fundo branco, tornando-se a base para um **robô seguidor de linha**.

![Sensor de Linha](/home/ubuntu/curso_robotica/imagens/tcrt5000_module.jpg)
*Figura 1: Um módulo com o sensor TCRT5000. Ele já inclui o circuito necessário e um pino de saída digital e/ou analógico.*

### Unidade de Medição Inercial (IMU) - MPU-6050

A IMU é um dos sensores mais poderosos para robótica. O MPU-6050 é um chip que combina dois sensores em um:

1.  **Acelerômetro**: Mede a aceleração linear em três eixos (X, Y, Z). Pode ser usado para detectar inclinação e movimento.
2.  **Giroscópio**: Mede a velocidade angular (rotação) em três eixos (X, Y, Z). É essencial para saber o quão rápido o robô está virando.

Combinando os dados desses dois sensores (um processo chamado de **fusão de sensores**), podemos obter uma estimativa muito precisa da orientação do robô no espaço (seu *roll*, *pitch* e *yaw*). Isso é crucial para realizar curvas precisas (ex: virar exatamente 90 graus) ou para manter o robô equilibrado.

![Sensor IMU MPU-6050](/home/ubuntu/curso_robotica/imagens/mpu6050_wiring.png)
*Figura 2: Um módulo MPU-6050 conectado a um Arduino via protocolo I2C, que usa apenas dois fios de dados (SDA e SCL).*

---

## Projeto Prático: Navegador com IMU

Vamos construir um programa que lê os dados do MPU-6050 e os exibe no Monitor Serial. Este é o primeiro passo para usar a IMU em um sistema de navegação.

**Materiais Necessários:**
- 1x ESP32 DevKit
- 1x Módulo MPU-6050
- Protoboard e Fios Jumper

**Montagem do Circuito (Protocolo I2C):**

O MPU-6050 se comunica usando o protocolo I2C, que é muito conveniente pois usa apenas dois pinos de dados.

1.  **Alimentação**: Conecte o pino `VCC` do MPU-6050 ao pino `3.3V` do ESP32. Conecte o `GND` do MPU-6050 ao `GND` do ESP32.
2.  **Dados I2C**:
    -   Conecte o pino `SCL` (Serial Clock) do MPU-6050 ao pino **GPIO 22** do ESP32 (pino SCL padrão).
    -   Conecte o pino `SDA` (Serial Data) do MPU-6050 ao pino **GPIO 21** do ESP32 (pino SDA padrão).

**Código do Projeto:**

Primeiro, instale a biblioteca para o MPU-6050. Vá em `Ferramentas > Gerenciar Bibliotecas` e instale a biblioteca **"Adafruit MPU6050"** e suas dependências (como a **"Adafruit BusIO"** e a **"Adafruit Unified Sensor"**).

```cpp
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Cria um objeto para o sensor MPU6050
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);

  // Tenta inicializar o sensor
  if (!mpu.begin()) {
    Serial.println(\"Falha ao encontrar o chip MPU6050. Verifique as conexões!\");
    while (1) {
      delay(10);
    }
  }
  Serial.println(\"MPU6050 Encontrado!\");

  // Configura as faixas de medição (opcional)
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DPS);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  // Cria variáveis para armazenar os eventos (leituras) dos sensores
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Imprime os dados do Acelerômetro (em m/s^2)
  Serial.print(\"Aceleração X: \");
  Serial.print(a.acceleration.x);
  Serial.print(\", Y: \");
  Serial.print(a.acceleration.y);
  Serial.print(\", Z: \");
  Serial.print(a.acceleration.z);
  Serial.println(\" m/s^2\");

  // Imprime os dados do Giroscópio (em rad/s)
  Serial.print(\"Rotação X: \");
  Serial.print(g.gyro.x);
  Serial.print(\", Y: \");
  Serial.print(g.gyro.y);
  Serial.print(\", Z: \");
  Serial.print(g.gyro.z);
  Serial.println(\" rad/s\");

  Serial.println(\"---\" );

  delay(500); // Pausa de meio segundo entre as leituras
}
```

**Resultado Esperado:**

Abra o Monitor Serial. Você verá um fluxo contínuo de dados do acelerômetro e do giroscópio. Tente mover e girar o sensor MPU-6050. Observe como os valores nos eixos X, Y e Z mudam de acordo com o movimento.

-   **Acelerômetro**: Com o sensor parado e nivelado, o eixo Z deve mostrar um valor próximo a 9.8 m/s², que é a aceleração da gravidade. Ao inclinar o sensor, a gravidade será distribuída entre os eixos X e Y.
-   **Giroscópio**: Com o sensor parado, os valores devem ser próximos de zero. Ao girá-lo, você verá picos de velocidade angular no eixo correspondente.

Entender e interpretar esses dados é o primeiro passo para criar algoritmos de controle sofisticados, que é exatamente o que faremos no próximo módulo.
