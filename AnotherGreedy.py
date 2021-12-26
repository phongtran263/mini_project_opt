from random_generate import gen
import time

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

def Solve(filename):
  N, M, t, g, s, c = input(filename)
  info_classes = []
  sum_period = 0
  teacher = []
  for i in range(N):
    info_classes.append([t[i],g[i],s[i]])
    sum_period += t[i]
    teacher.append(g[i])
  state_teacher = [[True for _ in range(len(set(teacher)) + 1)] for __ in range(60)]
  state_room = [[True for _ in range(M)] for __ in range(60)]
  Greedy(info_classes, state_room, state_teacher, c)

def Greedy(info_classes, state_room, state_teacher, rooms):
  timetable = {}
  for i in range(len(info_classes)):
    info_class = info_classes[i]
    timetable[i] = []
    for _ in range(info_class[0]):
      found = False
      for p in range(60):
        for r in range(len(rooms)):
          if Feasible(info_class, state_room, state_teacher, rooms, p, r):
            state_room[p][r] = False
            state_teacher[p][info_class[1]] = False
            timetable[i].append((p, r))
            found = True
            break
        if found:
          break
      if not found:
        print("FAILURE")
        return False
  PrintSolution(timetable)
  return True

def Feasible(info_class, state_room, state_teacher, rooms, p, r):
  # At a moment, a teacher teaches at most one class
  if not state_teacher[p][info_class[1]]:
    return False
  # At a moment, a room is used by at most one class
  if not state_room[p][r]:
    return False
  # The room's capacity is bigger than the number of student in class
  if info_class[2] > rooms[r]:
    return False
  return True

def PrintSolution(timetable):
  classes = sorted(list(timetable.keys()))
  convert = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
  p = lambda x: 12 if x % 12 == 0 else x % 12
  for i in classes:
    for j, k in timetable[i]:
      print(f'Class {i+1} has lessons at period {p(j+1)} on {convert[j//12]} at room {k}')
    print()

if __name__ == "__main__":
  filename = "random_data.txt"
  gen(filename, 15, 2, hard=True)
  start = time.time()
  Solve(filename)
  end = time.time()
  print("Time:", end - start)