from typing import Set, Dict, Tuple, Optional

class AFD:
    """
    Implementación de un Motor de Autómatas Finito Determinista (AFD).
    
    Un AFD es una tupla (Q, Σ, δ, q0, F) donde:
    - Q: Conjunto finito de estados
    - Σ: Alfabeto finito de símbolos de entrada
    - δ: Función de transición (Q × Σ → Q)
    - q0: Estado inicial (q0 ∈ Q)
    - F: Conjunto de estados de aceptación (F ⊆ Q)
    
    Esta clase permite cargar, mostrar y simular el comportamiento de un AFD.
    
    Atributos:
        estados (Set[str]): Conjunto de estados del autómata
        alfabeto (Set[str]): Conjunto de símbolos del alfabeto
        transiciones (Dict[Tuple[str, str], str]): Función de transición
        estado_inicial (Optional[str]): Estado inicial del autómata
        estados_finales (Set[str]): Conjunto de estados de aceptación
    """
    def __init__(self) -> None:
        """
        Inicializa un AFD vacío.
        
        Crea un autómata sin estados, alfabeto, transiciones ni estados finales.
        El estado inicial se establece como None.
        """
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
        
        Formato del archivo:
            1. Línea 1: Estados separados por comas (ej: q0,q1,q2)
            2. Línea 2: Alfabeto separado por comas (ej: 0,1)
            3. Línea 3: Estado inicial (ej: q0)
            4. Línea 4: Estados finales separados por comas (ej: q1,q2)
            5. Líneas restantes: Transiciones (estado,símbolo,estado_destino)
        
        Args:
            archivo (str): Ruta del archivo que contiene la definición del AFD
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato del archivo es incorrecto
            KeyError: Si hay referencias a estados no definidos
            
        Ejemplo de archivo:
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
        """

        # LIMPIAR DATOS ANTERIORES
        self.limpiar()
        
        with open(archivo, 'r') as f:
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
        
        # Verificar que el AFD sea determinista (ya garantizado por la validación anterior)
        print(f"✓ AFD cargado exitosamente desde '{archivo}'")
        print(f"  Estados: {len(self.estados)}, Transiciones: {len(self.transiciones)}")
    
    def cargar_manual(self) -> None:
        """
        Carga interactivamente la configuración del AFD mediante entrada por consola.
        
        Solicita al usuario ingresar:
            1. Conjunto de estados
            2. Alfabeto de símbolos
            3. Estado inicial
            4. Estados finales
            5. Función de transición
        
        La función valida las entradas y garantiza que el AFD sea determinista.
        
        Ejemplo de uso interactivo:
            Estados (separados por comas): q0,q1,q2
            Alfabeto (símbolos separados por comas): 0,1
            Estado inicial: q0
            Estados finales (separados por comas): q2
            Transiciones:
                q0,0,q1
                q0,1,q0
                fin
        """
        print("\n" + "="*50)
        print("CARGAR AFD MANUALMENTE")
        print("="*50)

        # LIMPIAR DATOS ANTERIORES
        self.limpiar()
        
        # Estados
        while True:
            estados_input = input("\nEstados (separados por comas, ej: q0,q1,q2): ").strip()
            if estados_input:
                self.estados = set(estado.strip() for estado in estados_input.split(','))
                if len(self.estados) > 0:
                    break
                print("Error: Debe ingresar al menos un estado.")
            else:
                print("Error: Campo obligatorio.")
        
        # Alfabeto
        while True:
            alfabeto_input = input("\nAlfabeto (símbolos separados por comas, ej: 0,1): ").strip()
            if alfabeto_input:
                self.alfabeto = set(simbolo.strip() for simbolo in alfabeto_input.split(','))
                if len(self.alfabeto) > 0:
                    break
                print("Error: Debe ingresar al menos un símbolo.")
            else:
                print("Error: Campo obligatorio.")
        
        # Estado inicial
        while True:
            self.estado_inicial = input("\nEstado inicial: ").strip()
            if self.estado_inicial in self.estados:
                break
            print(f"Error: El estado inicial debe estar en {self.estados}")
        
        # Estados finales
        while True:
            finales_input = input("\nEstados finales (separados por comas): ").strip()
            if finales_input:
                self.estados_finales = set(estado.strip() for estado in finales_input.split(','))
                # Validar que todos los estados finales estén en Q
                if self.estados_finales.issubset(self.estados):
                    break
                estados_invalidos = self.estados_finales - self.estados
                print(f"Error: Los siguientes estados no existen: {estados_invalidos}")
            else:
                print("Error: Campo obligatorio.")
        
        # Transiciones
        print("\n" + "-"*50)
        print("INGRESAR TRANSICIONES")
        print("-"*50)
        print("Formato: estado_actual,símbolo,estado_siguiente")
        print("Escribe 'fin' para terminar o 'mostrar' para ver transiciones actuales")
        print("Ejemplo: q0,0,q1")
        
        while True:
            transicion = input("\nTransición > ").strip()
            
            if transicion.lower() == 'fin':
                # Verificar completitud de la función de transición
                self._verificar_completitud_transiciones()
                break
            elif transicion.lower() == 'mostrar':
                self._mostrar_transiciones_parciales()
                continue
            elif transicion.lower() == 'help':
                print("\nComandos disponibles:")
                print("  fin      - Terminar de ingresar transiciones")
                print("  mostrar  - Mostrar transiciones ingresadas")
                print("  help     - Mostrar esta ayuda")
                print("  estados  - Mostrar estados disponibles")
                print("  alfabeto - Mostrar símbolos del alfabeto")
                continue
            elif transicion.lower() == 'estados':
                print(f"\nEstados: {sorted(self.estados)}")
                continue
            elif transicion.lower() == 'alfabeto':
                print(f"\nAlfabeto: {sorted(self.alfabeto)}")
                continue
            
            partes = transicion.split(',')
            if len(partes) != 3:
                print("Error: Formato incorrecto. Use: estado,símbolo,estado_destino")
                continue
            
            estado_actual, simbolo, estado_siguiente = [p.strip() for p in partes]
            
            # Validaciones
            if estado_actual not in self.estados:
                print(f"Error: Estado actual '{estado_actual}' no existe")
                continue
            
            if estado_siguiente not in self.estados:
                print(f"Error: Estado destino '{estado_siguiente}' no existe")
                continue
            
            if simbolo not in self.alfabeto:
                print(f"Error: Símbolo '{simbolo}' no está en el alfabeto")
                continue
            
            clave = (estado_actual, simbolo)
            if clave in self.transiciones:
                print(f"Error: Ya existe transición para δ({estado_actual}, '{simbolo}') = {self.transiciones[clave]}")
                continue
            
            self.transiciones[clave] = estado_siguiente
            print(f"✓ Transición agregada: δ({estado_actual}, '{simbolo}') = {estado_siguiente}")
        
        print(f"\n✓ AFD configurado manualmente con {len(self.transiciones)} transiciones")
    
    def _verificar_completitud_transiciones(self) -> None:
        """
        Verifica si la función de transición está completa.
        
        Un AFD debe tener una transición definida para cada par (estado, símbolo).
        Si hay transiciones faltantes, muestra una advertencia.
        """
        total_transiciones_esperadas = len(self.estados) * len(self.alfabeto)
        transiciones_faltantes = total_transiciones_esperadas - len(self.transiciones)
        
        if transiciones_faltantes > 0:
            print(f"\n⚠ Advertencia: Faltan {transiciones_faltantes} transiciones para un AFD completo")
            print("El autómata puede bloquearse con ciertas cadenas.")
    
    def _mostrar_transiciones_parciales(self) -> None:
        """Muestra las transiciones ingresadas hasta el momento."""
        if not self.transiciones:
            print("\nNo se han ingresado transiciones aún.")
            return
        
        print("\nTransiciones ingresadas:")
        for (estado, simbolo), destino in sorted(self.transiciones.items()):
            print(f"  δ({estado}, {simbolo}) = {destino}")
    
    def procesar_cadena(self, cadena: str, verbose: bool = True) -> bool:
        """
        Procesa una cadena de entrada y determina si es aceptada por el AFD.
        
        El procesamiento sigue la función de transición δ desde el estado inicial.
        La cadena es aceptada si al procesar todos los símbolos se llega a un
        estado final.
        
        Args:
            cadena (str): Cadena de símbolos a procesar
            verbose (bool): Si True, muestra el proceso paso a paso
            
        Returns:
            bool: True si la cadena es aceptada, False en caso contrario
            
        Raises:
            ValueError: Si la cadena contiene símbolos no pertenecientes al alfabeto
            KeyError: Si no existe transición para algún par (estado, símbolo)
            
        Ejemplo:
            >>> afd.procesar_cadena("0101")
            Procesando cadena: 0101
            Estado inicial: q0
            δ(q0, '0') = q1
            δ(q1, '1') = q0
            δ(q0, '0') = q1
            δ(q1, '1') = q0
            Estado final: q0
            ✗ Cadena RECHAZADA
            False
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
                    print(f"Alfabeto válido: {sorted(self.alfabeto)}")
                return False
            
            # Obtener transición
            clave = (estado_actual, simbolo)
            if clave not in self.transiciones:
                if verbose:
                    print(f"\n✗ Error en posición {i}: No hay transición definida para δ({estado_actual}, '{simbolo}')")
                    # Mostrar transiciones disponibles desde el estado actual
                    transiciones_disponibles = [k[1] for k in self.transiciones.keys() if k[0] == estado_actual]
                    if transiciones_disponibles:
                        print(f"Transiciones disponibles desde {estado_actual}: {sorted(transiciones_disponibles)}")
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
        
        Incluye:
            1. Conjunto de estados
            2. Alfabeto
            3. Estado inicial
            4. Estados finales
            5. Tabla de transiciones
        
        La tabla de transiciones se muestra en formato matricial para
        facilitar la visualización de la función δ.
        """
        print("\n" + "="*60)
        print("INFORMACIÓN DEL AUTÓMATA FINITO DETERMINISTA")
        print("="*60)
        
        # Información básica
        print(f"\n▪ CONJUNTO DE ESTADOS (Q):")
        print(f"  {sorted(self.estados)}")
        print(f"  Cardinalidad: |Q| = {len(self.estados)}")
        
        print(f"\n▪ ALFABETO (Σ):")
        print(f"  {sorted(self.alfabeto)}")
        print(f"  Cardinalidad: |Σ| = {len(self.alfabeto)}")
        
        print(f"\n▪ ESTADO INICIAL (q₀):")
        print(f"  {self.estado_inicial}")
        
        print(f"\n▪ ESTADOS DE ACEPTACIÓN (F):")
        if self.estados_finales:
            print(f"  {sorted(self.estados_finales)}")
            print(f"  Cardinalidad: |F| = {len(self.estados_finales)}")
        else:
            print("  ∅ (No hay estados de aceptación)")
        
        # Tabla de transiciones
        print(f"\n▪ FUNCIÓN DE TRANSICIÓN (δ: Q × Σ → Q):")
        if not self.transiciones:
            print("  No hay transiciones definidas")
        else:
            # Crear tabla ordenada
            estados_ordenados = sorted(self.estados)
            simbolos_ordenados = sorted(self.alfabeto)
            
            # Encabezado de la tabla
            print(f"\n  {'Estado':<10}", end="")
            for simbolo in simbolos_ordenados:
                print(f"{simbolo:>10}", end="")
            print()
            print("  " + "-" * (10 + 10 * len(simbolos_ordenados)))
            
            # Filas de la tabla
            for estado in estados_ordenados:
                print(f"  {estado:<10}", end="")
                for simbolo in simbolos_ordenados:
                    destino = self.transiciones.get((estado, simbolo), "-")
                    print(f"{destino:>10}", end="")
                print()
        
        # Estadísticas
        print(f"\n▪ ESTADÍSTICAS:")
        print(f"  Total de transiciones definidas: {len(self.transiciones)}")
        
        total_posibles = len(self.estados) * len(self.alfabeto)
        if total_posibles > 0:
            porcentaje = (len(self.transiciones) / total_posibles) * 100
            print(f"  Completitud: {len(self.transiciones)}/{total_posibles} ({porcentaje:.1f}%)")
        
        print("="*60)


def main() -> None:
    """
    Función principal del simulador de AFD.
    
    Proporciona una interfaz de menú interactiva para:
        1. Cargar AFD desde archivo
        2. Configurar AFD manualmente
        3. Mostrar información del AFD actual
        4. Procesar cadenas de prueba
        5. Procesar múltiples cadenas desde archivo
        6. Salir del programa
    
    El programa está diseñado para ser educativo y permite comparar
    resultados con herramientas como JFLAP.
    """
    afd = AFD()
    
    print("="*70)
    print("SIMULADOR DE AUTÓMATA FINITO DETERMINÍSTICO (AFD)")
    print("="*70)
    print("Herramienta educativa para simular y analizar autómatas finitos")
    print("Ideal para comparar resultados con JFLAP y otros simuladores")
    print("="*70)
    
    while True:
        print("\n" + "─"*40)
        print("MENÚ PRINCIPAL")
        print("─"*40)
        print("1. Cargar AFD desde archivo")
        print("2. Configurar AFD manualmente")
        print("3. Mostrar información del AFD actual")
        print("4. Procesar una cadena")
        print("5. Procesar múltiples cadenas desde archivo")
        print("6. Salir")
        print("─"*40)
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            # Opción 1: Cargar desde archivo
            print("\n[1] CARGAR AFD DESDE ARCHIVO")
            print("─"*40)
            archivo = input("Ruta del archivo: ").strip()
            
            if not archivo:
                print("Operación cancelada.")
                continue
            
            try:
                afd.cargar_desde_archivo(archivo)
                input("\nPresione Enter para continuar...")
            except FileNotFoundError:
                print(f"✗ Error: No se encontró el archivo '{archivo}'")
                input("Presione Enter para continuar...")
            except ValueError as e:
                print(f"✗ Error en el formato del archivo: {e}")
                input("Presione Enter para continuar...")
            except Exception as e:
                print(f"✗ Error inesperado: {e}")
                input("Presione Enter para continuar...")
        
        elif opcion == '2':
            # Opción 2: Configuración manual
            print("\n[2] CONFIGURAR AFD MANUALMENTE")
            afd.cargar_manual()
            input("\nPresione Enter para continuar...")
        
        elif opcion == '3':
            # Opción 3: Mostrar información
            print("\n[3] INFORMACIÓN DEL AFD ACTUAL")
            if not afd.estados:
                print("No hay AFD cargado. Use las opciones 1 o 2 primero.")
            else:
                afd.mostrar_afd()
            input("\nPresione Enter para continuar...")
        
        elif opcion == '4':
            # Opción 4: Procesar una cadena
            print("\n[4] PROCESAR CADENA")
            if not afd.estados:
                print("Error: No hay AFD cargado. Use las opciones 1 o 2 primero.")
                input("Presione Enter para continuar...")
                continue
            
            cadena = input("\nIngrese la cadena a procesar: ").strip()
            
            if not cadena:
                print("Cadena vacía ingresada (cadena ε)")
                cadena = ""
            
            try:
                resultado = afd.procesar_cadena(cadena)
                print(f"\nRESULTADO FINAL: La cadena '{cadena}' fue {'ACEPTADA' if resultado else 'RECHAZADA'}")
            except Exception as e:
                print(f"✗ Error al procesar la cadena: {e}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == '5':
            # Opción 5: Procesar múltiples cadenas desde archivo
            print("\n[5] PROCESAR MÚLTIPLES CADENAS DESDE ARCHIVO")
            if not afd.estados:
                print("Error: No hay AFD cargado. Use las opciones 1 o 2 primero.")
                input("Presione Enter para continuar...")
                continue
            
            archivo_cadenas = input("\nRuta del archivo con cadenas (una por línea): ").strip()
            
            if not archivo_cadenas:
                print("Operación cancelada.")
                input("Presione Enter para continuar...")
                continue
            
            try:
                with open(archivo_cadenas, 'r') as f:
                    cadenas = [linea.strip() for linea in f.readlines()]
                
                print(f"\nProcesando {len(cadenas)} cadenas...")
                print("-"*50)
                
                resultados = []
                for cadena in cadenas:
                    aceptada = afd.procesar_cadena(cadena, verbose=False)
                    resultados.append((cadena, aceptada))
                    simbolo = "✓" if aceptada else "✗"
                    print(f"{simbolo} '{cadena}': {'Aceptada' if aceptada else 'Rechazada'}")
                
                # Resumen estadístico
                print("-"*50)
                total_aceptadas = sum(1 for _, aceptada in resultados if aceptada)
                total_rechazadas = len(resultados) - total_aceptadas
                print(f"\nRESUMEN:")
                print(f"  Total de cadenas procesadas: {len(resultados)}")
                print(f"  Cadenas aceptadas: {total_aceptadas}")
                print(f"  Cadenas rechazadas: {total_rechazadas}")
                
            except FileNotFoundError:
                print(f"✗ Error: No se encontró el archivo '{archivo_cadenas}'")
            except Exception as e:
                print(f"✗ Error: {e}")
            
            input("\nPresione Enter para continuar...")
        
        elif opcion == '6':
            # Opción 6: Salir
            print("\n" + "="*70)
            print("¡Gracias por usar el Simulador de AFD!")
            print("Desarrollado con fines educativos")
            print("="*70)
            break
        
        else:
            print("\n✗ Opción inválida. Por favor, seleccione una opción del 1 al 6.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()