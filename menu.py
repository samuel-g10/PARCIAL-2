from clases import (ArchivoCSV, ArchivoMAT, Registro,
                    pedir_entero, pedir_ruta, elegir_de_lista,
                    suma, resta, multiplicacion)

# ---------------------------------------------------------------------
# CARGA DE ARCHIVOS
# ---------------------------------------------------------------------

def cargar_csv(registro):
    ruta = pedir_ruta("Ruta del archivo CSV (ej: Arch_CSV/ERP_01.csv): ", ".csv")
    try:
        objeto = ArchivoCSV(ruta)
        registro.agregar(objeto)
        print("Archivo cargado correctamente:", objeto.nombre)
    except Exception as error:
        print("No se pudo cargar el archivo:", error)


def cargar_mat(registro):
    ruta = pedir_ruta("Ruta del archivo MAT (ej: Archs_MAT/Sound_Cue.mat): ", ".mat")
    print("Cargando, puede tardar unos segundos...")
    try:
        objeto = ArchivoMAT(ruta)
        registro.agregar(objeto)
        print("Archivo cargado correctamente:", objeto.nombre)
    except Exception as error:
        print("No se pudo cargar el archivo:", error)

# ---------------------------------------------------------------------
# BÚSQUEDA
# ---------------------------------------------------------------------

def buscar_archivo(registro):
    texto = input("Escriba parte del nombre a buscar: ")
    encontrados = registro.buscar(texto)
    if len(encontrados) == 0:
        print("No se encontró ningún archivo con ese nombre.")
    else:
        print("Archivos encontrados:")
        for objeto in encontrados:
            print("  -", objeto.tipo, objeto.nombre)

# ---------------------------------------------------------------------
# SUBMENÚ CSV
# ---------------------------------------------------------------------

def menu_csv(objeto):
    while True:
        print("\n--- Archivo CSV:", objeto.nombre, "---")
        print("1. Ver información del archivo (info y describe)")
        print("2. Graficar por condición (stem, histograma y scatter)")
        print("3. Diferencia interhemisférica entre dos canales")
        print("0. Volver")
        opcion = pedir_entero("Opción: ", 0, 3)

        if opcion == 0:
            break

        elif opcion == 1:
            print(objeto)

        elif opcion == 2:
            condicion = elegir_de_lista("Condiciones disponibles:", objeto.obtener_condiciones())
            canales = objeto.obtener_canales()
            canal = elegir_de_lista("\nCanal para el stem y el histograma:", canales)
            canal_x = elegir_de_lista("\nCanal para el eje X del scatter:", canales)
            canal_y = elegir_de_lista("\nCanal para el eje Y del scatter:", canales)
            objeto.graficar_condicion(condicion, canal, canal_x, canal_y)

        elif opcion == 3:
            print("Pares homólogos (izquierda-derecha): FC3-FC4, C3-C4, CP3-CP4")
            canales = objeto.obtener_canales()
            canal1 = elegir_de_lista("\nPrimer canal (se le resta el segundo):", canales)
            canal2 = elegir_de_lista("\nSegundo canal:", canales)
            condicion = elegir_de_lista("\nCondición para graficar:", objeto.obtener_condiciones())
            objeto.diferencia_interhemisferica(canal1, canal2, condicion)
# ---------------------------------------------------------------------
# SUBMENÚ MAT
# ---------------------------------------------------------------------

def elegir_cuatro_canales(total_canales):
    canales = []
    while len(canales) < 4:
        numero = pedir_entero("Canal " + str(len(canales) + 1) + " de 4 (1-" +
                              str(total_canales) + "): ", 1, total_canales)
        if numero in canales:
            print("Ese canal ya fue elegido, escoja otro.")
        else:
            canales.append(numero)
    return canales


def menu_mat(objeto):
    while True:
        print("\n--- Archivo MAT:", objeto.nombre, "---")
        print("1. Ver variables del archivo (dimensiones y tipos)")
        print("2. Operar 4 canales (suma, resta o multiplicación)")
        print("3. Promedio y desviación estándar en dos ejes (boxplot)")
        print("0. Volver")
        opcion = pedir_entero("Opción: ", 0, 3)

        if opcion == 0:
            break

        elif opcion == 1:
            print(objeto)

        elif opcion == 2:
            print("Operaciones: 1) Suma  2) Resta  3) Multiplicación")
            num_op = pedir_entero("Elija la operación: ", 1, 3)
            if num_op == 1:
                funcion = suma
            elif num_op == 2:
                funcion = resta
            else:
                funcion = multiplicacion

            canales = elegir_cuatro_canales(objeto.num_canales())

            total = objeto.num_puntos_2d()
            print("La matriz en 2D tiene", total, "puntos por canal.")
            print("(cada", objeto.matriz.shape[1], "puntos es un ensayo de",
                  objeto.matriz.shape[1] / objeto.fs, "s)")
            punto_min = pedir_entero("Punto mínimo (0-" + str(total - 2) + "): ", 0, total - 2)
            punto_max = pedir_entero("Punto máximo (" + str(punto_min + 1) + "-" +
                                     str(total) + "): ", punto_min + 1, total)

            objeto.operar_canales(funcion, canales, punto_min, punto_max)

        elif opcion == 3:
            print("Ejes de la matriz: 0 = canales, 1 = muestras (tiempo), 2 = ensayos")
            eje1 = pedir_entero("Primer eje (0-2): ", 0, 2)
            eje2 = pedir_entero("Segundo eje (0-2): ", 0, 2)
            while eje2 == eje1:
                print("Error: los dos ejes deben ser diferentes.")
                eje2 = pedir_entero("Segundo eje (0-2): ", 0, 2)
            objeto.promedio_y_desviacion(eje1, eje2)
