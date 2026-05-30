import os
from typing import Set, Dict, Tuple, Optional

class AFD:
    """
    Implementación de un Motor de Autómatas Finito Determinista (AFD).
    
    Un AFD es una tupla (Q, Σ, δ, q0, F) donde:
    - Q: Conjunto finito de estados
    - Σ: Alfabeto finito de símbolos de entrada
    - δ: Función de transición (Q X Σ → Q)
    - q0: Estado inicial (q0 ∈ Q)
    - F: Conjunto de estados de aceptación (F ⊆ Q)
    
    Esta clase permite cargar, mostrar y simular el comportamiento de un AFD.
    """
    def __init__(self) -> None:
        """
        Inicializa un AFD vacío.
        """
        self.limpiar()

    def limpiar(self) -> None:
        """
        Reinicia todos los atributos del AFD a su estado vacío.
        """
        self.estados: Set[str] = set()
        self.alfabeto: Set[str] = set()
        self.transiciones: Dict[Tuple[str, str], str] = {}
        self.estado_inicial: Optional[str] = None
        self.estados_finales: Set[str] = set()
    
    def cargar_desde_archivo(self, archivo: str) -> None:
        """
        Carga la configuración del AFD desde un archivo de texto.
        """
        # LIMPIAR DATOS ANTERIORES
        self.limpiar()
        
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            
        # Validar que el archivo tenga al menos 5 líneas
        if len(lineas) < 5:
            raise ValueError("Archivo incompleto. Debe tener al menos 5 líneas.")
        
        # Leer estados
        self.estados = set(lineas[0].strip().split(','))
        
        # Leer alfabeto
        self.alfabeto = set(lineas[1].strip().split(','))
        
        # Leer estado inicial
        self.estado_inicial = lineas[2].strip()
        
        # Validar que el estado inicial esté en el conjunto de estados
        if self.estado_inicial not in self.estados:
            raise ValueError(f"Estado inicial '{self.estado_inicial}' no está en el conjunto de estados.")
        
        # Leer estados finales
        self.estados_finales = set(lineas[3].strip().split(','))
        
        # Validar que los estados finales estén en el conjunto de estados
        for estado_final in self.estados_finales:
            if estado_final not in self.estados:
                raise ValueError(f"Estado final '{estado_final}' no está en el conjunto de estados.")
        
        # Leer transiciones
        for i, linea in enumerate(lineas[4:], start=5):
            if linea.strip():
                partes = linea.strip().split(',')
                if len(partes) != 3:
                    raise ValueError(f"Línea {i}: Formato incorrecto. Se esperaba 'estado,símbolo,estado_destino'")
                
                estado_actual, simbolo, estado_siguiente = partes
                
                # Validar estados y símbolos
                if estado_actual not in self.estados:
                    raise ValueError(f"Línea {i}: Estado '{estado_actual}' no definido")
                if estado_siguiente not in self.estados:
                    raise ValueError(f"Línea {i}: Estado '{estado_siguiente}' no definido")
                if simbolo not in self.alfabeto:
                    raise ValueError(f"Línea {i}: Símbolo '{simbolo}' no está en el alfabeto")
                
                # Verificar que no haya transiciones duplicadas
                clave = (estado_actual, simbolo)
                if clave in self.transiciones:
                    raise ValueError(f"Línea {i}: Transición duplicada para δ({estado_actual}, '{simbolo}')")
                
                self.transiciones[clave] = estado_siguiente
        
        print(f"✓ AFD cargado exitosamente desde '{archivo}'")
        print(f"  Estados: {len(self.estados)}, Transiciones: {len(self.transiciones)}")
    
    def procesar_cadena(self, cadena: str, verbose: bool = True) -> bool:
        """
        Procesa una cadena de entrada y determina si es aceptada por el AFD.
        """
        if not self.estado_inicial:
            raise ValueError("AFD no inicializado. No hay estado inicial definido.")
        
        estado_actual = self.estado_inicial
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"PROCESANDO CADENA: '{cadena}'")
            print(f"{'='*60}")
            print(f"Estado inicial: {estado_actual}")
            print("-"*60)
        
        for i, simbolo in enumerate(cadena, 1):
            # Validar símbolo
            if simbolo not in self.alfabeto:
                if verbose:
                    print(f"\n✗ Error en posición {i}: Símbolo '{simbolo}' no está en el alfabeto")
                return False
            
            # Obtener transición
            clave = (estado_actual, simbolo)
            if clave not in self.transiciones:
                if verbose:
                    print(f"\n✗ Error en posición {i}: No hay transición definida para δ({estado_actual}, '{simbolo}')")
                return False
            
            # Aplicar transición
            estado_siguiente = self.transiciones[clave]
            if verbose:
                print(f"Paso {i}: δ({estado_actual}, '{simbolo}') = {estado_siguiente}")
            
            estado_actual = estado_siguiente
        
        if verbose:
            print("-"*60)
            print(f"Estado final alcanzado: {estado_actual}")
            print(f"Estados de aceptación: {sorted(self.estados_finales)}")
            print("-"*60)
        
        # Verificar si el estado final es de aceptación
        aceptada = estado_actual in self.estados_finales
        
        if verbose:
            if aceptada:
                print("✓ CADENA ACEPTADA")
                print("="*60)
            else:
                print("✗ CADENA RECHAZADA")
                print("="*60)
        
        return aceptada
    
    def mostrar_afd(self) -> None:
        """
        Muestra información detallada del AFD en formato legible.
        """
        print("\n" + "="*60)
        print("INFORMACIÓN DEL AUTÓMATA FINITO DETERMINISTA")
        print("="*60)
        
        print(f"\n▪ CONJUNTO DE ESTADOS (Q):")
        print(f"  {sorted(self.estados)}")
        
        print(f"\n▪ ALFABETO (Σ):")
        print(f"  {sorted(self.alfabeto)}")
        
        print(f"\n▪ ESTADO INICIAL (q₀):")
        print(f"  {self.estado_inicial}")
        
        print(f"\n▪ ESTADOS DE ACEPTACIÓN (F):")
        if self.estados_finales:
            print(f"  {sorted(self.estados_finales)}")
        else:
            print("  ∅ (No hay estados de aceptación)")
        
        print(f"\n▪ FUNCIÓN DE TRANSICIÓN (δ: Q × Σ → Q):")
        if not self.transiciones:
            print("  No hay transiciones definidas")
        else:
            estados_ordenados = sorted(self.estados)
            simbolos_ordenados = sorted(self.alfabeto)
            
            print(f"\n  {'Estado':<10}", end="")
            for simbolo in simbolos_ordenados:
                print(f"{simbolo:>10}", end="")
            print()
            print("  " + "-" * (10 + 10 * len(simbolos_ordenados)))
            
            for estado in estados_ordenados:
                print(f"  {estado:<10}", end="")
                for simbolo in simbolos_ordenados:
                    destino = self.transiciones.get((estado, simbolo), "-")
                    print(f"{destino:>10}", end="")
                print()
        print("="*60)

