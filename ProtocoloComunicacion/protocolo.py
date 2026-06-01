"""
Interfaz REPL para simular la interacción entre el Cajero (AFD) y el Banco (Mealy).
- Permite enviar símbolos del cajero (Cs1..Cs7) al banco y ver las respuestas (Cr...)
- Permite enviar símbolos del cajero local (E1, V1, Af1, etc.) al AFD y ver cambios de estado
- Permite mapear manualmente una salida del banco a un símbolo del cajero para reinyectarla
- Permite procesar una cadena del cajero paso a paso y enviar Cs automáticamente
"""
from AFD.cajeroAFD import AFD
from AutomataMealy.bancoMealy import ServidorBancoMealy
import sys
import io

# Mapeos por defecto (puedes ajustarlos aquí)
DEFAULT_AFD_TO_CS = {
    'E1': ['Cs1'],     # inserción tarjeta -> verificar tarjeta
    'E3': ['Cs2'],     # ingreso PIN -> verificar clave
    'O1': ['Cs3'],     # opción consultar saldo -> consultar_saldo
    'O2': ['Cs4'],     # opción retiro -> autorizar retiro (o E7)
    'E7': ['Cs4'],     # ingreso monto -> autorizar retiro
    'Af5': ['Cs5'],    # mostrar saldo -> registrar transacción
    'Af6': ['Cs5'],    # acción de retiro -> registrar transacción
}

DEFAULT_CR_TO_AFD = {
    'Cr1': 'V6',  # tarjeta_verificada -> V6
    'Cr2': 'Am4', # tarjeta_rechazada -> Am4 (mensaje sistema)
    'Cr3': 'V1',  # clave_autorizada -> V1
    'Cr4': 'V2',  # clave_no_autorizada -> V2
    'Cr5': 'Af5', # saldo_disponible -> Af5
    'Cr6': 'Am6', # retiro_autorizado -> Am6
    'Cr7': 'V5',  # retiro_rechazado -> V5
    'Cr8': 'Am1', # clave_actualizada -> Am1
    'Cr9': 'St',  # error_comunicacion -> St
    'Cr10': 'Sh', # sistema_no_disponible -> Sh
}


def cargar_cajero():
    cajero = AFD()
    # Suprimir la salida durante la carga para evitar mensajes en el menú principal
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        cajero.cargar_desde_archivo(r"AFD/Definiciones/definicionCajero.txt")
    finally:
        sys.stdout = old_stdout
    return cajero


def cargar_banco():
    banco = ServidorBancoMealy()
    # Suprimir la salida durante la carga para evitar mensajes en el menú principal
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        banco.cargar_desde_archivo(r"AutomataMealy/Definiciones/definicionBanco.txt")
    finally:
        sys.stdout = old_stdout
    return banco


def mostrar_menu():
    print("\n--- Interfaz de Simulación Cajero-Banco ---")
    print("1. Enviar símbolo del Cajero al Banco (Cs)")
    print("2. Enviar símbolo local al Cajero (E/V/Af/Am)")
    print("3. Mostrar alfabetos y símbolos disponibles")
    print("4. Mapear manualmente una salida del Banco a un símbolo del Cajero")
    print("5. Procesar cadena del Cajero (paso a paso) y enviar Cs automáticamente")
    print("6. Mostrar mapeos por defecto (AFD -> Cs, Cr -> AFD)")
    print("0. Salir")


