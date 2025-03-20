#!/usr/bin/env python

import termios
import tty
import sys
import gymnasium as gym
import gymnasium_csv
from gymnasium_csv.wrappers import BoxToDiscreteObservation
import numpy as np

# Crear el entorno personalizado con las coordenadas y mapa especificados
env_raw = gym.make(
    'gymnasium_csv-v0',
    render_mode='human',  # "human", "text", None
    inFileStr='../assets/map2.csv',
    initX=1,
    initY=1,
    goalX=10,
    goalY=8
)
env = BoxToDiscreteObservation(env_raw)

# Inicializar la tabla Q (SARSA utiliza una tabla similar)
Q = np.zeros([env.observation_space.n, env.action_space.n])

# Hiperparámetros para SARSA
alpha = 0.5  # Tasa de aprendizaje
gamma = 0.95  # Factor de descuento para recompensas futuras
epsilon = 0.1  # Probabilidad de exploración (epsilon-greedy)
episodes = 500  # Número de episodios de entrenamiento

print("Entrenando con SARSA...")

# Entrenamiento SARSA
for episode in range(episodes):
    state, _ = env.reset()
    done = False

    # Seleccionar la primera acción usando una política epsilon-greedy
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()  # Exploración
    else:
        action = np.argmax(Q[state, :])  # Explotación

    total_reward = 0

    while not done:
        # Ejecutar la acción seleccionada y obtener el siguiente estado y recompensa
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # Seleccionar la próxima acción usando una política epsilon-greedy
        if np.random.uniform(0, 1) < epsilon:
            next_action = env.action_space.sample()  # Exploración
        else:
            next_action = np.argmax(Q[next_state, :])  # Explotación

        # Actualizar la tabla Q usando la fórmula SARSA:
        Q[state, action] += alpha * (
            reward + gamma * Q[next_state, next_action] - Q[state, action]
        )

        total_reward += reward
        state = next_state
        action = next_action

    print(f"Episodio {episode + 1}/{episodes}, Recompensa total: {total_reward}")

print("Entrenamiento completado.")
print("Tabla Q final:")
print(Q)

print("Presiona cualquier tecla para ejecutar la política aprendida...")
# Esperar entrada del usuario antes de ejecutar la política aprendida
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Evaluar la política aprendida en el entorno
state, _ = env.reset()
done = False

while not done:
    # Seleccionar la mejor acción según la tabla Q entrenada (política greedy)
    action = np.argmax(Q[state, :])
    next_state, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated

    env.render()
    print(f"Estado: {state}, Acción: {action}, Recompensa: {reward}, Terminado: {done}")
    state = next_state

print("Ejecución completada.")

