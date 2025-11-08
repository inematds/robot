# Módulo 3.2: Reconhecimento de Objetos com Inteligência Artificial

## Ensinando o Robô a Entender o que Vê

No módulo anterior, demos ao nosso robô o sentido da visão. Agora, vamos dar-lhe um cérebro capaz de **interpretar** essa visão. Não basta ver uma coleção de pixels; um robô inteligente precisa saber que aqueles pixels formam um "gato", uma "pessoa" ou um "obstáculo". É aqui que a **Inteligência Artificial (IA)**, e mais especificamente as **Redes Neurais Convolucionais (CNNs)**, entram em jogo.

---

## O que é uma Rede Neural Convolucional (CNN)?

Inspiradas no córtex visual humano, as CNNs são um tipo especializado de rede neural projetado para processar dados que têm uma topologia de grade, como uma imagem. Em vez de olhar para cada pixel individualmente, uma CNN aprende a reconhecer **características (features)** em diferentes níveis de complexidade.

1.  **Camadas Iniciais**: Aprendem a detectar características simples, como bordas, cantos e cores.
2.  **Camadas Intermediárias**: Combinam essas características simples para reconhecer padrões mais complexos, como olhos, narizes ou texturas.
3.  **Camadas Finais**: Juntam esses padrões para identificar objetos completos, como o rosto de uma pessoa ou um carro.

Esse processo de aprendizado hierárquico torna as CNNs extremamente poderosas para tarefas de visão computacional, como **classificação de imagens** (dizer o que está na imagem) e **detecção de objetos** (encontrar onde os objetos estão na imagem e desenhar uma caixa ao redor deles).

![Robô com IA](/home/ubuntu/curso_robotica/imagens/ai_robot.jpg)
*Figura 1: Um robô com IA não apenas vê, mas entende o conteúdo da imagem, permitindo interações muito mais complexas.*

---

## Edge AI: IA na Ponta dos Dedos do Robô

Tradicionalmente, o processamento de IA exigia servidores poderosos na nuvem. No entanto, para um robô móvel, enviar um fluxo de vídeo para a internet, processá-lo e esperar a resposta é muito lento e depende de uma conexão constante. A solução é o **Edge AI**, ou IA na Borda.

Edge AI envolve a execução de modelos de IA diretamente no dispositivo (na "borda" da rede), como no nosso ESP32 ou Raspberry Pi. Isso proporciona respostas em tempo real e independência da internet.

### TensorFlow Lite para Microcontroladores

**TensorFlow Lite** é uma versão otimizada do popular framework de machine learning do Google, projetada para rodar em dispositivos com recursos limitados. A variante **TensorFlow Lite for Microcontrollers** é ainda mais leve, permitindo que modelos de IA sejam executados em hardware com apenas alguns kilobytes de memória, como o ESP32.

Ele converte um modelo treinado do TensorFlow em um formato compacto e eficiente, que pode ser integrado diretamente ao nosso código C++ no Arduino IDE.

---

## Modelos Pré-treinados: O Conhecimento do Mundo ao seu Alcance

Treinar uma CNN do zero exige milhões de imagens e um poder computacional imenso. Felizmente, não precisamos fazer isso. Podemos usar **modelos pré-treinados**, que são modelos de IA que já foram treinados por grandes empresas (como Google e Facebook) em conjuntos de dados massivos (como o ImageNet).

-   **MobileNet**: Uma família de modelos de visão extremamente eficientes, projetados especificamente para dispositivos móveis e embarcados. São ótimos para classificação de imagens (ex: "Esta imagem contém um cachorro").
-   **YOLO (You Only Look Once)**: Um modelo de detecção de objetos incrivelmente rápido e popular. Ele consegue identificar múltiplos objetos em uma imagem e desenhar caixas delimitadoras ao redor deles em uma única passagem.

Usar um modelo pré-treinado nos permite ter um sistema de visão de alta performance com muito pouco esforço. Também podemos usar uma técnica chamada **Transfer Learning (Aprendizado por Transferência)**, onde pegamos um modelo pré-treinado e o re-treinamos com nossas próprias imagens para reconhecer objetos específicos do nosso interesse.

---

## Projeto Prático: Detector de Pessoas com ESP32-CAM

Vamos criar um projeto incrível que demonstra o poder do Edge AI. Usaremos um ESP32-CAM com um modelo pré-treinado para detectar a presença de uma pessoa em seu campo de visão e acender um LED como alerta.

**Materiais:**
- 1x ESP32-CAM
- 1x Conversor FTDI para programação
- 1x LED e 1x Resistor de 220Ω (opcional, para um indicador externo)

**Montagem:**
- A mesma do projeto de streaming de vídeo (Módulo 3.1). Se for usar o LED externo, conecte-o a um pino GPIO disponível (ex: GPIO 16).

**Código do Projeto:**

O Arduino IDE para ESP32 já vem com um exemplo perfeito para isso.

1.  **Abra o Exemplo**: Vá em `Arquivo > Exemplos > ESP32 > Camera` e abra o exemplo `CameraWebServer`. Este é o mesmo código base do módulo anterior.
2.  **Habilite a Detecção de Rosto**: Dentro do código, procure por uma linha comentada que diz `// #define CONFIG_ESP_FACE_DETECT_ENABLED`. **Descomente** essa linha (remova o `//` do início).
    -   Este recurso, embora chamado de "detecção de rosto", usa um modelo que é eficaz para detectar a silhueta de uma pessoa em geral.
3.  **Configure a Placa e o Wi-Fi**: Assim como no projeto anterior, certifique-se de que o modelo da sua câmera (`CAMERA_MODEL_AI_THINKER`) está selecionado e insira suas credenciais de Wi-Fi (`ssid` e `password`).
4.  **Carregue o Código**: Coloque o ESP32-CAM em modo de flash (jumper entre GPIO 0 e GND), carregue o código, remova o jumper e resete a placa.

**Resultado Esperado:**

1.  Acesse o endereço de IP do seu ESP32-CAM no navegador.
2.  Inicie o streaming de vídeo clicando em **"Start Stream"**.
3.  Na interface web, você verá novas opções relacionadas à detecção de rosto. **Habilite a opção "Face Detection"**.

Agora, aponte a câmera para uma pessoa. Quando o modelo de IA detectar um rosto/pessoa, uma **caixa delimitadora vermelha** será desenhada ao redor dela diretamente no fluxo de vídeo! O ESP32 está executando um modelo de rede neural em tempo real para encontrar uma pessoa na imagem.

**Para ir além:**

O código de exemplo já cria uma estrutura (`box_t`) com as coordenadas da caixa detectada. Você pode usar essa informação no seu `loop()` para tomar decisões. Por exemplo:

```cpp
// Dentro do loop, após a captura do frame
if (detection_enabled) {
  // fb é o frame buffer (a imagem)
  dl_matrix3du_t *image_matrix = dl_matrix3du_alloc(1, fb->width, fb->height, 3);
  // ... (código de conversão de formato)

  // A função face_detect retorna uma lista de caixas
  box_list_t *boxes = face_detect(image_matrix, &mtmn_config);

  if (boxes) {
    // PELO MENOS UM ROSTO/PESSOA FOI DETECTADO!
    // Acenda um LED, mova um servo, envie um alerta, etc.
    digitalWrite(pinoLedAlerta, HIGH);
  } else {
    digitalWrite(pinoLedAlerta, LOW);
  }
}
```

Você acabou de implementar um sistema de vigilância inteligente em um dispositivo que custa poucos dólares. Este é o poder da IA embarcada. No próximo módulo, vamos explorar outro sentido humano fundamental para a interação: a audição e a fala.