def main():
    cajero = cargar_cajero()
    banco = cargar_banco()

    # Mostrar resumen de carga con título antes del menú
    print("\n=== Simulación Cajero-Banco — Autómatas cargados ===")
    print("✓ AFD cargado exitosamente desde 'AFD/Definiciones/definicionCajero.txt'")
    print(f"  Estados: {len(getattr(cajero, 'estados', []))}, Transiciones: {len(getattr(cajero, 'transiciones', {}))}")
    print(f"✓ Autómata del Banco cargado. {len(getattr(banco, 'transiciones', {}))} transiciones registradas.")
    print("Carga completada. Use la interfaz para enviar símbolos y observar respuestas.")

    # No inyectamos adaptadores automáticos; el usuario controlará el flujo
    protocolo_stub = None

    while True:
        mostrar_menu()
        opc = input("Opción: ").strip()
        if opc == '0':
            print("Saliendo...")
            break

        if opc == '1':
            print("Alfabeto de entrada del banco (símbolos Cs):")
            print(sorted(list(banco.alfabeto_entrada)))
            simbolo = input("Ingrese símbolo Cs a enviar (ej: Cs1) o una lista separada por comas: ").strip()
            if not simbolo:
                continue
            if ',' in simbolo:
                lista = [s.strip() for s in simbolo.split(',') if s.strip()]
            else:
                lista = [simbolo]
            # Procesar en el banco
            salidas = banco.procesar_cadena(lista, verbose=True)
            print("Salida(s) del banco:", salidas)

        elif opc == '2':
            print("Alfabeto local del cajero (ej: E1,V1,Af1,Am1):")
            print(sorted(list(cajero.alfabeto)))
            simbolo = input("Ingrese símbolo(s) para el AFD (ej: E1 o E1,E3): ").strip()
            if not simbolo:
                continue
            if ',' in simbolo:
                lista = [s.strip() for s in simbolo.split(',') if s.strip()]
            else:
                lista = list(simbolo)
            # El AFD espera una 'cadena'; pasamos la lista para procesar secuencia
            try:
                aceptada = cajero.procesar_cadena(lista, verbose=True)
                print("Resultado AFD (aceptada/bool):", aceptada)
            except Exception as e:
                print("Error al procesar en el AFD:", e)

        elif opc == '3':
            print("\n--- Alfabetos ---")
            print("Cajero (ΣL):", sorted(list(getattr(cajero, 'alfabeto', set()))) )
            print("Banco - entradas (ΣB):", sorted(list(getattr(banco, 'alfabeto_entrada', set()))) )
            print("Banco - salidas (ΓB):", sorted(list(getattr(banco, 'alfabeto_salida', set()))) )

        elif opc == '6':
            print("\n--- Mapeos por defecto ---")
            print("AFD -> Cs (cuando el AFD envía estas señales se solicita al banco):")
            for k, v in DEFAULT_AFD_TO_CS.items():
                print(f"  {k} -> {v}")
            print("\nCr -> AFD (reinyeción de respuestas del banco a símbolos del cajero):")
            for k, v in DEFAULT_CR_TO_AFD.items():
                print(f"  {k} -> {v}")

        elif opc == '5':
            print("Ingrese la cadena del cajero como símbolos separados por comas (ej: E1,V6,E3,V1,O1,Af5,E8,Af9)")
            cadena = input("Cadena: ").strip()
            if not cadena:
                continue
            lista_simbolos = [s.strip() for s in cadena.split(',') if s.strip()]
            afd_to_cs = DEFAULT_AFD_TO_CS
            cr_to_afd = DEFAULT_CR_TO_AFD

            auto_reinject = True
            reinject_choice = input("Reinyectar automáticamente las respuestas Cr al AFD? (s/n) [s]: ").strip().lower()
            if reinject_choice == 'n':
                auto_reinject = False

            # Preguntar si usar modo determinista/aleatorio para el Banco en esta ejecución
            det_prompt = "Usar modo determinista para el banco? (s/n) [n]: "
            det_choice = input(det_prompt).strip().lower()
            if det_choice == 's':
                det_mode = True
            elif det_choice == 'n':
                det_mode = False
            else:
                det_mode = False

            estado_actual = cajero.estado_inicial
            print(f"Estado inicial AFD: {estado_actual}")

            aborted = False
            aborted = False
            idx = 0
            while idx < len(lista_simbolos):
                simbolo = lista_simbolos[idx]
                paso = idx + 1
                clave = (estado_actual, simbolo)
                print(f"\nPaso {paso}: procesando símbolo del cajero: {simbolo} (desde {estado_actual})")
                if clave not in cajero.transiciones:
                    print(f"✗ No hay transición definida para δ({estado_actual}, '{simbolo}'). Terminando procesamiento.")
                    aborted = True
                    break
                estado_siguiente = cajero.transiciones[clave]
                print(f"δ({estado_actual}, '{simbolo}') -> {estado_siguiente}")
                estado_actual = estado_siguiente

                # Si este símbolo del AFD requiere una solicitud al banco, envíala
                if simbolo in afd_to_cs:
                    cs_list = afd_to_cs[simbolo]
                    for cs in cs_list:
                        print(f"Enviando solicitud al banco: {cs}")
                        salidas = banco.procesar_cadena([cs], verbose=False, deterministic=det_mode)
                        if salidas is None:
                            print("Advertencia: el banco no devolvió respuesta (None) para la solicitud", cs)
                            salidas = []
                        else:
                            print(f"Respuestas del banco: {salidas}")
                        # Reinyectar si corresponde
                        if auto_reinject and salidas:
                            for cr in salidas:
                                mapped = cr_to_afd.get(cr)
                                if mapped:
                                    print(f"Reinyectando {cr} -> símbolo AFD '{mapped}'")
                                    clave2 = (estado_actual, mapped)
                                    if clave2 in cajero.transiciones:
                                        estado_siguiente2 = cajero.transiciones[clave2]
                                        print(f"δ({estado_actual}, '{mapped}') -> {estado_siguiente2}")
                                        # Si la reinyeción coincide con el siguiente símbolo original, saltarlo
                                        next_idx = idx + 1
                                        estado_actual = estado_siguiente2
                                        if next_idx < len(lista_simbolos) and lista_simbolos[next_idx] == mapped:
                                            print(f"Siguiente símbolo original '{mapped}' coincide con la reinyeción; se omitirá para evitar duplicado.")
                                            idx += 1
                                    else:
                                        print(f"No hay transición para δ({estado_actual}, '{mapped}') durante la reinyeción")
                idx += 1

            # Al finalizar el procesamiento (y reinyeciones), indicar si la cadena es aceptada
            if aborted:
                print("\nResultado: cadena NO aceptada por el AFD (transición faltante).")
            else:
                aceptada = estado_actual in getattr(cajero, 'estados_finales', set())
                if aceptada:
                    print(f"\nResultado: cadena ACEPTADA por el AFD (estado final: {estado_actual}).")
                else:
                    print(f"\nResultado: cadena NO aceptada por el AFD (estado final: {estado_actual}).")

        elif opc == '4':
            cr = input("Ingrese salida del banco Cr (ej: Cr1) o lista separada por comas: ").strip()
            if not cr:
                continue
            cr_list = [s.strip() for s in cr.split(',') if s.strip()]
            print("Para cada Cr puede mapear a un símbolo del cajero (ej: V1, Af3, Am6, E3)")
            mappings = {}
            for c in cr_list:
                sym = input(f"Mapear {c} -> ").strip()
                if sym:
                    mappings[c] = sym
            # Reinyectar: procesar símbolos en AFD
            for c, sym in mappings.items():
                print(f"Procesando en AFD el símbolo '{sym}' (mapeado desde {c})")
                try:
                    res = cajero.procesar_cadena([sym], verbose=True)
                    print(f"Resultado AFD para {sym}: {res}")
                except Exception as e:
                    print("Error al procesar en AFD:", e)

        else:
            print("Opción no válida.")


