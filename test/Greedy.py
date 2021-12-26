from random_generate import gen
import time
import random as rd

def input(filename):
	t = []
	g = []
	s = []
	with open(filename) as f:
		[N, M] = [int(x) for x in f.readline().split()]
		for _ in range(N):
			l = [int(x) for x in f.readline().split()]
			t.append(l[0])
			g.append(l[1])
			s.append(l[2])
		c = [int(x) for x in f.readline().split()]
	return N, M, t, g, s, c

def Time(i):
    if 1<= i <= 12:
        day = 'Monday'
    elif 13<= i <= 24:
        day = 'Tuesday'
    elif 25 <= i <= 36:
        day = 'Wednesday'
    elif 37 <= i <= 48:
        day = 'Thursday'
    else:
        day = 'Friday'
    j = i % 12
    if j == 0:
        lesson = 12
    else:
        lesson = j
    return lesson,day

def PrintSolution(solution):
    if solution == 'Failure':
        print(solution)
        return
    print('Solution is found')
    for k in range(len(N)):
        for i in range(t[k]):
            Class = k + 1
            time,room = solution[k,i]
            room += 1
            time = Time(time+1)
            print(f'Class {Class}' + ' '*(3 - len(str(Class))) + f'has a lesson in room {room}'
                  + ' '*(3 - len(str(room)))+ f'at the {time[0]}' + f' shift on {time[1]}' )
        print()    

def Select(solution,var):
    for i in range(num_time_slots):
        for j in M:
            if candidates[i,j]:
                new_solution = solution.copy()
                new_solution[var] = (i,j)
                if Feasible(new_solution):
                    return (i,j)
    return False
    
    
def Feasible(solution):
    d1 = {}
    d2 = {}
    for i,j in solution.items():
        Class = i[0]
        time_slot = j[0]
        room = j[1]
        # capacity of the room must be less than the number of students of a class
        if c[room] < s[Class]:
            return False
        # at a given time, a class can't take part in more than 1 lecture
        d1[Class,time_slot] = d1.get((Class,time_slot),-1) + 1
        if d1[Class,time_slot] > 0:
            return False
        # two class having the same teacher can't study at the same time
        d2[time_slot] = d2.get(time_slot,set())
        d2[time_slot].add(Class)
       
       
    for i in d2.values():
        d3 = {}
        for j in i:
            d3[g[j]] = d3.get(g[j],-1) + 1
            if d3[g[j]] > 0:
                return False
    return True             

def Greedy():
    solution = {}
    for i in N:
        for j in range(t[i]):
            candidate = Select(solution,(i,j))
            if candidate == False:
                return 'Failure'
            solution[i,j] = candidate
            candidates[candidate] = False
    return solution

if __name__ == '__main__':
    filename = "random_data.txt"
    gen(filename, 15, 2, hard=False)
    N,M,t,g,s,c = input(filename)
    num_time_slots = 5*12
    candidates =  {}
    for i in range(num_time_slots):
        for j in range(M):
            candidates[i,j] = True
    # sort the room set in increasing order in terms of its capacity
    M = [(c[i],i) for i in range(M)]
    M.sort()
    M = [i[1] for i in M]
    # sort the class set in decreasing order in terms of its number of students
    N = [(s[i],i) for i in range(N)]
    N.sort(reverse = True)
    N = [i[1] for i in N]
    start = time.time()
    solution = Greedy()
    end = time.time()
    PrintSolution(solution)
    print('Time:',end - start)

            
                
            
                
    
    
    
    
