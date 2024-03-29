'''
• Có N lớp 1,2,..., N cần được xếp thời khóa biểu. Mỗi lớp i có t(i) là số tiết và g(i) là giáo viên đã được phân công dạy lớp đó và s(i) là số sinh viên của lớp
• Có M phòng học 1, 2, ..., M, trong đó c(i) là số chỗ ngồi của phòng i
• Trong tuần có 5 ngày (từ thứ 2 đến thứ 5), mỗi ngày chia thành 12 tiết (6 tiết sáng và 6 tiết chiều).
• Hãy lập thời khóa biểu (xác định ngày, tiết và phòng gán cho mỗi lớp):
	• Hai lớp có chung giáo viên thì phải xếp thời khóa biểu tách rời nhau
	• Số sinh viên trong mỗi lớp phải nhỏ hơn hoặc bằng số chỗ ngồi của phòng học

• Input
	• Dòng1: ghi N và M
	• Dòng i+1 (i = 1,..., N): ghi t(i), g(i) và s(i) 
	• Dòng N+2: ghi c(1), c(2), ..., c(M)
'''
'''
• Notations:
	• G[i]: set of class taught ny teacher i
• Variables:
	• Time_Table[n][i][j][m] = 1 if class n ∈ {1, 2, ..., N} has lesson in shift j ∈ {1, 2, ..., 12} of day i ∈ {1, 2, ..., 5} at room m ∈ {1, 2, ..., M} else 0
• Constraints:
	• Sum[Time_Table[k][i][j][m] | k ∈ G(p), m in range(M)] ∈ {0, 1} as p ∈ {1, 2, ..., numG}
	• If Time_Table[n][i][j][m] = 1 --> c(m) >= s(n)
	• Sum[Time_Table[n][i][j][m] | i ∈ {1, 2, ..., 5}, j ∈ {1, 2, ..., 12}, m ∈ {1, 2, ..., M}] == t(n)
	• Sum[Time_Table[n][i][j][m] | n ∈ {1, 2, ..., N}] ∈ {0, 1}
'''

from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
	#print intermediate solution
	def __init__(self,vars, N, M, c, s, g, limit = 1):
		cp_model.CpSolverSolutionCallback.__init__(self) 
		self.__vars = vars 
		self.__solution_count = 0
		self.__N = N
		self.__M = M
		self.__c = c
		self.__s = s
		self.__g = g
		self.__limit = limit
	def on_solution_callback(self):
		self.__solution_count += 1
		print(f'\nSolution {self.__solution_count}:')
		for n in range(self.__N):
			for i in range(5):
				for j in range(12):
					for m in range(self.__M):
						if self.Value(self.__vars[n][i][j][m]):
							print(f'\tClass {n} has lesson in shift {j} of day {i} at room {m} having {self.__c[m]} slots, has {self.__s[n]} students and is taught by teacher {self.__g[n]}')
		Most_Shifts_Day = [max(sum(self.Value(self.__vars[n][i][j][m]) for j in range(12) for m in range(self.__M)) for i in range(5)) for n in range(self.__N)]
		Least_Shifts_Day = [min(sum(self.Value(self.__vars[n][i][j][m]) for j in range(12) for m in range(self.__M)) for i in range(5)) for n in range(self.__N)]
		fstar = sum(Most_Shifts_Day[n] - Least_Shifts_Day[n] for n in range(self.__N))
		print(f'f* = {fstar}')
		if self.__solution_count >= self.__limit:
			self.StopSearch()
	def solution_count(self):
		return self.__solution_count

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

def CP(f, limit = 1, optimal = False):
	# Notations and data
	N, M, t, g, s, c = input(f)
	model = cp_model.CpModel()
	G0 = set(g)
	G = {}
	for i in G0:
		G[i] = [j for j in range(N) if g[j] == i]

	# Create a model and set variables
	Time_Table = [[[[model.NewIntVar(0, 1, f'Time_Table[{i}][{d}][{k}][{r}]') \
			for r in range(M)] for k in range(12)] for d in range(5)] for i in range(N)]

	# Constraints
	## A teacher teach only one class at a moment
	for p in G:
		for d in range(5):
			for k in range(12):
				model.AddLinearConstraint(\
					sum(Time_Table[i][d][k][r] \
						for i in G[p] for r in range(M)), 0, 1)

	## If a class study in a room, then the number of students is less than the room's capacity
	for i in range(N):
		for r in range(M):
			b = model.NewBoolVar('b')
			model.Add(c[r] < s[i]).OnlyEnforceIf(b)
			for d in range(5):
				for k in range(12):
					model.Add(Time_Table[i][d][k][r] == 0).OnlyEnforceIf(b)
					
	## Guarantee enough lessons for each class
	for i in range(N):
		model.Add(sum(Time_Table[i][d][k][r] for r in range(M)\
			 for k in range(12) for d in range(5)) == t[i])

	## At a moment, there is only one class in a room
	for d in range(5):
		for k in range(12):
			for r in range(M):
				model.AddLinearConstraint(sum(Time_Table[i][d][k][r]\
					 for i in range(N)), 0, 1)

	# Solve
	if optimal:
		Total_Shifts = {}
		for i in range(N):
			for d in range(5):
				Total_Shifts[i, d] = model.NewIntVar(0, t[i], f'Total_Shifts[{i}, {d}]')
				model.Add(Total_Shifts[i, d] - sum(Time_Table[i][d][k][r] for k in range(12) for r in range(M)) == 0)

		Most_Shifts_Day = {}
		for i in range(N):
			Most_Shifts_Day[i] = model.NewIntVar(0, t[i], f'Most_Shifts_Day[{i}]')
			model.AddMaxEquality(Most_Shifts_Day[i], [Total_Shifts[i, d] for d in range(5)])

		Least_Shifts_Day = {}
		for i in range(N):
			Least_Shifts_Day[i] = model.NewIntVar(0, t[i], f'Least_Shifts_Day[{i}]')
			model.AddMinEquality(Least_Shifts_Day[i], [Total_Shifts[i, d] for d in range(5)])
		
		model.Minimize(sum(Most_Shifts_Day[i] - Least_Shifts_Day[i] for i in range(N)))
		solver = cp_model.CpSolver()
		solver.parameters.search_branching == cp_model.FIXED_SEARCH

		solver.Solve(model)
		result = [[[[solver.Value(Time_Table[i][d][k][r]) for r in range(M)] for k in range(12)] for d in range(5)] for i in range(N)]
		for n in range(N):
			for i in range(5):
				for j in range(12):
					for m in range(M):
						if result[n][i][j][m]:
							print(f'\tClass {n + 1} has lesson in shift {j + 1} of day {i + 1} at room {m + 1} having {c[m]} slots, has {s[n]} students and is taught by teacher {g[n]}')
			print()		
		print(f'f* = {solver.ObjectiveValue()}')
		print(f'Wall time: {solver.WallTime()}')
	
	else:
		solver = cp_model.CpSolver()
		solver.parameters.search_branching == cp_model.FIXED_SEARCH

		solution_printer = VarArraySolutionPrinter(Time_Table, N, M,c, s, g, limit)
		solver.SearchForAllSolutions(model, solution_printer)
		print(f'Wall time: {solver.WallTime()}')

if __name__ == '__main__':
	from random_generate import *
	filename = "random_data.txt"
	gen(filename, 15, 2)
	CP(filename, optimal= True)