if __name__ == '__main__':
    main()
"""
Módulo de protocolo de comunicación entre Cajero (AFD) y Banco (Mealy)
"""

class ProtocoloComunicacion:
    """
    Protocolo de comunicación entre Cajero (AFD) y Banco (Mealy).
    Soporta todos los tipos de solicitudes y respuestas definidos en la integración.
    """
    def __init__(self, cajero, banco):
        self.cajero = cajero
        self.banco = banco

    def enviar_solicitud(self, operacion, datos=None):
        """
        Envía una solicitud genérica al banco.
        """
        mensaje = {
            'tipo': 'solicitud',
            'operacion': operacion,
            'datos': datos or {}
        }
        return self.banco.procesar_mensaje(mensaje)

    def recibir_respuesta(self, mensaje):
        """
        Procesa la respuesta del banco y retorna los datos.
        """
        if mensaje['tipo'] == 'respuesta':
            return mensaje['datos']
        else:
            raise ValueError('Mensaje no válido')

    # Métodos específicos para cada tipo de solicitud
    def verificar_tarjeta(self, datos=None):
        return self.enviar_solicitud('verificar_tarjeta', datos)

    def verificar_clave(self, datos=None):
        return self.enviar_solicitud('verificar_clave', datos)

    def consultar_saldo(self, datos=None):
        return self.enviar_solicitud('consultar_saldo', datos)

    def autorizar_retiro(self, datos=None):
        return self.enviar_solicitud('autorizar_retiro', datos)

    def registrar_transaccion(self, datos=None):
        return self.enviar_solicitud('registrar_transaccion', datos)

    def actualizar_clave(self, datos=None):
        return self.enviar_solicitud('actualizar_clave', datos)

    def verificar_bloqueo(self, datos=None):
        return self.enviar_solicitud('verificar_bloqueo', datos)

    # Documentación de posibles respuestas del banco (Cr)
    RESPUESTAS_BANCO = [
        'tarjeta_verificada', 'tarjeta_rechazada', 'clave_autorizada', 'clave_no_autorizada',
        'saldo_disponible', 'retiro_autorizado', 'retiro_rechazado', 'clave_actualizada',
        'error_comunicacion', 'sistema_no_disponible'
    ]

    # Puedes agregar aquí lógica adicional para mapear respuestas o validarlas
