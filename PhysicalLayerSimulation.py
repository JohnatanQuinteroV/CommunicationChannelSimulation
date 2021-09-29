# Made by: Johnatan Quintero and Edin Cascante
# How to run?: python3 PhysicalLayerSimulation.py

import matplotlib.pyplot as plt
import random
import hamming_codec
import numpy as np
from random import random, uniform

#recibe bc(l) y devuelve señal modulada s(t)
def modulador4ASK(bcT):
    # salida sT y la señal c(t) portadora
    sT, c = [], []
    #vector de tiempo
    dt = 0.2
    t = np.arange(0, 6.4, dt) #tiempo de un periodo de seno        
    seno = np.sin(t)    #un periodo de seno
    #plt.plot(t,seno)
    #plt.show()
    for i in seno: #guardamos las 32 muestras del periodo de seno en c(t)
        c.append(round(i,4))     
    #Tomamos bcT y lo unificamos en una sola linea de bits
    UnitChain  = ''
    for k in bcT:
        for i in k:
            UnitChain += str(i)    
    #No es necesario rellenar con 0's la secuencia de entrada debido. 
    #Que la entrada de esta función es una secuencia de longitud par.
    #Ahora agrupamos bits en grupos de 2 debido a que se está simulando un modulador 4ASK.            
    counter1 = 0
    AuxString = ''
    AuxEntradaCodec = []        
    for k in UnitChain:
        counter1 += 1
        AuxString += k
        if counter1 == 2:
            AuxEntradaCodec.append(AuxString)
            counter1 = 0
            AuxString = ''
    Aux2bits = []
    for k in AuxEntradaCodec:
        k = bin(int(k,2))[2:].zfill(2)
        Aux2bits.append(k)
    # Se recorre el nuevo arreglo de bits y se asignan los símbolos
    # cada simbolo se multiplica por las 32 muestras que representan c(t).
    for k in Aux2bits:
        #print(k)
        if k == '00':  
            for i in c:
                sT.append(round(1*i, 4))  #se guarda un simbolo 1
        if k == '01':
            for i in c:
                sT.append(round(3*i, 4))  ##se guarda un simbolo 3
        if k == '10':
            for i in c:
                sT.append(round(5*i, 4))  #se guarda un simbolo 5             
        if k == '11':
            for i in c:
                sT.append(round(7*i, 4))  #se guarda un simbolo 7
    #print('Estos son los grupitos de 2 bits:\n', Aux2bits, '\n Y hay ', len(Aux2bits))
    #print('Estas son las',len(c), 'muestras del periodo de seno: ',c)
    #print('señal sT: ', sT, '\n Es de tamaño:',len(sT))
    return sT #retorna señal modulada paso banda


#recibe s(t) y devuelve señal con ruido s*(t)
def MedioRuidoso(sT):
    amplitudAWGN = 0.4   #ruido blanco gausseano
    dt = 1
    t = np.arange(0,len(sT),dt)  #vector de tiempo de tamano de sT
    AWGN = amplitudAWGN * np.random.randn(len(t)) #ruido AWGN de tamaño de la entrada
    #sumamos la señal modulada con el AWGN
    sRaux = sT+AWGN
    sR=[]
    for i in sRaux: #vamos a redondear cada valor
        sR.append(round(i, 5)) #guardamos la senal con ruido en sR
    #print('Se muestra la graafica de la señal de entrada al medio y la señal + ruido \n')    
    fig, axs = plt.subplots(3)
    axs[0].plot(t, sT)
    axs[0].set_ylabel('señal sT')
    axs[1].plot(t, AWGN, color='red')
    axs[1].set_ylabel('ruido')
    axs[2].plot(t, sRaux, color='purple')
    axs[2].set_ylabel('señal sR')
    axs[2].set_xlabel('tiempo')
    plt.show() 
    return sR


#recibe s*(t) y devuelve senal demodulada bc*(l)
def demulador4ASK(sR):
    #detector de envolvente, busca los picos de la señal
    grupode32, sR2 = [], []  # un grupo de 32 datos, representa un simbolo
    cont = 1
    for i in sR:  
        grupode32.append(i)  
        if cont == 32:   
            simboloAprox = max(grupode32) #valor max entre los 32 datos
            sR2.append(simboloAprox) #se guarda en sR2 como posible simbolo
            cont = 0
            grupode32 = [] #reiniciando el array y el contador
        cont += 1   
    #print('Detector de envolvente, los simbolos aproximados: \n',sR2,'de tamaño: ', len(sR2))
    bcR, AuxArray = [], []
    for k in sR2:         # Recorremos sR2 para ver a cuál símbolo se aproxima
        if 0.5 <= k < 2 :
            AuxArray.append(1)
        elif 2 <= k < 4:
            AuxArray.append(3)   #en este for se guardan los simbolos en AuxArray
        elif 4 <= k < 6:
            AuxArray.append(5)
        elif 6 <= k < 8:
            AuxArray.append(7)
    #print(AuxArray)
    #Finalmente se realiza la decodificación con los símbolos asignados anteriormente.
    for k in AuxArray:
        if k == 1:  
            bcR.append('00')  
        if k == 3:  
            bcR.append('01')    #en este for se decodifican los simbolos, guardando los bits en bcR
        if k == 5:  
            bcR.append('10')
        if k == 7:  
            bcR.append('11')
    #print(bcR)
    AuxChain=''
    for k in bcR:
        AuxChain+=k
    bcR=[]
    for k in AuxChain:
        Aux = bin(int(k,2))[2:].zfill(1)   #acomodando la salida en forma de cadena de bits
        bcR.append(Aux)
    return bcR


