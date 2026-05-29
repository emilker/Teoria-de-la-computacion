import random
from typing import Set, Dict, Tuple, Optional, List

class ServidorBancoMealy:
    """
    Especificación Formal del Autómata del Banco (Máquina de Mealy).
    Representa el protocolo de comunicación entre el cajero automático y el banco.
    """
    def __init__(self) -> None:
        self.estados: Set[str] = {
            'b0', 'b_validando_tarjeta', 'b_validando_clave', 
            'b_consultando_saldo', 'b_autorizando_retiro', 
            'b_actualizando_clave', 'b_registrando_transaccion', 
            'b_bloqueado', 'b_error'
        } 
        
        self.alfabeto_entrada: Set[str] = {
            'Cs1', 'Cs2', 'Cs3', 'Cs4', 'Cs5', 'Cs6', 'Cs7'
        } 
        
        self.alfabeto_salida: Set[str] = {
            'Cr1', 'Cr2', 'Cr3', 'Cr4', 'Cr5', 
            'Cr6', 'Cr7', 'Cr8', 'Cr9', 'Cr10'
        } 
        
        self.estado_inicial: str = 'b0' 
        
        # Diccionario de transiciones: (estado_actual, entrada) -> (estado_siguiente, [posibles_salidas])
        # Las salidas múltiples simulan la lógica de negocio del banco (ej. tarjeta aceptada o rechazada).
        self.transiciones: Dict[Tuple[str, str], Tuple[str, List[str]]] = {
            ('b0', 'Cs1'): ('b_validando_tarjeta', ['Cr1', 'Cr2']), 
            ('b0', 'Cs2'): ('b_validando_clave', ['Cr3', 'Cr4']),
            ('b0', 'Cs3'): ('b_consultando_saldo', ['Cr5']), 
            ('b0', 'Cs4'): ('b_autorizando_retiro', ['Cr6', 'Cr7']),
            ('b0', 'Cs6'): ('b_actualizando_clave', ['Cr8']), 
            ('b0', 'Cs7'): ('b_validando_clave', ['Cr9']),
            ('b_validando_tarjeta', 'Cs5'): ('b_registrando_transaccion', ['Cr5']),
            ('b_validando_clave', 'Cs2'): ('b_validando_clave', ['Cr3', 'Cr4']),
            ('b_consultando_saldo', 'Cs5'): ('b_registrando_transaccion', ['Cr5']),
            ('b_autorizando_retiro', 'Cs5'): ('b_registrando_transaccion', ['Cr6']), 
            ('b_actualizando_clave', 'Cs5'): ('b_registrando_transaccion', ['Cr8']),
        }
        for cs in self.alfabeto_entrada:
            self.transiciones[('b_registrando_transaccion', cs)] = ('b0', ['Cr1'])

    def procesar_cadena(self, cadena_solicitudes: List[str], verbose: bool = True) -> Optional[List[str]]:
        """
        Procesa una secuencia de solicitudes (Cs) y genera las respuestas (Cr).
        El lenguaje generado es secuencias alternadas de solicitud-respuesta.
        Cada símbolo de entrada genera exactamente un símbolo de salida.
        """
        estado_actual = self.estado_inicial
        salidas_generadas = []
        intentos_clave = 0
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"PROCESANDO SOLICITUDES: {cadena_solicitudes}")
            print(f"{'='*60}")
            print(f"Estado inicial: {estado_actual} (Esperando solicitud)")
            print("-" * 60)
        
        for i, solicitud in enumerate(cadena_solicitudes, 1):
            if solicitud == "error":
                salida = random.choice(['Cr9', 'Cr10'])
                estado_actual = 'b_error'
                if verbose:
                    print(f"Paso {i}: Ingresa ERROR | Transición -> b_error | Salida: {salida}")
                salidas_generadas.append(salida)
                break
                
            if solicitud not in self.alfabeto_entrada:
                if verbose: print(f"✗ Error: Solicitud '{solicitud}' no está en el alfabeto ΣB")
                return None
            
            clave = (estado_actual, solicitud)
            
            if clave not in self.transiciones:
                if verbose: print(f"✗ Error: Transición no válida para ({estado_actual}, '{solicitud}')")
                return None
            
            estado_siguiente, posibles_salidas = self.transiciones[clave]
            simbolo_salida = random.choice(posibles_salidas)
            
            if estado_actual == 'b_validando_clave' and solicitud == 'Cs2':
                if simbolo_salida == 'Cr4': 
                    intentos_clave += 1
                    if intentos_clave >= 3:
                        estado_siguiente = 'b_bloqueado'
                else:
                    intentos_clave = 0 
            
            if verbose:
                print(f"Paso {i}: Ingresa '{solicitud}' | Transición: {estado_actual} → {estado_siguiente} | Salida: '{simbolo_salida}'")
            
            salidas_generadas.append(simbolo_salida)
            estado_actual = estado_siguiente
            
            if estado_actual == 'b_bloqueado':
                if verbose: print("⚠ Cuenta bloqueada. Terminando sesión.")
                break
        
        if verbose:
            print("-" * 60)
            print(f"Estado final alcanzado: {estado_actual}")
            print(f"CADENA DE SALIDA: {salidas_generadas}")
            print("=" * 60)
        
        return salidas_generadas

def main() -> None:
    banco = ServidorBancoMealy()
    
    print("=" * 70)
    print("SIMULADOR DEL AUTÓMATA DEL BANCO (MÁQUINA DE MEALY)")
    print("=" * 70)
    
    secuencia_1 = ['Cs1', 'Cs5', 'Cs3', 'Cs5']
    banco.procesar_cadena(secuencia_1)
    
    secuencia_2 = ['Cs2', 'Cs2', 'Cs2', 'Cs2']
    banco.procesar_cadena(secuencia_2)

if __name__ == "__main__":
    main()