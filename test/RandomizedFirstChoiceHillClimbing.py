import random
import time
from mini_project_instance_generator import gen

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
    if 1 <= j <= 6:
        daytime = 'Morning'
        lesson = j
    else:
        daytime = 'Afternoon'
        if j == 0:
            lesson = 6
        else:
            lesson = j - 6
    return lesson,daytime,day

def PrintSolution(solution):
    for k in range(N):
        for i in range(t[k]):
            Class = k + 1
            time,room = solution[k,i]
            room += 1
            time = Time(time+1)
            print(f'Class {Class}' + ' '*(3 - len(str(Class))) + f'has a lesson in room {room}'
                  + ' '*(3 - len(str(room)))+ f'at the {time[0]}' + f' lesson in the {time[1]}' 
                  + ' ' * (9 - len(str(time[1]))) + f' on {time[2]}')
        print()    

class TimetableSchedule():
    
    def __init__(self,N,M,t,g,s,c):
        self.N = N
        self.M = M
        self.t = t
        self.g = g
        self.s = s
        self.c = c
        self.num_time_slots = 5 * 12
        self.candidate = [(i,j) for i in range(self.num_time_slots) for j in range(self.M)]
            
    def initial(self):
        # generate a random initial state
        # a state is a dictionary with key:(class_name,lecture),value:(time_slot,room)
        candidate = self.candidate
        state = {}
        for i in range(self.N):
            for j in range(self.t[i]):
                state[i,j] = None
        for i,j in zip(random.sample(candidate,len(state)),state.keys()):
            state[j] = i
        return state
    
    def goal_test(self, state):
        return self.value(state) == 0
    def value(self, state):
        #heuristics function
        violations = 0
        d1 = {}
        d2 = {}
        for i,j in state.items():
            Class = i[0]
            time_slot = j[0]
            room = j[1]
            # capacity of the room must be less than the number of students in a class
            if self.c[room] < self.s[Class]:
                violations += 1
            # at a given time, a class can't take part in more than 1 lecture
            d1[Class,time_slot] = d1.get((Class,time_slot),-1) + 1
            # two class having the same teacher can't study at the same time 
            d2[time_slot] = d2.get(time_slot,set())
            d2[time_slot].add(Class)
        violations += sum(d1.values())
       
        for i in d2.values():
            d3 = {}
            for j in i:
                d3[self.g[j]] = d3.get(self.g[j],-1) + 1
            violations += sum(d3.values())
        return violations
    
    
    def get_candidate(self):
        return self.candidate

def randomized_first_choice_hill_climbing(problem, limit = 10000):
    current = problem.initial()
    vars = list(current.keys()) 
    iterations = 0
    while True:
        min_val = problem.value(current)
        if min_val == 0:
            break
        good_neighbor = current
        candidate = problem.get_candidate().copy()
        for i in current.values():
            candidate.remove(i)
        cnt = 0
        while cnt <= limit:
            i =  random.choice(vars)
            j =  random.choice(candidate)
            if problem.c[j[1]] < problem.s[i[0]]:
                continue
            new_state = current.copy()
            new_state[i] = j
            violations = problem.value(new_state)
            if violations < min_val:
                min_val = violations
                good_neighbor = new_state
                break
            cnt += 1
    
        if problem.value(good_neighbor) >= problem.value(current):
            break
        current = good_neighbor
        iterations += 1
        print(f'Iterations:{iterations},violations:{min_val}')
    return current,iterations

def random_restart(problem, limit = 10):
    state = problem.initial()
    cnt = 0
    num_iterations = 0
    while problem.goal_test(state) == False and cnt < limit:
        state,iterations = randomized_first_choice_hill_climbing(problem)
        num_iterations += iterations
        cnt += 1
    if problem.goal_test(state):
        status = 'Feasible'
    else:
        status = 'Solution not found'
    return state,status,cnt,num_iterations


def input(filename):
    with open(filename) as f:
        N,M = [int(i) for i in f.readline().split()]
        class_info = []
        for i in range(N):
            class_info.append([int(i) for i in f.readline().split()])
        c = [int(i) for i in f.readline().split()]
    t = []
    g = []
    s = []
    for i in class_info:
        t.append(i[0])
        g.append(i[1])
        s.append(i[2])
    return N,M,t,g,s,c

if __name__ == '__main__':
    gen('data_15.txt',27,5)
    N,M,t,g,s,c = input('data_15.txt')
    problem = TimetableSchedule(N, M, t, g, s, c)
    start = time.time()
    solution,status,num_trials,num_iterations = random_restart(problem)
    end = time.time()
    PrintSolution(solution)
    print('Time:',end - start)
    print(status)
    print('Number of iterations:',num_iterations)
    print('Number of trials:',num_trials)
    

    