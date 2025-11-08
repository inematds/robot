# Módulo 3.7: Braço Robótico com Visão

## Manipulação Inteligente: A Coordenação Olho-Mão

Até agora, nosso foco tem sido em robôs móveis. Agora, vamos mudar para um dos pilares da automação industrial e da robótica de serviços: os **braços robóticos** (ou manipuladores). Um braço robótico que pode **ver** o que está fazendo e tomar decisões com base nisso é uma ferramenta incrivelmente poderosa, capaz de realizar tarefas de *pick-and-place* (pegar e colocar), montagem e interação com objetos.

O desafio central aqui é a **coordenação olho-mão**: como traduzir a posição de um objeto detectado por uma câmera em uma série de ângulos de junta que o braço robótico precisa para alcançar esse objeto.

![Braço Robótico com Visão](/home/ubuntu/curso_robotica/imagens/robotic_arm_vision.png)
*Figura 1: Um braço robótico industrial usando um sistema de visão para pegar objetos em uma esteira. Este é um exemplo clássico de coordenação olho-mão.*

---

## Cinemática: A Matemática do Movimento

A cinemática é o estudo do movimento sem considerar as forças que o causam. Para um braço robótico, existem dois problemas cinemáticos fundamentais:

### 1. Cinemática Direta (Forward Kinematics - FK)

-   **A Pergunta**: Se eu sei os ângulos de todas as juntas do meu braço robótico, onde no espaço estará a sua ponta (o efetuador final ou garra)?
-   **A Solução**: Este é o problema "fácil". Usando trigonometria (senos e cossenos), podemos calcular a posição (X, Y, Z) do efetuador final a partir dos ângulos das juntas e dos comprimentos dos elos do braço. Cada junta adiciona uma transformação (rotação e translação) à cadeia cinemática.

### 2. Cinemática Inversa (Inverse Kinematics - IK)

-   **A Pergunta**: Se eu quero que a ponta do meu braço robótico vá para uma posição específica (X, Y, Z) no espaço, quais são os ângulos que cada uma das juntas precisa ter?
-   **A Solução**: Este é o problema "difícil" e o mais importante para a automação. A solução matemática para a IK pode ser muito complexa, muitas vezes não tendo uma solução única (o braço pode alcançar o mesmo ponto de várias maneiras) ou, às vezes, nenhuma solução (o ponto está fora do alcance). Para braços robóticos simples (como um braço 2D com 2 ou 3 juntas), a solução pode ser encontrada com geometria. Para braços mais complexos, são usados métodos numéricos iterativos (o computador "chuta" uma solução e a refina até encontrar uma que funcione).

---

## O Pipeline de um Sistema Pick-and-Place

Vamos detalhar os passos que um braço robótico com visão executa para pegar um objeto:

1.  **Calibração Câmera-Robô**: Este é um passo crucial, feito uma única vez. Precisamos estabelecer uma relação matemática entre o sistema de coordenadas da câmera (em pixels) e o sistema de coordenadas do robô (em milímetros ou centímetros). Isso geralmente é feito mostrando ao robô um padrão conhecido (como um tabuleiro de xadrez) em várias posições e calculando a matriz de transformação que mapeia um sistema ao outro.

2.  **Detecção de Objetos**: O sistema de visão (rodando em um Raspberry Pi, por exemplo) captura uma imagem do espaço de trabalho. Ele usa um algoritmo de visão computacional (como detecção de cor, forma ou um modelo de IA) para encontrar o objeto de interesse. O resultado é a posição do objeto em **coordenadas de pixel** (ex: pixel 250, 480).

3.  **Transformação de Coordenadas**: Usando a matriz de calibração do passo 1, o sistema converte as coordenadas de pixel do objeto em **coordenadas do mundo real** no sistema de referência do robô (ex: X=15.2 cm, Y=22.5 cm).

4.  **Cálculo da Cinemática Inversa**: O cérebro do robô (o Raspberry Pi) agora tem um ponto de destino (X, Y, Z). Ele alimenta essas coordenadas em seu solucionador de IK. O solucionador calcula o conjunto de ângulos necessários para cada junta do braço (ex: Junta 1 = 45°, Junta 2 = 30°, Junta 3 = 75°) para que a garra chegue ao local do objeto.

