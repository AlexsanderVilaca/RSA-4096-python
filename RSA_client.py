from socket import *
import math

serverName = "10.1.70.17"
serverPort = 1300

def shifttext(text, shift):
    data = list(text)
    for i, char in enumerate(data):
        print(i, char)
        data[i] = chr((ord(char) + shift))
        print(i, data[i], '\n')
    output = ''.join(data)
    return output

def totient_of(x, y):
    if x < 1 or y < 1:
        raise Exception("x e y devem ser inteiros maiores que 0") 
    return (x - 1) * (y - 1)

def get_numero_divisores(a, b):
    return math.gcd(a, b)

def criptografa_char(caracter, e, N):
    # return chr(ord(caracter) ** e % N)
    return chr(pow(ord(caracter), e, N))

def decifra_char(caracter, d, N):
    # print("o char", chr(ord(caracter)))
    return (ord(caracter) ** d) % N

def cifra_mensagem(msg, divisor_encontrado, N):
    retorno=[]
    for char in msg:
        retorno.append(pow(ord(char), divisor_encontrado, N))
    return retorno

def decifra_mensagem(msg, d, N):
    retorno = []
    for char in msg:
        retorno.append(chr(pow(char,d,N)))
    return retorno

def remove_brackets(text):
    return text.replace('[', '').replace(']', '')


p = 9370238212440980033 
q = 11745888732460184683

N = p * q #Este N que dá o tamanho da nossa chave RSA
totient = totient_of(p, q)

divisores_encontrados = 0
divisor_encontrado = -1

for e in range(2, totient):
    divisores_encontrados = 0
    # for j in range(e, totient):
    if get_numero_divisores(totient, e) > 1: 
        continue
    else:
        divisor_encontrado = e
        break
    # if divisor_encontrado > 0:
    #     break


#pode haver mais de um 'd' que satisfaça essa igualdade,
#por conveniência pegamos o primeiro que encontramos
# d = 0
# while True:
#     if divisor_encontrado * d % totient == 1:
#         break
#     d+=1

d = pow(divisor_encontrado, -1, totient)

print("Chave pública = fator 'e'", divisor_encontrado)
print("Chave privada = fator 'd'", d)

mensagem = 'The information security is of significant importance to ensure the privacy of communications'

# print(cifra_mensagem(mensagem, divisor_encontrado, N))
# print(decifra_mensagem(cifra_mensagem(mensagem, divisor_encontrado, N), d, N))

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM) 
    clientSocket.connect((serverName,serverPort))

    # print("Texto decifrado a ser enviado", ','.join(mensagem))
    texto_cifrado = cifra_mensagem(mensagem, divisor_encontrado, N)
    texto_tratado = str(texto_cifrado).replace('[', '').replace(']', '')

    # print("Texto cifrado a ser enviado para o server", texto_cifrado)
    clientSocket.send(bytes(str(texto_tratado), 'utf-8'))

    msg_retorno = str(clientSocket.recv(65000), 'utf-8')

    msg_retorno = remove_brackets(msg_retorno).split(',')
    msg_retorno = [int(x) for x in msg_retorno]

    # print("Mensagem pura recebida do server", msg_retorno)
    print("Mensagem recebida do server é:", ''.join(decifra_mensagem(msg_retorno, d, N)))

    clientSocket.close()
    break