# Protocolo de Comunicación

Esta carpeta contiene la implementación y documentación del protocolo de comunicación entre el AFD del Cajero y el Autómata de Mealy del Banco.

## Estructura
También hay un runner en la raíz `main.py` que lanza la interfaz interactiva del protocolo.

Resumen rápido del funcionamiento

- El Cajero está modelado como un AFD que avanza por símbolos locales (E1, V1, Af5, etc.).
- Algunos símbolos del AFD disparan solicitudes al Banco (Cs1, Cs2, ...). Estas relaciones están en `DEFAULT_AFD_TO_CS` dentro de `protocolo.py`.
- El Banco (Máquina de Mealy) recibe solicitudes `CsX` y devuelve respuestas `CrY`. Las transiciones y posibles salidas están definidas en `AutomataMealy/Definiciones/definicionBanco.txt`.
- Las respuestas `CrY` pueden mapearse de vuelta a símbolos del AFD para reinyectarlos (mapeos en `DEFAULT_CR_TO_AFD`).
- En la interfaz (opción 5) puedes procesar una cadena de símbolos del AFD paso a paso, elegir si reinyectar automáticamente las `Cr` y optar por modo determinista/aleatorio para el Banco.

Cómo ejecutar

```bash
python main.py
```

Sugerencia: usa la opción 5 para simular sesiones reales y observar el flujo de solicitudes/respuestas.
El protocolo define cómo el Cajero (AFD) y el Banco (Mealy) intercambian información para simular operaciones bancarias seguras y coordinadas.
