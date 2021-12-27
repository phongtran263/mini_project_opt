import random as rd
import time
from data_generator import gen

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
    for k in range(N):
        for i in range(t[k]):
            Class = k + 1
            time,room = solution[k,i]
            room += 1
            time = Time(time+1)
            print(f'Class {Class}' + ' '*(3 - len(str(Class))) + f'has a lesson in room {room}'
                  + ' '*(3 - len(str(room)))+ f'at the {time[0]}' + f' shift on {time[1]}' )
        print()    


def Initial():
        # generate a random initial state
        # a state is a dictionary with key:(class_name,lecture),value:(time_slot,room)
        state = {}
        for i in range(N):
            for j in range(t[i]):
                state[i,j] = None
        for i,j in zip(rd.sample(candidates.keys(),len(state)),state.keys()):
            state[j] = i
        return state
    
    
def Value(state):
        #heuristic function
        violations = 0
        d1 = {}
        for i,j in state.items():
            Class = i[0]
            time_slot = j[0]
            room = j[1]
            # capacity of the room must be less than the number of students of a class
            if c[room] < s[Class]:
                violations += 1
            # at a given time, a teacher can't teach at more than 1 room
            d1[time_slot] = d1.get(time_slot,[])
            d1[time_slot].append(Class)
       
        for i in d1.values():
            d2 = {}
            for j in i:
                d2[g[j]] = d2.get(g[j],-1) + 1
            violations += sum(d2.values())
        return violations


def GoalTest(state):
        return Value(state) == 0    

    
def HillClimbing():
    current = Initial()
    vars = list(current.keys())
    for candidate in current.values():
        candidates[candidate] = False
    curr_violations = Value(current)
    iterations = 0
    while curr_violations > 0:
        min_violations = curr_violations
        for var in vars:
            for candidate in candidates.keys():
                if not candidates[candidate]:
                    continue
                if c[candidate[1]] < s[var[0]]:
                    continue
                temp = current[var]
                current[var] = candidate
                violations = Value(current)
                if violations <= min_violations:
                    best_var = var
                    best_candidate = candidate
                    min_violations = violations
                current[var] = temp
        if min_violations > curr_violations:
            break
        curr_violations = min_violations
        try:
            temp = current[best_var]
        except:
            break
        current[best_var] = best_candidate
        candidates[best_candidate] = False
        candidates[temp] = True
        iterations += 1
        print(f'Iterations:{iterations},violations:{curr_violations}')
    return current,iterations


def FirstChoiceHillClimbing(limit = 20000):
    current = Initial()
    vars = list(current.keys())
    for candidate in current.values():
        candidates[candidate] = False
    curr_violations = Value(current)
    iterations = 0
    while curr_violations > 0:
        cnt = 0
        while cnt <= limit:
            var = rd.choice(vars)
            candidate = rd.choice(list(candidates.keys()))
            if not candidates[candidate]:
                continue
            if c[candidate[1]] < s[var[0]]:
                continue
            temp = current[var]
            current[var] = candidate
            violations = Value(current)
            if violations <= curr_violations:
                candidates[candidate] = False
                candidates[temp] = True
                curr_violations = violations
                break
            current[var] = temp
            cnt += 1
        if cnt > limit:
            break
        iterations += 1
        print(f'Iterations:{iterations},violations:{curr_violations}')
    return current,iterations


def RandomRestart(flag,limit = 100):
    # flag == True, FirstChoiceHillClimbing
    # flag == False, HillClimbing
    state = Initial()
    cnt = 0
    num_iterations = 0
    while GoalTest(state) == False and cnt < limit:
        if flag:
            state,iterations = FirstChoiceHillClimbing()
        else:
            state,iterations = HillClimbing()
        for i in range(num_time_slots):
            for j in range(M):
                candidates[i,j] = True
        num_iterations += iterations
        cnt += 1
    if GoalTest(state):
        status = 'Feasible'
    else:
        status = 'Failure'
    return state,status,cnt,num_iterations



if __name__ == '__main__':
    filename = "data.txt"
    gen(filename, 15, 2, hard=False)
    N,M,t,g,s,c = input(filename)
    num_time_slots = 5 * 12
    candidates =  {}
    for i in range(num_time_slots):
            for j in range(M):
                candidates[i,j] = True
    start = time.time()
    solution,status,num_trials,num_iterations = RandomRestart(True)
    end = time.time()
    PrintSolution(solution)
    print('Time:',end - start)
    print(status)
    print('Number of iterations:',num_iterations)
    print('Number of trials:',num_trials)
        
            