5.  **Execução do Movimento**: O Raspberry Pi envia os ângulos calculados para o controlador de baixo nível (um Arduino ou ESP32), que gera os sinais PWM precisos para mover cada servo para sua posição de destino.

6.  **Ação da Garra**: Uma vez que o braço está posicionado, um comando é enviado para fechar a garra e pegar o objeto.

7.  **Movimento para o Destino**: O processo é repetido para o local de entrega. O robô calcula a IK para o ponto de destino, move o braço e, finalmente, abre a garra.

---

## Projeto Prático: Braço Robótico 2-DOF que Segue um Objeto

Vamos construir um projeto que implementa a parte central da coordenação olho-mão. Usaremos um ESP32-CAM para detectar um objeto colorido e controlar um braço robótico simples de 2 juntas (pan/tilt) para que a câmera siga o objeto.

**Materiais:**
- 1x ESP32-CAM
- 2x Servos Padrão (SG90)
- 1x Kit de montagem Pan/Tilt para servos
- 1x Objeto de cor viva (ex: uma bola de tênis ou um post-it vermelho)

**Montagem:**

1.  Monte o kit pan/tilt com os dois servos. Um servo controlará o movimento horizontal (pan) e o outro, o vertical (tilt).
2.  Fixe o ESP32-CAM no topo do mecanismo pan/tilt.
3.  Conecte os servos ao ESP32 (ou a uma placa controladora separada, como no módulo de arquitetura híbrida). Lembre-se de usar uma fonte de 5V externa para os servos.
    -   Servo Pan (Horizontal): **GPIO 12**
    -   Servo Tilt (Vertical): **GPIO 13**

**Lógica do Código:**

O código rodará inteiramente no ESP32-CAM.

1.  **Captura de Imagem**: O loop principal captura um quadro da câmera.
2.  **Detecção de Cor**: O código converte a imagem do espaço de cor RGB para **HSV (Hue, Saturation, Value)**. O espaço de cor HSV é muito melhor para detecção de cor, pois o componente **Hue (Matiz)** representa a cor pura, independentemente da iluminação (Value) ou da intensidade da cor (Saturation).
3.  **Limiarização (Thresholding)**: Nós definimos uma faixa de valores de Hue, Saturation e Value que correspondem à cor do nosso objeto. O código cria uma imagem binária (preta e branca) onde os pixels brancos representam as áreas da imagem que correspondem à cor do objeto.
4.  **Encontrar o Centroide**: O algoritmo calcula o "centro de massa" (centroide) de todos os pixels brancos. Isso nos dá a coordenada (X, Y) do centro do objeto na imagem.
5.  **Cálculo do Erro**: O código calcula o erro entre a posição do centroide do objeto e o centro da imagem. 
    -   `erro_X = centroide_X - (largura_imagem / 2)`
    -   `erro_Y = centroide_Y - (altura_imagem / 2)`
6.  **Controle Proporcional (PID Simplificado)**: Usamos um simples controle proporcional para ajustar os ângulos dos servos. 
    -   `novo_angulo_pan = angulo_pan_atual - Kp * erro_X`
    -   `novo_angulo_tilt = angulo_tilt_atual + Kp * erro_Y`
    O objetivo é mover os servos de forma a zerar o erro, ou seja, trazer o centroide do objeto para o centro da imagem.
7.  **Comando dos Servos**: Os novos ângulos são enviados para os servos pan e tilt.

**Resultado Esperado:**

Ao ligar o sistema, aponte a câmera para o objeto colorido. O mecanismo pan/tilt se moverá automaticamente para centralizar o objeto na visão da câmera. Se você mover o objeto, o braço o seguirá, mantendo-o sempre no centro do seu campo de visão. 

Você acabou de criar um sistema de rastreamento ativo, a base para qualquer tarefa de manipulação robótica com visão. No projeto final do curso, vamos integrar todos esses conceitos de IA para criar um robô assistente completo.
