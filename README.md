# Telão DJ - Visualizador Interativo com Pygame

Este projeto é um sistema de visualização interativa para apresentações de DJ, desenvolvido em Python usando **Pygame**. Ele apresenta múltiplas cenas visuais, efeitos psicodélicos, strobe, starfield e renderização 3D de texto, com controles via teclado para manipular animações em tempo real.

---

## Estrutura do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Arquivo principal que inicializa o Pygame, gerencia troca de cenas, loop principal e eventos de teclado. |
| `cena1.py` | Cena com efeitos de partículas geométricas (círculos, quadrados, triângulos) que crescem e rotacionam. |
| `cena2.py` | Cena com fractais psicodélicos e efeitos de zoom e rotação (inspirada em fractais). |
| `cena3.py` | Starfield 3D com rastro, profundidade e centro móvel via WASD. Possui controle de velocidade, quantidade de estrelas e fade. |
| `cena4.py` | Texto psicodélico repetido em faixas horizontais, com rotação e strobe sincronizado com BPM. Permite alternar modo psicodélico e animação de faixas. |
| `cena5.py` | Texto circular 3D (“DOPE.”) com rotação, pulsação global, modo psicodélico e strobe. Letras são renderizadas com profundidade e escala variável. |
| `utils.py` | Funções auxiliares compartilhadas entre cenas: rotação de pontos, conversão HSV→RGB, desenho de formas, geração de objetos aleatórios e efeitos de glitch/RGB split. |

---

## Funcionalidades Principais

- Múltiplas cenas visuais com diferentes estilos:
  - **Geometria animada** (`cena1.py`)
  - **Fractais e psicodelia** (`cena2.py`)
  - **Starfield 3D** (`cena3.py`)
  - **Texto em faixas e strobe** (`cena4.py`)
  - **Texto circular 3D com profundidade** (`cena5.py`)
- Controles via teclado:
  - **Cena 3 (Starfield)**: ↑/↓ velocidade, ←/→ quantidade de estrelas, W/A/S/D movimento, espaço liga/desliga rastro, L alterna linha/ponto.
  - **Cena 4 (Texto faixas)**: Z liga/desliga psy-mode, X liga/desliga strobe, ↑/↓ ajusta BPM, ←/→ altera número de faixas, A ativa/desativa animação de faixas, Q/E rotaciona texto.
  - **Cena 5 (Texto circular)**: Z liga/desliga psy-mode, X liga/desliga strobe, ↑/↓ ajusta BPM, ←/→ altera raio base, C liga/desliga pulsação global.
- Efeitos visuais avançados:
  - Fade com half-life em starfield
  - RGB split e glitch slices
  - Pulsação e rotação de textos e formas
  - Animações interpoladas de faixas de texto

---

## Dependências

- Python 3.10+
- [Pygame](https://www.pygame.org/)

Instalação do Pygame via pip:

```bash
pip install pygame
```

---

## Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/telao-dj.git
cd telao-dj
```

2. Execute o arquivo principal:

```bash
python main.py
```

3. Durante a execução, utilize as teclas para navegar entre as cenas e interagir com os efeitos visuais.

---

## Estrutura de Eventos e Controles

O `main.py` captura todos os eventos do teclado e repassa para a cena ativa:

- **Cena 3 (Starfield)**  
  - ↑ / ↓ → aumenta/diminui velocidade  
  - ← / → → aumenta/diminui quantidade de estrelas  
  - W/A/S/D → move o centro da tela  
  - Espaço → liga/desliga rastro  
  - L → alterna linha/ponto  
  - R → reseta o campo de estrelas

- **Cena 4 (Texto em faixas)**  
  - Z → ativa/desativa modo psicodélico  
  - X → ativa/desativa strobe  
  - ↑ / ↓ → altera BPM do strobe  
  - ← / → → altera número de faixas  
  - A → ativa/desativa animação de faixas  
  - Q/E → rotaciona o texto  
  - W → reseta rotação

- **Cena 5 (Texto circular)**  
  - Z → ativa/desativa modo psicodélico  
  - X → ativa/desativa strobe  
  - ↑ / ↓ → altera BPM  
  - ← / → → ajusta raio base do círculo  
  - C → ativa/desativa pulsação global

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