#recibe texto con info y devuelve la secuencia de bits bf(l)
def codificadorFuente(archivoEntrada):     
    with open(archivoEntrada) as f:  
        texto = ''
        info = []  
        line = True 
        while line: #vamos a leer archivo de entrada
            line = f.readline()
            texto += line      
            for simbolos in line:  
                info.append(simbolos) #se guarda cada simbolo en arreglo info
    print('Texto de entrada al codificador de fuente: \n', texto) 
    bfTaux = [] #arreglo para la secuencia de bits bf(l)
    for vT in info:  #vT es un simbolo 
        aux = ord(vT)  #se convirte el simbolo a ASCII
        bkT = bin(aux)[2:].zfill(8)  #bkT contiene los bits del simbolo
        bfTaux.append(bkT) #se guarda los bits en arreglo bfT
    # La info viene en secuencias de 8 bits, lo pasamos a una sola cadena
    bfT = ''
    for k in bfTaux:
        bfT += k    
    return bfT  

#recibe la secuencia de bits bf(l) devuelve la secuencia de bits bc(l)
def codificadorCanal(bfT):
    # Se agrupan en secuencias de 4 bits en una lista auxiliar
    counter1 = 0
    m = '' #string para secuencia de 4 bits
    AuxEntradaCod = [] #arreglo para concatenar todas las secuencias de 4 bits
    for bit in bfT:
        counter1 += 1
        m += bit  #guardamos cada bit en vector m
        if counter1 == 4:
            AuxEntradaCod.append(m)  #al llegar a 4 bits, se guarda m en AuxEntradaCod
            counter1 = 0 #reiniciando contador
            m = '' #limpiando el vector m
    mVectores = [] 
    for m in AuxEntradaCod:
        m = bin(int(m,2))[2:].zfill(4) #estamos recorriendo AuxEntradaCodec, y acomodando
        mVectores.append(m)  #guardamos m en arreglo de vectores m
    # Se define un codificador que toma secuencias de 4 bits y extensión n=3.
    # Se define la matriz G 4x4:
    b1 = [1 ,0 ,0 ,0]
    b2 = [0, 1 ,0 ,0]
    b3 = [0 ,0 ,1 ,0]
    b4 = [0 ,0 ,0, 1]
    # Las 3 columnas restantes, mediante método de vectores de bits de paridad
    p1, p2, p3 = [], [], []
    #Para p1
    for i in range(4):
        p1.append((b2[i] ^ b3[i] ^ b4[i]))
    #Para p2
    for i in range(4):
        p2.append((b1[i] ^ b3[i] ^ b4[i]))	
    #Para p3
    for i in range(4):
        p3.append((b1[i] ^ b2[i] ^ b4[i]))
    # Definimos una matriz auxiliar aux y la matriz G final
    G, aux1 = [], [] 
    for i in range(len(b1)): 
        aux1.append(p1[i])
        aux1.append(p2[i])
        aux1.append(p3[i]) 
        aux1.append(b1[i]) 
        aux1.append(b2[i])
        aux1.append(b3[i])
        aux1.append(b4[i])  
        G.append(aux1)
        aux1 = []
    G = np.matrix(G)
    print('Matriz G: \n',G)
    # teniendo los vectores m y la matriz G, multiplicamos
    bcT = []
    for m in mVectores:
        mAux = [int(m[0]),int(m[1]),int(m[2]),int(m[3])] #vector de m de 4 bits
        mAux = np.matrix(mAux)
        v = mAux * G   #multiplicando vector m por G
        v = v.tolist()
        v = v[0]  #tomando el resultado actual
        for k in range(len(v)): #revisando que todo sea binario
            if v[k]%2 == 0:
                v[k]=0
            else:
                v[k]=1
        bcT.append(v) #guardamos la secuencia de bits bc(l) en bcT
    return bcT
    
