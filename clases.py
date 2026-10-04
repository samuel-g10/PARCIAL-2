import os
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat, whosmat

# Carpeta donde se guardan todos los gráficos
CARPETA_GRAFICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos")


# =====================================================================
# FUNCIONES DE VALIDACIÓN
# =====================================================================

def pedir_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        try:
            numero = int(texto)
        except ValueError:
            print("Error: debe escribir un número entero.")
            continue

        if numero < minimo or numero > maximo:
            print("Error: el número debe estar entre", minimo, "y", maximo)
        else:
            return numero

def pedir_ruta(mensaje, extension):
    while True:
        ruta = input(mensaje).strip().strip('"')
        if not os.path.isfile(ruta):
            print("Error: ese archivo no existe. Revise la ruta.")
        elif not ruta.lower().endswith(extension):
            print("Error: el archivo debe terminar en", extension)
        else:
            return ruta


def elegir_de_lista(titulo, lista):
    print(titulo)
    for i in range(len(lista)):
        print("  ", i + 1, ")", lista[i])
    posicion = pedir_entero("Elija una opción: ", 1, len(lista))
    return lista[posicion - 1]


def guardar_y_mostrar(nombre):
    if not os.path.exists(CARPETA_GRAFICOS):
        os.makedirs(CARPETA_GRAFICOS)
    ruta = os.path.join(CARPETA_GRAFICOS, nombre + ".png")
    plt.savefig(ruta, dpi=150)
    print("Gráfico guardado en:", ruta)
    plt.show()
    plt.close()

# =====================================================================
# FUNCIONES DE OPERACIÓN
# =====================================================================

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

# =====================================================================
# CLASE PARA ARCHIVOS CSV
# =====================================================================

class ArchivoCSV:

    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        self.tipo = "CSV"

        datos = pd.read_csv(ruta)

        if "time_ms" not in datos.columns or "condition" not in datos.columns:
            raise ValueError("El CSV debe tener las columnas 'time_ms' y 'condition'.")

        self.datos = datos.set_index("time_ms")

    def __str__(self):
        buffer = io.StringIO()
        self.datos.info(buf=buffer)

        texto = "=" * 60 + "\n"
        texto += "ARCHIVO CSV: " + self.nombre + "\n"
        texto += "=" * 60 + "\n"
        texto += "--- info() ---\n"
        texto += buffer.getvalue()
        texto += "\n--- describe() ---\n"
        texto += self.datos.describe().to_string()
        return texto

    def obtener_canales(self):
        canales = []
        for columna in self.datos.columns:
            if columna != "subject" and columna != "condition":
                canales.append(columna)
        return canales

    def obtener_condiciones(self):
        return sorted(self.datos["condition"].unique())

    def graficar_condicion(self, condicion, canal, canal_x, canal_y):
        datos_cond = self.datos[self.datos["condition"] == condicion]
        tiempo = datos_cond.index.values
        senal = datos_cond[canal].values

        plt.figure(figsize=(12, 9))

        plt.subplot2grid((2, 3), (0, 0), colspan=3)
        plt.stem(tiempo, senal, markerfmt=",", basefmt="gray")
        plt.axvline(0, color="red", linestyle="--", label="t = 0 ms")
        plt.title("Stem del canal " + canal)
        plt.xlabel("Tiempo (ms)")
        plt.ylabel("Amplitud (µV)")
        plt.legend()

        plt.subplot2grid((2, 3), (1, 0), colspan=2)
        plt.hist(senal, bins=30, color="steelblue", edgecolor="black")
        plt.title("Histograma del canal " + canal)
        plt.xlabel("Amplitud (µV)")
        plt.ylabel("Frecuencia (número de muestras)")

        plt.subplot2grid((2, 3), (1, 2))
        plt.scatter(datos_cond[canal_x].values, datos_cond[canal_y].values,
                    s=5, alpha=0.5, color="darkgreen")
        plt.title("Scatter " + canal_x + " vs " + canal_y)
        plt.xlabel(canal_x + " (µV)")
        plt.ylabel(canal_y + " (µV)")

        plt.suptitle(self.nombre + " - Condición " + str(condicion))
        plt.tight_layout()

        nombre_sin_ext = self.nombre.replace(".csv", "")
        guardar_y_mostrar(nombre_sin_ext + "_cond" + str(condicion) + "_" + canal)

    def diferencia_interhemisferica(self, canal1, canal2, condicion):

        nombre_columna = canal1 + "-" + canal2
        self.datos[nombre_columna] = self.datos[canal1] - self.datos[canal2]

        print("\nSe creó la columna nueva:", nombre_columna)
        print(self.datos[[canal1, canal2, nombre_columna]].head())
        print("\nResumen de la nueva columna:")
        print(self.datos[nombre_columna].describe())
   
        datos_cond = self.datos[self.datos["condition"] == condicion]
        plt.figure(figsize=(10, 5))
        plt.plot(datos_cond.index.values, datos_cond[nombre_columna].values,
                 color="purple", label=nombre_columna)
        plt.axvline(0, color="red", linestyle="--", label="t = 0 ms")
        plt.axhline(0, color="gray", linewidth=0.8)
        plt.title("Diferencia interhemisférica " + nombre_columna +
                  " - Condición " + str(condicion))
        plt.xlabel("Tiempo (ms)")
        plt.ylabel("Diferencia de amplitud (µV)")
        plt.legend()

        nombre_sin_ext = self.nombre.replace(".csv", "")
        guardar_y_mostrar(nombre_sin_ext + "_dif_" + nombre_columna + "_cond" + str(condicion))

