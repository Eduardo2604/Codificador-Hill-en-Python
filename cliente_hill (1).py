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

# ======= Cifrado =======
def cifrarMensaje(textoPlano, matrizClave):
    listaNumeros = textoANumeros(textoPlano)
    while len(listaNumeros) % len(matrizClave) != 0:
        listaNumeros.append(letraANumero[" "])
    bloques = [listaNumeros[i:i+len(matrizClave)] for i in range(0, len(listaNumeros), len(matrizClave))]
    resultado = []
    for bloque in bloques:
        producto = np.dot(matrizClave, bloque) % 27
        resultado.extend(producto)
    return numerosATexto(resultado)

# ======= Configuración del cliente =======
ipServidor = "192.168.1.10"  # Cambiar por la IP real del servidor
puertoServidor = 5000
matrizClave = np.array([
    [2, 3, 1],
    [1, 1, 1],
    [1, 2, 1]
])

# ======= Mensaje a enviar =======
mensajeOriginal = "HOLA MUNDO"
mensajeCifrado = cifrarMensaje(mensajeOriginal, matrizClave)
print(f"Mensaje original: {mensajeOriginal}")
print(f"Mensaje cifrado: {mensajeCifrado}")

# ======= Envío del mensaje =======
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ipServidor, puertoServidor))
cliente.send(mensajeCifrado.encode("utf-8"))
print("Mensaje enviado correctamente.")

# ======= Cierre =======
cliente.close()
