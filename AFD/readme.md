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
2. Alfabeto de símbolos  
3. Estado inicial  
4. Estados de aceptación  
5. Función de transición δ  

Durante este proceso se realizan validaciones automáticas para asegurar que el autómata sea determinista y consistente.

Esta modalidad es especialmente útil para **aprendizaje, pruebas rápidas y ejercicios académicos**.

---

## ▶ Ejecución del motor

Ejecuta el programa desde la terminal:

```bash
python afd.py
````

Se mostrará un **menú interactivo** con las siguientes opciones:

1. Cargar AFD desde archivo
2. Configurar AFD manualmente
3. Mostrar información del AFD
4. Procesar una cadena
5. Procesar múltiples cadenas desde archivo
6. Salir

---

##  Procesamiento de cadenas

El motor permite procesar cadenas de símbolos:

* Modo **detallado** (paso a paso)
* Modo **silencioso** (ideal para procesamiento masivo)

Ejemplo de salida:

```
Procesando cadena: 0101
Estado inicial: q0
δ(q0, '0') = q1
δ(q1, '1') = q0
...
Estado final alcanzado: q0
✗ CADENA RECHAZADA
```

---

##  Visualización del AFD

El motor muestra:

* Conjunto de estados
* Alfabeto
* Estado inicial
* Estados finales
* Tabla matricial de la función de transición
* Porcentaje de completitud del autómata

Esto facilita la **verificación formal y didáctica** del AFD.

---

##  Objetivo del proyecto

Este motor fue desarrollado con fines **educativos**, buscando:

* Reforzar la comprensión de los AFD
* Servir como base para simuladores, visualizadores o extensiones futuras
* Facilitar la validación manual y automática de autómatas

---

##  Tecnologías utilizadas

* **Python 3**
* Tipado estático (`typing`)
* Programación orientada a objetos
* Entrada y salida por consola

---

##  Uso académico

Este motor puede ser utilizado como:

* Herramienta de apoyo en cursos universitarios
* Base para proyectos de Lenguajes Formales
* Implementación de referencia para prácticas y evaluaciones
* Comparador de resultados con herramientas gráficas

---

##  Autor

Desarrollado con fines educativos y académicos.
Pensado para claridad, corrección formal y extensibilidad.

---