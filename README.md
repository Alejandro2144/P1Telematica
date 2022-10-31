# Descargar Proxy

`git clone https://github.com/Alejandro2144/P1Telematica.git`

# Configurar proxy

Para configurar el proxy usa el archivo de constants.py. En este defines todas las configuraciones del programa.

ENCONDING_FORMAT : Formato de codificación de los mensajes del programa.

BUFF_SIZE: El tamaño del buffer que usa sockets para coger request. (No hacerlo muy pequeño porque puede llevar a el programa mande error)

SERVERS: Una lista de tuplas de servidores y su puertos.

TTL: El time to live del cache del sistema.

CACHE_SIZE: El tamaño del cache.

# Correr Proxy

`./run.sh`

Deberia aparecer en terminal

`Se estableció correctamente la conexión`

# Detalles del código

El código esta divido en 7 archivos. Cada uno tiene una función especifica.

## constants.py

Las configuraciones del programa.

## main.py

Este es el archivo principal del programa. Este inicia el proxy y maneja a alto nivel el funcionamiento de él. Incia el proxy y espera conexiones de los usuarios mientras actualiza el caché.

## HandleConection.py

Éste archivo maneja la conexión del cliente. A grandes rasgos el programa escucha por una petición del cliente y abre un hilo. En el hilo, revisa el caché por si ya tiene la petición. Si no le manda la petición a un servidor, usundo el sistema de balance de carga round robin, espera la respuesta del servidor. La guarda en el cacheé y se le manda la respuesta al cliente.

## ReceiveHTTP.py

Éste archivo se encarga de receivir los mensajes HTTP. El método que usamos fue leer la primera parte del mensaje que nos captura la cabeza del mensaje. Ahi encontramos Content-length y ahi con la longitud del mensaje podemos seguir leyendo hasta que recibamos todo el mensaje.

## methods.py

Este archivo tiene unos métodos que se usan varios archivos y no tienen ni un tipo de relación.

## Queue.py

Este archivo se implementa una cola para poder hacer un caché LRU.(Last Resource Used)

## Cache.py

En este archivo se implementa el caché. El caché agrega lo último que se usa en el servidor. Hace esto con una cola de lo último que se ha usado. Esta cola se revisa para constantemente ver si al primero ya se le acabo el tiempo de vida y si eso pasa se saca del caché. Para cosultar rápidamente las fuciones del cahé se usa un mapa con la llave siendo la petición y el valor siendo la respuesta.