#recibe lo bits transmitidos bc(l), devuelve los bits recibidos bc*(l)    
def canalBSC(pe, bcT):
    longitud=len(bcT)   #guarda longitud de cadena de entrada
    bcTcompleta = []
    for i in bcT:
        for j in i:
            bcTcompleta.append(j)
    print('CANAL BSC. Cadena original que sale al canal:\n  ' ,bcTcompleta)
    #segun el error elejido y la longitud, se obtiene la cantidad de errores
    cantErrores = int(pe*longitud)
    cadena2=[]   #arreglo para las posiciones de bits con error
    cont=0
    while cont<cantErrores:   #crea lista con las posiciones aleatorias de bits con error
       temp=random.randrange(longitud)
       cadena2.append(temp)  
       cont=cont+1
    bcR= bcTcompleta #creamos arreglo para el resultado de bits leidos   
    for i in cadena2:  #para la lista cadena2 con las posiciones erroneas, cambiamos el bit
        temp2=bcR[i]
        if temp2 == 0:  #si es cero, lo borramos con del y insertamos un 1
            del bcR[i]
            bcR.insert(i,1)
        if temp2 == 1: #si es uno, lo borramos con del y insertamos un 0
            del bcR[i]
            bcR.insert(i,0)   
    print('CANAL BSC. Cadena luego de pasar por el canal: \n', bcR)
    return bcR
      
#recibe la secuencia de bits bc*(l) y devuelve la secuencia de bits bf*(l)    
def decodificadorCanal(bcR):
    # se agrupan en secuencias de 7 bits donde m ocupa 4 bits
    counter1 = 0
    AuxString = ''
    AuxEntradaCodec = []
    for k in bcR:
        counter1 += 1
        AuxString += str(k)
        if counter1 == 7:
            AuxEntradaCodec.append(AuxString) #creamos paquetes de 7 bits, luego de pasar por el BSC
            counter1 = 0
            AuxString = ''
    vectoresV = [] #guardara los vectores v
    for v in AuxEntradaCodec:
        v = bin(int(v,2))[2:].zfill(7)
        vectoresV.append(v)   
    #ahora obtenemos p1 p2 p3, que se obtienen con b1 b2 b3 y b4 
    b1 = [1 ,0 ,0 ,0]
    b2 = [0, 1 ,0 ,0]
    b3 = [0 ,0 ,1 ,0]
    b4 = [0 ,0 ,0, 1]
    # Posteriormente se deben definir las restantes 4 restantes columnas de la matriz H.
    # Esto por el método de vectores de bits de paridad que se obtienen como:
    p1, p2, p3 = [], [], []
	#Para p1
    for i in range(4):
        p1.append((b2[i] ^ b3[i] ^ b4[i])) 
	#Para p2
    for i in range(4):
        p2.append((b1[i] ^ b3[i] ^ b4[i]))	
	#Para p3
    for i in range(4):
        p3.append((b1[i] ^ b2[i] ^ b4[i]))
    # Definimos una matriz auxiliar aux y la matriz H final
    H, aux1 = [], []
    tmp=[p1,p2,p3]   #note que p1 p2 y p3 son de 4 bits y forman 4 filas 
    c1 = [1 ,0 ,0]
    c2 = [0, 1 ,0]
    c3 = [0 ,0 ,1]
    for i in range(len(c1)):  #matriz identidad 3x3 para el Decodificador
        aux1.append(c1[i]) 
        aux1.append(c2[i])
        aux1.append(c3[i])
        for j in tmp[i]:  #adjuntamos los bits de p1 p2 y p3 
            aux1.append(j)    
        H.append(aux1)
        aux1 = []
    H = np.matrix(H) #obtenemos H de forma 7x3
    H = np.transpose(H)
    print('Matriz H:\n',H)
    # ahora necesitamos saber si el paquete de 7bits recibido tiene error
    # multiplicamos el vector v por H, debe ser 0 si no hay error
    sindromes = []
    for v in vectoresV: #vamos a multiplicar v por H
        AuxList = [int(v[0]),int(v[1]),int(v[2]),int(v[3]),int(v[4]),int(v[5]),int(v[6])]
        AuxList = np.matrix(AuxList)
        vH = AuxList * H
        vH = vH.tolist()
        vH = vH[0]   #sindrome del paquete actual 
        for k in range(len(vH)):
            if vH[k]%2 == 0:
                vH[k]=0
            else:
                vH[k]=1
        sindromes.append(vH)
    #vectores de error de 7 bits
    e1 = [1 ,0 ,0, 0, 0, 0, 0]
    e2 = [0, 1 ,0, 0, 0, 0, 0]
    e3 = [0 ,0 ,1, 0, 0, 0, 0]
    e4 = [0 ,0 ,0, 1, 0, 0, 0]
    e5 = [0, 0 ,0, 0, 1, 0, 0]
    e6 = [0 ,0 ,0, 0, 0, 1, 0]
    e7 = [0 ,0 ,0, 0, 0, 0, 1]
    errores = [e1,e2,e3,e4,e5,e6,e7]  #arreglo con errores    
    entradaDeco = [] #guadara todos los paquetes de 7 bits correjidos
    Aux=0 # contador para ver si hay algun 1 en el sindrome
    vecV=0 
    #vamos a recorrer el arreglo de sindromes, hay unos solo con ceros. Otros con error
    for vH in sindromes:
        sindrome=vH
        for j in vH:
            if j == 1:
                Aux=Aux+1
        if Aux == 0: # en el sindrome solo hay ceros, no hay error
            entradaDeco.append(vectoresV[vecV]) 
        if Aux > 0:  # hay error en el sindrome hay algun 1
            actual=0
            vecVactual=vectoresV[vecV]
            numVectorError=0
            for k in errores:   #vamos a multiplicar todos los e1, e2, e3, .. por H
                AuxList = [int(k[0]),int(k[1]),int(k[2]),int(k[3]),int(k[4]),int(k[5]),int(k[6])]
                AuxList = np.matrix(AuxList)
                errorxH = AuxList * H
                errorxH = errorxH.tolist()
                errorxH = errorxH[0]
                #vamos a comparar si el resultado es igual a vH, si es igual dice cual bit es el malo
                if errorxH[0] == sindrome[0] and errorxH[1] == sindrome[1] and errorxH[2] == sindrome[2]:
                    actual= numVectorError #actual dice el bit con error                 
                numVectorError=numVectorError+1        
            vecAux='' #guarda los 7 bits correjidos
            conta1=0           
            for h in vecVactual:  #en el paquete de 7 bits, correjimos el bit con error
                if conta1 != actual: #va guardando bits 
                    vecAux=vecAux+h
                if conta1 == actual: #encontro el bit con error y se cambia
                    if h == 0:  #si es cero, agregamos un 1
                        vecAux=vecAux+'1'
                    else: #si es uno, agregamos un 0
                        vecAux=vecAux+'0'
                conta1=conta1+1                            
            entradaDeco.append(vecAux)  #guardamos el paquete de 7 bits ya correjidos en array
        Aux=0
        vecV=vecV+1 
    bfR=[] #guardara los vectores m
    for i in entradaDeco:    #guardamos solo el vector m, osea los ultimos 4 bits. 
        array=[i[3:7]]
        bfR.append(array)      
    return bfR  #retorna array con los vectores m
    
    
