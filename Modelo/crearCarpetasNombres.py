import os
import unicodedata

# Lista original con nombres completos
nombres_completos = [
    "Gonzalo Alfaro Caso",
    "Bladimir Alferez Vicente",
    "Margiory Alvarado Chávez",
    "Max Bryam Antúnez Alfaro",
    "Josué Mauricio Arriaga Colchado",
    "Nicolas Mateo Arroyo Chávez",
    "Stuart Diego Arteaga Montes",
    "Marcos Daniel Ayala Pineda",
    "Kelvin Andreí Cahuana Condori",
    "Alejandro Gerardo Calizaya Álvarez",
    "Aaron Arturo Camacho Valencia",
    "Enzo Gabriel Camizan Vidal",
    "Anderson David Cárcamo Vargas",
    "José Rafael Chachi Rodriguez",
    "Edgar Moisés Chambilla Mamani",
    "Alexandro Martin Chamochumbi Gutierrez",
    "Luis Antonio Gutierrez Guanilo",
    "Alexander Guzmán Bendezú",
    "Juan Jose Leandro Blas",
    "Davi Magalhaes Eler",
    "Luis Méndez Lázaro",
    "Rensso Victor Hugo Mora Cloque",
    "Ernesto Paolo Ormeño Gonzales",
    "Jose Eddison Pinedo Espinoza",
    "Dimael Antonio Rivas Chavez",
    "Andres Jaffet Riveros Soto",
    "Luis David Torres Osorio",
    "Isaac Alfredo Vera Romero",
    "Jose Francisco Wong Orrillo"
]

# Función para normalizar texto: minúsculas, sin tildes ni caracteres especiales
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    return texto

# Crear carpetas con el formato nombre_apellido
for nombre_completo in nombres_completos:
    partes = nombre_completo.strip().split()
    if len(partes) >= 2:
        primer_nombre = normalizar(partes[0])
        primer_apellido = normalizar(partes[-2])  # penúltimo si hay más de dos apellidos
        nombre_carpeta = f"{primer_nombre}_{primer_apellido}"
        os.makedirs(nombre_carpeta, exist_ok=True)
        print(f"Carpeta creada: {nombre_carpeta}")
    else:
        print(f"No se pudo procesar: {nombre_completo}")
