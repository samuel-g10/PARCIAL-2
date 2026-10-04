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
