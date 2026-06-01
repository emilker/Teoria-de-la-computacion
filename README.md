 # Prácticas de Teoría de la Computación (ULA, 2026)

 Este repositorio reúne implementaciones y utilidades didácticas para trabajar con autómatas finitos deterministas (AFD) y máquinas de Mealy, así como un pequeño protocolo de comunicación que integra ambos módulos.

 **Propósito**
 - Centralizar las prácticas y ejemplos del curso.
 - Proveer un entorno sencillo para simular la interacción entre un cajero (AFD) y un banco (Mealy).

 **Visión general**
 El proyecto está pensado para ser educativo y fácilmente extensible: los autómatas se definen en archivos de texto, y los módulos principales proveen funciones para cargar, simular y depurar las ejecuciones.

 **Estructura del repositorio**
 - `main.py`: Punto de entrada. Lanza la interfaz REPL que integra el `AFD` (cajero) y el `ServidorBancoMealy` (banco).
 - `AFD/`
   - `afd.py`: Implementación del simulador de Autómatas Finitos Deterministas (cargar definiciones, procesar cadenas, mostrar estado, etc.).
   - `Definiciones/`: Archivos de definición del AFD (ej. `definicionCajero.txt`).
   - `examples/` (o `examples` según versión): Cadenas o ejemplos de prueba (`cadenasCajero.txt`).
 - `AutomataMealy/`
   - `bancoMealy.py`: Implementación de la máquina de Mealy que actúa como servidor del banco. Permite cargar transiciones desde un archivo y procesar solicitudes (`procesar_cadena`).
   - `Definiciones/`: Definición del autómata Mealy (`definicionBanco.txt`).
   - `example/` o `Example/`: Ejemplos de cadenas para pruebas (`cadenasBanco.txt`).
 - `ProtocoloComunicacion/`
   - `protocolo.py`: Lógica de integración y REPL. Contiene funciones para cargar ambos autómatas y un menú interactivo que permite enviar símbolos, procesar cadenas paso a paso y mapear respuestas.

 **Cómo está diseñado / flujo básico**
 - Los autómatas se describen en archivos de texto: estados, alfabetos, estado inicial y la lista de transiciones. Cada módulo (`AFD` y `AutomataMealy`) implementa un método `cargar_desde_archivo(path)` para poblar su estructura interna.
 - `main.py` importa la función `main` desde `ProtocoloComunicacion/protocolo.py`. Al ejecutar `python main.py` se inicia la interfaz REPL que:
   1. Carga el AFD del cajero y la máquina Mealy del banco (suprimiendo salidas de carga para limpieza).
   2. Muestra un menú con opciones para enviar símbolos, procesar cadenas, ver alfabetos y configurar mapeos entre salidas del banco (`Cr*`) y símbolos del cajero.
   3. En el modo de procesamiento paso a paso, consulta el AFD por cada símbolo y puede enviar solicitudes al banco cuando el AFD lo requiera (mappeado por defecto en `protocolo.py`).

 **Qué hace `main.py` exactamente**
 - Llama a `cargar_cajero()` y `cargar_banco()` para inicializar los autómatas desde:
   - `AFD/Definiciones/definicionCajero.txt`
   - `AutomataMealy/Definiciones/definicionBanco.txt`
 - Presenta un menú interactivo con las siguientes acciones:
   - Enviar símbolos `Cs` directamente al banco.
   - Enviar símbolos locales al AFD (E/V/Af/Am) y ver el resultado.
   - Mostrar alfabetos cargados.
   - Procesar una cadena del cajero paso a paso, enviar solicitudes al banco y opcionalmente reinyectar las respuestas.

 **Ejecución / Requisitos**
 - Requisitos: Python 3.8+ (no hay dependencias externas externas aparte de la librería estándar).
 - Ejecutar el REPL:
 ```bash
 python main.py
 ```
 - No se compila: el proyecto es puro Python. Para distribuir puedes crear un entorno virtual y empaquetarlo, pero no es necesario para ejecutar localmente.

 **Archivos de definición**
 - Los archivos en `AFD/Definiciones/` y `AutomataMealy/Definiciones/` siguen un formato simple (líneas con estados, alfabetos, estado inicial y transiciones). Revisa `AFD/readme.md` y los comentarios en `bancoMealy.py` para el formato exacto.

 **Consejos para depuración y extensiones**
 - Si algo falla al cargar, revisa las rutas relativas y que los archivos de definición estén presentes.
 - Para pruebas deterministas del banco, `AutomataMealy/bancoMealy.py` ahora acepta un parámetro `deterministic` en `procesar_cadena` para forzar salidas deterministas (usar la primera salida definida en la transición).
 - Puedes modificar los mapeos por defecto entre AFD → Cs y Cr → AFD en `ProtocoloComunicacion/protocolo.py` para adaptar el flujo.