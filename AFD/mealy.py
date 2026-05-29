from typing import Set, Dict, Tuple, Optional

class MaquinaMealy:
    """
    Implementación de un Motor de Máquina de Mealy.
    
    Una Máquina de Mealy es una séxtupla (Q, Σ, Γ, δ, λ, q0) donde:
    - Q: Conjunto finito de estados
    - Σ: Alfabeto finito de símbolos de entrada
    - Γ: Alfabeto finito de símbolos de salida
    - δ: Función de transición (Q × Σ → Q)
    - λ: Función de salida (Q × Σ → Γ)
    - q0: Estado inicial (q0 ∈ Q)
    """
    def __init__(self) -> None:
        self.limpiar()

    def limpiar(self) -> None:
        """Reinicia todos los atributos de la máquina a su estado vacío."""
        self.estados: Set[str] = set()
        self.alfabeto_entrada: Set[str] = set()
        self.alfabeto_salida: Set[str] = set()
        self.transiciones: Dict[Tuple[str, str], Tuple[str, str]] = {}
        self.estado_inicial: Optional[str] = None
    
    def cargar_desde_archivo(self, archivo: str) -> None:
        """Carga la configuración de la Máquina de Mealy desde un archivo de texto."""
        self.limpiar()
        
        with open(archivo, 'r') as f:
            lineas = f.readlines()
            
        if len(lineas) < 5:
            raise ValueError("Archivo incompleto. Debe tener al menos 5 líneas.")
        
        self.estados = set(lineas[0].strip().split(','))
        self.alfabeto_entrada = set(lineas[1].strip().split(','))
        self.alfabeto_salida = set(lineas[2].strip().split(','))
        self.estado_inicial = lineas[3].strip()
        
        if self.estado_inicial not in self.estados:
            raise ValueError(f"Estado inicial '{self.estado_inicial}' no está en el conjunto de estados.")
        
        for i, linea in enumerate(lineas[4:], start=5):
            if linea.strip():
                partes = linea.strip().split(',')
                if len(partes) != 4:
                    raise ValueError(f"Línea {i}: Formato incorrecto. Se esperaba 'estado,entrada,estado_destino,salida'")
                
                estado_actual, sim_in, estado_siguiente, sim_out = partes
                
                if estado_actual not in self.estados:
                    raise ValueError(f"Línea {i}: Estado '{estado_actual}' no definido")
                if estado_siguiente not in self.estados:
                    raise ValueError(f"Línea {i}: Estado destino '{estado_siguiente}' no definido")
                if sim_in not in self.alfabeto_entrada:
                    raise ValueError(f"Línea {i}: Símbolo de entrada '{sim_in}' no está en el alfabeto Σ")
                if sim_out not in self.alfabeto_salida:
                    raise ValueError(f"Línea {i}: Símbolo de salida '{sim_out}' no está en el alfabeto Γ")
                
                clave = (estado_actual, sim_in)
                if clave in self.transiciones:
                    raise ValueError(f"Línea {i}: Transición duplicada para δ({estado_actual}, '{sim_in}')")
                
                # Se almacena la tupla (estado_destino, simbolo_salida)
                self.transiciones[clave] = (estado_siguiente, sim_out)
        
        print(f"✓ Máquina de Mealy cargada exitosamente desde '{archivo}'")
        print(f"  Estados: {len(self.estados)}, Transiciones: {len(self.transiciones)}")
    
    def procesar_cadena(self, cadena: str, verbose: bool = True) -> Optional[str]:
        """
        Procesa una cadena de entrada y genera la cadena de salida correspondiente.
        """
        if not self.estado_inicial:
            raise ValueError("Máquina no inicializada. No hay estado inicial definido.")
        
        estado_actual = self.estado_inicial
        salida_generada = ""
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"PROCESANDO CADENA: '{cadena}'")
            print(f"{'='*60}")
            print(f"Estado inicial: {estado_actual}")
            print("-"*60)
        
        for i, simbolo in enumerate(cadena, 1):
            if simbolo not in self.alfabeto_entrada:
                if verbose:
                    print(f"\n✗ Error en posición {i}: Símbolo '{simbolo}' no está en el alfabeto Σ")
                return None
            
            clave = (estado_actual, simbolo)
            if clave not in self.transiciones:
                if verbose:
                    print(f"\n✗ Error en posición {i}: No hay transición definida para ({estado_actual}, '{simbolo}')")
                return None
            
            estado_siguiente, simbolo_salida = self.transiciones[clave]
            
            if verbose:
                print(f"Paso {i}: Ingresa '{simbolo}' | Transición: {estado_actual} → {estado_siguiente} | Salida: '{simbolo_salida}'")
            
            salida_generada += simbolo_salida
            estado_actual = estado_siguiente
        
        if verbose:
            print("-"*60)
            print(f"Estado final alcanzado: {estado_actual}")
            print(f"CADENA DE SALIDA: {salida_generada}")
            print("="*60)
        
        return salida_generada
    
    def mostrar_maquina(self) -> None:
        """Muestra información detallada de la Máquina de Mealy."""
        print("\n" + "="*60)
        print("INFORMACIÓN DE LA MÁQUINA DE MEALY")
        print("="*60)
        
        print(f"\n▪ CONJUNTO DE ESTADOS (Q): {sorted(self.estados)}")
        print(f"▪ ALFABETO DE ENTRADA (Σ): {sorted(self.alfabeto_entrada)}")
        print(f"▪ ALFABETO DE SALIDA (Γ): {sorted(self.alfabeto_salida)}")
        print(f"▪ ESTADO INICIAL (q₀): {self.estado_inicial}")
        
        print(f"\n▪ TABLA DE TRANSICIONES Y SALIDAS:")
        if not self.transiciones:
            print("  No hay transiciones definidas")
        else:
            estados_ord = sorted(self.estados)
            simbolos_in_ord = sorted(self.alfabeto_entrada)
            
            # Encabezado (Estado actual | Entradas...)
            print(f"\n  {'Estado':<10}", end="")
            for sim in simbolos_in_ord:
                print(f"Entrada '{sim}': Q/Γ".center(20), end="")
            print("\n  " + "-" * (10 + 20 * len(simbolos_in_ord)))
            
            for estado in estados_ord:
                print(f"  {estado:<10}", end="")
                for sim in simbolos_in_ord:
                    tupla_dest = self.transiciones.get((estado, sim))
                    if tupla_dest:
                        txt = f"{tupla_dest[0]} / {tupla_dest[1]}"
                    else:
                        txt = "- / -"
                    print(txt.center(20), end="")
                print()
        print("="*60)

