# Motor de Autómatas Finitos Deterministas (AFD)

Este proyecto implementa un **Motor de Autómatas Finitos Deterministas (AFD)** en Python, diseñado con fines educativos y académicos.  
El motor permite **definir, validar, analizar y ejecutar** autómatas finitos deterministas a partir de definiciones formales, ya sea mediante archivos de texto o entrada interactiva por consola.

La herramienta es ideal para cursos de **Lenguajes Formales, Teoría de la Computación y Autómatas**.

---

##  Características principales

- Implementación formal de un AFD como la tupla **(Q, Σ, δ, q₀, F)**
- Carga de autómatas desde archivo de texto
- Configuración manual e interactiva del AFD
- Validación de:
  - Estados y símbolos
  - Determinismo
  - Completitud de la función de transición
- Procesamiento paso a paso de cadenas de entrada
- Evaluación automática de múltiples cadenas desde archivo
- Visualización clara de la tabla de transiciones
- Mensajes de error explicativos y orientados al aprendizaje

---

##  Definición formal

Un **Autómata Finito Determinista (AFD)** se define como:

- **Q**: Conjunto finito de estados  
- **Σ**: Alfabeto finito de símbolos  
- **δ**: Función de transición (Q × Σ → Q)  
- **q₀**: Estado inicial  
- **F**: Conjunto de estados de aceptación  

Este motor implementa fielmente esta definición y garantiza el comportamiento determinista del autómata.

---

##  Formato del archivo de entrada

El AFD puede cargarse desde un archivo de texto con el siguiente formato:

```

q0,q1,q2
0,1
q0
q2
q0,0,q1
q0,1,q0
q1,0,q2
q1,1,q0
q2,0,q2
q2,1,q2

````

### Descripción del formato

1. **Estados** (separados por comas)
2. **Alfabeto**
3. **Estado inicial**
4. **Estados finales**
5. **Transiciones**: `estado_actual,símbolo,estado_destino`

---
## Definición interactiva por consola

Además del uso de archivos, el motor permite **definir completamente un AFD desde la consola**, solicitando al usuario:

1. Conjunto de estados  
 # Motor de Autómatas Finitos Deterministas (AFD)

Este repositorio contiene un simulador educativo de Autómatas Finitos Deterministas (AFD) escrito en Python. Permite definir autómatas, validar su estructura y simular el procesamiento de cadenas, ya sea mediante archivos de definición o mediante entrada interactiva por consola.

**Áreas de uso:** cursos de Teoría de la Computación, Lenguajes Formales y prácticas académicas.

**Contenido del repositorio**
- `AFD/afd.py`: implementación principal del simulador y la interfaz de consola.
- `AFD/examples/automata.txt`: ejemplo de definición de AFD.
- `AFD/examples/cadena.txt`: ejemplo de archivo con cadenas de prueba (una por línea).

**Características principales**
- Carga de AFD desde archivo de texto
- Configuración manual interactiva por consola
- Validaciones (estados, alfabeto, determinismo, completitud parcial)
- Procesamiento paso a paso de cadenas y modo silencioso para lote
- Visualización de tabla de transiciones y estadísticas

**Requisitos**
- Python 3.8+ (probable compatibilidad con 3.7)

## Formato del archivo de definición
El archivo de definición debe contener al menos 5 líneas con este orden:

1. Conjunto de estados (separados por comas)
2. Alfabeto (símbolos separados por comas)
3. Estado inicial
4. Estados finales (separados por comas)
5. Transiciones, una por línea: `estado_actual,símbolo,estado_destino`

Ejemplo mínimo:

```
q0,q1,q2
0,1
q0
q2
q0,0,q1
q0,1,q0
q1,0,q2
q1,1,q0
q2,0,q2
q2,1,q2
```

## Uso

Abrir una terminal, situarse en la carpeta `AFD` y ejecutar:

```bash
python afd.py
```

Se mostrará un menú interactivo con las opciones:

1. Cargar AFD desde archivo
2. Configurar AFD manualmente
3. Mostrar información del AFD actual
4. Procesar una cadena
5. Procesar múltiples cadenas desde archivo
6. Salir

Pasos rápidos con los archivos de ejemplo:

- Para cargar el autómata de ejemplo, desde la opción 1 ingresa la ruta:

  `examples/automata.txt`

- Para procesar varias cadenas (una por línea), usa la opción 5 e ingresa:

  `examples/cadena.txt`

Nota: las rutas pueden ser relativas a la carpeta `AFD` o rutas absolutas en tu sistema.

## Mensajes y errores frecuentes

- Si el archivo no contiene suficientes líneas, el programa mostrará un error de formato.
- Si una transición referencia un estado o símbolo no declarado, se informará la línea problemática.
- El simulador indica si faltan transiciones para un AFD «completo» (advertencia, no obliga a completarlo).

## Ejemplo de flujo (manual)

1. Ejecutar `python afd.py`.
2. Elegir opción 1 y cargar `examples/automata.txt`.
3. Elegir opción 4 para procesar una cadena individual o opción 5 para un archivo de cadenas.

## Contribuciones

Pequeñas mejoras, correcciones de formato y adición de nuevos ejemplos son bienvenidas. Para cambios mayores, por favor abre un issue describiendo el objetivo.

## Licencia

Proyecto con fines educativos. Puedes reutilizar el código en ejercicios y proyectos académicos citando su procedencia.

---

## Ejemplos

Se incluyen dos archivos de ejemplo en la carpeta `examples/`:

- `examples/automata.txt`: definición de un AFD de ejemplo.
- `examples/cadena.txt`: conjunto de cadenas de prueba (una por línea).

Contenido de ejemplo (`examples/automata.txt`):

```
q0,q1,q2
0,1
q0
q2
q0,0,q1
q0,1,q0
q1,0,q2
q1,1,q0
q2,0,q2
q2,1,q2
```

Ejemplo de `examples/cadena.txt` (selección):

```
00
100
0100
1100
000
001
... (más cadenas)
```

## Comandos rápidos

Abrir una terminal, situarse en la carpeta `AFD` y ejecutar el simulador:

```bash
python afd.py
```

Pasos útiles desde la línea de comandos:

- Cargar el autómata de ejemplo (opción 1): escribe `examples/automata.txt` cuando se pida la ruta.
- Procesar múltiples cadenas (opción 5): escribe `examples/cadena.txt` cuando se pida la ruta.

Si prefieres, también puedes usar rutas absolutas en lugar de rutas relativas.

---