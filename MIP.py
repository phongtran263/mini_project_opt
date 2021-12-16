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
	• S[n][i][j][m] = 1 if class n ∈ {1, 2, ..., N} has lesson in shift j ∈ {1, 2, ..., 12} of day i ∈ {1, 2, ..., 5} at room m ∈ {1, 2, ..., M} else 0
	• Most_Shifts_Day[n] = day with the most shifts of class n
	• Least_Shifts_Day[n] = day with the least shifts of class n
• Constraints:
	• Sum[S[k][i][j][m] | k ∈ G(p)] ∈ {0, 1} as p ∈ {1, 2, ..., numG}
	• If c(m) < s(n) --> S[n][i][j][m] = 0  
	• Sum[S[n][i][j][m] | i ∈ {1, 2, ..., 5}, j ∈ {1, 2, ..., 12}, m ∈ {1, 2, ..., M}] == t(n)
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

N, M, t, g, s, c = input('/Users/phong/Documents/Optimization/Code/mini_project_opt/data.txt')#Copy yours file's path here
maxc = max(c)
G0 = set(g)
G = {}
for i in G0:
	G[i] = [j for j in range(N) if g[j] == i]
ubDevi = max(t)

solver = pywraplp.Solver.CreateSolver('CBC')
inf = solver.infinity()
Time_Table = [[[[solver.IntVar(0, 1, f'Time_Table[{n}][{i}][{j}][{m}]') for m in range(M)] for j in range(12)] for i in range(5)] for n in range(N)]
Most_Shifts_Day = [solver.IntVar(0, ubDevi, f'Most_Shifts_Day[{n}]') for n in range(N)]
Least_Shifts_Day = [solver.IntVar(0, ubDevi, f'Least_Shifts_Day[{n}]') for n in range(N)]

for p in G:
	for i in range(5):
		for j in range(12):
			for m in range(M):
				cstr = solver.Constraint(0, 1)
				for n in G[p]:
					cstr.SetCoefficient(Time_Table[n][i][j][m], 1)

for n in range(N):
	for m in range(M):
		if s[n] > c[m]:
			for i in range(5):
				for j in range(12):
					cstr = solver.Constraint(0, 0)
					cstr.SetCoefficient(Time_Table[n][i][j][m], 1)
				
for n in range(N):
	cstr = solver.Constraint(t[n], t[n])
	for i in range(5):
		for j in range(12):
			for m in range(M):
				cstr.SetCoefficient(Time_Table[n][i][j][m], 1)

for n in range(N):
	for i in range(5):
		cstr = solver.Constraint(0, inf)
		cstr.SetCoefficient(Most_Shifts_Day[n], 1)
		for j in range(12):
			for m in range(M):
				cstr.SetCoefficient(Time_Table[n][i][j][m], -1)

for n in range(N):
	for i in range(5):
		cstr = solver.Constraint(-inf, 0)
		cstr.SetCoefficient(Least_Shifts_Day[n], 1)
		for j in range(12):
			for m in range(M):
				cstr.SetCoefficient(Time_Table[n][i][j][m], -1)

obj = solver.Objective()
for n in range(N):
	obj.SetCoefficient(Most_Shifts_Day[n], 1)
	obj.SetCoefficient(Least_Shifts_Day[n], -1)

obj.SetMinimization()
solver.Solve()
print(obj.Value())
solu = [[[[Time_Table[n][i][j][m].solution_value() for m in range(M)] for j in range(12)] for i in range(5)] for n in range(N)]
for n in range(N):
	for i in range(5):
		for j in range(12):
			for m in range(M):
				if solu[n][i][j][m]:
					print(f'\tClass {n + 1} has lesson in shift {j + 1} of day {i + 1} at room {m + 1} having {c[m]} slots, has {s[n]} students and is taught by teacher {g[n]}')