def main() -> None:
    afd = AFD()
    
    print("="*70)
    print("SIMULADOR DE AUTÓMATA FINITO DETERMINÍSTICO (AFD)")
    print("="*70)
    
    # Rutas estáticas a los archivos usando raw strings
    archivo_definicion = r"AFD\Definiciones\automata.txt"
    archivo_cadenas = r"AFD\Examples\cadena.txt"
    
    # 1. Cargar el AFD automáticamente
    print(f"\nIntentando cargar definición desde: {archivo_definicion}")
    if os.path.exists(archivo_definicion):
        try:
            afd.cargar_desde_archivo(archivo_definicion)
        except Exception as e:
            print(f"✗ Error al cargar el archivo: {e}")
            return
    else:
        print("✗ Archivo de definición no encontrado. Verifica la ruta.")
        return

    # 2. Procesar las cadenas automáticamente
    print(f"\nIntentando procesar cadenas desde: {archivo_cadenas}")
    if os.path.exists(archivo_cadenas):
        try:
            with open(archivo_cadenas, 'r', encoding='utf-8') as f:
                # Si en el archivo hay '""' simulando epsilon, lo reemplazamos por cadena vacía real
                cadenas = [linea.strip().replace('""', '') for linea in f.readlines()]
            
            print(f"\nProcesando {len(cadenas)} cadenas...")
            print("-"*50)
            
            resultados = []
            for cadena in cadenas:
                # Se oculta el verbose para un procesamiento por lotes limpio
                aceptada = afd.procesar_cadena(cadena, verbose=False)
                resultados.append((cadena, aceptada))
                simbolo = "✓" if aceptada else "✗"
                
                # Se visualiza ε si la cadena está vacía
                cadena_str = cadena if cadena else "ε (vacía)"
                print(f"{simbolo} '{cadena_str}': {'Aceptada' if aceptada else 'Rechazada'}")
            
            # Resumen estadístico
            print("-"*50)
            total_aceptadas = sum(1 for _, aceptada in resultados if aceptada)
            total_rechazadas = len(resultados) - total_aceptadas
            print(f"\nRESUMEN:")
            print(f"  Total de cadenas procesadas: {len(resultados)}")
            print(f"  Cadenas aceptadas: {total_aceptadas}")
            print(f"  Cadenas rechazadas: {total_rechazadas}")
            
        except Exception as e:
            print(f"✗ Error al procesar las cadenas: {e}")
    else:
        print("✗ Archivo de cadenas no encontrado. Verifica la ruta.")

if __name__ == "__main__":
    main()