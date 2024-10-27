import pandas as pd
import re
from graphviz import Digraph

def imprimirMatriz(estados_lista, simbolos_entrada, matriz, estados_aceptacion_num):
    df = pd.DataFrame(matriz, index=estados_lista)
    columnas_multiindex = pd.MultiIndex.from_product([['Simbolos de Entrada'], simbolos_entrada])
    df.columns = columnas_multiindex
    df[('Estados de Aceptación', '')] = estados_aceptacion_num
    print(df)

def graficarBurbuja(estados_lista, matriz, estados_aceptacion, simbolos_entrada, nombre_diagrama):
    dot = Digraph()
    for i, estado in enumerate(estados_lista):
        if estados_aceptacion[i] == 1:
            dot.node(estado, estado, shape='doublecircle')
        else:
            dot.node(estado, estado, shape='circle')
    for i, estado in enumerate(estados_lista):
        for j, simbolo in enumerate(simbolos_entrada):
            transiciones = matriz[i][j]
            if transiciones:
                for transicion in transiciones.split(','):
                    dot.edge(estado, transicion, label=str(simbolo))
    dot.node('Inicio', 'Inicio', shape='plaintext')
    dot.edge('Inicio', estados_lista[0], label='')
    dot.render(nombre_diagrama, format='png', cleanup=True)

matrizNoDeterministica = []
matrizDeterministica = []
estados = []
simbolosEntrada = []
estadosAceptacionDeterministico = []
estadosAceptacionNumero = []
estadosAceptacionLetra = []
estadoNoDeterministico = []
fila = []
evaluacionEstadosAceptacion = []
nuevoEstado = 1
estadoMatrizDeterministica = ''
filaNuevaMatriz = 0
siguienteEstado = ''
estadosSinDuplicados = ''
estadoAcepta = False
estadoDeError = False
automataEsNoDeterministico = False

def solicitar_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("El dato debe de ser un número. Por favor, intente de nuevo.")

cantidadDeEstados = solicitar_numero('Digite la cantidad de ESTADOS del autómata: ')
for cantidadEstado in range(cantidadDeEstados):
    estados.append(input(f'Digite el ESTADO, número {cantidadEstado + 1}: ').upper())

cantidadDeSimbolosEntrada = solicitar_numero('Digite la cantidad de SÍMBOLOS DE ENTRADA del autómata: ')
for cantidadSimboloEntrada in range(cantidadDeSimbolosEntrada):
    simbolosEntrada.append(input(f'Digite el SÍMBOLO DE ENTRADA, número {cantidadSimboloEntrada + 1}: '))

cantidadDeEstadosAceptacion = solicitar_numero('Digite la cantidad de ESTADOS DE ACEPTACIÓN del autómata: ')
for cantidadEstadoAceptacion in range(cantidadDeEstadosAceptacion):
    estadosAceptacionLetra.append(input(f'Digite el ESTADO DE ACEPTACIÓN número {cantidadEstadoAceptacion + 1}: ').upper())

print('\nPara decir que un estado no va a ninguna parte (ERROR), por favor no digite nada, solo presione ENTER\n')
print('Para poner que un estado va hacia dos o más estados, por favor separar por comas, ejemplo: A,B\n')

for filaMatrizInicial in range(len(estados)):
    matrizNoDeterministica.append([])
    for columnaMatrizInicial in range(len(simbolosEntrada)):
        estadoEnCadena = input(f'En el estado {estados[filaMatrizInicial]}, cuando llega un {simbolosEntrada[columnaMatrizInicial]}, ¿hacia dónde va?: ').upper()
        estadoEnCadena = re.sub(r',+', ',', estadoEnCadena.strip())
        if estadoEnCadena.endswith(','):
            estadoEnCadena = estadoEnCadena[:-1]
        if ',' in estadoEnCadena:
            automataEsNoDeterministico = True
        if estadoEnCadena == '':
            estadoEnCadena = None
        matrizNoDeterministica[filaMatrizInicial].append(estadoEnCadena)

colaDeEstados = [estados[0]]
estadosNuevos = [estados[0]]

for iterador in range(len(estados)):
    if estados[iterador] in estadosAceptacionLetra:
        estadosAceptacionNumero.append(1)
    else:
        estadosAceptacionNumero.append(0)

