import fileinput

# S-boxes
sbox1 = [["01","00","11","10"],["11","10","01","00"],["00","10","01","11"],["11","01","11","10"]]
sbox2 = [["00","01","10","11"],["10","00","01","11"],["11","00","01","00"],["10","01","00","11"]]

# Lee entradas
lines = []
for line in fileinput.input():
    lines.append(line)

# Permutación inicial
def permut(text, mode):
    if mode == 0:
        out = text[1]+text[5]+text[2]+text[0]+text[3]+text[7]+text[4]+text[6]
    elif mode == 1:
        out = text[3]+text[0]+text[2]+text[4]+text[6]+text[1]+text[7]+text[5]
    return out

# Subkeys inicial
def subkey(key):
    sub1 = key[0]+key[6]+key[8]+key[3]+key[7]+key[2]+key[9]+key[5]
    sub2 = key[7]+key[2]+key[5]+key[4]+key[9]+key[1]+key[8]+key[0]
    return sub1, sub2

# Paso feistel
def feistel(perm, subk):
    global sbox1, sbox2

    # Dividir, extender parte derecha 
    left = perm[0]+perm[1]+perm[2]+perm[3]
    right = perm[4]+perm[5]+perm[6]+perm[7]
    rightPer = right[3]+right[0]+right[1]+right[2]+right[1]+right[2]+right[3]+right[0]

    # Mezclar con subkey
    mix = int(rightPer, base=2)^int(subk, base=2)
    mix = "{0:08b}".format(mix) # Cambiar a int

    # Sacar valores de las s-boxes
    svalues = sbox1[int(mix[0]+mix[3], base = 2)][int(mix[1]+mix[2], base = 2)]+ sbox2[int(mix[4]+mix[7], base = 2)][int(mix[5]+mix[6], base = 2)]
    svalues = svalues[1]+svalues[3]+svalues[2]+svalues[0]

    # Mezclar parte izq son svalues
    mix = int(left, base=2)^int(svalues, base=2)
    mix = "{0:04b}".format(mix) # Cambiar a int

    # Regresar concatenación
    return mix + right

def algSDES(mode, key, text):
    perm = permut(text,0) # Perm Inicial
    sk1, sk2 = subkey(key) # Subkeys
    # Pasos feiste
    if mode == 'E':
        perm = feistel(perm, sk1)
        perm = perm[4]+perm[5]+perm[6]+perm[7]+perm[0]+perm[1]+perm[2]+perm[3] # Cambiar izq por der
        perm = feistel(perm, sk2)
    elif mode == 'D':
        perm = feistel(perm, sk2)
        perm = perm[4]+perm[5]+perm[6]+perm[7]+perm[0]+perm[1]+perm[2]+perm[3] # Cambiar izq por der
        perm = feistel(perm, sk1)
    perm = permut(perm,1) # Perm Inicial
    return perm

# Obtener las llaves y texto plano, limpiando el input
mode = lines[0].replace("\n","")
key = lines[1].replace("\n","")
text = lines[2].replace("\n","")

# Algoritmo main
print(algSDES(mode,key,text))