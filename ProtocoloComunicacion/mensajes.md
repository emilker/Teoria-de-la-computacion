# Especificación de Mensajes

Este documento describe los tipos de mensajes y el flujo de comunicación entre el Cajero y el Banco.

## Tipos de Mensajes
- **Solicitud**: Enviada por el Cajero al Banco (ej: solicitud de retiro, consulta de saldo).
- **Respuesta**: Enviada por el Banco al Cajero (ej: saldo actual, confirmación de retiro, error).

## Formato Sugerido
- Mensaje: `{ 'tipo': 'solicitud'|'respuesta', 'operacion': 'retiro'|'saldo'|..., 'datos': {...} }`

## Ejemplo de Flujo
1. Cajero → Banco: Solicitud de retiro
2. Banco → Cajero: Respuesta (éxito o error)

## Mapeos entre símbolos (implementación actual)

- Mapeo AFD -> Cs (cuando el AFD produce este símbolo, se envía la(s) solicitud(es) Cs al banco):

	- `E1` -> `Cs1`  (inserción tarjeta → verificar tarjeta)
	- `E3` -> `Cs2`  (ingreso PIN → verificar clave)
	- `O1` -> `Cs3`  (consultar saldo)
	- `O2` -> `Cs4`  (iniciar retiro)
	- `E7` -> `Cs4`  (ingreso monto → autorizar retiro)
	- `Af5`, `Af6` -> `Cs5` (acciones que registran transacción)

- Mapeo Cr -> AFD (respuestas del banco que pueden reinyectarse como símbolos AFD):

	- `Cr1` -> `V6` (tarjeta verificada)
	- `Cr2` -> `Am4` (tarjeta rechazada)
	- `Cr3` -> `V1` (clave autorizada)
	- `Cr4` -> `V2` (clave no autorizada)
	- `Cr5` -> `Af5` (saldo disponible)
	- `Cr6` -> `Am6` (retiro autorizado)
	- `Cr7` -> `V5` (retiro rechazado)
	- `Cr9` -> `St` (error de comunicación)
	- `Cr10` -> `Sh` (sistema no disponible)

## Notas sobre determinismo

El servidor del Banco puede operar en modo aleatorio (selecciona entre salidas posibles al azar) o en modo determinista (elige la primera salida definida). En la interfaz de simulación puedes elegir el modo para cada ejecución de la opción 5.