## Recibe la secuencia de bits bf*(l) y devuelve texto         
def decodificadorFuente(bfR, archivoSalida):  
    bfRcompleta = ''  
    for secuencia in bfR:  # recorremos bfR
        for bit in secuencia:
            bfRcompleta += str(bit)  # guardamos cada bit en bfRcompleta      
    cont = 0  # contador para contar grupos de 8 bits      
    info = ''   # guardara el texto de salida
    bkR = ''  # guardara los bits de cada simbolo
    for bitsSimbolo in bfRcompleta: 
        bkR += bitsSimbolo  
        cont += 1  
        if cont == 8:  # si se han recorrido 8 posiciones
            ascii = int(bkR,2) # pasa a codigo ASCII
            vR = chr(ascii)  # pasa a simbolo que son letras  
            info += vR  # concatena cada letra en string info
            cont=0  
            bkR=''   
    f2 = open(archivoSalida, 'w') # guardamos en un .text  
    f2.write(info)  
    f2.close()
    return info  # retorna el string con la info 

def main():
    
    archivoEntrada = 'Test.txt'  
    archivoSalida = 'TextOut.txt'  
    
    ## Codificador de Fuente
    bfT = codificadorFuente(archivoEntrada)
    print('Salida del codificador de fuente:\n',bfT)
    
    ## Codificador de Canal 
    bcT = codificadorCanal(bfT)  
    print('Salida del codificador de canal:\n',bcT)

    ## Modulador banda base
    sT = modulador4ASK(bcT)
    print('Salida del modulador paso banda 4ASK (solo se muestra una parte): \n',sT[0:100])
    
    ## Medio de transmicion con ruido
    sR = MedioRuidoso(sT)
    print('Salida del medio ruidoso (solo se muestra una parte): \n',sR[0:100])

    ## Demodulador banda base
    bcR = demulador4ASK(sR)
    print('Salida del demodulador paso banda 4ASK: \n',bcR)
    
    #pe= 0.1  
    #bcR = canalBSC(pe, bcT)  
    
    ## Decodificador de Canal
    bfR = decodificadorCanal(bcR)  
    print('Salida de decodificador de canal: \n',bfR)
    
    ## Decodificador de Fuente
    info = decodificadorFuente(bfR, archivoSalida)
    print('Salida del decodificador de fuente: \n', info) 
    
main = main()

