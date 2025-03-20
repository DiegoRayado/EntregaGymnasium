#!/usr/bin/env python

import gymnasium as gym
import gymnasium_csv
import numpy as np
import heapq
import time

"""
# Coordinate Systems for `.csv` and `print(numpy)`

X points down (rows); Y points right (columns); Z would point outwards.

*--> Y (columns)
|
v
X (rows)
"""
UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

# Algoritmo A*
def a_star(grid, start, goal):
    """
    Algoritmo A* para encontrar el camino óptimo.
    """
    open_list = [(0, tuple(start))]
    came_from = {tuple(start): None}
    g_score = {tuple(start): 0}
    f_score = {tuple(start): np.sum(np.abs(start - goal))}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        if current == tuple(goal):
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + move[0], current[1] + move[1])
            
            # Verificar si la posición es válida dentro del grid y no es un obstáculo
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and grid[neighbor] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + np.sum(np.abs(np.array(neighbor) - goal))
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return []

# Inicializar el entorno
env = gym.make('gymnasium_csv-v0',
               render_mode='human',  # "human", "text", None
               inFileStr='/home/diego/Descargas/gymnasium-csv-026/assets/map2.csv',
               initX=1,
               initY=1,
               goalX=10,
               goalY=8)

# Llamar a reset() antes de renderizar
observation, info = env.reset()

# Definir posiciones iniciales y finales directamente
start_position = (1, 1)  # Coordenadas iniciales conocidas
goal_position = (10, 8)  # Coordenadas finales conocidas

# Cargar el mapa desde el archivo CSV
grid = np.genfromtxt('/home/diego/Descargas/gymnasium-csv-026/assets/map2.csv', delimiter=',')

# Ejecutar el algoritmo A*
path = a_star(grid=grid, start=np.array(start_position), goal=np.array(goal_position))

# Simulación del movimiento del robot en el entorno Gymnasium
SIM_PERIOD_MS = 500.0

print("Camino calculado:", path)
env.render()  # Renderizar después de reset()
time.sleep(0.5)

for step in path[1:]:
    # Determinar la acción necesaria para moverse al siguiente paso del camino
    move_map = {
        (1, 0): DOWN,
        (-1, 0): UP,
        (0, 1): RIGHT,
        (0, -1): LEFT,
        (1, 1): DOWN_RIGHT,
        (-1, -1): UP_LEFT,
        (1, -1): DOWN_LEFT,
        (-1, 1): UP_RIGHT,
    }
    move_vector = (step[0] - observation[0], step[1] - observation[1])
    action = move_map.get(move_vector)

    # Realizar la acción en el entorno
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()
    print("observation: " + str(observation) + ", reward: " + str(reward) +
          ", terminated: " + str(terminated) + ", truncated: " + str(truncated) +
          ", info: " + str(info))
    
    time.sleep(SIM_PERIOD_MS / 1000.0)
    
    if terminated or truncated:
        break

env.close()

