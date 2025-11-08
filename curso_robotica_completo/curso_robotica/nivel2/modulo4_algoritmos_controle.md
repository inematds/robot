_# Módulo 2.4: Algoritmos de Controle

## Dando Inteligência ao Movimento

Até agora, nossos robôs ou eram controlados diretamente por nós (teleoperados) ou tinham uma lógica de decisão muito simples (se a distância for menor que X, faça Y). Para criar robôs verdadeiramente autônomos, precisamos de **algoritmos de controle**: um conjunto de regras e cálculos que permitem ao robô tomar decisões inteligentes com base nos dados dos sensores para atingir um objetivo.

Neste módulo, vamos explorar dois algoritmos fundamentais: a lógica para seguir uma linha e o famoso controle PID.

---

## Lógica de um Robô Seguidor de Linha

Um dos desafios clássicos da robótica é construir um robô que possa seguir uma linha preta em um fundo branco. A lógica por trás disso é um excelente exercício de controle.

Imagine que nosso robô tem **três sensores de linha** (TCRT5000) na frente: um à esquerda, um no centro e um à direita.

![Ilustração de Robô Autônomo](/home/ubuntu/curso_robotica/imagens/ilustracao_robo_autonomo.png)
*Figura 1: Um robô autônomo precisa de algoritmos para interpretar os dados dos seus sensores e decidir como se mover.*

A lógica de decisão pode ser descrita como uma série de regras "SE-ENTÃO":

| Leitura dos Sensores (Esquerda, Centro, Direita) | Situação | Ação do Robô |
| :--- | :--- | :--- |
| Branco, **Preto**, Branco | O robô está perfeitamente sobre a linha. | **Mover para frente** em velocidade normal. |
| Branco, Branco, **Preto** | O robô está desviando para a esquerda. | **Virar para a direita** para corrigir. |
| **Preto**, Branco, Branco | O robô está desviando para a direita. | **Virar para a esquerda** para corrigir. |
| Branco, Branco, Branco | O robô perdeu a linha (ou chegou a uma interrupção). | **Parar** ou iniciar uma rotina de busca. |
| **Preto**, **Preto**, **Preto** | O robô encontrou uma intersecção ou a linha de chegada. | **Parar** ou tomar uma decisão mais complexa. |

Este é um exemplo de uma **máquina de estados finitos**, onde o robô está sempre em um de vários estados possíveis e transita entre eles com base nas leituras dos sensores.

---

## Controle PID: O Segredo da Precisão

A lógica "SE-ENTÃO" funciona, mas muitas vezes resulta em um movimento oscilante, onde o robô ziguezagueia sobre a linha. Para um movimento suave e preciso, usamos um **Controlador Proporcional-Integral-Derivativo (PID)**.

O PID é um algoritmo de controle de malha fechada amplamente utilizado na indústria e na robótica. Seu objetivo é minimizar o **erro** entre o estado atual de um sistema e o estado desejado (o *setpoint*).

No nosso robô seguidor de linha, o **erro** pode ser definido como a distância do sensor central até o centro da linha. O PID calcula uma **saída de correção** para os motores com base em três termos:

![Fluxograma de Programa](/home/ubuntu/curso_robotica/imagens/diagrama_fluxo_programa.png)
*Figura 2: Um fluxograma de programa de robô. O controle PID se encaixa no passo de "Processar Dados" e "Tomar Decisão".*

### 1. Termo Proporcional (P)

O termo **Proporcional** é a parte mais intuitiva. A correção é **proporcional ao erro atual**. 

-   Se o robô está muito longe da linha (erro grande), a correção é forte (vira bruscamente).
-   Se o robô está perto da linha (erro pequeno), a correção é suave.

**Correção_P = Kp * erro**

O `Kp` é uma constante de ganho que ajustamos. Um `Kp` muito alto causa oscilações; um `Kp` muito baixo torna o robô lento para reagir.

### 2. Termo Integral (I)

O termo **Integral** lida com o **erro acumulado ao longo do tempo**. Ele serve para corrigir pequenos erros persistentes que o termo P sozinho não consegue eliminar (erro de estado estacionário).

-   Se o robô fica consistentemente um pouco à direita da linha, o erro se acumula, e o termo I aumenta gradualmente a correção para a esquerda até que o erro seja zerado.

