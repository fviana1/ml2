from flask import Flask, jsonify, request, abort
import array
from satelite import Satelite
import math
from satelites import satelites 

app = Flask(__name__)

@app.route('/ruta1')
def ruta1():
    return jsonify({"message": 'ola k ase'})


##Función para obtener las coordenadas del emisor
def GetLocation(distances):
    #Satelite 1:
    x0 = sats[0].coordenadasX
    y0 = sats[0].coordenadasY
    r0 = distances[0]

    #Satelite 2:
    x1 = sats[1].coordenadasX
    y1 = sats[1].coordenadasY
    r1 = distances[1]

    #Satelite 3:
    x2 = sats[2].coordenadasX
    y2 = sats[2].coordenadasY
    r2 = distances[2]

    #Intersección satelites 1 y 2:
    res1 = GetIntersections(x0, y0, r0, x1, y1, r1)

    #Intersección satelites 1 y 3:
    res2 = GetIntersections(x0, y0, r0, x2, y2, r2)

    if res1 == None or res2 == None:
        location = []
    elif (res1[0] == res2[0] and res1[1] == res2[1]):
        location = (res1[0], res1[1])
    elif (res1[0] == res2[2] and res1[1] == res2[3]):
        location = (res1[0], res1[1])
    elif (res1[2] == res2[0] and res1[3] == res2[1]):
        location = (res1[2], res1[3])
    elif (res1[2] == res2[2] and res1[3] == res2[3]):
        location = (res1[2], res1[3])

    #Revisar si hay una ubicación o no se encontró.

    return location

##Fin función GetLocation


@app.route('/topsecret', methods=['POST'])
def topSecret():
    i = len(request.json['satellites']) #Cantidad de satelites
    distancias = []
    mensajes = []

    for s in request.json['satellites']:
        distancias.append(s['distance'])
        mensajes.append(s['message'])

    print(distancias)
    print(mensajes)

    ubicacion = []
    ubicacion = GetLocation(distancias)

    if ubicacion != []:
        return 
        {
            "position": 
                {
                "x": ubicacion[0],
                "y": ubicacion[1]
                },
            "message": GetMessage(mensajes)
        }
    elif(ubicacion == []):
        return abort(404)


##Función para obtener la intersección de dos círculos
def GetIntersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)
##Fin función get_Inteserseccion

#Función para descifrar el mensaje
def GetMessage(messages):
    #tamaño del mensaje en cantidad de palabras
    tam = len(messages[0])

    msgDescifrado = [""] * tam

    for mensaje in messages:
        i = 0
        for palabra in mensaje:
            if palabra != "" and msgDescifrado[i] == "":
                msgDescifrado[i] = palabra
            i = i + 1

    msg = ""
    for pal in msgDescifrado:
        msg = msg + pal + " " 
    
    return msg
##Fin función GetMessage


#Función para inicializar los satelites
def Inicializar():
    #cantidad de satelites
    k = len(satelites)

    sats = [None] * k
    i = 0
    for sat in satelites:
        sats[i] = Satelite(sat['name'], sat['coordenadasX'], sat['coordenadasY'])
        i = i + 1

    return sats
##Fin función Inicializar

if __name__ == '__main__':
    sats = Inicializar()
    app.run(debug=True, port=5000)
