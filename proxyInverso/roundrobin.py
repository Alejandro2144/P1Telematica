

# bt = tiempo quemado -> burst time -> requerido para completar el proceso 
# wt = tiempo de espera -> waiting time ->  Diferencia entre turn around time y burst time 
# quantum = unidad de tiempo 
# n -> procesos
# tat -> turn around time -> Turn Around Time = Completion Time – Arrival Time

def findWaitingTime(processes, n, bt, wt, quantum):
	rem_bt = [0] * n # Matriz rem_bt[] para realizar un seguimiento del tiempo de ráfaga restante de los procesos.
                    # Esta matriz es inicialmente una copia de bt[] (matriz de tiempos de ráfaga)

	# Copia el tiempo de ráfaga en rt[]
	for i in range(n):
		rem_bt[i] = bt[i]
	t = 0 # Tiempo actual

	# Continúe recorriendo los procesos en forma rotativa hasta que no terminen todos.
	while(1):
		done = True

		# Recorre todos los procesos uno por uno repetidamente
		for i in range(n):
			
			# Si el tiempo de ráfaga de un proceso es mayor que 0, solo necesita procesar más
			if (rem_bt[i] > 0) :
				done = False # Hay un proceso pendiente
				
				if (rem_bt[i] > quantum) :
				
					# Aumenta el valor de t, es decir, muestra cuánto tiempo se ha procesado un proceso
					t += quantum

					# Disminuir el burst_time del proceso actual por quantum
					rem_bt[i] -= quantum
				
				# Si el tiempo de ráfaga es menor o igual a la cantidad. Último ciclo para este proceso
				else:
				
					# Aumenta el valor de t, es decir, muestra cuánto tiempo se ha procesado un proceso
					t = t + rem_bt[i]

					# El tiempo de espera es el tiempo actual menos el tiempo utilizado por este proceso
					wt[i] = t - bt[i]

					# A medida que el proceso se ejecuta por completo, haga que su tiempo de ráfaga restante sea = 0
					rem_bt[i] = 0
				
		# Si todos los preocesos terminaron 
		if (done == True):
			break
			
# Calcular el turn around time
def findTurnAroundTime(processes, n, bt, wt, tat):
	for i in range(n):
		tat[i] = bt[i] + wt[i]


# Calcular average waiting y turn-around times.
def findavgTime(processes, n, bt, quantum):
	wt = [0] * n
	tat = [0] * n

	# Encontrar waiting time de todos los procesos 
	findWaitingTime(processes, n, bt, wt, quantum)

	# Ecnontrar turn around time para todos los procesos
	findTurnAroundTime(processes, n, bt, wt, tat)

	print("Processes Burst Time	 Waiting",
					"Time Turn-Around Time")
	total_wt = 0
	total_tat = 0
	for i in range(n):

		total_wt = total_wt + wt[i]
		total_tat = total_tat + tat[i]
		print(" ", i + 1, "\t\t", bt[i],
			"\t\t", wt[i], "\t\t", tat[i])

	print("\nAverage waiting time = %.5f "%(total_wt /n) )
	print("Average turn around time = %.5f "% (total_tat / n))
	

if __name__ =="__main__":
	
	
	proc = [1, 2, 3]
	n = 3
	burst_time = [10, 5, 8]
	quantum = 2;
	findavgTime(proc, n, burst_time, quantum)

