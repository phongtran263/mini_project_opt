from ortools.sat.python import cp_model

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

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables,N,M,num_time_slots,limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.N = N
        self.M = M
        self.num_time_slots = num_time_slots
        self.__solution_limit = limit

    def on_solution_callback(self):
        self.__solution_count += 1
        print('Solution:',self.solution_count())
        for k in range(self.N):
            for i in range(self.num_time_slots):
                for j in range(self.M):
                    if self.Value(self.__variables[i,j,k]):
                        time = Time(i+1)
                        room = j+1
                        Class = k+1
                        print(f'Class {Class}' + ' '*(3 - len(str(Class))) + f'has a lesson in room {room}'
                             + ' '*(3 - len(str(room)))+ f'at the {time[0]}' + f' lesson in the {time[1]}' 
                             + ' ' * (9 - len(str(time[1]))) + f' on {time[2]}')
        print()    
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after %i solutions' % self.__solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count


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


N,M,t,g,s,c = input('data_project_15.txt')
num_time_slots = 5*12

model = cp_model.CpModel()

# x[i,j,k] = 1 if class k has a lecture at the time slot i in the room j else 0
x = {}
for i in range(num_time_slots):
    for j in range(M):
        for k in range(N):
            x[i,j,k] = model.NewBoolVar(f'x[{i},{j},{k}]')

# y[i,k] = 1 if class k has a lecture at the time slot i else 0            
y = {}
for i in range(num_time_slots):
    for k in range(N):
        y[i,k] = model.NewBoolVar(f'y[{i},{k}]')
        model.Add(sum([x[i,j,k] for j in range(M)]) == y[i,k])

#The number of lessons of the class k
for k in range(N):
    model.Add(sum([y[i,k] for i in range(num_time_slots)]) == t[k])

#At the time slot i in the room j,there is no more than one class     
for i in range(num_time_slots):
    for j in range(M):
        model.Add(sum([x[i,j,k] for k in range(N)]) <= 1)

#The number of students in the class k must be less than the capacity of the room j
for k in range(N):
    for j in range(M):
        if s[k] > c[j]:
            for i in range(num_time_slots):
                model.Add(x[i,j,k] == 0)

#Two classes h and k has the same teacher have to be scheduled seperately
for h in range(N):
    for k in range(h+1,N):
        if g[h] == g[k]:
            for i in range(num_time_slots):
                model.Add(y[i,h] + y[i,k] <= 1)
                    
                    
solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinterWithLimit(x,N,M,num_time_slots,10)
solver.parameters.enumerate_all_solutions = True
status = solver.Solve(model,solution_printer)

print('Time:',solver.WallTime())
print('Status = %s' % solver.StatusName(status))
print('Number of solutions found: %i' % solution_printer.solution_count())

    
