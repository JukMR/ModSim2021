from random import random, seed
import math

seed(0) ## Fijar la semilla para debuggear

# Opcion 2 (Notas)
def Poisson_homogeneo(lamb, T, mu, t_inicial=0):
    t_inicial = 0
    NT = 0
    Eventos = []
    while t_inicial < T:
        U = 1 - random()
        t_inicial += -math.log(U)/lamb
        if t_inicial <= T:
            NT += 1
            Eventos.append((t_inicial, exponencial(mu)))
    return NT, Eventos, Eventos[-1]


def exponencial(lamda):
    U = 1-random()
    return -math.log(U)/lamda

# print(exponencial(1))


def simular_canal(lamb=0.5, T=10, mu=1):
    neventos, canal, ultimo_tiempo = Poisson_homogeneo(lamb=lamb, T=T, mu=1, t_inicial=0)

    ultimo_tiempo = ultimo_tiempo[0]

    # print(f"neventos es {neventos}")
    # print(f"canal es {canal}")

    # for i in range(len(canal)):
    #     print(canal[i][0], canal[i][1], canal[i][0] + canal[i][1])

    paquetes_enviados = 0
    tiempo_actual = 0
    encolados = 0

    buffer = []
    tiempos_salida = []

    while tiempo_actual <= ultimo_tiempo:
        if len(buffer) > 0: ## Tengo algo en el buffer
            tiempo_actual += (buffer[0][1])
            tiempos_salida.append(tiempo_actual)
            paquetes_enviados += 1
            buffer.pop(0)
        else: ## El buffer esta vacio
            if len(canal) > 0: ## El canal tiene algun paquete
                if tiempo_actual > canal[0][0]: ## Me pasé algún paquete que tengo que encolar
                    buffer.append(canal[0])
                    canal.pop(0)
                    encolados += 1
                else: ## El buffer esta vacio y no perdí ningún paquete. Atiendo el paquete
                    tiempo_actual = canal[0][0] + canal[0][1]
                    paquetes_enviados += 1
                    tiempos_salida.append(canal[0][0] + canal[0][1])
                    canal.pop(0)

            else: ## El canal esta vacio. Simulo nuevos paquetes
                nuevaIter = Poisson_homogeneo(lamb=lamb, T=ultimo_tiempo+10, mu=1, t_inicial=ultimo_tiempo)
                neventos += nuevaIter[0]
                for i in nuevaIter[1]:
                    canal.append(i)
                ultimo_tiempo = nuevaIter[2][0]

    return paquetes_enviados, tiempo_actual, tiempos_salida, encolados


def revisar_simular_canal(res):
    tmp = 0
    for i in res[2]:
        if tmp > i:
            raise ValueError('Los tiempos de salida se solapan')
        tmp = i
    return True



res = simular_canal(lamb=0.5, T=10, mu=1)

print(f"\nPaquetes enviados {res[0]}\n tiempo_actual {res[1]}\n tiempos_salida {res[2]}\n encolados {res[3]}\n")

assert(revisar_simular_canal(res))