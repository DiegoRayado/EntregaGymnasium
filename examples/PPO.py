import gymnasium as gym
import gymnasium_csv
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Crear el entorno personalizado con las coordenadas y mapa especificados
env = gym.make(
    'gymnasium_csv-v0',
    render_mode='human',  # "human", "text", None
    inFileStr='../assets/map2.csv',
    initX=1,
    initY=1,
    goalX=10,
    goalY=8
)

# Convertir el entorno a un vectorizado para PPO (opcional si quieres usar múltiples instancias)
vec_env = make_vec_env(lambda: env, n_envs=1)  # n_envs puede ser >1 para paralelismo

# Entrenar el modelo PPO
model = PPO(
    "MlpPolicy",  # Política basada en redes neuronales (Multi-Layer Perceptron)
    vec_env,      # Entorno vectorizado
    verbose=1,    # Mostrar detalles del entrenamiento en consola
    learning_rate=0.0003,  # Tasa de aprendizaje
    n_steps=2048,          # Pasos por actualización
    gamma=0.99,            # Factor de descuento para recompensas futuras
    clip_range=0.2         # Rango de recorte para garantizar estabilidad
)

print("Entrenando el modelo PPO...")
model.learn(total_timesteps=50000)  # Ajusta los pasos de aprendizaje según sea necesario

# Guardar el modelo entrenado
model.save("ppo_custom_env")
print("Modelo guardado como 'ppo_custom_env'.")

# Cargar el modelo para pruebas (opcional)
model = PPO.load("ppo_custom_env")
print("Modelo cargado exitosamente.")

# Probar el modelo entrenado en el entorno personalizado
obs = env.reset()
done = False

print("Ejecutando la política aprendida...")
while not done:
    action, _states = model.predict(obs)  # Predecir la acción usando la política aprendida
    obs, reward, done, _, _ = env.step(action)  # Ejecutar acción en el entorno
    env.render()  # Renderizar cada paso para visualizar la ejecución

print("Ejecución completada.")

