# ======= Importaciones =======
import socket
import numpy as np

# ======= Alfabeto y diccionarios =======
alfabetoZ27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
letraANumero = {letra: indice for indice, letra in enumerate(alfabetoZ27)}
numeroALetra = {indice: letra for indice, letra in enumerate(alfabetoZ27)}

# ======= Funciones de utilidad =======
def textoANumeros(texto):
    return [letraANumero[letra] for letra in texto.upper()]

def numerosATexto(listaNumeros):
    return ''.join(numeroALetra[numero % 27] for numero in listaNumeros)

def inversoMultiplicativo(numero, modulo):
    for posibleInverso in range(1, modulo):
        if (numero * posibleInverso) % modulo == 1:
            return posibleInverso
    raise ValueError(f"No hay inverso para {numero} módulo {modulo}")

def matrizInversaModulo(matriz, modulo):
    determinante = int(round(np.linalg.det(matriz))) % modulo
    inversoDeterminante = inversoMultiplicativo(determinante, modulo)
    adjunta = np.round(determinante * np.linalg.inv(matriz)).astype(int) % modulo
    return (inversoDeterminante * adjunta) % modulo

# ======= Descifrado =======
def descifrarMensaje(textoCifrado, matrizClave):
    matrizClaveInversa = matrizInversaModulo(matrizClave, 27)
    listaNumeros = textoANumeros(textoCifrado)
    bloques = [listaNumeros[i:i+len(matrizClave)] for i in range(0, len(listaNumeros), len(matrizClave))]
    resultado = []
    for bloque in bloques:
        producto = np.dot(matrizClaveInversa, bloque) % 27
        resultado.extend(producto)
    return numerosATexto(resultado)

# ======= Configuración del servidor =======
ipServidor = "0.0.0.0"
puertoServidor = 5000
matrizClave = np.array([
    [2, 3, 1],
    [1, 1, 1],
    [1, 2, 1]
])

# ======= Inicio del servidor =======
print("Iniciando servidor...")
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ipServidor, puertoServidor))
servidor.listen(1)
print(f"Esperando conexión en el puerto {puertoServidor}...")

cliente, direccionCliente = servidor.accept()
print(f"Conectado desde {direccionCliente}")

# ======= Recepción y descifrado =======
mensajeCifrado = cliente.recv(1024).decode("utf-8")
print(f"Mensaje cifrado recibido: {mensajeCifrado}")

mensajeDescifrado = descifrarMensaje(mensajeCifrado, matrizClave)
print(f"Mensaje descifrado: {mensajeDescifrado}")

# ======= Cierre =======
cliente.close()
servidor.close()
