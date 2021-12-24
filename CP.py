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
'''

from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
	#print intermediate solution
	def __init__(self,vars, N, M, c, s, g, limit):
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
		if self.__solution_count == self.__limit:
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

def CP(f):
	# Notations and data
	N, M, t, g, s, c = input(f)
	G0 = set(g)
	G = {}
	for i in G0:
		G[i] = [j for j in range(N) if g[j] == i]

	# Create a model and set variables
	model = cp_model.CpModel()
	Time_Table = [[[[model.NewIntVar(0, 1, f'Time_Table[{n}][{i}][{j}][{m}]') for m in range(M)] for j in range(12)] for i in range(5)] for n in range(N)]

	# Constraints
	for p in G:
		for i in range(5):
			for j in range(12):
				model.AddLinearConstraint(sum(Time_Table[k][i][j][m] for k in G[p] for m in range(M)), 0, 1)

	for n in range(N):
		for i in range(5):
			for j in range(12):
				for m in range(M):
					b = model.NewBoolVar('b')
					model.Add(Time_Table[n][i][j][m] == 1).OnlyEnforceIf(b)
					model.Add(Time_Table[n][i][j][m] == 0).OnlyEnforceIf(b.Not())
					model.Add(c[m] >= s[n]).OnlyEnforceIf(b)

	for n in range(N):
		model.Add(sum(Time_Table[n][i][j][m] for m in range(M) for j in range(12) for i in range(5)) == t[n])

	# Solve
	solver = cp_model.CpSolver()
	solver.parameters.search_branching == cp_model.FIXED_SEARCH

	solution_printer = VarArraySolutionPrinter(Time_Table, N, M,c, s, g, 50)
	solver.SearchForAllSolutions(model, solution_printer)
	solver.Solve(model, solution_printer)
	print(f'Wall time: {solver.WallTime()}')

if __name__ == '__main__':
	CP('data.txt')
