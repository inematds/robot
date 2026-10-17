# 🦾 Robótica do Zero ao Expert — edição 2026

Curso aberto e gratuito do **INEMA.CLUB**: do primeiro LED no ESP32 ao braço robótico que aprende por demonstração. Sem carga horária: cada trilha resolve um problema e você entra pela que precisa hoje.

**Acesse:** [Português](https://inematds.github.io/robot/) · [English](https://inematds.github.io/robot/en/) · [Español](https://inematds.github.io/robot/es/)

## Trilhas

| Trilha | Módulos |
|---|---|
| 1 · Primeiros passos | O que é um robô e o seu kit · Eletrônica essencial · ESP32: o primeiro programa · Sensores · Motores e energia · **Projeto:** rover que desvia de obstáculos |
| 2 · Robô autônomo | Controle pelo celular (Wi-Fi e BLE) · IMU e encoders · Controle PID · Várias tarefas ao mesmo tempo · Telemetria · **Projeto:** seguidor de linha com PID |
| 3 · Visão e IA embarcada | Raspberry Pi 5 e Linux · Câmera e OpenCV · YOLO26 · IA no microcontrolador · Pi conversa com o ESP32 · **Projeto:** robô que segue um objeto |
| 4 · ROS 2 e navegação | ROS 2 sem medo · URDF e Gazebo · micro-ROS no ESP32 · LiDAR e SLAM · Nav2 · **Projeto:** robô que mapeia e navega |
| 5 · IA moderna e braço robótico | LLM como cérebro · Voz local · SO-101 e LeRobot · Aprender por demonstração · Simular antes do real · **Projeto final:** robô assistente |
| 6 · Para o professor | Como ministrar este curso (turmas, kits, avaliação, segurança) |

São 31 módulos e 188 tópicos. Cada módulo tem explicação, diagramas, código pronto para copiar e "como verificar". O progresso, as dúvidas e as anotações ficam salvos no seu navegador, e você pode exportá-los em "Minha jornada".

## O que mudou na edição 2026

- Formato novo (INEMA curso v2), com progresso, anotações e temas de leitura.
- Conteúdo atualizado: ESP32 core 3.x (`ledcAttach`), ROS 2 Lyrical/Jazzy, Gazebo, YOLO26, LeRobot com o braço SO-101.
- Todos os sketches de ESP32 compilados com `arduino-cli` + esp32 core 3.3.12.
- Trilha 6 nova, para quem vai dar o curso em escola ou clube.
- A versão antiga continua em [/robot/v1/](https://inematds.github.io/robot/v1/).

## Estrutura do repositório

```
docs/              site publicado (GitHub Pages)
  index.html       landing
  curso/trilhaN/   índice e módulos de cada trilha
  curso/_shared/   manifesto, convenções, currículo, fatos conferidos
  en/  es/         versões traduzidas (geradas)
  v1/              site antigo
i18n/              catálogo PT e traduções EN/ES (cache)
scripts/           validate.py, compile-check.py, browser-check.cjs, localization.py, translate.py, render-locales.py
```

Para conferir: `python3 scripts/validate.py pt|en|es` e `python3 scripts/compile-check.py <filtro>`.

---

## English

**Robotics from Zero to Expert, 2026 edition.** A free, open INEMA.CLUB course that goes from your first LED on an ESP32 to a robot arm that learns by demonstration. Six tracks (first steps, autonomous robot, vision and edge AI, ROS 2 and navigation, modern AI and the SO-101 arm, and a track for teachers), 31 modules, no fixed schedule. → [inematds.github.io/robot/en/](https://inematds.github.io/robot/en/)

## Español

**Robótica de Cero a Experto, edición 2026.** Curso abierto y gratuito de INEMA.CLUB: del primer LED en el ESP32 al brazo robótico que aprende por demostración. Seis rutas (primeros pasos, robot autónomo, visión e IA embebida, ROS 2 y navegación, IA moderna y el brazo SO-101, y una ruta para el docente), 31 módulos, sin carga horaria. → [inematds.github.io/robot/es/](https://inematds.github.io/robot/es/)

## Mais no INEMA.CLUB

- [Ficha deste curso](https://www.inema.club/cursos/29-robotica-do-zero-ao-expert-do-primeiro-led-ao-robo-com-ia/)
- [Guia: como aprender inteligência artificial](https://www.inema.club/aprender-inteligencia-artificial/)
- [Todos os cursos](https://www.inema.club/cursos/)

## Licença

MIT. Veja [LICENSE](LICENSE).
