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
    print(f"neventos es {neventos}")
    canal.insert(3, 6.5)
    print(f"canal es {canal}")
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
                    print("Termine simulacion")
                    break
            else:
                print("Termine simulacion")
                break

    return paquetes_enviados, paquetes_rotos,  colisiones, len(paquetes_enviados)



res = simular_canal_aloha(lamb=0.5, T=20)

print("paquetes_enviados", res[0])
print("paquetes_rotos", res[1])
print("colisiones", res[2])
print("tiempo_uso", res[3])


# Para este algoritmos los paquetes entran al canal en el momento ti. Si se
# generaron entre un t(i-1) y t(i) entonces "esperaran" hasta t(i) para entrar
# al canal

print()
print()
print()
def simular_canal_aloha_ranurado(lamb=0.5, T=10):
    neventos, canal = Poisson_homogeneo(lamb, T)
    print(f"neventos es {neventos}")
    canal.insert(3, 6.5)
    print(f"canal es {canal}")


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
            print("Termine simulacion")
            break

    return paquetes_enviados, paquetes_rotos,  n_paquetes_caidos, len(paquetes_enviados)


res = simular_canal_aloha_ranurado(lamb=0.6, T=20)

print("paquetes_enviados", res[0])
print("paquetes_rotos", res[1])
print("n_paquetes_caidos", res[2])
print("tiempo_uso", res[3])