estadosAceptacionDeterministico.append(estadosAceptacionNumero[0])

print(' AUTOMATA NO DETERMINISTICO \n')
imprimirMatriz(estados, simbolosEntrada, matrizNoDeterministica, estadosAceptacionNumero)
graficarBurbuja(estados, matrizNoDeterministica, estadosAceptacionNumero, simbolosEntrada, 'diagramaNoDeterministico')
print('Diagrama generado: diagramaNoDeterministico.png')

if not automataEsNoDeterministico:
    print('\nEl autómata ya es determinístico')
else:
    while colaDeEstados:
        fila = []
        siguienteEstado = colaDeEstados[0]
        if (',' in siguienteEstado):
            estadoNoDeterministico = siguienteEstado.replace(' ', '').split(',')
            for estadoIndependiente in estadoNoDeterministico:
                fila.append(estados.index(estadoIndependiente))
        else:
            fila.append(estados.index(siguienteEstado))
        fila.sort()
        matrizDeterministica.append([])
        for simboloEntrada in range(len(simbolosEntrada)):
            estadoMatrizDeterministica = ''
            for indiceFila in fila:
                estadoActual = matrizNoDeterministica[indiceFila][simboloEntrada]
                if estadoActual is not None:
                    if estadoMatrizDeterministica is None:
                        estadoMatrizDeterministica = ''
                    estadoMatrizDeterministica += estadoActual + ','
                if estadoMatrizDeterministica == '':
                    estadoMatrizDeterministica = None
            if estadoMatrizDeterministica is not None:
                estadoMatrizDeterministica = estadoMatrizDeterministica.rstrip(',')
                estadoMatrizDeterministica = ','.join(sorted(estadoMatrizDeterministica.split(',')))
                estadosSinDuplicados = ','.join(dict.fromkeys(estadoMatrizDeterministica.split(',')))
                estadoMatrizDeterministica = estadosSinDuplicados
                if not(estadoMatrizDeterministica.replace(' ', '').replace(',', '') in estadosNuevos):
                    colaDeEstados.append(estadoMatrizDeterministica)
                    estadosNuevos.append(estadoMatrizDeterministica.replace(' ', '').replace(',', ''))
                    evaluacionEstadosAceptacion = estadoMatrizDeterministica.split(',')
                    estadoAcepta = any(estadoAceptacion in evaluacionEstadosAceptacion for estadoAceptacion in estadosAceptacionLetra)
                    if estadoAcepta:
                        estadosAceptacionDeterministico.append(1)
                    else:
                        estadosAceptacionDeterministico.append(0)
                matrizDeterministica[filaNuevaMatriz].append(estadoMatrizDeterministica.replace(' ', '').replace(',', ''))
            else:
                matrizDeterministica[filaNuevaMatriz].append(estadoMatrizDeterministica)
        filaNuevaMatriz += 1
        colaDeEstados.pop(0)
        if filaNuevaMatriz == 15:
            print('Iteraciones Máximas alcanzadas')
            break

    for filaMatriz in range(len(matrizDeterministica)):
        for columnaMatriz in range(len(matrizDeterministica[filaMatriz])):
            if matrizDeterministica[filaMatriz][columnaMatriz] is None:
                estadoDeError = True
                matrizDeterministica[filaMatriz][columnaMatriz] = 'ERROR'

    for filaMatriz in range(len(matrizNoDeterministica)):
        for columnaMatriz in range(len(matrizNoDeterministica[filaMatriz])):
            if matrizNoDeterministica[filaMatriz][columnaMatriz] is None:
                matrizNoDeterministica[filaMatriz][columnaMatriz] = ''

    if estadoDeError:
        estadosNuevos.append('ERROR')
        matrizDeterministica.append(['ERROR'] * len(simbolosEntrada))
        estadosAceptacionDeterministico.append(0)

    print('\nAUTOMATA DETERMINISTICO\n')
    imprimirMatriz(estadosNuevos, simbolosEntrada, matrizDeterministica, estadosAceptacionDeterministico)
    graficarBurbuja(estadosNuevos, matrizDeterministica, estadosAceptacionDeterministico, simbolosEntrada, 'diagramaDeterministico')
    print('Diagrama generado: diagramaDeterministico.png')
