# Módulo 1.1: Introdução à Robótica e Eletrônica Básica

## O Que é um Robô?

Bem-vindo ao início da sua jornada no fascinante mundo da robótica! Um **robô** é, em sua essência, uma máquina programável capaz de realizar uma série de ações de forma autônoma ou semi-autônoma. A palavra "robô" foi popularizada pelo escritor tcheco Karel Čapek em sua peça de 1920, "R.U.R." (Rossum's Universal Robots), derivando da palavra tcheca *robota*, que significa "trabalho forçado".

Os robôs modernos são compostos por três pilares fundamentais:

1.  **Mecânica**: O corpo físico do robô, incluindo seu chassi, rodas, braços e garras.
2.  **Eletrônica**: O sistema nervoso do robô, composto por sensores, atuadores e a unidade de controle (o "cérebro").
3.  **Programação**: A inteligência do robô, o conjunto de instruções que define seu comportamento.

Neste curso, exploraremos todos os três pilares, começando com os blocos de construção da eletrônica.

![Componentes Eletrônicos](/home/ubuntu/curso_robotica/imagens/componentes_eletronicos.png)
*Figura 1: Diversos componentes eletrônicos que formam a base da robótica.*

---

## Conceitos Fundamentais de Eletrônica

Para construir robôs, é crucial entender três conceitos básicos da eletricidade: Tensão, Corrente e Resistência.

| Conceito | Unidade | Analogia com Água |
| :--- | :--- | :--- |
| **Tensão (V)** | Volt (V) | A **pressão** da água em uma mangueira. É a "força" que impulsiona os elétrons. |
| **Corrente (I)** | Ampere (A) | O **fluxo** de água que passa pela mangueira. É a quantidade de elétrons em movimento. |
| **Resistência (R)** | Ohm (Ω) | Um **estreitamento** na mangueira que limita o fluxo de água. Controla a quantidade de corrente. |

A **Lei de Ohm** relaciona esses três conceitos: **V = I * R**. Esta é a lei mais fundamental da eletrônica e nos ajuda a calcular como os componentes se comportarão em um circuito.

---

## Componentes Eletrônicos Essenciais

Vamos conhecer alguns dos componentes mais comuns que você usará.

### Protoboard (Matriz de Contatos)

A protoboard é uma ferramenta que permite montar e testar circuitos eletrônicos sem a necessidade de solda. Suas conexões internas facilitam a prototipagem rápida.

![Protoboard](/home/ubuntu/curso_robotica/imagens/ilustracao_protoboard.png)
*Figura 2: Diagrama de uma protoboard mostrando as conexões internas das fileiras e colunas.*

-   **Linhas de Alimentação**: As colunas nas laterais (geralmente marcadas com `+` e `-`) são conectadas verticalmente. São usadas para distribuir a tensão (VCC) e o terra (GND) por todo o circuito.
-   **Área de Componentes**: As fileiras na área central são conectadas horizontalmente. Cada fileira é um nó elétrico, permitindo conectar os terminais dos componentes.

### LED (Diodo Emissor de Luz)

O LED é um componente que emite luz quando a corrente elétrica passa por ele. Ele é um **diodo**, o que significa que a corrente só pode fluir em uma direção. O terminal mais longo é o **anodo (+)** e o mais curto é o **catodo (-)**.

### Resistor

O resistor é um componente que limita a passagem de corrente. Ele é crucial para proteger componentes sensíveis, como os LEDs, de receberem corrente excessiva e queimarem. O valor de um resistor é medido em Ohms (Ω).

![Circuito de LED](/home/ubuntu/curso_robotica/imagens/led_circuit.png)
*Figura 3: Esquema de um circuito simples para acender um LED, mostrando a necessidade de um resistor para limitar a corrente.*

---

## Projeto Prático: Acendendo seu Primeiro LED

Vamos aplicar o que aprendemos montando um circuito físico simples. Este projeto não requer programação, apenas uma fonte de energia.

**Materiais Necessários:**
- 1x Protoboard
- 1x LED (qualquer cor)
- 1x Resistor de 220Ω a 330Ω
- Fios Jumper
- 1x Fonte de alimentação de 5V (pode ser um power bank ou a saída 5V de uma placa Arduino/ESP32)

**Passos da Montagem:**

1.  **Conecte a Alimentação**: Use fios jumper para conectar a saída de 5V da sua fonte à linha de alimentação positiva (`+`) da protoboard e o GND à linha negativa (`-`).
2.  **Posicione o LED**: Espete o LED na área central da protoboard, com cada terminal em uma fileira diferente.
3.  **Conecte o Resistor**: Conecte uma perna do resistor na mesma fileira do terminal **anodo (+)** do LED.
4.  **Feche o Circuito**:
    -   Use um fio para conectar a outra perna do resistor à linha de alimentação positiva (`+`).
    -   Use outro fio para conectar a fileira do terminal **catodo (-)** do LED à linha de alimentação negativa (`-`).

**Resultado Esperado:**

Ao ligar a fonte de alimentação, o LED deve acender! Se não acender, verifique as conexões, a polaridade do LED (anodo/catodo) e se a fonte está funcionando.

Parabéns! Você montou seu primeiro circuito eletrônico. No próximo módulo, aprenderemos a controlar componentes como este usando programação.