**Correção_I = Ki * (soma_dos_erros)**

O `Ki` é a constante integral. Um `Ki` muito alto pode levar a uma correção exagerada e instabilidade.

### 3. Termo Derivativo (D)

O termo **Derivativo** olha para a **taxa de variação do erro** (a "velocidade" com que o erro está mudando). Ele tem um efeito de amortecimento, prevendo o erro futuro e agindo para evitar que a correção seja excessiva (*overshoot*).

-   Se o robô está se aproximando da linha muito rápido, o termo D reduz a força da correção para que ele não passe direto pelo centro.

**Correção_D = Kd * (erro_atual - erro_anterior)**

O `Kd` é a constante derivativa. Ele ajuda a estabilizar o sistema e reduzir as oscilações.

### A Equação Final do PID

A correção total aplicada aos motores é a soma dos três termos:

**Correção_Final = (Kp * erro) + (Ki * soma_dos_erros) + (Kd * (erro_atual - erro_anterior))**

Esta `Correção_Final` é então usada para ajustar a velocidade dos motores esquerdo e direito, fazendo o robô seguir a linha de forma suave e eficiente.

---

## Projeto Prático: Simulação de Controle PID

Implementar um PID completo em hardware requer um ajuste cuidadoso (chamado de *tuning*) das constantes Kp, Ki e Kd. Antes de colocar no robô, vamos fazer um programa simples que simula a lógica do PID no Monitor Serial.

**Materiais:**
- Apenas um ESP32 DevKit.

**Código do Projeto:**

Este código simula um sistema (como nosso robô) que tenta alcançar um `setpoint` (ponto desejado) de `100`.

```cpp
// Variáveis do sistema simulado
double setpoint = 100.0; // O valor que queremos alcançar
double valorAtual = 0.0;   // O valor atual do sistema
double saidaMotor = 0.0;  // A "força" aplicada ao sistema

// Constantes do PID (Tuning)
double Kp = 0.5;
double Ki = 0.2;
double Kd = 0.1;

// Variáveis do PID
double erro;
double erroAnterior = 0;
double integral = 0;
double derivativo;

unsigned long tempoAnterior;

void setup() {
  Serial.begin(115200);
  tempoAnterior = millis();
}

void loop() {
  unsigned long tempoAtual = millis();
  double dt = (double)(tempoAtual - tempoAnterior) / 1000.0; // Delta T em segundos
  tempoAnterior = tempoAtual;

  // ===== Lógica do PID =====
  erro = setpoint - valorAtual;
  integral += erro * dt;
  derivativo = (erro - erroAnterior) / dt;
  erroAnterior = erro;

  // Calcula a saída do PID
  double saidaPID = (Kp * erro) + (Ki * integral) + (Kd * derivativo);

  // ===== Simulação do Sistema =====
  // A saída do PID afeta o valor atual do sistema (simulando o motor empurrando o robô)
  valorAtual += saidaPID * dt;

  // Imprime os resultados
  Serial.print("Setpoint: "); Serial.print(setpoint);
  Serial.print(" | Valor Atual: "); Serial.print(valorAtual);
  Serial.print(" | Erro: "); Serial.print(erro);
  Serial.print(" | Saída PID: "); Serial.println(saidaPID);

  // Para a simulação quando chegar perto do setpoint
  if (abs(erro) < 0.1) {
    Serial.println("\nSetpoint alcançado! Fim da simulação.");
    while(true) delay(1000);
  }

  delay(100);
}
```

**Resultado Esperado:**

Abra o Monitor Serial. Você verá o `Valor Atual` começar em 0 e gradualmente se aproximar do `Setpoint` de 100. Observe como a `Saída PID` é alta no início (quando o erro é grande) e diminui à medida que o `Valor Atual` se aproxima do `Setpoint`.

Experimente mudar os valores de `Kp`, `Ki` e `Kd`:
-   Aumente `Kp`: o sistema responderá mais rápido, mas pode passar do setpoint e oscilar.
-   Aumente `Ki`: o sistema eliminará erros pequenos mais rápido, mas pode se tornar instável.
-   Aumente `Kd`: o sistema ficará mais estável e com menos oscilações.

Entender essa dinâmica é a chave para aplicar o PID em projetos reais. No projeto final deste nível, usaremos essa lógica para criar um robô autônomo que navega com precisão.
