# Entrega Gymnasium
## Tabla de Contenidos
1. [Introducción](#Introduccion)
2. [Pioneer](#Pioneer)
3. [Controlador](#Controlador)
4. [Lanzar el programa](#i4)
## Introducción <a name="Introduccion"></a>
Tal y como se meciona en el guión se genera un laberinto de tamaño 10x12 (Según mi nombre) utilizando la LibreOffice. El mapa es el siguiente:

<pre><code> 
env_raw = gym.make('gymnasium_csv-v0',
                 render_mode='human',  # "human", "text", None
                 inFileStr='../assets/map2.csv',
                 initX=1,
                 initY=1,
                 goalX=10,
                 goalY=8)
</code></pre>
![Captura](images/mapa2.png)

Se posicion el robot pionner en el inicio (2,2). Por lo que se determina que el punto final se encuentra en la coordenada (11,9) ya que es la esquina opuesta. 


## Pioneer <a name="Pioneer"></a>

### Cambios en el modelo 

Se añade un sensor, utilizando el codigo propocionado, pero se cambia el angulo de vision y el alcance del mismo.  

![Captura](images/sensor_add.png)

Se añade también un gps. Aunque para conocer la posción del robot se usa: `ignition::math::Pose3d pose = model->WorldPose();`  

![Captura](images/gps_add.png)

## Controlador <a name="Controlador"></a>
### Video
Video del funcionamiento del controlador
[Enlace](https://youtu.be/X8nPELdxMe0)
### Descripcion
El controlador usa una logica muy simple, hace avanzar al robot hasta encontrar una pared. Cundo se topa con una pared realiza un giro de 90 grados y sigue avanzando (sino se topa con ninguna pared de nuevo). Finalmente se añade la detencion del robot cuando llega a meta. Como podemos observar es un controlador muy simple que no podria resolver ciertos mapas. Sin embargo, esto podría corregirse añadiendo un componente de aleatoriedad a los grados que gira y la direccion del giro. 
### Version Random
Como se ha mencionado anteriormente el controlado anterior no resuelve todos los mapas, por lo que se modifica el tiempo de giro para que este sea aletorio y por tanto el robot pueda girar de 0 a 360 grados de forma aletoria. Este controlador no es nada óptimo, pero para un tiempo infinito puede resolver todos los mapas que existan. 
La modificacion se realiza en la linea 35 y es la siguiente:
<pre><code>rotationDuration = static_cast<double>(rand()) / RAND_MAX * 9.0;</code></pre>
Video del funcionamiento del controlador en modo aleatorio (Este video puede causar ansiedad a los amantes de la eficiencia)
[Enlace](https://youtu.be/HKttFVv7WkM)
## Lanzar el programa <a name="i4"></a>
Antes de todo en `EntregaGazebo/Controlador/build` ejecutar:
<pre><code>cmake ..
make</code></pre>

Para lanzar el mundo de Gazebo con el modelo Pioneer, simplemente ejecuta el siguiente script:

<pre><code>./launch.sh</code></pre>

Este script realizará dos tareas principales:

1. Configurará automáticamente el `GAZEBO_MODEL_PATH` mediante el script de Python `set_gazebo_path.py`, que apunta a la carpeta del modelo (pioneer).
2. Lanzará Gazebo con el archivo `map.world.xml` (mundo de Gazebo) que se encuentra en la carpeta `mundos`.

Si se quisiera usar otro modelo Pioneer, es necesario modificar el archivo correspondiente para cambiar la variable GAZEBO_MODEL_PATH. Esto puede hacerse editando el script set_gazebo_path.py o exportando manualmente la nueva ruta en la terminal antes de ejecutar el script. Por ejemplo:
<pre><code>export GAZEBO_MODEL_PATH=/ruta/a/tu/modelo:$GAZEBO_MODEL_PATH</code></pre>

Esto permitirá que Gazebo cargue el modelo deseado desde la nueva ubicación especificada. Asegúrate de que los archivos del modelo estén correctamente configurados y que el archivo del mundo (map.world.xml) haga referencia al nuevo modelo. Finalmente:
Sino se ha modificado `set_gazebo_path.py`
<pre><code>gazebo map.world.xml</code></pre>
o si, si se ha modificado
<pre><code>./launch.sh</code></pre>
