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
	• Most_Shifts_Day[n] = day with the most shifts of class n
	• Least_Shifts_Day[n] = day with the least shifts of class n
• Constraints:
	• Sum[Time_Table[k][i][j][m] | k ∈ G(p), m in range(M)] ∈ {0, 1} as p ∈ {1, 2, ..., numG}
	• If c(m) < s(n) --> Time_Table[n][i][j][m] = 0  
	• Sum[Time_Table[n][i][j][m] | i ∈ {1, 2, ..., 5}, j ∈ {1, 2, ..., 12}, m ∈ {1, 2, ..., M}] == t(n)
	• Most_Shifts_Day[n] >= Time_Table[n][i][j][k] (sum of j from 1 to 12 and m from 1 to M)
	• Least_Shifts_Day[n] <= Time_Table[n][i][j][k] (sum of j from 1 to 12 and m from 1 to M)
	• Sum[Time_Table[n][i][j][m] | n ∈ {1, 2, ..., N}] ∈ {0, 1} (Constraint about room in specific time)
• Objective Function: sum(Most_Shifts_Day) - sum(Least_Shifts_Day) --> Minimize
'''

from ortools.linear_solver import pywraplp

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

def MIP(filename):
	# Notations & data
	N, M, t, g, s, c = input(filename)
	G0 = set(g)
	G = {}
	solver = pywraplp.Solver.CreateSolver('CBC')
	inf = solver.infinity()

	for i in G0:
		G[i] = [j for j in range(N) if g[j] == i]

	Time_Table = [[[[solver.IntVar(0, 1, f'Time_Table[{i}][{d}][{k}][{r}]') \
			for r in range(M)] for k in range(12)] for d in range(5)] for i in range(N)]


	# Constraints
	## A teacher teach only one class at a moment
	for p in G:
		for d in range(5):
			for k in range(12):
				cstr = solver.Constraint(0, 1)
				for r in range(M):
					for i in G[p]:
						cstr.SetCoefficient(Time_Table[i][d][k][r], 1)

	## If a class study in a room, then the number of 
	## students is less than the room's capacity
	for i in range(N):
		for r in range(M):
			if s[i] > c[r]:
				for d in range(5):
					for k in range(12):
						cstr = solver.Constraint(0, 0)
						cstr.SetCoefficient(Time_Table[i][d][k][r], 1)
					
	## Guarantee enough lessons for each class
	for i in range(N):
		cstr = solver.Constraint(t[i], t[i])
		for d in range(5):
			for k in range(12):
				for r in range(M):
					cstr.SetCoefficient(Time_Table[i][d][k][r], 1)
  
	Most_Shifts_Day = {}
	for i in range(N):
		Most_Shifts_Day[i] = solver.IntVar(0, t[i], f'Most_Shifts_Day[{i}]')
		for d in range(5):
			cstr = solver.Constraint(0, inf)
			cstr.SetCoefficient(Most_Shifts_Day[i], 1)
			for k in range(12):
				for r in range(M):
					cstr.SetCoefficient(Time_Table[i][d][k][r], -1)

	Least_Shifts_Day = {}
	for i in range(N):
		Least_Shifts_Day[i] = solver.IntVar(0, t[i], f'Least_Shifts_Day[{i}]')
		for d in range(5):
			cstr = solver.Constraint(-inf, 0)
			cstr.SetCoefficient(Least_Shifts_Day[i], 1)
			for k in range(12):
				for r in range(M):
					cstr.SetCoefficient(Time_Table[i][d][k][r], -1)

	## At a moment, there is only one class in a room
	for d in range(5):
		for k in range(12):
			for r in range(M):
				cstr = solver.Constraint(0, 1)
				for i in range(N):
					cstr.SetCoefficient(Time_Table[i][d][k][r], 1)

	# Objective function and solving
	obj = solver.Objective()
	for i in range(N):
		obj.SetCoefficient(Most_Shifts_Day[i], 1)
		obj.SetCoefficient(Least_Shifts_Day[i], -1)

	obj.SetMinimization()
	solver.Solve()
	
	result = [[[[Time_Table[n][i][j][m].solution_value() for m in range(M)] for j in range(12)] for i in range(5)] for n in range(N)]
	for n in range(N):
		for i in range(5):
			for j in range(12):
				for m in range(M):
					if result[n][i][j][m]:
						print(f'\tClass {n + 1} has lesson in shift {j + 1} of day {i + 1} at room {m + 1} having {c[m]} slots, has {s[n]} students and is taught by teacher {g[n]}')
		print()
	print(obj.Value())
	print(f'Wall time: {solver.WallTime()/1000}')

if __name__ == '__main__':
	from random_generate import *
	file_name = "random_data.txt"
	gen(file_name, 15, 4, hard=False)
	MIP(file_name)
