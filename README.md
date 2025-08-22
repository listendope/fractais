# Telão DJ – Visualizador Interativo com Pygame

Este projeto é um visualizador interativo para apresentações de DJ, desenvolvido em Python com **Pygame**. Ele oferece múltiplas cenas visuais dinâmicas, efeitos psicodélicos, animações de texto, starfield 3D e controles em tempo real via teclado, ideal para projeções em festas, eventos ou performances ao vivo.

---

## Estrutura do Projeto

| Arquivo      | Descrição                                                                                                                        |
|--------------|----------------------------------------------------------------------------------------------------------------------------------|
| `main.py`    | Loop principal do programa. Inicializa o Pygame, gerencia eventos, troca de cenas e renderização.                               |
| `cena1.py`   | Cena de partículas geométricas (círculos, quadrados, triângulos) que crescem, rotacionam e mudam de cor.                        |
| `cena2.py`   | Cena psicodélica com anéis concêntricos e raios coloridos, efeitos de glitch, RGB split e auto-modulação animada.               |
| `cena3.py`   | Starfield 3D: campo de estrelas com profundidade, rastro, movimento do centro via WASD e ajuste de velocidade/fade.             |
| `cena4.py`   | Texto "DOPE" em faixas horizontais, com rotação, animação de deslocamento, strobe sincronizado com BPM e modo psicodélico.      |
| `cena5.py`   | Texto circular 3D ("EPOD.") com rotação, pulsação global, efeitos de cor psicodélica e strobe.                                  |
| `utils.py`   | Funções utilitárias: rotação de pontos, conversão HSV→RGB, desenho de formas, geração de objetos e efeitos visuais (glitch etc).|

---

## Funcionalidades Principais

- **Múltiplas cenas visuais**:
  - **Cena 1:** Geometria animada – círculos, quadrados e triângulos que crescem, rotacionam e mudam de cor.
  - **Cena 2:** Psicodelia fractal – anéis e raios coloridos, efeitos de glitch, RGB split e auto-modulação.
  - **Cena 3:** Starfield 3D – estrelas em perspectiva, rastro com fade, controle de velocidade, quantidade e centro móvel.
  - **Cena 4:** Texto em faixas – texto "DOPE" repetido, rotação, animação de faixas, strobe sincronizado e modo psicodélico.
  - **Cena 5:** Texto circular 3D – texto "EPOD." em círculo, rotação, pulsação, efeitos de cor e strobe.

- **Efeitos visuais avançados**:
  - Glitch em fatias e RGB split (Cena 2)
  - Fade com half-life ajustável (Cena 3)
  - Strobe sincronizado por BPM (Cenas 4 e 5)
  - Pulsação e rotação de textos e formas
  - Animação interpolada de faixas de texto

- **Controles via teclado** (em tempo real):
  - Troca de cenas: F1–F5
  - Cada cena possui controles específicos para manipular parâmetros visuais, ativar/desativar efeitos e animar elementos.

---

## Controles de Teclado

### Troca de Cenas
- **F1**: Cena 1 (Geometria)
- **F2**: Cena 2 (Psicodelia/Glitch)
- **F3**: Cena 3 (Starfield)
- **F4**: Cena 4 (Texto em faixas)
- **F5**: Cena 5 (Texto circular 3D)

### Cena 1 – Geometria Animada
- **← / →**: Troca de cor de fundo
- **↑ / ↓**: Aumenta/diminui zoom das formas
- **W**: Adiciona círculo no centro
- **Q**: Adiciona quadrado no centro
- **E**: Adiciona triângulo no centro
- **Espaço**: Move o centro para posição aleatória
- **A / D**: Rotação anti-horária/horária
- **S**: Reseta rotação
- **R**: Ativa/desativa modo aleatório (cor e objetos automáticos)

### Cena 2 – Psicodelia/Glitch
- **R**: Ativa/desativa auto-modulação de raios e espaçamento
- **W**: Ativa/desativa efeito glitch
- **↑ / ↓**: Aumenta/diminui intervalo do glitch
- **← / →**: Diminui/aumenta quantidade de raios
- **A / D**: Diminui/aumenta espaçamento dos círculos

### Cena 3 – Starfield 3D
- **↑ / ↓**: Aumenta/diminui velocidade das estrelas
- **← / →**: Diminui/aumenta quantidade de estrelas
- **W/A/S/D**: Move o centro do campo de estrelas
- **Espaço**: Liga/desliga rastro (fade)
- **L**: Alterna entre linhas e pontos
- **R**: Reseta o campo de estrelas
- **Q / E**: Diminui/aumenta o half-life do fade

### Cena 4 – Texto em Faixas
- **Z**: Ativa/desativa modo psicodélico (cores animadas)
- **X**: Ativa/desativa strobe sincronizado com BPM
- **↑ / ↓**: Aumenta/diminui BPM do strobe
- **← / →**: Diminui/aumenta número de faixas de texto
- **A**: Ativa/desativa animação automática do número de faixas
- **Q / E**: Rotação anti-horária/horária do texto
- **W**: Reseta rotação

### Cena 5 – Texto Circular 3D
- **Z**: Ativa/desativa modo psicodélico (cores animadas)
- **X**: Ativa/desativa strobe sincronizado com BPM
- **↑ / ↓**: Aumenta/diminui BPM do strobe
- **← / →**: Diminui/aumenta raio base do círculo
- **C**: Ativa/desativa pulsação global do círculo

---

## Instalação e Execução

**Pré-requisitos:**
- Python 3.10 ou superior
- [Pygame](https://www.pygame.org/) instalado

**Instale o Pygame:**
```bash
pip install pygame
```

**Execute o projeto:**
```bash
python main.py
```

Durante a execução, utilize as teclas para navegar entre as cenas e interagir com os efeitos visuais.

---

## Contribuição

Contribuições são bem-vindas!  
- Novos efeitos visuais ou animações  
- Otimizações de desempenho  
- Novas cenas interativas  

Faça um fork, crie uma branch, adicione suas melhorias e abra um pull request.

---

## Licença

Este projeto está licenciado sob a **MIT License**. Sinta-se à vontade para usar, modificar e distribuir.