# =====================================================================
# CLASE PARA ARCHIVOS MAT
# =====================================================================
class ArchivoMAT:
    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        self.tipo = "MAT"
        self.fs = 250  
        
                
        self.variables = whosmat(ruta)
        
        contenido = loadmat(ruta)
        self.llave = self.variables[0][0]      
        self.matriz = contenido[self.llave]     

    def __str__(self):
        texto = "=" * 60 + "\n"
        texto += "ARCHIVO MAT: " + self.nombre + "\n"
        texto += "Frecuencia de muestreo: " + str(self.fs) + " muestras/s\n"
        texto += "=" * 60 + "\n"
        texto += "Variable".ljust(18) + "Dimensiones".ljust(22) + "Tipo de dato\n"
        texto += "-" * 60 + "\n"
        for variable in self.variables:
            nombre = variable[0]
            dimensiones = str(variable[1])
            tipo = variable[2]
            texto += nombre.ljust(18) + dimensiones.ljust(22) + tipo + "\n"
        texto += "-" * 60 + "\n"
        texto += "(canales, muestras, ensayos)"
        return texto

    def num_canales(self):
        return self.matriz.shape[0]
    def num_puntos_2d(self):
            return self.matriz.shape[1] * self.matriz.shape[2]
    
    def operar_canales(self, funcion, canales, punto_min, punto_max):
        """Aplica suma, resta o multiplicacion sobre 4 canales, entre punto_min y punto_max.
        Grafica los 4 canales en un subplot y el resultado en otro."""
    
        matriz_2d = self.matriz.reshape(self.matriz.shape[0], -1)

        tramo = matriz_2d[:, punto_min:punto_max].astype(float)
    
        tiempo = np.arange(punto_min, punto_max) / self.fs
    
        resultado = tramo[canales[0] - 1]
        for i in range(1, len(canales)):
            resultado = funcion(resultado, tramo[canales[i] - 1])

        nombre_op = funcion.__name__
        if nombre_op == "suma":
            titulo = "Suma de los 4 canales"
            unidad = "µV"
        elif nombre_op == "resta":
            titulo = "Resta de los 4 canales"
            unidad = "µV"
        else:
            titulo = "Multiplicación de los 4 canales"
            unidad = "µV⁴"   

        plt.figure(figsize=(12, 8))


        plt.subplot(2, 1, 1)
        for c in canales:
            plt.plot(tiempo, tramo[c - 1], label="Canal " + str(c))
        plt.title("Canales seleccionados - " + self.nombre)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud (µV)")
        plt.legend(loc="upper right")

        plt.subplot(2, 1, 2)
        plt.plot(tiempo, resultado, color="black", label=titulo)
        plt.title(titulo)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Resultado (" + unidad + ")")
        plt.legend(loc="upper right")

        plt.tight_layout()
        nombre_sin_ext = self.nombre.replace(".mat", "")
        guardar_y_mostrar(nombre_sin_ext + "_" + nombre_op)

def promedio_y_desviacion(self, eje1, eje2):
        """Calcula promedio y desviación estándar sobre la matriz 3D original."""

        ejes = (eje1, eje2)
        promedio = np.mean(self.matriz, axis=ejes)
        desviacion = np.std(self.matriz, axis=ejes)

        print("\nForma del vector de promedios:", promedio.shape)
        print("Forma del vector de desviaciones estándar:", desviacion.shape)

        nombres_ejes = ["canales", "muestras", "ensayos"]
        eje_restante = 3 - eje1 - eje2

        plt.figure(figsize=(8, 6))
        plt.boxplot([promedio, desviacion])
        plt.xticks([1, 2], ["Promedio", "Desviación estándar"])
        plt.title("Distribución por " + nombres_ejes[eje_restante] +
                  "\n(calculado sobre ejes: " + nombres_ejes[eje1] +
                  " y " + nombres_ejes[eje2] + ") - " + self.nombre)
        plt.ylabel("Amplitud (µV)")
        plt.xlabel("Estadístico")

        nombre_sin_ext = self.nombre.replace(".mat", "")
        guardar_y_mostrar(nombre_sin_ext + "_boxplot_ejes" + str(eje1) + str(eje2))

# =====================================================================
# CLASE REGISTRO (punto extra): guarda todos los objetos y permite buscarlos
# =====================================================================

class Registro:
    def __init__(self):
        self.objetos = []

    def agregar(self, objeto):
        self.objetos.append(objeto)

    def cantidad(self):
        return len(self.objetos)

    def listar(self):
        if len(self.objetos) == 0:
            print("Todavía no hay archivos cargados.")
        for i in range(len(self.objetos)):
            objeto = self.objetos[i]
            print(i + 1, ")", objeto.tipo, "-", objeto.nombre)

    def buscar(self, texto):
        encontrados = []
        for objeto in self.objetos:
            if texto.lower() in objeto.nombre.lower():
                encontrados.append(objeto)
        return encontrados

    def obtener(self, posicion):
        return self.objetos[posicion - 1]