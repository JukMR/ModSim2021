# Introducción

## Ejercicio 1

En este ejercicio debemos simular un canal en el que los paquetes llegan a él con una distribución de Poisson. El largo de los paquetes corresponde a una exponencial de media 1/mu, o también de parámetro mu, en donde mu = 1. También asumimos que el canal puede transmitir C = 1 bits por segundo. De esta formal, la tasa de servicio del canal será de mu * C  = 1 paquetes por segundo.

El algoritmo principal que simula el canal generará paquetes utilizando un Proceso de Poisson Homogéneo y luego atenderá los paquetes colocando los resultados en los arreglos correspondientes.

### Inciso 1
Para poder estudiar la variable `tau_m` correspondiente al `tiempo medio de demora` el algoritmo irá agregando en un arreglo el tiempo que demora cada paquete desde que llega al canal hasta que efectivamente se envía. Estos, luego serán los datos simulados que utilizaremos en los ejercicios 1, 2, 3 y 4.

Para obtener el intervalo de confianza de la estimación de la variable `tau_m` utilizaremos el algoritmo visto en el teórico con pequeñas modificaciones.

### Inciso 2
En este inciso debemos generar histogramas para los Nsim tiempos de demora obtenidos en el inciso 1 y para los nuevos valores que serán generados a partir de una exponencial de parámetro 0.5. Así conformaremos nuestra hipótesis nula, y en el siguiente inciso realizaremos un test de bondad de ajuste Chi cuadrado para comprobar la hipótesis.


### Inciso 3
Para aplicar el test Chi-Cuadrado, dado que nuestros datos simulados son tiempos continuos necesitamos poder discretizarlos. Para esto distribuiremos los datos 18 intervalos. Luego recorreremos los intervalos desde 0 hasta 18 y el primero intervalo `i` que observemos que su número de observaciones sea menor a 5, será unificado junto con los siguientes i, i+1, .. , n, n+1 intervalos en donde el ultimo n+1 albergará los valores desde `[x, inf)`.


Con los intervalos ya conformados, obtendremos el estadístico T que nos permitirá evaluar la Chi-Cuadrado para obtener el p-valor y así finalmente rechazar o no rechazar nuestra hipótesis nula.

### Inciso 4

Para analizar la variable `tiempo de espera en cola` o `t_c_media` utilizaremos los datos que generamos en el Inciso 1 en el algoritmo para el cálculo del intervalo de confianza. Estos datos los comparemos con Nsim nuevos datos simulados de una distribución Gamma con parámetros alfa=0.5 y Beta=2. De esta forma, cumplimos con alfa * beta = `t_c_media`.

Estos nuevos datos luego los distribuiremos, al igual que en el Inciso 2, en los mismos intervalos que utilizamos para los datos simulados para luego poder calcular la probabilidad teórica de cada intervalo que necesitaremos para el cálculo del estadístico T. Una vez que consigamos este estadístico podremos rechazar o no rechazar la hipótesis nula de que los `tiempos de espera en cola` provienen de una distribución Gamma con parámetros alfa=0.5 y beta=2.


## Ejercicio 2

En este ejercicio, el ingreso de paquetes a un canal corresponde a una distribución de Poisson de parámetro lambda y será simulada mediante un proceso de Poisson con lambda.


En la simulación de los protocolos `Aloha Puro` y `Aloha Ranurado` como la tasa de servicio es constante e igual a 1, se asume que todos los paquetes tendrán una longitud igual a 1. Ademas, en el `Aloha Ranurado`, los paquetes solo podrán ingresar al canal en los momentos t0, t1, t2, t3,... etc. Es decir, si un paquete esta listo para ingresar al canal en el momento (t_i + t_i+1) / 2 deberá esperar hasta t_i+1 para recién ingresar.

En ambos protocolos, si dos o mas paquetes quieren enviarse en el mismo instante de tiempo, ambos colisionaran, se dañaran y serán descartados.

Para obtener los resultados se iterará sobre los distintos valores posibles de lambda (0.1, 0.2, 0.3, ..., 3.0) y se realizaran simulaciones con Nsim = 10000 para estimar la tasa de uso del canal y la probabilidad de que la transmisión de un paquete sea exitoso.

# Algoritmo y descripción de las variables

# Resultados

Nota: Todos los resultados obtenidos aquí se realizaron utilizando la semilla 0 para el generador pseudo-aleatorio de numeros.



# Conclusiones

