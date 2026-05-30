import random
import os
from typing import Set, Dict, Tuple, Optional, List

class ServidorBancoMealy:
    """
    Especificación Formal del Autómata del Banco (Máquina de Mealy).
    Representa el protocolo de comunicación entre el cajero automático y el banco.
    """
    def __init__(self) -> None:
        self.estados: Set[str] = set()
        self.alfabeto_entrada: Set[str] = set()
        self.alfabeto_salida: Set[str] = set()
        self.estado_inicial: Optional[str] = None
        # Diccionario: (estado_actual, entrada) -> (estado_siguiente, [posibles_salidas])
        self.transiciones: Dict[Tuple[str, str], Tuple[str, List[str]]] = {}

    def cargar_desde_archivo(self, archivo: str) -> None:
        """Carga la definición del autómata desde un archivo de texto."""
        self.estados.clear()
        self.alfabeto_entrada.clear()
        self.alfabeto_salida.clear()
        self.transiciones.clear()
        
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
            
        if len(lineas) < 5:
            raise ValueError("Archivo incompleto. Debe tener al menos 5 líneas.")
        
        self.estados = set(lineas[0].split(','))
        self.alfabeto_entrada = set(lineas[1].split(','))
        self.alfabeto_salida = set(lineas[2].split(','))
        self.estado_inicial = lineas[3]
        
        if self.estado_inicial not in self.estados:
            raise ValueError(f"Estado inicial '{self.estado_inicial}' no definido en los estados.")
            
        for i, linea in enumerate(lineas[4:], start=5):
            partes = linea.split(',')
            if len(partes) != 4:
                raise ValueError(f"Línea {i}: Formato incorrecto. Se esperaba 'estado,entrada,estado_destino,salida1|salida2'")
            
            estado_actual, sim_in, estado_siguiente, salidas_str = partes
            
            # Separar las posibles salidas usando el delimitador '|'
            posibles_salidas = salidas_str.split('|')
            
            clave = (estado_actual, sim_in)
            self.transiciones[clave] = (estado_siguiente, posibles_salidas)
            
        print(f"✓ Autómata del Banco cargado. {len(self.transiciones)} transiciones registradas.")

    def procesar_cadena(self, cadena_solicitudes: List[str], verbose: bool = True) -> Optional[List[str]]:
        if not self.estado_inicial:
            print("✗ Error: El autómata no ha sido cargado.")
            return None
            
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
            
            # Lógica dura de negocio específica del banco
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
    
    # Rutas estáticas a los archivos usando raw strings (r"") para evitar problemas con \T, \A, etc.
    archivo_definicion = r"AutomataMealy\Definiciones\definicionBanco.txt"
    archivo_cadenas = r"AutomataMealy\example\cadenasBanco.txt"
    
    # 1. Cargar el autómata automáticamente
    print(f"\nIntentando cargar definición desde: {archivo_definicion}")
    if os.path.exists(archivo_definicion):
        banco.cargar_desde_archivo(archivo_definicion)
    else:
        print("✗ Archivo de definición no encontrado. Verifica la ruta.")
        return # Termina la ejecución si no hay autómata

    # 2. Procesar las cadenas automáticamente
    print(f"\nIntentando procesar cadenas desde: {archivo_cadenas}")
    if os.path.exists(archivo_cadenas):
        with open(archivo_cadenas, 'r', encoding='utf-8') as f:
            cadenas = [linea.strip() for linea in f.readlines() if linea.strip()]
        
        for cadena_str in cadenas:
            # Convierte string "Cs1,Cs5,Cs3" a lista ['Cs1', 'Cs5', 'Cs3']
            lista_solicitudes = cadena_str.split(',')
            banco.procesar_cadena(lista_solicitudes)
    else:
        print("✗ Archivo de cadenas no encontrado. Verifica la ruta.")

if __name__ == "__main__":
    main()