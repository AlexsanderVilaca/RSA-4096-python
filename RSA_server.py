from socket import *
import math
import ast

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5)
print ("TCP Server\n")

def totient_of(x, y):
    if x < 1 or y < 1:
        raise Exception("x e y devem ser inteiros maiores que 0") 
    return (x - 1) * (y - 1)

def get_numero_divisores(a, b):
    return math.gcd(a, b)

def criptografaMensagem(msg, e, N):
    retorno=[]
    for char in msg:
        retorno.append(pow(ord(char),e,N))
    return retorno

def decifraMensagem(msg, d, N):
    retorno = []
    for char in msg:
        retorno.append(chr(pow(char,d,N)))
    return retorno

p = 9370238212440980033
q = 11745888732460184683

N = p * q
print('Número de 4096 bits: ',N)
totient = totient_of(p, q)

divisor_encontrado = -1

for e in range(2, totient):
    if get_numero_divisores(totient, e) > 1: 
        continue
    else:
        divisor_encontrado = e
        break
    
d = pow(divisor_encontrado, -1, totient)

while True:
    
    connectionSocket, addr = serverSocket.accept()

    msgCriptografada = str(connectionSocket.recv(65000),'utf-8')
    msgCriptografada = msgCriptografada.split(',')

    integer_list = [int(element) for element in msgCriptografada]
    
    msgDecriptograda = ''.join(decifraMensagem(integer_list, d, N))
    
    msgDecriptograda = msgDecriptograda.upper()
    msgCriptografada = criptografaMensagem(msgDecriptograda, e, N)
    
    print("Enviando mensagem: ", msgCriptografada)
    connectionSocket.send(bytes(str(msgCriptografada),'utf-8'))

    connectionSocket.close()

    break