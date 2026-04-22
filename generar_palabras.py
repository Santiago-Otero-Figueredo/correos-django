import string

def generar_palabras_3_letras():
    letras = string.ascii_lowercase  # abcdefghijklmnopqrstuvwxyz
    
    for l1 in letras:
        for l2 in letras:
            for l3 in letras:
                palabra = l1 + l2 + l3
                print(palabra)

# Ejecutar
generar_palabras_3_letras()