def main() -> None:
    mealy = MaquinaMealy()
    
    print("="*70)
    print("SIMULADOR DE MÁQUINA DE MEALY")
    print("="*70)
    
    while True:
        print("\n" + "─"*40)
        print("MENÚ PRINCIPAL")
        print("─"*40)
        print("1. Cargar Máquina desde archivo")
        print("2. Mostrar información de la Máquina")
        print("3. Procesar una cadena")
        print("4. Procesar múltiples cadenas desde archivo")
        print("5. Salir")
        print("─"*40)
        
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            archivo = input("\nRuta del archivo: ").strip()
            if archivo:
                try:
                    mealy.cargar_desde_archivo(archivo)
                except Exception as e:
                    print(f"✗ Error: {e}")
            input("\nPresione Enter para continuar...")
            
        elif opcion == '2':
            if not mealy.estados:
                print("\nNo hay Máquina cargada. Use la opción 1 primero.")
            else:
                mealy.mostrar_maquina()
            input("\nPresione Enter para continuar...")
            
        elif opcion == '3':
            if not mealy.estados:
                print("\nError: No hay Máquina cargada.")
                continue
            cadena = input("\nIngrese la cadena de entrada a procesar: ").strip()
            try:
                mealy.procesar_cadena(cadena)
            except Exception as e:
                print(f"✗ Error al procesar la cadena: {e}")
            input("\nPresione Enter para continuar...")
            
        elif opcion == '4':
            if not mealy.estados:
                print("\nError: No hay Máquina cargada.")
                continue
            archivo_cadenas = input("\nRuta del archivo con cadenas de entrada: ").strip()
            if archivo_cadenas:
                try:
                    with open(archivo_cadenas, 'r') as f:
                        cadenas = [linea.strip() for linea in f.readlines()]
                    
                    print(f"\nProcesando {len(cadenas)} cadenas...")
                    print("-" * 60)
                    for cadena in cadenas:
                        if not cadena: continue
                        salida = mealy.procesar_cadena(cadena, verbose=False)
                        if salida is not None:
                            print(f"Entrada: {cadena:<15} | Salida: {salida}")
                        else:
                            print(f"Entrada: {cadena:<15} | Salida: [ERROR EN TRANSICIÓN/ALFABETO]")
                except Exception as e:
                    print(f"✗ Error: {e}")
            input("\nPresione Enter para continuar...")
            
        elif opcion == '5':
            print("\n¡Gracias por usar el Simulador de Máquina de Mealy!")
            break
        
        else:
            print("\n✗ Opción inválida.")

if __name__ == "__main__":
    main()