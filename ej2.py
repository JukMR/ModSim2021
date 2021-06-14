from random import random, seed
from math import log, ceil

seed(0) ## Fijar la semilla para debuggear

def Poisson_homogeneo(lamb, T):
    t = 0
    NT = 0
    Eventos = []
    while t < T:
        U = 1 - random()
        t += -log(U)/lamb
        if t <= T:
            NT += 1
            Eventos.append(t)
    return NT, Eventos



def simular_canal_aloha(lamb=0.5, T=10):
    neventos, canal = Poisson_homogeneo(lamb, T)
    # print(f"neventos es {neventos}")
    # print(f"canal es {canal}")
    colisiones= 0


    t_actual = 0
    paquetes_enviados = []
    paquetes_rotos = []

    while t_actual < T:
        if len(canal) > 1:
            if t_actual <= canal[0]:
                if canal[0] + 1 < canal[1]: ## Revisar que tengo tiempo suficiente para mandar el paquete
                    t_actual = canal[0] + 1
                    paquetes_enviados.append(canal[0] + 1)
                    canal.pop(0)

                else: ## No tengo tiempo para mandar el paquete, se rompe
                    paquetes_rotos.append(canal[0] + 1)
                    t_actual = canal[0] + 1
                    colisiones += 1
                    canal.pop(0)

            else:
                t_actual = canal[0] + 1
                paquetes_rotos.append(canal[0] + 1)
                canal.pop(0)
                colisiones += 1
        else:
            if len(canal) == 1:
                if canal[0] + 1 < T:
                        t_actual = canal[0] + 1
                        paquetes_enviados.append(canal[0] + 1)
                        canal.pop(0)
                else:
                    # print("Termine simulacion")
                    break
            else:
                # print("Termine simulacion")
                break

    return paquetes_enviados, paquetes_rotos,  colisiones, len(paquetes_enviados), neventos



res = simular_canal_aloha(lamb=0.5, T=20)

# print("paquetes_enviados", res[0])
# print("paquetes_rotos", res[1])
# print("colisiones", res[2])
# print("tiempo_uso", res[3])
# print("paquetes totales", res[4])



# Para este algoritmos los paquetes entran al canal en el momento ti. Si se
# generaron entre un t(i-1) y t(i) entonces "esperaran" hasta t(i) para entrar
# al canal

print()
def simular_canal_aloha_ranurado(lamb=0.5, T=10):
    neventos, canal = Poisson_homogeneo(lamb, T)
    # print(f"neventos es {neventos}")
    # print(f"canal es {canal}")


    n_paquetes_caidos = 0
    t_actual = 0
    paquetes_enviados = []
    paquetes_rotos = []

    while t_actual < T:
        if len(canal) > 1: ## El canal tiene dos elementos para comparar
            if ceil(canal[0]) + 1 <= canal[1]: ## En el intervalo solo un paquete quiere transmitir, exito.
                if len(paquetes_rotos) != 0 and paquetes_rotos[-1] == ceil(canal[0]): ## tirar el segundo paquete colapsado
                    paquetes_rotos.append(ceil(canal[0]))
                    canal.pop(0)
                    n_paquetes_caidos += 1
                else:
                    paquetes_enviados.append(ceil(canal[0]) + 1)
                    t_actual = ceil(canal[0]) + 1
                    canal.pop(0)

            else:
                if ceil(canal[0]) == ceil(canal[1]):
                    t_actual = ceil(canal[1])
                    paquetes_rotos.append(ceil(canal[0]))
                    canal.pop(0)
                    n_paquetes_caidos += 1
                else:
                    paquetes_enviados.append(ceil(canal[0]) + 1)
                    t_actual = ceil(canal[0])
                    canal.pop(0)

        else:
            # print("Termine simulacion")
            break

    return paquetes_enviados, paquetes_rotos,  n_paquetes_caidos, len(paquetes_enviados), neventos


res = simular_canal_aloha_ranurado(lamb=0.6, T=20)

# print("paquetes_enviados", res[0])
# print("paquetes_rotos", res[1])
# print("n_paquetes_caidos", res[2])
# print("tiempo_uso", res[3])
# print("paquetes totales", res[4])


# print(f"La tasa de uso es {res[3] / 20 * 100} %")


# Ejercicio a

def tasa_uso_puro(lamb, T):
    tiempo_uso = simular_canal_aloha(lamb=lamb, T=T)[3]
    return tiempo_uso/T * 100

def tasa_uso_ranurado(lamb, T):
    tiempo_uso = simular_canal_aloha_ranurado(lamb=lamb, T=T)[3]
    return tiempo_uso/T * 100


def ejercicio1(f, string):
    for k in range(1, 31):
        print(f"{string} : {f(0.1 * k, 10000):.2f} % para lamb = {0.1 * k:.2f}")


# ejercicio1(tasa_uso_puro, "tasa_uso_puro")
# ejercicio1(tasa_uso_ranurado, "tasa_uso_ranurado")

# ==================================================================
# Ejercicio b

def prob_paquete_puro(lamb, T):
    tmp = simular_canal_aloha(lamb=lamb, T=T)
    return tmp[3] / tmp[4]

def prob_paquete_ranurado(lamb, T):
    tmp = simular_canal_aloha_ranurado(lamb=lamb, T=T)
    return tmp[3] / tmp[4]

def ejercicio2(f, string):
    for k in range(1, 31):
        print(f"{string} : p = {f(0.1 * k, 10000):.2f} para lamb = {0.1 * k:.2f}")


# ejercicio2(prob_paquete_puro, "prob_paquete_puro")
# ejercicio2(prob_paquete_ranurado, "prob_paquete_ranurado")


# ==================================================================
# Ejercicio c

def ejercicio3(f, string):
    tasas, lambs  = [], []
    for k in range(1, 31):
        lamb = 0.1 * k
        Nsim = 10000

        lambs.append(lamb)
        tasas.append(f(lamb, Nsim)) # guardar tasa en un arreglo

        # print(f"{string} : {tasas[-1]:.2f} % para lamb = {lamb:.2f}")

    maximo = max(tasas)
    lamb_max = lambs[tasas.index(maximo)]

    return maximo, lamb_max

# print(ejercicio3(tasa_uso_puro, "tasa_uso_puro"))
# print(ejercicio3(tasa_uso_ranurado, "tasa_uso_ranurado"))

# ==================================================================
# Ejercicio d




tasas_uso_puro = [tasa_uso_puro(0.1 * k, T=10000) for k in range(1,31)]
tasas_uso_ranurado = [tasa_uso_ranurado(0.1 * k, T=10000) for k in range(1,31)]

lambs = [0.1 * k for k in range(1,31)]

# print(tasas_uso_puro)
# print(tasas_uso_ranurado)
# print(lambs)

import matplotlib.pyplot as plt

plt.title("Comparación tasas de uso versus distintos λ")
plt.plot(lambs, tasas_uso_puro, marker='o', color='blue', label="Aloha puro")
plt.xlabel("Lambdas")
plt.ylabel("Tasas uso")

plt.plot(lambs, tasas_uso_ranurado, marker='o', color='red', label="Aloha Ranurado")
plt.legend(loc='best')
plt.show()

