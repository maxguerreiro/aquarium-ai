# Aquarium AI

Simulação 2D minimalista feita com Pygame e Gymnasium. Um tubarão usa uma
política PPO V1 treinada para caçar, enquanto os peixes podem usar uma política
PPO compartilhada para fugir.

## Requisitos

Use Python 3.13 e instale as dependências registradas:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Executar

Todos os comandos abaixo devem ser executados a partir da raiz do repositório.

```powershell
# Simulação original: controlador programado do tubarão
.\.venv\Scripts\python.exe main.py

# Tubarão PPO V1
.\.venv\Scripts\python.exe -m visualization.watch_ppo

# Um peixe PPO contra o tubarão V1
.\.venv\Scripts\python.exe -m visualization.watch_fish_ppo

# Dez peixes controlados pelo mesmo PPO contra o tubarão V1
.\.venv\Scripts\python.exe -m visualization.watch_all_fish_ppo
```

## Treinar e avaliar

Os modelos distribuídos em `models/` são artefatos treinados. Os comandos de
treinamento abaixo podem sobrescrever o respectivo arquivo de saída; não os
execute se quiser preservar o checkpoint atual.

```powershell
# Treinar o tubarão V1 e o peixe
.\.venv\Scripts\python.exe -m training.train
.\.venv\Scripts\python.exe -m training.train_fish

# Avaliar políticas existentes
.\.venv\Scripts\python.exe -m evaluation.evaluate_ppo
.\.venv\Scripts\python.exe -m evaluation.evaluate_fish_ppo
```

## Testes

```powershell
.\.venv\Scripts\python.exe -m tests.test_env
.\.venv\Scripts\python.exe -m tests.test_fish_env
.\.venv\Scripts\python.exe -m tests.test_fish_obs
.\.venv\Scripts\python.exe -m tests.test_fish_control
.\.venv\Scripts\python.exe -m tests.test_rewards
```

## Estrutura

```text
aquarium_ai/     núcleo da simulação e ambientes Gymnasium
training/        comandos de treinamento PPO
evaluation/      avaliação, benchmark e análise de política
visualization/   visualizadores Pygame
tests/           validações executáveis
models/          checkpoints PPO preservados
main.py          ponto de entrada original
```

Os arquivos V2 continuam preservados por compatibilidade, mas não fazem parte
do fluxo principal documentado.
