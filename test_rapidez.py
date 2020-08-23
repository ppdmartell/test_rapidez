import time
from colorama import Fore, Style
import numpy as np
import matplotlib.pyplot as plt

VALORES = {}
CANT_EJEC = 5
GRAFICAR = 'S'

def ciclo(fn):
    def interna():
        for i in range(0, CANT_EJEC):
            fn()
    return interna

def logger(fn):
    @ciclo
    def interna():
        inicio = time.time()
        fn()
        duracion = time.time() - inicio
        if fn.__name__ not in VALORES:
            VALORES[fn.__name__] = [0, []]
        VALORES[fn.__name__][0] += 1
        VALORES[fn.__name__][1].append(duracion)
    return interna

def graficar():
    valores_nfunc = []
    valores_tprom = []
    valores_tmax = []
    valores_tmin = []
    for key in VALORES.keys():
        valores_nfunc.append(key)
    for valor in VALORES.values():
        valores_tprom.append(sum(valor[1])/len(valor[1]))
    for valor in VALORES.values():
        valores_tmax.append(max(valor[1]))
    for valor in VALORES.values():
        valores_tmin.append(min(valor[1]))

    plt.figure(figsize=[15, 10])
    X = np.arange(len(valores_tmin))
    plt.bar(X, valores_tmin, color = 'black', width = 0.25)
    plt.bar(X + 0.25, valores_tprom, color = 'g', width = 0.25)
    plt.bar(X + 0.5, valores_tmax, color = 'b', width = 0.25)
    plt.legend(['Tiempo mínimo', 'Tiempo promedio', 'Tiempo máximo'])
    plt.xticks([i + 0.25 for i in range(len(valores_nfunc))], valores_nfunc)
    plt.title(f"Tiempo de ejecución de las funciones luego de {CANT_EJEC} iteraciones.")
    plt.xlabel('Funciones')
    plt.ylabel('Tiempo de ejecución')
    plt.savefig('4BarPlot.png')
    plt.show()

########################## Espacio de configuración ##########################

@logger
def func_uno():
    print('Esta es la función UNO.')

@logger
def func_dos():
    print('Esta es la función DOS.')

@logger
def func_tres():
    print('Esta es la función TRES.')

def funciones_registradas():
    func_uno()
    func_dos()
    func_tres()

##############################################################################

def resultados():
    print('\n')
    print('#############################################################')
    print('#             RESULTADOS DE LA EJECUCIÓN:                   #')
    print('#############################################################')
    print('\n')
    for fnombre, datos in VALORES.items():
        tiempo_max = max(datos[1])
        tiempo_min = min(datos[1])
        tiempo_promedio = sum(datos[1]) / len(datos[1])
        print(f'La función "{Fore.BLUE}{fnombre}{Style.RESET_ALL}"" se ejecutó {Fore.BLUE}{CANT_EJEC}{Style.RESET_ALL} veces con los resultados:\n')
        print(f'{Fore.GREEN}Tiempo mínimo:{Style.RESET_ALL}      {tiempo_min}')
        print(f'{Fore.RED}Tiempo máximo:{Style.RESET_ALL}      {tiempo_max}')
        print(f'Tiempo promedio:    {tiempo_promedio}\n')
        print('------------------------------------------------------------------------')

def ejecutar_test():
    error = True
    while error:
        try:
            global CANT_EJEC
            CANT_EJEC = int(input('Entre la cantidad de ejecuciones a realizar: '))
        except ValueError:
            print('El tipo de dato introducido es incorrecto.')
        else:
            error = False

    funciones_registradas()
    resultados()

ejecutar_test()
error = False
while not error:
        GRAFICAR = input('Desea graficar resultados? (S/N): ')
        if (GRAFICAR.lower() != 'n' and GRAFICAR.lower() != 's'):
            print('Valor distinto de los posibles requeridos.')
        elif GRAFICAR.lower() == 's':
            graficar()
            error = True
        else:
            error = True
